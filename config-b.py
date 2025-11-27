"""
Configuration and constants for Tabu weds Mousumi application
"""

# Application Settings
APP_TITLE = "Tabu weds Mousumi"
APP_SUBTITLE = "Wedding Management System"

# Color Palette - Romantic & Elegant
COLORS = {
    "primary": "#d4af37",  # Gold
    "secondary": "#fdf5e6",  # Cream
    "accent": "#c41e3a",  # Deep red/maroon
    "text": "#2c3e50",  # Dark blue-gray
    "light": "#f8f6f1",  # Off-white
    "success": "#27ae60",  # Green
    "warning": "#f39c12",  # Orange
    "error": "#e74c3c",  # Red
}

# Ingredient Lists Configuration
INGREDIENT_LISTS = {
    "Local-List": "Local List",
    "Reception-Raasan": "Reception - Raasan",
    "Reception-Tent": "Reception - Tent",
    "Reception-Extras": "Reception - Extras",
    "Reception-Pakoda": "Reception - Pakoda",
    "Reception-Coffee": "Reception - Coffee",
    "Home-Raasan": "Home - Raasan",
    "Home-Dessert": "Home - Dessert",
    "Home-Tent": "Home - Tent",
}

# Invitee Lists Configuration
INVITEE_LISTS = {
    "Invitee-List-Poite-03.12.25": "Poite (03/12/25)",
    "Invitee-List-Barati-05.12.25": "Barati (05/12/25)",
    "Invitee-List-Boubhaat-07.12.25": "Boubhaat (07/12/25)",
    "Invitee-List-Return-06.12.25": "Return (06/12/25)",
}

# Menu List Configuration
MENU_DATES = {
    "03/12/25": ["Breakfast", "Lunch", "Dinner"],
    "04/12/25": ["Breakfast", "Lunch", "Dinner"],
    "05/12/25": ["Lunch"],
    "06/12/25": ["Lunch"],
    "07/12/25": ["Breakfast", "Lunch", "Dinner"],
}

# Delivery Status Options
DELIVERY_STATUS = {
    "Completed": "✓ Completed",
    "Incomplete": "✗ Incomplete",
    "Not Started": "○ Not Started",
}

# Travel Options for Barati
TRAVEL_OPTIONS = ["Bus", "Car", "Not"]

# Database Configuration
DB_NAME = "wedding_management.db"
DB_TIMEOUT = 30

# Session State Keys
SESSION_KEYS = {
    "db_initialized": "db_initialized",
    "selected_ingredient_list": "selected_ingredient_list",
    "selected_invitee_list": "selected_invitee_list",
    "search_query": "search_query",
    "global_search_query": "global_search_query",
    "add_ingredient_mode": "add_ingredient_mode",
    "edit_ingredient_mode": "edit_ingredient_mode",
    "add_invitee_mode": "add_invitee_mode",
    "edit_invitee_mode": "edit_invitee_mode",
}

# CSS Styling
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #2c3e50 !important;
        letter-spacing: 1px;
    }
    
    .header-main {
        background: linear-gradient(135deg, #fdf5e6 0%, #fff9f0 100%);
        padding: 40px 20px;
        text-align: center;
        border-bottom: 3px solid #d4af37;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .header-main h1 {
        font-size: 2.5em;
        margin: 10px 0;
        color: #c41e3a;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-main p {
        color: #d4af37;
        font-size: 1.1em;
        font-style: italic;
    }
    
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    .card-style {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #d4af37;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    .status-complete {
        color: #27ae60;
        font-weight: 600;
    }
    
    .status-incomplete {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .btn-romantic {
        background-color: #c41e3a !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(196, 30, 58, 0.3);
    }
    
    .btn-romantic:hover {
        background-color: #a01830 !important;
        box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4);
        transform: translateY(-2px);
    }
    
    .table-style {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .search-bar {
        background: linear-gradient(135deg, #fdf5e6 0%, #fff9f0 100%);
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #d4af37;
        margin-bottom: 20px;
    }
    
    .flower-divider::before {
        content: "❀ ✿ ❀";
        display: block;
        text-align: center;
        color: #d4af37;
        margin: 20px 0;
        font-size: 1.2em;
        letter-spacing: 10px;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #c41e3a 0%, #a01830 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2em;
        box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);
    }
    
    .info-badge {
        display: inline-block;
        background-color: #d4af37;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }
    
    .footer-romantic {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        border-top: 2px solid #d4af37;
        color: #2c3e50;
        font-style: italic;
    }
    
    .streamlit-expanderHeader {
        background-color: #fdf5e6;
        border-left: 4px solid #d4af37;
    }
</style>
"""
