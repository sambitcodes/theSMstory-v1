# 📁 Project Files Summary

## Complete Codebase for "Tabu weds Mousumi" Wedding Management System

### Core Application Files

#### 1. **app.py** (Main Application)
- Entry point for the Streamlit application
- Contains all UI logic and page structure
- Implements 4 main tabs: Ingredients, Invitees, Menu, Global Search
- Handles CSV loading, database operations, and user interactions
- Features:
  - Beautiful header and footer
  - Ingredient tracking with status updates
  - Guest management with headcount control
  - Menu viewing and search functionality
  - Custom CSS styling integrated

**Size**: ~450 lines | **Imports**: streamlit, pandas, config, database, utils

---

#### 2. **database.py** (Database Management)
- SQLite database abstraction layer
- WeddingDatabase class with comprehensive CRUD operations
- Three main tables: ingredients, invitees, menus

**Key Methods**:
- `get_connection()` - Database connection management
- `load_ingredient_list()` - Import CSV data
- `load_invitee_list()` - Import guest data
- `load_menu_data()` - Import menu data
- `get_ingredients()` - Retrieve ingredients
- `add_ingredient()`, `update_ingredient()`, `delete_ingredient()`
- `get_invitees()` - Retrieve guests
- `add_invitee()`, `update_invitee()`, `delete_invitee()`
- `search_ingredients()` - Global ingredient search
- `search_invitees()` - Global guest search
- `get_total_headcount()` - Calculate headcount
- `get_menu()`, `get_all_dates()`, `get_meals_for_date()`

**Size**: ~400 lines | **Dependencies**: sqlite3, pandas

---

#### 3. **config.py** (Configuration & Constants)
- Central configuration for the entire application
- Color palette (gold, cream, maroon theme)
- List configurations (ingredient & invitee lists)
- Menu dates and meal types
- Delivery status options
- Travel options for Barati
- Session state keys
- Custom CSS styling

**Contents**:
- APP_TITLE = "Tabu weds Mousumi"
- COLORS dictionary (8 colors)
- INGREDIENT_LISTS (9 lists)
- INVITEE_LISTS (4 lists)
- MENU_DATES configuration
- DELIVERY_STATUS options
- TRAVEL_OPTIONS for transport
- CUSTOM_CSS with romantic styling

**Size**: ~200 lines | **No external dependencies**

---

#### 4. **utils.py** (Utility Functions)
- Helper functions for UI rendering
- Data validation and formatting
- Alert and notification rendering
- Search functionality
- Input validation

**Key Functions**:
- `render_header()` - Styled header section
- `render_footer()` - Footer with celebration message
- `render_status_badge()` - Colored status display
- `render_alert()` - Custom alerts
- `render_metric_box()` - Metric display cards
- `render_empty_state()` - Empty state UI
- `validate_ingredient_input()` - Input validation
- `validate_invitee_input()` - Input validation
- `format_quantity_display()` - Format display
- `search_in_list()` - Search utility
- `render_wedding_theme_background()` - Apply theme

**Size**: ~350 lines | **Imports**: streamlit, pandas

---

### Configuration Files

#### 5. **requirements.txt** (Dependencies)
```
streamlit==1.31.1
pandas==2.1.3
openpyxl==3.10.10
```

**Purpose**: Specifies all Python package requirements for installation

---

#### 6. **.streamlit-config.toml** (Streamlit Configuration)
- Theme configuration (light mode, color scheme)
- Client settings (toolbar, error handling)
- Server settings (headless mode, port)
- Browser settings (gather stats, etc.)

---

#### 7. **.gitignore** (Git Ignore Rules)
Ignores:
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `ENV/`)
- IDE files (`.vscode/`, `.idea/`)
- SQLite database (`*.db`, `wedding_management.db`)
- OS files (`.DS_Store`, `Thumbs.db`)

---

### Documentation Files

#### 8. **README.md** (Main Documentation)
- Project overview
- Features list
- Project structure
- Setup instructions (local & cloud)
- Dependencies list
- Database information
- Browser compatibility

---

