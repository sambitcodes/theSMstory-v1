"""
Main Streamlit Application - Tabu weds Mousumi
Wedding Management System with Beautiful UI.
Includes per-card Reset for ingredients and invitees and enhanced metrics.
"""

import os
import time

import pandas as pd
import streamlit as st

from config import (
    APP_TITLE,
    COLORS,
    INGREDIENT_LISTS,
    INVITEE_LISTS,
    DELIVERY_STATUS,
    TRAVEL_OPTIONS,
)
from database import WeddingDatabase
from utils import (
    render_header,
    render_footer,
    render_decorative_line,
    render_status_badge,
    render_alert,
    render_empty_state,
    validate_ingredient_input,
    validate_invitee_input,
    format_quantity_display,
    render_metric_box,
    render_wedding_theme_background,
)

# ---------------------------------------------------------------------
# Streamlit page config
# ---------------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Database init (cached)
# ---------------------------------------------------------------------
@st.cache_resource
def init_db() -> WeddingDatabase:
    return WeddingDatabase()


db = init_db()

# ---------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------
render_wedding_theme_background()
render_header()

# ---------------------------------------------------------------------
# CSV mappings (root-level files)
# ---------------------------------------------------------------------
csv_files_ingredients = {
    "Local-List": "data/ingredients/Local-List.csv",
    "Reception-Raasan": "data/ingredients/Reception-Raasan.csv",
    "Reception-Tent": "data/ingredients/Reception-Tent.csv",
    "Reception-Extras": "data/ingredients/Reception-Extras.csv",
    "Reception-Pakoda": "data/ingredients/Reception-Pakoda.csv",
    "Reception-Coffee": "data/ingredients/Reception-Coffee.csv",
    "Home-Raasan": "data/ingredients/Home-Raasan.csv",
    "Home-Dessert": "data/ingredients/Home-Dessert.csv",
    "Home-Tent": "data/ingredients/Home-Tent.csv",
}

csv_files_invitees = {
    "Invitee-List-Poite-03.12.25": "data/invitees/Invitee-List-Poite-03.12.25.csv",
    "Invitee-List-Barati-05.12.25": "data/invitees/Invitee-List-Barati-05.12.25.csv",
    "Invitee-List-Boubhaat-07.12.25": "data/invitees/Invitee-List-Boubhaat-07.12.25.csv",
    "Invitee-List-Return-06.12.25": "data/invitees/Invitee-List-Return-06.12.25.csv",
}

menu_csv = "data/menus/Menus-List.csv"

# ---------------------------------------------------------------------
# One-time CSV -> DB load (cached)
# ---------------------------------------------------------------------
@st.cache_resource
def load_initial_data() -> None:
    """Load CSV files into SQLite once per deployment."""
    # Ingredients
    for list_name, path in csv_files_ingredients.items():
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df.columns = df.columns.str.strip()
                db.load_ingredient_list(list_name, df)
                time.sleep(0.05)
            except Exception as e:
                st.warning(f"Could not load {path}: {e}")

    # Invitees
    for list_name, path in csv_files_invitees.items():
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df.columns = df.columns.str.strip()
                db.load_invitee_list(list_name, df)
                time.sleep(0.05)
            except Exception as e:
                st.warning(f"Could not load {path}: {e}")

    # Menus
    if os.path.exists(menu_csv):
        try:
            df = pd.read_csv(menu_csv)
            df.columns = df.columns.str.strip()
            db.load_menu_data(df)
        except Exception as e:
            st.warning(f"Could not load {menu_csv}: {e}")


load_initial_data()

# ---------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📦 Track Ingredients", "👥 Track Invitees", "🍽️ Menu Planning", "🔍 Global Search"]
)

