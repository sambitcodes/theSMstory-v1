"""
Database module for Tabu weds Mousumi application
Handles all SQLite database operations for ingredients and invitees
Fixed for Streamlit Cloud with proper connection handling
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Tuple, Optional
import os
import time
from config import DB_NAME, DB_TIMEOUT, INGREDIENT_LISTS, INVITEE_LISTS

class WeddingDatabase:
    """Main database class for managing wedding data with thread-safe operations"""
    
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper timeout and isolation"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=DB_TIMEOUT, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            # Enable WAL mode to prevent locking issues
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            return conn
        except sqlite3.OperationalError as e:
            # Retry on lock
            time.sleep(0.1)
            return sqlite3.connect(self.db_path, timeout=DB_TIMEOUT, check_same_thread=False)
    
    def init_database(self):
        """Initialize database tables"""
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                
                # Ingredients table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name TEXT NOT NULL,
                        item_name TEXT NOT NULL,
                        quantity REAL NOT NULL,
                        unit TEXT NOT NULL,
                        delivered_quantity REAL DEFAULT 0,
                        status TEXT DEFAULT 'Not Started',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(list_name, item_name)
                    )
                ''')
                
                # Invitees table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invitees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name TEXT NOT NULL,
                        name TEXT NOT NULL,
                        lunch INTEGER NOT NULL,
                        to_sakti INTEGER,
                        travel_by TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(list_name, name)
                    )
                ''')
                
                # Menu items table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS menus (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        meal TEXT NOT NULL,
                        headcount INTEGER NOT NULL,
                        menu_items TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(date, meal)
                    )
                ''')
                
                conn.commit()
                conn.close()
                break
            except sqlite3.OperationalError as e:
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.2)
                else:
                    print(f"Database initialization error: {e}")
    
    # ============== INGREDIENT OPERATIONS ==============
    
    def load_ingredient_list(self, list_name: str, df: pd.DataFrame) -> bool:
        """Load ingredient list from CSV to database"""
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    
                    # Clear existing list
                    cursor.execute('DELETE FROM ingredients WHERE list_name = ?', (list_name,))
                    
                    # Insert new data
                    for _, row in df.iterrows():
                        try:
                            cursor.execute('''
                                INSERT INTO ingredients 
                                (list_name, item_name, quantity, unit, delivered_quantity, status)
                                VALUES (?, ?, ?, ?, 0, 'Not Started')
                            ''', (list_name, str(row['Item Name']), float(row['Quantity']), str(row['Unit'])))
                        except (KeyError, ValueError, sqlite3.IntegrityError) as e:
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
        """Get all ingredients from a list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM ingredients WHERE list_name = ? ORDER BY item_name
            ''', (list_name,))
            
            ingredients = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return ingredients
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []
    
    def update_ingredient_status(self, list_name: str, item_name: str, 
                                status: str, delivered_qty: float = 0):
        """Update ingredient delivery status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE ingredients 
                SET status = ?, delivered_quantity = ?
                WHERE list_name = ? AND item_name = ?
            ''', (status, delivered_qty, list_name, item_name))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating ingredient status: {e}")
    
    def add_ingredient(self, list_name: str, item_name: str, 
                      quantity: float, unit: str):
        """Add new ingredient to list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ingredients 
                (list_name, item_name, quantity, unit, status)
                VALUES (?, ?, ?, ?, 'Not Started')
            ''', (list_name, item_name, quantity, unit))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False
    
    def update_ingredient(self, list_name: str, item_name: str, 
                         quantity: float, unit: str):
        """Update ingredient quantity"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE ingredients 
                SET quantity = ?, unit = ?
                WHERE list_name = ? AND item_name = ?
            ''', (quantity, unit, list_name, item_name))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating ingredient: {e}")
    
    def delete_ingredient(self, list_name: str, item_name: str) -> bool:
        """Delete ingredient from list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM ingredients 
                WHERE list_name = ? AND item_name = ?
            ''', (list_name, item_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting ingredient: {e}")
            return False
    
    def search_ingredients(self, search_term: str, list_name: Optional[str] = None) -> List[Dict]:
        """Search for ingredients across lists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term}%"
            
            if list_name:
                cursor.execute('''
                    SELECT * FROM ingredients 
                    WHERE list_name = ? AND item_name LIKE ?
                    ORDER BY list_name, item_name
                ''', (list_name, search_pattern))
            else:
                cursor.execute('''
                    SELECT * FROM ingredients 
                    WHERE item_name LIKE ?
                    ORDER BY list_name, item_name
                ''', (search_pattern,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"Error searching ingredients: {e}")
            return []
    
    # ============== INVITEE OPERATIONS ==============
    
    def load_invitee_list(self, list_name: str, df: pd.DataFrame) -> bool:
        """Load invitee list from CSV to database"""
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    
                    # Clear existing list
                    cursor.execute('DELETE FROM invitees WHERE list_name = ?', (list_name,))
                    
                    # Insert new data
                    for _, row in df.iterrows():
                        try:
                            to_sakti = None
                            travel_by = None
                            
                            if 'To SAKTI' in row.index:
                                val = row['To SAKTI']
                                to_sakti = int(val) if pd.notna(val) else None
                            if 'Travel By' in row.index:
                                val = row['Travel By']
                                travel_by = str(val) if pd.notna(val) else None
                            
                            cursor.execute('''
                                INSERT INTO invitees 
                                (list_name, name, lunch, to_sakti, travel_by)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (list_name, str(row['Name']), int(row['Lunch']), to_sakti, travel_by))
                        except (KeyError, ValueError, sqlite3.IntegrityError) as e:
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
        """Get all invitees from a list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM invitees WHERE list_name = ? ORDER BY name
            ''', (list_name,))
            
            invitees = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return invitees
        except Exception as e:
            print(f"Error getting invitees: {e}")
            return []
    
    def add_invitee(self, list_name: str, name: str, lunch: int,
                   to_sakti: Optional[int] = None, travel_by: Optional[str] = None) -> bool:
        """Add new invitee to list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO invitees 
                (list_name, name, lunch, to_sakti, travel_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (list_name, name, lunch, to_sakti, travel_by))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding invitee: {e}")
            return False
    
    def update_invitee(self, list_name: str, name: str, 
                      lunch: int, to_sakti: Optional[int] = None,
                      travel_by: Optional[str] = None):
        """Update invitee details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if to_sakti is not None and travel_by is not None:
                cursor.execute('''
                    UPDATE invitees 
                    SET lunch = ?, to_sakti = ?, travel_by = ?
                    WHERE list_name = ? AND name = ?
                ''', (lunch, to_sakti, travel_by, list_name, name))
            else:
                cursor.execute('''
                    UPDATE invitees 
                    SET lunch = ?
                    WHERE list_name = ? AND name = ?
                ''', (lunch, list_name, name))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating invitee: {e}")
    
    def delete_invitee(self, list_name: str, name: str) -> bool:
        """Delete invitee from list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM invitees 
                WHERE list_name = ? AND name = ?
            ''', (list_name, name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting invitee: {e}")
            return False
    
    def get_total_headcount(self, list_name: str) -> int:
        """Get total headcount for a list"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT SUM(lunch) as total FROM invitees WHERE list_name = ?
            ''', (list_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['total'] if result['total'] else 0
        except Exception as e:
            print(f"Error getting headcount: {e}")
            return 0
    
    def search_invitees(self, search_term: str, list_name: Optional[str] = None) -> List[Dict]:
        """Search for invitees across lists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term}%"
            
            if list_name:
                cursor.execute('''
                    SELECT * FROM invitees 
                    WHERE list_name = ? AND name LIKE ?
                    ORDER BY list_name, name
                ''', (list_name, search_pattern))
            else:
                cursor.execute('''
                    SELECT * FROM invitees 
                    WHERE name LIKE ?
                    ORDER BY list_name, name
                ''', (search_pattern,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except Exception as e:
            print(f"Error searching invitees: {e}")
            return []
    
    # ============== MENU OPERATIONS ==============
    
    def load_menu_data(self, df: pd.DataFrame) -> bool:
        """Load menu data from CSV"""
        try:
            retry_count = 0
            while retry_count < 3:
                try:
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    
                    # Clear existing menus
                    cursor.execute('DELETE FROM menus')
                    
                    # Insert new data
                    for _, row in df.iterrows():
                        try:
                            if pd.notna(row['Date']) and pd.notna(row['Meal']):
                                cursor.execute('''
                                    INSERT INTO menus 
                                    (date, meal, headcount, menu_items)
                                    VALUES (?, ?, ?, ?)
                                ''', (str(row['Date']), str(row['Meal']), 
                                      int(row['Headcount']), str(row['Menu Items'])))
                        except (KeyError, ValueError, sqlite3.IntegrityError) as e:
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
        """Get menu for specific date and meal"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM menus WHERE date = ? AND meal = ?
            ''', (date, meal))
            
            result = cursor.fetchone()
            conn.close()
            
            return dict(result) if result else None
        except Exception as e:
            print(f"Error getting menu: {e}")
            return None
    
    def get_all_dates(self) -> List[str]:
        """Get all unique dates from menus"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT DISTINCT date FROM menus ORDER BY date')
            dates = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return dates
        except Exception as e:
            print(f"Error getting dates: {e}")
            return []
    
    def get_meals_for_date(self, date: str) -> List[str]:
        """Get all meals for a specific date"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT DISTINCT meal FROM menus WHERE date = ? ORDER BY meal', (date,))
            meals = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return meals
        except Exception as e:
            print(f"Error getting meals: {e}")
            return []