#### 9. **DEPLOYMENT.md** (Cloud Deployment Guide)
- Pre-deployment checklist
- GitHub repository setup
- Streamlit Cloud deployment steps
- Configuration instructions
- Verification checklist
- File structure for cloud
- Troubleshooting guide
- Security notes

---

#### 10. **QUICKSTART.md** (Quick Start Guide)
- Installation instructions (local & cloud)
- Prerequisites
- Step-by-step setup
- User guide for each tab
- Features overview
- Troubleshooting FAQs
- Common questions

---

### Data Files (CSV Format)

#### Ingredient Lists (9 files)

1. **Local-List.csv** - 43 items
   - Rice, flour, spices, oils, milk products, etc.

2. **Reception-Raasan.csv** - 58 items
   - Comprehensive reception cooking ingredients

3. **Reception-Tent.csv** - 16 items
   - Kitchen equipment and utensils

4. **Reception-Extras.csv** - 26 items
   - Vegetables, proteins, fruits

5. **Reception-Pakoda.csv** - 17 items
   - Snack preparation ingredients

6. **Reception-Coffee.csv** - 3 items
   - Coffee, milk, sugar

7. **Home-Raasan.csv** - 68 items
   - Home ceremony cooking items

8. **Home-Dessert.csv** - 11 items
   - Dessert ingredients

9. **Home-Tent.csv** - 16 items
   - Home ceremony equipment

#### Invitee Lists (4 files)

1. **Invitee-List-Poite-03.12.25.csv**
   - 43 guests with headcount

2. **Invitee-List-Barati-05.12.25.csv**
   - 23 entries with Sakti count and travel mode

3. **Invitee-List-Boubhaat-07.12.25.csv**
   - 20+ guests with headcount

4. **Invitee-List-Return-06.12.25.csv**
   - 26 guests with headcount

#### Menu File

1. **Menus-List.csv**
   - 5 dates with meals
   - Each entry: date, meal type, headcount, menu details

---

## 🗂️ Directory Structure

```
tabu-weds-mousumi/
├── app.py                                 (450 lines)
├── database.py                            (400 lines)
├── config.py                              (200 lines)
├── utils.py                               (350 lines)
├── requirements.txt
├── .streamlit-config.toml
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── QUICKSTART.md
├── Local-List.csv
├── Reception-Raasan.csv
├── Reception-Tent.csv
├── Reception-Extras.csv
├── Reception-Pakoda.csv
├── Reception-Coffee.csv
├── Home-Raasan.csv
├── Home-Dessert.csv
├── Home-Tent.csv
├── Invitee-List-Poite-03.12.25.csv
├── Invitee-List-Barati-05.12.25.csv
├── Invitee-List-Boubhaat-07.12.25.csv
├── Invitee-List-Return-06.12.25.csv
└── Menus-List.csv
```

---

## 📊 Code Statistics

| File Type | Count | Total Lines | Purpose |
|-----------|-------|------------|---------|
| Python Core | 4 | ~1400 | Application logic |
| Config Files | 2 | ~50 | Configuration |
| CSV Data | 14 | N/A | Ingredient & guest data |
| Documentation | 4 | ~800 | Guides & instructions |
| **TOTAL** | **24** | **~2250** | Complete project |

---

## ✨ Key Features Implemented

✅ **4 Main Tabs**
1. Track Ingredients (CRUD + Status)
2. Track Invitees (CRUD + Headcount)
3. Menu Planning (View & Download)
4. Global Search (Cross-list search)

✅ **Database Functionality**
- Persistent SQLite storage
- Automatic data initialization
- CRUD operations
- Search across lists

✅ **UI/UX Features**
- Romantic color scheme
- Custom CSS styling
- Responsive design
- Real-time updates
- Input validation
- Confirmation dialogs

✅ **Data Management**
- 9 ingredient lists
- 4 invitee lists
- Menu tracking
- Headcount calculations
- Delivery status tracking

---

## 🚀 Deployment Ready

✅ Designed for Streamlit Cloud
✅ SQLite (no external database needed)
✅ Complete documentation
✅ Error handling
✅ Input validation
✅ Beautiful UI

---

**Total Project Size**: ~2250 lines of code + 14 data files

**Created for**: Tabu & Mousumi's Wedding 💕
**December 2025**
