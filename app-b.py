"""
Main Streamlit Application - Tabu weds Mousumi
Wedding Management System with Beautiful UI
FIXED: Improved data loading with error handling
"""

import streamlit as st
import pandas as pd
import io
from config import (
    APP_TITLE, COLORS, INGREDIENT_LISTS, INVITEE_LISTS, 
    MENU_DATES, DELIVERY_STATUS, TRAVEL_OPTIONS, SESSION_KEYS
)
from database import WeddingDatabase
from utils import (
    render_header, render_footer, render_decorative_line,
    render_status_badge, render_alert, render_empty_state,
    validate_ingredient_input, validate_invitee_input,
    format_quantity_display, render_summary_card, render_metric_box,
    render_wedding_theme_background
)
import os

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database in session state
@st.cache_resource
def init_db():
    return WeddingDatabase()

db = init_db()

# Apply wedding theme
render_wedding_theme_background()

# Render header
render_header()

# Initialize CSV data files mapping
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

# put in data/menus folder
menu_csv = "data/menus/Menus-List.csv"

# Load data on first run with improved error handling
@st.cache_resource
def load_initial_data():
    """Load initial CSV data into database with error handling"""
    import time
    
    # Load ingredients
    for list_name, csv_file in csv_files_ingredients.items():
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                # Normalize column names
                df.columns = df.columns.str.strip()
                success = db.load_ingredient_list(list_name, df)
                time.sleep(0.1)  # Small delay between operations
            except Exception as e:
                st.warning(f"Could not load {csv_file}: {str(e)}")
    
    # Load invitees
    for list_name, csv_file in csv_files_invitees.items():
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                # Normalize column names
                df.columns = df.columns.str.strip()
                success = db.load_invitee_list(list_name, df)
                time.sleep(0.1)  # Small delay between operations
            except Exception as e:
                st.warning(f"Could not load {csv_file}: {str(e)}")
    
    # Load menus
    if os.path.exists(menu_csv):
        try:
            df = pd.read_csv(menu_csv)
            # Normalize column names
            df.columns = df.columns.str.strip()
            success = db.load_menu_data(df)
        except Exception as e:
            st.warning(f"Could not load {menu_csv}: {str(e)}")

# Load data
load_initial_data()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📦 Track Ingredients", "👥 Track Invitees", "🍽️ Menu Planning", "🔍 Global Search"])

# ======================== TAB 1: TRACKING INGREDIENTS ========================