# ---------------------------------------------------------------------
# TAB 1: INGREDIENTS
# ---------------------------------------------------------------------
with tab1:
    st.markdown("### 📦 Ingredient Delivery Tracking")
    render_decorative_line()

    c1, c2 = st.columns([3, 1])
    with c1:
        selected_list = st.selectbox(
            "Select Ingredient List",
            options=list(INGREDIENT_LISTS.keys()),
            format_func=lambda k: INGREDIENT_LISTS[k],
            key="ingredient_list_selector",
        )
    with c2:
        if st.button("🔄 Refresh", key="refresh_ingredients"):
            st.rerun()

    if selected_list:
        ingredients = db.get_ingredients(selected_list)

        if ingredients:
            # Summary metrics (counts)
            total_items = len(ingredients)
            completed_items = [i for i in ingredients if i["status"] == "Completed"]
            incomplete_items = [i for i in ingredients if i["status"] == "Incomplete"]

            s1, s2, s3 = st.columns(3)
            with s1:
                render_metric_box("Total Items", str(total_items), "📊")
            with s2:
                render_metric_box("Completed Items", str(len(completed_items)), "✅")
            with s3:
                render_metric_box("Incomplete Items", str(len(incomplete_items)), "⚠️")

            # Quantities: total, complete, incomplete
            total_qty = sum(float(i["quantity"]) for i in ingredients)
            total_incomplete_qty = sum(
                float(i.get("delivered_quantity") or 0.0) for i in incomplete_items
            )
            total_complete_qty = total_qty - total_incomplete_qty

            q1, q2, q3 = st.columns(3)
            with q1:
                render_metric_box("Total Quantity", str(total_qty), "📦")
            with q2:
                render_metric_box("Completed Qty", str(total_complete_qty), "✅")
            with q3:
                render_metric_box("Incomplete Qty", str(total_incomplete_qty), "⚠️")

            st.divider()

            # Local search
            sc1, sc2 = st.columns([3, 1])
            with sc1:
                search_term = st.text_input(
                    "🔍 Search in this list", key=f"local_search_{selected_list}"
                )
            with sc2:
                st.write("")
                if st.button("Clear", key=f"clear_search_{selected_list}"):
                    search_term = ""
                    st.session_state[f"local_search_{selected_list}"] = ""

            if search_term:
                filtered = [
                    i
                    for i in ingredients
                    if search_term.lower() in i["item_name"].lower()
                ]
            else:
                filtered = ingredients

            if filtered:
                # Split into sections
                incomplete_filtered = [
                    i for i in filtered if i["status"] == "Incomplete"
                ]
                completed_filtered = [i for i in filtered if i["status"] == "Completed"]
                other_filtered = [
                    i
                    for i in filtered
                    if i["status"] not in ("Incomplete", "Completed")
                ]

                def render_ingredient_cards(items, section_key_prefix: str):
                    for idx, ing in enumerate(items):
                        row_key = f"{section_key_prefix}_{idx}_{selected_list}"
                        with st.container():
                            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                                [2.2, 1.4, 1.2, 1.6, 1.2, 1.2, 0.7]
                            )

                            # Name
                            with col1:
                                st.write(f"**{ing['item_name']}**")

                            # Current quantity
                            with col2:
                                st.write(
                                    format_quantity_display(
                                        ing["quantity"], ing["unit"]
                                    )
                                )

                            # Status
                            with col3:
                                st.markdown(
                                    render_status_badge(ing["status"]),
                                    unsafe_allow_html=True,
                                )

                            # Complete / Incomplete
                            with col4:
                                b1, b2 = st.columns(2)
                                with b1:
                                    if st.button(
                                        "✓",
                                        key=f"complete_{row_key}",
                                        help="Mark complete",
                                    ):
                                        db.update_ingredient_status(
                                            selected_list,
                                            ing["item_name"],
                                            "Completed",
                                            0.0,
                                        )
                                        st.rerun()
                                with b2:
                                    if st.button(
                                        "✗",
                                        key=f"incomplete_{row_key}",
                                        help="Mark incomplete",
                                    ):
                                        st.session_state[
                                            f"enter_qty_{row_key}"
                                        ] = True

                            # Edit quantity
                            with col5:
                                if st.button(
                                    "Edit Qty",
                                    key=f"edit_qty_btn_{row_key}",
                                    help="Update item quantity",
                                ):
                                    st.session_state[
                                        f"edit_qty_{row_key}"
                                    ] = True

                            # Reset to original
                            with col6:
                                if st.button(
                                    "Reset",
                                    key=f"reset_{row_key}",
                                    help="Reset to original quantity & status",
                                ):
                                    db.reset_ingredient(selected_list, ing["item_name"])
                                    st.rerun()

                            # Spacer
                            with col7:
                                pass

                            # Incomplete quantity entry
                            if st.session_state.get(
                                f"enter_qty_{row_key}", False
                            ):
                                q = st.number_input(
                                    f"Quantity not delivered for {ing['item_name']}",
                                    min_value=0.0,
                                    max_value=float(ing["quantity"]),
                                    key=f"qty_input_{row_key}",
                                )
                                s1c, s2c = st.columns([1, 3])
                                with s1c:
                                    if st.button(
                                        "Save",
                                        key=f"save_incomplete_{row_key}",
                                    ):
                                        db.update_ingredient_status(
                                            selected_list,
                                            ing["item_name"],
                                            "Incomplete",
                                            q,
                                        )
                                        st.session_state[
                                            f"enter_qty_{row_key}"
                                        ] = False
                                        st.rerun()

                            # Edit quantity form
                            if st.session_state.get(
                                f"edit_qty_{row_key}", False
                            ):
                                new_q_col1, new_q_col2 = st.columns([2, 1])
                                with new_q_col1:
                                    new_qty_val = st.number_input(
                                        f"New quantity for {ing['item_name']}",
                                        min_value=0.0,
                                        value=float(ing["quantity"]),
                                        key=f"new_qty_val_{row_key}",
                                    )
                                with new_q_col2:
                                    if st.button(
                                        "Update",
                                        key=f"update_qty_{row_key}",
                                    ):
                                        db.update_ingredient(
                                            selected_list,
                                            ing["item_name"],
                                            new_qty_val,
                                            ing["unit"],
                                        )
                                        st.session_state[
                                            f"edit_qty_{row_key}"
                                        ] = False
                                        st.rerun()

                            st.divider()

                # Sections
                if incomplete_filtered:
                    st.markdown("#### ⚠️ Incomplete Items")
                    render_ingredient_cards(incomplete_filtered, "inc")
                if completed_filtered:
                    st.markdown("#### ✅ Completed Items")
                    render_ingredient_cards(completed_filtered, "comp")
                if other_filtered:
                    st.markdown("#### 📦 Other Items")
                    render_ingredient_cards(other_filtered, "other")
            else:
                render_empty_state("No ingredients found", "🔍")

            # Add new ingredient
            st.markdown("#### ➕ Add New Ingredient")
            a1, a2, a3, a4 = st.columns([2, 1.5, 1, 1])
            with a1:
                new_name = st.text_input(
                    "Item Name", key=f"new_item_{selected_list}"
                )
            with a2:
                new_qty = st.number_input(
                    "Quantity", min_value=0.0, key=f"new_qty_{selected_list}"
                )
            with a3:
                new_unit = st.text_input("Unit", key=f"new_unit_{selected_list}")
            with a4:
                st.write("")
                if st.button("Add Item", key=f"add_item_{selected_list}"):
                    ok, msg = validate_ingredient_input(
                        new_name, str(new_qty), new_unit
                    )
                    if ok:
                        if db.add_ingredient(
                            selected_list,
                            new_name,
                            float(new_qty),
                            new_unit,
                        ):
                            render_alert("Ingredient added.", "success")
                            st.rerun()
                        else:
                            render_alert("Ingredient already exists.", "error")
                    else:
                        render_alert(msg, "error")
        else:
            render_empty_state("No ingredients in this list", "📭")

