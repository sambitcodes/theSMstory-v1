"""
Database module for Tabu weds Mousumi application
Handles all SQLite database operations for ingredients, invitees and menus.
Optimised for Streamlit Cloud (WAL, timeouts, retries) and supports per-row reset.
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Optional
import time

from config import DB_NAME, DB_TIMEOUT


class WeddingDatabase:
    """Main database class for managing wedding data with thread-safe operations"""

    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path
        self.init_database()

    # ---------------------------------------------------------------------
    # Core connection helpers
    # ---------------------------------------------------------------------
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper timeout and isolation."""
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=DB_TIMEOUT,
                check_same_thread=False,
            )
            conn.row_factory = sqlite3.Row
            # WAL mode reduces locking issues on Streamlit Cloud
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            return conn
        except sqlite3.OperationalError:
            time.sleep(0.1)
            conn = sqlite3.connect(
                self.db_path,
                timeout=DB_TIMEOUT,
                check_same_thread=False,
            )
            conn.row_factory = sqlite3.Row
            return conn

    def init_database(self) -> None:
        """Initialize database tables (idempotent)."""
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()

                # Ingredients table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name TEXT NOT NULL,
                        item_name TEXT NOT NULL,
                        quantity REAL NOT NULL,
                        unit TEXT NOT NULL,
                        delivered_quantity REAL DEFAULT 0,
                        status TEXT DEFAULT 'Not Started',
                        original_quantity REAL NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(list_name, item_name)
                    )
                    """
                )

                # Invitees table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS invitees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name TEXT NOT NULL,
                        name TEXT NOT NULL,
                        lunch INTEGER NOT NULL,
                        to_sakti INTEGER,
                        travel_by TEXT,
                        original_lunch INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(list_name, name)
                    )
                    """
                )

                # Menus table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS menus (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        meal TEXT NOT NULL,
                        headcount INTEGER NOT NULL,
                        menu_items TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(date, meal)
                    )
                    """
                )

                conn.commit()
                conn.close()
                break
            except sqlite3.OperationalError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Database initialization error: {e}")
                else:
                    time.sleep(0.2)

    # ---------------------------------------------------------------------
    # INGREDIENT OPERATIONS
    # ---------------------------------------------------------------------
    def load_ingredient_list(self, list_name: str, df: pd.DataFrame) -> bool:
        """Load ingredient list from CSV into database, replacing that list."""
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        "DELETE FROM ingredients WHERE list_name = ?",
                        (list_name,),
                    )

                    for _, row in df.iterrows():
                        try:
                            name_raw = row.get("Item Name", None)
                            qty_raw = row.get("Quantity", None)
                            unit_raw = row.get("Unit", None)

                            if pd.isna(name_raw) or pd.isna(qty_raw) or pd.isna(
                                unit_raw
                            ):
                                continue

                            item_name = str(name_raw).strip()
                            if not item_name:
                                continue

                            quantity = float(qty_raw)
                            unit = str(unit_raw).strip()

                            cursor.execute(
                                """
                                INSERT INTO ingredients
                                (list_name, item_name, quantity, unit,
                                 delivered_quantity, status, original_quantity)
                                VALUES (?, ?, ?, ?, 0, 'Not Started', ?)
                                """,
                                (list_name, item_name, quantity, unit, quantity),
                            )
                        except (ValueError, sqlite3.IntegrityError, KeyError):
                            continue

                    conn.commit()
                    conn.close()
                    return True
                except sqlite3.OperationalError:
                    retry_count += 1
                    time.sleep(0.2)
            return False
        except Exception as e:
            print(f"Error loading ingredient list: {e}")
            return False

    def get_ingredients(self, list_name: str) -> List[Dict]:
        """Get all ingredients for a list."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM ingredients
                WHERE list_name = ?
                ORDER BY item_name
                """,
                (list_name,),
            )
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []

    def update_ingredient_status(
        self,
        list_name: str,
        item_name: str,
        status: str,
        delivered_qty: float = 0.0,
    ) -> None:
        """Update ingredient status and delivered quantity."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE ingredients
                SET status = ?, delivered_quantity = ?
                WHERE list_name = ? AND item_name = ?
                """,
                (status, delivered_qty, list_name, item_name),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating ingredient status: {e}")

    def add_ingredient(
        self,
        list_name: str,
        item_name: str,
        quantity: float,
        unit: str,
    ) -> bool:
        """Add new ingredient, with original_quantity set to first value."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO ingredients
                (list_name, item_name, quantity, unit,
                 delivered_quantity, status, original_quantity)
                VALUES (?, ?, ?, ?, 0, 'Not Started', ?)
                """,
                (list_name, item_name, quantity, unit, quantity),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False

    def update_ingredient(
        self,
        list_name: str,
        item_name: str,
        quantity: float,
        unit: str,
    ) -> None:
        """Update quantity/unit, leaving original_quantity unchanged."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE ingredients
                SET quantity = ?, unit = ?
                WHERE list_name = ? AND item_name = ?
                """,
                (quantity, unit, list_name, item_name),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating ingredient: {e}")

    def delete_ingredient(self, list_name: str, item_name: str) -> bool:
        """Delete ingredient from list."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM ingredients
                WHERE list_name = ? AND item_name = ?
                """,
                (list_name, item_name),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting ingredient: {e}")
            return False

    def reset_ingredient(self, list_name: str, item_name: str) -> None:
        """Reset one ingredient to its original quantity and clear status."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE ingredients
                SET quantity = original_quantity,
                    delivered_quantity = 0,
                    status = 'Not Started'
                WHERE list_name = ? AND item_name = ?
                """,
                (list_name, item_name),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error resetting ingredient: {e}")

    def search_ingredients(
        self,
        search_term: str,
        list_name: Optional[str] = None,
    ) -> List[Dict]:
        """Search ingredients by name, optionally within one list."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            pattern = f"%{search_term}%"
            if list_name:
                cur.execute(
                    """
                    SELECT * FROM ingredients
                    WHERE list_name = ? AND item_name LIKE ?
                    ORDER BY list_name, item_name
                    """,
                    (list_name, pattern),
                )
            else:
                cur.execute(
                    """
                    SELECT * FROM ingredients
                    WHERE item_name LIKE ?
                    ORDER BY list_name, item_name
                    """,
                    (pattern,),
                )
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            print(f"Error searching ingredients: {e}")
            return []

    # ---------------------------------------------------------------------
    # INVITEE OPERATIONS
    # ---------------------------------------------------------------------
    def load_invitee_list(self, list_name: str, df: pd.DataFrame) -> bool:
        """
        Load invitee list from CSV into database, replacing that list.
        Skips header/separator/summary rows like '117 Total', and blank names.
        """
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        "DELETE FROM invitees WHERE list_name = ?",
                        (list_name,),
                    )

                    for _, row in df.iterrows():
                        try:
                            name_raw = row.get("Name", None)
                            lunch_raw = row.get("Lunch", None)

                            if pd.isna(name_raw) or pd.isna(lunch_raw):
                                continue

                            name = str(name_raw).strip()
                            if (
                                not name
                                or name.lower().startswith("index")
                                or name.lower().endswith("total")
                            ):
                                # skip header / summary line like '117 Total'
                                continue  # [attached_file:11]

                            lunch = int(lunch_raw)

                            to_sakti = None
                            travel_by = None
                            if "To SAKTI" in row.index:
                                val = row["To SAKTI"]
                                to_sakti = int(val) if pd.notna(val) else None
                            if "Travel By" in row.index:
                                val = row["Travel By"]
                                travel_by = (
                                    str(val).strip() if pd.notna(val) else None
                                )

                            cursor.execute(
                                """
                                INSERT INTO invitees
                                (list_name, name, lunch, to_sakti, travel_by, original_lunch)
                                VALUES (?, ?, ?, ?, ?, ?)
                                """,
                                (list_name, name, lunch, to_sakti, travel_by, lunch),
                            )
                        except (ValueError, sqlite3.IntegrityError, KeyError):
                            continue

                    conn.commit()
                    conn.close()
                    return True
                except sqlite3.OperationalError:
                    retry_count += 1
                    time.sleep(0.2)
            return False
        except Exception as e:
            print(f"Error loading invitee list: {e}")
            return False

    def get_invitees(self, list_name: str) -> List[Dict]:
        """Get all invitees for a list."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM invitees
                WHERE list_name = ?
                ORDER BY name
                """,
                (list_name,),
            )
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            print(f"Error getting invitees: {e}")
            return []

    def add_invitee(
        self,
        list_name: str,
        name: str,
        lunch: int,
        to_sakti: Optional[int] = None,
        travel_by: Optional[str] = None,
    ) -> bool:
        """Add new invitee with original_lunch set to first lunch value."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO invitees
                (list_name, name, lunch, to_sakti, travel_by, original_lunch)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (list_name, name, lunch, to_sakti, travel_by, lunch),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding invitee: {e}")
            return False

    def update_invitee(
        self,
        list_name: str,
        name: str,
        lunch: int,
        to_sakti: Optional[int] = None,
        travel_by: Optional[str] = None,
    ) -> None:
        """Update invitee info; original_lunch stays unchanged."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            if to_sakti is not None or travel_by is not None:
                cur.execute(
                    """
                    UPDATE invitees
                    SET lunch = ?, to_sakti = ?, travel_by = ?
                    WHERE list_name = ? AND name = ?
                    """,
                    (lunch, to_sakti, travel_by, list_name, name),
                )
            else:
                cur.execute(
                    """
                    UPDATE invitees
                    SET lunch = ?
                    WHERE list_name = ? AND name = ?
                    """,
                    (lunch, list_name, name),
                )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating invitee: {e}")

    def delete_invitee(self, list_name: str, name: str) -> bool:
        """Delete invitee."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM invitees
                WHERE list_name = ? AND name = ?
                """,
                (list_name, name),
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting invitee: {e}")
            return False

    def reset_invitee(self, list_name: str, name: str) -> None:
        """Reset invitee lunch to original_lunch."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE invitees
                SET lunch = original_lunch
                WHERE list_name = ? AND name = ?
                """,
                (list_name, name),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error resetting invitee: {e}")

    def get_total_headcount(self, list_name: str) -> int:
        """Sum lunch for a list."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT SUM(lunch) AS total
                FROM invitees
                WHERE list_name = ?
                """,
                (list_name,),
            )
            row = cur.fetchone()
            conn.close()
            return int(row["total"]) if row and row["total"] is not None else 0
        except Exception as e:
            print(f"Error getting headcount: {e}")
            return 0

    def search_invitees(
        self,
        search_term: str,
        list_name: Optional[str] = None,
    ) -> List[Dict]:
        """Search invitees by name."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            pattern = f"%{search_term}%"
            if list_name:
                cur.execute(
                    """
                    SELECT * FROM invitees
                    WHERE list_name = ? AND name LIKE ?
                    ORDER BY list_name, name
                    """,
                    (list_name, pattern),
                )
            else:
                cur.execute(
                    """
                    SELECT * FROM invitees
                    WHERE name LIKE ?
                    ORDER BY list_name, name
                    """,
                    (pattern,),
                )
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            print(f"Error searching invitees: {e}")
            return []

    # ---------------------------------------------------------------------
    # MENU OPERATIONS
    # ---------------------------------------------------------------------
    def load_menu_data(self, df: pd.DataFrame) -> bool:
        """Load menus from CSV, replacing all."""
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cur = conn.cursor()

                    cur.execute("DELETE FROM menus")

                    for _, row in df.iterrows():
                        try:
                            if pd.isna(row.get("Date")) or pd.isna(row.get("Meal")):
                                continue
                            date = str(row["Date"]).strip()
                            meal = str(row["Meal"]).strip()
                            headcount = int(row["Headcount"])
                            items = str(row["Menu Items"])
                            cur.execute(
                                """
                                INSERT INTO menus
                                (date, meal, headcount, menu_items)
                                VALUES (?, ?, ?, ?)
                                """,
                                (date, meal, headcount, items),
                            )
                        except (ValueError, KeyError, sqlite3.IntegrityError):
                            continue

                    conn.commit()
                    conn.close()
                    return True
                except sqlite3.OperationalError:
                    retry_count += 1
                    time.sleep(0.2)
            return False
        except Exception as e:
            print(f"Error loading menu data: {e}")
            return False

    def get_menu(self, date: str, meal: str) -> Optional[Dict]:
        """Get menu row for a date+meal."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM menus
                WHERE date = ? AND meal = ?
                """,
                (date, meal),
            )
            row = cur.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting menu: {e}")
            return None

    def get_all_dates(self) -> List[str]:
        """Return all distinct menu dates."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT date FROM menus ORDER BY date")
            dates = [r[0] for r in cur.fetchall()]
            conn.close()
            return dates
        except Exception as e:
            print(f"Error getting dates: {e}")
            return []

    def get_meals_for_date(self, date: str) -> List[str]:
        """Return meal types available on a date."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                SELECT DISTINCT meal FROM menus
                WHERE date = ?
                ORDER BY meal
                """,
                (date,),
            )
            meals = [r[0] for r in cur.fetchall()]
            conn.close()
            return meals
        except Exception as e:
            print(f"Error getting meals: {e}")
            return []