with tab1:
    st.markdown("### 📦 Ingredient Delivery Tracking")
    render_decorative_line()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_list = st.selectbox(
            "Select Ingredient List",
            options=list(INGREDIENT_LISTS.keys()),
            format_func=lambda x: INGREDIENT_LISTS[x],
            key="ingredient_list_selector"
        )
    
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_ingredients"):
            st.rerun()
    
    if selected_list:
        ingredients = db.get_ingredients(selected_list)
        
        if ingredients:
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                render_metric_box("Total Items", str(len(ingredients)), "📊")
            with col2:
                completed = sum(1 for i in ingredients if i['status'] == 'Completed')
                render_metric_box("Completed", str(completed), "✓")
            with col3:
                incomplete = sum(1 for i in ingredients if i['status'] == 'Incomplete')
                render_metric_box("Incomplete", str(incomplete), "✗")
            
            st.divider()
            
            # Local search
            search_col1, search_col2 = st.columns([3, 1])
            with search_col1:
                search_term = st.text_input("🔍 Search in this list", key=f"local_search_{selected_list}")
            with search_col2:
                st.write("")
                if st.button("Clear", key=f"clear_search_{selected_list}"):
                    search_term = ""
            
            # Filter ingredients based on search
            if search_term:
                filtered_ingredients = [i for i in ingredients 
                                       if search_term.lower() in i['item_name'].lower()]
            else:
                filtered_ingredients = ingredients
            
            if filtered_ingredients:
                # Display ingredients
                for idx, ingredient in enumerate(filtered_ingredients):
                    with st.container():
                        col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1, 1.5, 1])
                        
                        with col1:
                            st.write(f"**{ingredient['item_name']}**")
                        
                        with col2:
                            st.write(f"{format_quantity_display(ingredient['quantity'], ingredient['unit'])}")
                        
                        with col3:
                            status_html = render_status_badge(ingredient['status'])
                            st.markdown(status_html, unsafe_allow_html=True)
                        
                        with col4:
                            # Status update buttons
                            col_c, col_i = st.columns(2)
                            with col_c:
                                if st.button("✓", key=f"complete_{idx}_{selected_list}", help="Mark Complete"):
                                    db.update_ingredient_status(selected_list, ingredient['item_name'], 'Completed', 0)
                                    st.rerun()
                            with col_i:
                                if st.button("✗", key=f"incomplete_{idx}_{selected_list}", help="Mark Incomplete"):
                                    st.session_state[f"enter_qty_{idx}"] = True
                        
                        with col5:
                            if st.button("⋮", key=f"menu_{idx}_{selected_list}"):
                                st.session_state[f"show_menu_{idx}_{selected_list}"] = True
                        
                        # Show quantity input if incomplete is selected
                        if st.session_state.get(f"enter_qty_{idx}"):
                            qty_input = st.number_input(
                                f"Quantity not delivered for {ingredient['item_name']}",
                                min_value=0.0,
                                max_value=float(ingredient['quantity']),
                                key=f"qty_input_{idx}_{selected_list}"
                            )
                            if st.button("Save", key=f"save_qty_{idx}_{selected_list}"):
                                db.update_ingredient_status(selected_list, ingredient['item_name'], 'Incomplete', qty_input)
                                st.session_state[f"enter_qty_{idx}"] = False
                                st.rerun()
                        
                        # Show menu options if menu button clicked
                        if st.session_state.get(f"show_menu_{idx}_{selected_list}"):
                            menu_col1, menu_col2, menu_col3 = st.columns([1, 1, 1])
                            with menu_col1:
                                if st.button(f"📝 Edit", key=f"edit_{idx}_{selected_list}"):
                                    st.session_state[f"edit_mode_{idx}"] = True
                            with menu_col2:
                                if st.button(f"🗑️ Delete", key=f"delete_{idx}_{selected_list}"):
                                    if st.session_state.get(f"confirm_delete_{idx}"):
                                        db.delete_ingredient(selected_list, ingredient['item_name'])
                                        st.session_state[f"show_menu_{idx}_{selected_list}"] = False
                                        st.rerun()
                                    else:
                                        st.session_state[f"confirm_delete_{idx}"] = True
                                        st.warning(f"Are you sure? Click again to confirm.")
                        
                        st.divider()
            else:
                render_empty_state("No ingredients found", "🔍")
            
            # Add new ingredient section
            st.markdown("#### ➕ Add New Ingredient")
            col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])
            
            with col1:
                new_item = st.text_input("Item Name", key=f"new_item_{selected_list}")
            with col2:
                new_qty = st.number_input("Quantity", min_value=0.0, key=f"new_qty_{selected_list}")
            with col3:
                new_unit = st.text_input("Unit", key=f"new_unit_{selected_list}")
            with col4:
                st.write("")
                if st.button("Add Item", key=f"add_item_{selected_list}"):
                    is_valid, error_msg = validate_ingredient_input(new_item, str(new_qty), new_unit)
                    if is_valid:
                        if db.add_ingredient(selected_list, new_item, new_qty, new_unit):
                            render_alert("✓ Ingredient added successfully!", "success")
                            st.rerun()
                        else:
                            render_alert("✗ Ingredient already exists", "error")
                    else:
                        render_alert(error_msg, "error")
        else:
            render_empty_state("No ingredients in this list", "📭")

# ======================== TAB 2: TRACKING INVITEES ========================