# ---------------------------------------------------------------------
# TAB 2: INVITEES
# ---------------------------------------------------------------------
with tab2:
    st.markdown("### 👥 Invitee Management")
    render_decorative_line()

    c1, c2 = st.columns([3, 1])
    with c1:
        selected_inv_list = st.selectbox(
            "Select Guest List",
            options=list(INVITEE_LISTS.keys()),
            format_func=lambda k: INVITEE_LISTS[k],
            key="invitee_list_selector",
        )
    with c2:
        if st.button("🔄 Refresh", key="refresh_invitees"):
            st.rerun()

    if selected_inv_list:
        invitees = db.get_invitees(selected_inv_list)
        total_headcount = db.get_total_headcount(selected_inv_list)

        is_barati = (
            "Barati" in selected_inv_list
            or "Barati" in INVITEE_LISTS.get(selected_inv_list, "")
        )

        if is_barati:
            # Extra stats for Barati
            total_to_sakti = sum(int(g.get("to_sakti") or 0) for g in invitees)

            def _travel(v: Optional[str]) -> str:
                return (v or "").strip().lower()

            bus_headcount = sum(
                int(g.get("to_sakti") or 0)
                for g in invitees
                if _travel(g.get("travel_by")) == "bus"
            )
            car_headcount = sum(
                int(g.get("to_sakti") or 0)
                for g in invitees
                if _travel(g.get("travel_by")) == "car"
            )

            c1m, c2m, c3m, c4m = st.columns(4)
            with c1m:
                render_metric_box("Total Guests", str(len(invitees)), "👥")
            with c2m:
                render_metric_box("Total Headcount", str(total_headcount), "🍽️")
            with c3m:
                render_metric_box("People to Sakti", str(total_to_sakti), "🧳")
            with c4m:
                render_metric_box(
                    "Travel (Bus / Car)",
                    f"Bus: {bus_headcount} | Car: {car_headcount}",
                    "🚌",
                )
        else:
            s1, s2, s3 = st.columns(3)
            with s1:
                render_metric_box("Total Guests", str(len(invitees)), "👥")
            with s2:
                render_metric_box("Total Headcount", str(total_headcount), "🍽️")
            with s3:
                render_metric_box("Barati Special", "No", "✨")

        st.divider()

        # Local search
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            inv_search = st.text_input(
                "🔍 Search guest", key=f"invitee_search_{selected_inv_list}"
            )
        with sc2:
            st.write("")
            if st.button(
                "Clear", key=f"clear_invitee_search_{selected_inv_list}"
            ):
                inv_search = ""
                st.session_state[f"invitee_search_{selected_inv_list}"] = ""

        if inv_search:
            filtered_inv = [
                g for g in invitees if inv_search.lower() in g["name"].lower()
            ]
        else:
            filtered_inv = invitees

        if filtered_inv:
            is_barati = (
                "Barati" in selected_inv_list
                or "Barati" in INVITEE_LISTS.get(selected_inv_list, "")
            )
            for idx, guest in enumerate(filtered_inv):
                with st.container():
                    if is_barati:
                        # Barati layout: name, lunch ±, Sakti ±, travel, reset
                        col1, col2, col3, col4, col5, col6, col7 = st.columns(
                            [2, 0.7, 0.7, 0.9, 1.8, 1.2, 0.9]
                        )
                        with col1:
                            st.write(f"**{guest['name']}**")

                        # Lunch - / count / +
                        with col2:
                            if st.button(
                                "➖",
                                key=f"lunch_minus_{idx}_{selected_inv_list}",
                            ):
                                if guest["lunch"] > 1:
                                    db.update_invitee(
                                        selected_inv_list,
                                        guest["name"],
                                        guest["lunch"] - 1,
                                        guest.get("to_sakti"),
                                        guest.get("travel_by"),
                                    )
                                    st.rerun()
                        with col3:
                            st.write(f"**{guest['lunch']}**")
                        with col4:
                            if st.button(
                                "➕",
                                key=f"lunch_plus_{idx}_{selected_inv_list}",
                            ):
                                db.update_invitee(
                                    selected_inv_list,
                                    guest["name"],
                                    guest["lunch"] + 1,
                                    guest.get("to_sakti"),
                                    guest.get("travel_by"),
                                )
                                st.rerun()

                        # Sakti - / label / +
                        current_sakti = int(guest.get("to_sakti") or 0)
                        with col5:
                            s1c, s2c, s3c = st.columns([0.8, 1.2, 0.8])
                            with s1c:
                                if st.button(
                                    "➖",
                                    key=f"sakti_minus_{idx}_{selected_inv_list}",
                                ):
                                    if current_sakti > 0:
                                        new_sakti = current_sakti - 1
                                        db.update_invitee(
                                            selected_inv_list,
                                            guest["name"],
                                            guest["lunch"],
                                            new_sakti,
                                            guest.get("travel_by"),
                                        )
                                        st.rerun()
                            with s2c:
                                st.write(f"Sakti: **{current_sakti}**")
                            with s3c:
                                if st.button(
                                    "➕",
                                    key=f"sakti_plus_{idx}_{selected_inv_list}",
                                ):
                                    if current_sakti < int(guest["lunch"]):
                                        new_sakti = current_sakti + 1
                                        db.update_invitee(
                                            selected_inv_list,
                                            guest["name"],
                                            guest["lunch"],
                                            new_sakti,
                                            guest.get("travel_by"),
                                        )
                                        st.rerun()

                        # Travel by
                        with col6:
                            travel = st.selectbox(
                                "Travel",
                                TRAVEL_OPTIONS,
                                index=TRAVEL_OPTIONS.index(
                                    guest.get("travel_by")
                                )
                                if guest.get("travel_by") in TRAVEL_OPTIONS
                                else 0,
                                key=f"travel_{idx}_{selected_inv_list}",
                            )
                            if travel != guest.get("travel_by"):
                                db.update_invitee(
                                    selected_inv_list,
                                    guest["name"],
                                    guest["lunch"],
                                    guest.get("to_sakti"),
                                    travel,
                                )
                                st.rerun()

                        # Reset: lunch, to_sakti, travel_by
                        with col7:
                            if st.button(
                                "Reset",
                                key=f"reset_guest_{idx}_{selected_inv_list}",
                            ):
                                db.reset_invitee(selected_inv_list, guest["name"])
                                st.rerun()
                    else:
                        # Non-Barati layout
                        col1, col2, col3, col4, col5 = st.columns(
                            [2, 0.7, 0.7, 0.9, 0.9]
                        )
                        with col1:
                            st.write(f"**{guest['name']}**")
                        with col2:
                            if st.button(
                                "➖",
                                key=f"lunch_minus_simple_{idx}_{selected_inv_list}",
                            ):
                                if guest["lunch"] > 1:
                                    db.update_invitee(
                                        selected_inv_list,
                                        guest["name"],
                                        guest["lunch"] - 1,
                                    )
                                    st.rerun()
                        with col3:
                            st.write(f"**{guest['lunch']}**")
                        with col4:
                            if st.button(
                                "➕",
                                key=f"lunch_plus_simple_{idx}_{selected_inv_list}",
                            ):
                                db.update_invitee(
                                    selected_inv_list,
                                    guest["name"],
                                    guest["lunch"] + 1,
                                )
                                st.rerun()
                        with col5:
                            if st.button(
                                "Reset",
                                key=f"reset_guest_simple_{idx}_{selected_inv_list}",
                            ):
                                db.reset_invitee(selected_inv_list, guest["name"])
                                st.rerun()

                st.divider()
        else:
            render_empty_state("No guests found", "🔍")

        # Add new guest
        st.markdown("#### ➕ Add New Guest")
        a1, a2, a3 = st.columns([2, 1, 1])
        with a1:
            new_name = st.text_input(
                "Guest Name", key=f"new_guest_{selected_inv_list}"
            )
        with a2:
            new_lunch = st.number_input(
                "Headcount",
                min_value=1,
                key=f"new_guest_lunch_{selected_inv_list}",
            )
        with a3:
            st.write("")
            if st.button("Add Guest", key=f"add_guest_{selected_inv_list}"):
                ok, msg = validate_invitee_input(new_name, str(new_lunch))
                if not ok:
                    render_alert(msg, "error")
                else:
                    if is_barati:
                        s1c, s2c = st.columns(2)
                        with s1c:
                            to_sakti = st.number_input(
                                "To Sakti",
                                min_value=0,
                                max_value=int(new_lunch),
                                key=f"new_sakti_{selected_inv_list}",
                            )
                        with s2c:
                            travel = st.selectbox(
                                "Travel",
                                TRAVEL_OPTIONS,
                                key=f"new_travel_{selected_inv_list}",
                            )
                        if db.add_invitee(
                            selected_inv_list,
                            new_name,
                            int(new_lunch),
                            int(to_sakti),
                            travel,
                        ):
                            render_alert("Guest added.", "success")
                            st.rerun()
                        else:
                            render_alert("Guest already exists.", "error")
                    else:
                        if db.add_invitee(
                            selected_inv_list, new_name, int(new_lunch)
                        ):
                            render_alert("Guest added.", "success")
                            st.rerun()
                        else:
                            render_alert("Guest already exists.", "error")