with tab2:
    st.markdown("### 👥 Invitee Management")
    render_decorative_line()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_invitee_list = st.selectbox(
            "Select Guest List",
            options=list(INVITEE_LISTS.keys()),
            format_func=lambda x: INVITEE_LISTS[x],
            key="invitee_list_selector"
        )
    
    with col2:
        if st.button("🔄 Refresh Data", key="refresh_invitees"):
            st.rerun()
    
    if selected_invitee_list:
        invitees = db.get_invitees(selected_invitee_list)
        total_headcount = db.get_total_headcount(selected_invitee_list)
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            render_metric_box("Total Guests", str(len(invitees)), "👥")
        with col2:
            render_metric_box("Total Headcount", str(total_headcount), "🍽️")
        with col3:
            is_barati = "Barati" in selected_invitee_list
            if is_barati:
                render_metric_box("Special Event", "Yes", "✨")
        
        st.divider()
        
        # Local search for invitees
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            invitee_search = st.text_input("🔍 Search guest", key=f"invitee_search_{selected_invitee_list}")
        with search_col2:
            st.write("")
            if st.button("Clear", key=f"clear_invitee_search_{selected_invitee_list}"):
                invitee_search = ""
        
        # Filter invitees
        if invitee_search:
            filtered_invitees = [i for i in invitees 
                                if invitee_search.lower() in i['name'].lower()]
        else:
            filtered_invitees = invitees
        
        if filtered_invitees:
            # Display invitees
            is_barati = "Barati" in selected_invitee_list
            
            for idx, invitee in enumerate(filtered_invitees):
                with st.container():
                    if is_barati:
                        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                        with col1:
                            st.write(f"**{invitee['name']}**")
                        with col2:
                            if st.button("➖", key=f"lunch_minus_{idx}_{selected_invitee_list}"):
                                if invitee['lunch'] > 1:
                                    db.update_invitee(selected_invitee_list, invitee['name'], 
                                                     invitee['lunch'] - 1, invitee['to_sakti'], invitee['travel_by'])
                                    st.rerun()
                        with col2:
                            st.write(f"**{invitee['lunch']}**")
                        with col2:
                            if st.button("➕", key=f"lunch_plus_{idx}_{selected_invitee_list}"):
                                db.update_invitee(selected_invitee_list, invitee['name'],
                                                 invitee['lunch'] + 1, invitee['to_sakti'], invitee['travel_by'])
                                st.rerun()
                        with col3:
                            st.write(f"Sakti: **{invitee['to_sakti']}**")
                        with col4:
                            travel = st.selectbox(
                                "Transport",
                                options=TRAVEL_OPTIONS,
                                index=TRAVEL_OPTIONS.index(invitee['travel_by']) if invitee['travel_by'] in TRAVEL_OPTIONS else 0,
                                key=f"travel_{idx}_{selected_invitee_list}"
                            )
                            if travel != invitee['travel_by']:
                                db.update_invitee(selected_invitee_list, invitee['name'],
                                                 invitee['lunch'], invitee['to_sakti'], travel)
                                st.rerun()
                        with col5:
                            if st.button("🗑️", key=f"delete_invitee_{idx}_{selected_invitee_list}"):
                                if st.session_state.get(f"confirm_delete_invitee_{idx}"):
                                    db.delete_invitee(selected_invitee_list, invitee['name'])
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_invitee_{idx}"] = True
                                    st.warning("Confirm deletion?")
                    else:
                        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                        with col1:
                            st.write(f"**{invitee['name']}**")
                        with col2:
                            if st.button("➖", key=f"lunch_minus_simple_{idx}_{selected_invitee_list}"):
                                if invitee['lunch'] > 1:
                                    db.update_invitee(selected_invitee_list, invitee['name'], invitee['lunch'] - 1)
                                    st.rerun()
                        with col2:
                            st.write(f"**{invitee['lunch']}**")
                        with col2:
                            if st.button("➕", key=f"lunch_plus_simple_{idx}_{selected_invitee_list}"):
                                db.update_invitee(selected_invitee_list, invitee['name'], invitee['lunch'] + 1)
                                st.rerun()
                        with col5:
                            if st.button("🗑️", key=f"delete_invitee_simple_{idx}_{selected_invitee_list}"):
                                if st.session_state.get(f"confirm_delete_invitee_simple_{idx}"):
                                    db.delete_invitee(selected_invitee_list, invitee['name'])
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_invitee_simple_{idx}"] = True
                                    st.warning("Confirm deletion?")
                    
                    st.divider()
        else:
            render_empty_state("No guests found", "🔍")
        
        # Add new invitee
        st.markdown("#### ➕ Add New Guest")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            new_name = st.text_input("Guest Name", key=f"new_name_{selected_invitee_list}")
        with col2:
            new_lunch = st.number_input("Headcount", min_value=1, key=f"new_lunch_{selected_invitee_list}")
        with col3:
            st.write("")
            if st.button("Add Guest", key=f"add_invitee_{selected_invitee_list}"):
                is_valid, error_msg = validate_invitee_input(new_name, str(new_lunch))
                if is_valid:
                    is_barati = "Barati" in selected_invitee_list
                    if is_barati:
                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            to_sakti = st.number_input("To Sakti", min_value=0, key=f"to_sakti_{selected_invitee_list}")
                        with col_s2:
                            travel = st.selectbox("Travel", TRAVEL_OPTIONS, key=f"travel_new_{selected_invitee_list}")
                        
                        if db.add_invitee(selected_invitee_list, new_name, new_lunch, to_sakti, travel):
                            render_alert("✓ Guest added successfully!", "success")
                            st.rerun()
                        else:
                            render_alert("✗ Guest already exists", "error")
                    else:
                        if db.add_invitee(selected_invitee_list, new_name, new_lunch):
                            render_alert("✓ Guest added successfully!", "success")
                            st.rerun()
                        else:
                            render_alert("✗ Guest already exists", "error")
                else:
                    render_alert(error_msg, "error")

# ======================== TAB 3: MENU PLANNING ========================

with tab3:
    st.markdown("### 🍽️ Menu Planning & Details")
    render_decorative_line()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        available_dates = db.get_all_dates()
        if available_dates:
            selected_date = st.selectbox(
                "Select Date",
                options=available_dates,
                key="menu_date_selector"
            )
        else:
            st.info("No menu data available")
            selected_date = None
    
    with col2:
        if st.button("🔄 Refresh", key="refresh_menu"):
            st.rerun()
    
    if selected_date:
        meals = db.get_meals_for_date(selected_date)
        
        if meals:
            selected_meal = st.selectbox(
                "Select Meal",
                options=meals,
                key=f"meal_selector_{selected_date}"
            )
            
            menu_data = db.get_menu(selected_date, selected_meal)
            
            if menu_data:
                st.divider()
                
                # Display menu summary
                col1, col2 = st.columns(2)
                with col1:
                    render_metric_box("Date", selected_date, "📅")
                with col2:
                    render_metric_box("Headcount", str(menu_data['headcount']), "🍽️")
                
                st.divider()
                
                st.markdown("#### 📋 Menu Items")
                st.markdown(f"""
                <div style="background: #fdf5e6; padding: 20px; border-radius: 10px; 
                            border-left: 4px solid #d4af37;">
                    {menu_data['menu_items']}
                </div>
                """, unsafe_allow_html=True)
                
                # Download menu
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    menu_text = f"Date: {selected_date}\nMeal: {selected_meal}\nHeadcount: {menu_data['headcount']}\n\nMenu:\n{menu_data['menu_items']}"
                    st.download_button(
                        label="📄 Download",
                        data=menu_text,
                        file_name=f"Menu_{selected_date}_{selected_meal}.txt"
                    )
        else:
            render_empty_state("No meals for this date", "🍽️")

# ======================== TAB 4: GLOBAL SEARCH ========================

with tab4:
    st.markdown("### 🔍 Global Search")
    render_decorative_line()
    
    search_type = st.radio("Search Type", ["Ingredients", "Guests"], horizontal=True)
    search_term = st.text_input("🔎 Search everywhere", placeholder="Enter item/guest name...")
    
    if search_term:
        if search_type == "Ingredients":
            results = db.search_ingredients(search_term)
            
            if results:
                st.success(f"Found {len(results)} ingredient(s)")
                
                # Group by list
                by_list = {}
                for result in results:
                    list_name = result['list_name']
                    if list_name not in by_list:
                        by_list[list_name] = []
                    by_list[list_name].append(result)
                
                for list_name, items in by_list.items():
                    with st.expander(f"📦 {INGREDIENT_LISTS.get(list_name, list_name)} ({len(items)})"):
                        for item in items:
                            col1, col2, col3 = st.columns([2, 1.5, 1])
                            with col1:
                                st.write(f"**{item['item_name']}**")
                            with col2:
                                st.write(f"{format_quantity_display(item['quantity'], item['unit'])}")
                            with col3:
                                status_html = render_status_badge(item['status'])
                                st.markdown(status_html, unsafe_allow_html=True)
            else:
                render_empty_state("No ingredients found", "🔍")
        
        else:  # Guests
            results = db.search_invitees(search_term)
            
            if results:
                st.success(f"Found {len(results)} guest(s)")
                
                # Group by list
                by_list = {}
                for result in results:
                    list_name = result['list_name']
                    if list_name not in by_list:
                        by_list[list_name] = []
                    by_list[list_name].append(result)
                
                for list_name, items in by_list.items():
                    with st.expander(f"👥 {INVITEE_LISTS.get(list_name, list_name)} ({len(items)})"):
                        for item in items:
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.write(f"**{item['name']}**")
                            with col2:
                                st.write(f"Headcount: **{item['lunch']}**")
            else:
                render_empty_state("No guests found", "🔍")
    else:
        render_empty_state("Enter a search term to begin", "🔍")

# Render footer
st.divider()
render_footer()