# ---------------------------------------------------------------------
# TAB 3: MENU
# ---------------------------------------------------------------------
with tab3:
    st.markdown("### 🍽️ Menu Planning & Details")
    render_decorative_line()

    c1, c2 = st.columns([3, 1])
    with c1:
        dates = db.get_all_dates()
        if dates:
            selected_date = st.selectbox(
                "Select Date", options=dates, key="menu_date_selector"
            )
        else:
            selected_date = None
            st.info("No menu data available.")
    with c2:
        if st.button("🔄 Refresh", key="refresh_menu"):
            st.rerun()

    if selected_date:
        meals = db.get_meals_for_date(selected_date)
        if meals:
            selected_meal = st.selectbox(
                "Select Meal", options=meals, key=f"meal_{selected_date}"
            )
            menu_row = db.get_menu(selected_date, selected_meal)
            if menu_row:
                st.divider()
                m1, m2 = st.columns(2)
                with m1:
                    render_metric_box("Date", selected_date, "📅")
                with m2:
                    render_metric_box(
                        "Headcount", str(menu_row["headcount"]), "🍽️"
                    )

                st.divider()
                st.markdown("#### 📋 Menu Items")
                st.markdown(
                    f"""
                    <div style="background:#fdf5e6;padding:20px;border-radius:10px;
                                border-left:4px solid #d4af37;">
                        {menu_row['menu_items']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                text = (
                    f"Date: {selected_date}\n"
                    f"Meal: {selected_meal}\n"
                    f"Headcount: {menu_row['headcount']}\n\n"
                    f"Menu:\n{menu_row['menu_items']}"
                )
                st.download_button(
                    "📄 Download",
                    data=text,
                    file_name=f"Menu_{selected_date}_{selected_meal}.txt",
                )
        else:
            render_empty_state("No meals for this date.", "🍽️")

# ---------------------------------------------------------------------
# TAB 4: GLOBAL SEARCH
# ---------------------------------------------------------------------
with tab4:
    st.markdown("### 🔍 Global Search")
    render_decorative_line()

    mode = st.radio("Search Type", ["Ingredients", "Guests"], horizontal=True)
    term = st.text_input("🔎 Search everywhere")

    if term:
        if mode == "Ingredients":
            res = db.search_ingredients(term)
            if res:
                st.success(f"Found {len(res)} ingredient(s).")
                by_list = {}
                for r in res:
                    by_list.setdefault(r["list_name"], []).append(r)
                for lst, items in by_list.items():
                    label = INGREDIENT_LISTS.get(lst, lst)
                    with st.expander(f"📦 {label} ({len(items)})"):
                        for r in items:
                            c1, c2, c3 = st.columns([2, 1.5, 1])
                            with c1:
                                st.write(f"**{r['item_name']}**")
                            with c2:
                                st.write(
                                    format_quantity_display(
                                        r["quantity"], r["unit"]
                                    )
                                )
                            with c3:
                                st.markdown(
                                    render_status_badge(r["status"]),
                                    unsafe_allow_html=True,
                                )
            else:
                render_empty_state("No ingredients found.", "🔍")
        else:
            res = db.search_invitees(term)
            if res:
                st.success(f"Found {len(res)} guest(s).")
                by_list = {}
                for r in res:
                    by_list.setdefault(r["list_name"], []).append(r)
                for lst, items in by_list.items():
                    label = INVITEE_LISTS.get(lst, lst)
                    with st.expander(f"👥 {label} ({len(items)})"):
                        for r in items:
                            c1, c2 = st.columns([2, 1])
                            with c1:
                                st.write(f"**{r['name']}**")
                            with c2:
                                st.write(f"Headcount: **{r['lunch']}**")
            else:
                render_empty_state("No guests found.", "🔍")
    else:
        render_empty_state("Enter a search term to begin.", "🔍")

st.divider()
render_footer()
