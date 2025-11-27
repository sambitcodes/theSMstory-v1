# 📚 Developer API Documentation

## Database Module (database.py)

### WeddingDatabase Class

#### Initialization
```python
from database import WeddingDatabase

db = WeddingDatabase(db_path="wedding_management.db")
```

---

### Ingredient Operations

#### Load Ingredient List
```python
db.load_ingredient_list(list_name: str, df: pd.DataFrame) -> bool
```
**Purpose**: Load CSV data into database
**Parameters**:
- `list_name`: Unique list identifier (e.g., "Local-List")
- `df`: pandas DataFrame with columns: Item Name, Quantity, Unit

**Returns**: True if successful, False otherwise

**Example**:
```python
df = pd.read_csv("Local-List.csv")
db.load_ingredient_list("Local-List", df)
```

---

#### Get All Ingredients
```python
db.get_ingredients(list_name: str) -> List[Dict]
```
**Purpose**: Retrieve all ingredients from a list

**Returns**: List of dictionaries with keys:
- `id`: Unique identifier
- `list_name`: List name
- `item_name`: Item name
- `quantity`: Total quantity
- `unit`: Unit of measurement
- `delivered_quantity`: Quantity delivered
- `status`: Delivery status

---

#### Add Ingredient
```python
db.add_ingredient(list_name: str, item_name: str, 
                 quantity: float, unit: str) -> bool
```
**Purpose**: Add new ingredient to list

**Example**:
```python
db.add_ingredient("Local-List", "Salt", 5, "kg")
```

---

#### Update Ingredient Status
```python
db.update_ingredient_status(list_name: str, item_name: str,
                           status: str, delivered_qty: float = 0)
```
**Purpose**: Update delivery status and quantity

**Parameters**:
- `status`: "Completed" | "Incomplete" | "Not Started"
- `delivered_qty`: Quantity not delivered (for Incomplete)

**Example**:
```python
db.update_ingredient_status("Local-List", "Salt", "Incomplete", 1.5)
```

---

#### Update Ingredient
```python
db.update_ingredient(list_name: str, item_name: str,
                    quantity: float, unit: str)
```
**Purpose**: Update quantity and unit

---

#### Delete Ingredient
```python
db.delete_ingredient(list_name: str, item_name: str) -> bool
```
**Purpose**: Remove ingredient from list

---

#### Search Ingredients
```python
db.search_ingredients(search_term: str, 
                     list_name: Optional[str] = None) -> List[Dict]
```
**Purpose**: Search across lists or within specific list

**Example**:
```python
# Search globally
results = db.search_ingredients("salt")

# Search in specific list
results = db.search_ingredients("salt", "Local-List")
```

---

### Invitee Operations

#### Load Invitee List
```python
db.load_invitee_list(list_name: str, df: pd.DataFrame) -> bool
```
**Purpose**: Load guest CSV data

**CSV Format**: Columns must include Name, Lunch, and optionally To SAKTI, Travel By

---

#### Get All Invitees
```python
db.get_invitees(list_name: str) -> List[Dict]
```
**Purpose**: Retrieve all guests from list

**Returns**: List of dictionaries with keys:
- `id`: Unique identifier
- `list_name`: List name
- `name`: Guest name
- `lunch`: Headcount
- `to_sakti`: Sakti count (optional)
- `travel_by`: Travel mode (optional)

---

#### Add Invitee
```python
db.add_invitee(list_name: str, name: str, lunch: int,
              to_sakti: Optional[int] = None,
              travel_by: Optional[str] = None) -> bool
```
**Purpose**: Add new guest

**Example**:
```python
db.add_invitee("Invitee-List-Barati-05.12.25", "John Doe", 4, 2, "Bus")
```

---

#### Update Invitee
```python
db.update_invitee(list_name: str, name: str, 
                 lunch: int, to_sakti: Optional[int] = None,
                 travel_by: Optional[str] = None)
```
**Purpose**: Update guest details

---

#### Delete Invitee
```python
db.delete_invitee(list_name: str, name: str) -> bool
```
**Purpose**: Remove guest

---

#### Get Total Headcount
```python
db.get_total_headcount(list_name: str) -> int
```
**Purpose**: Calculate total headcount for list

---

#### Search Invitees
```python
db.search_invitees(search_term: str,
                  list_name: Optional[str] = None) -> List[Dict]
```
**Purpose**: Search guests

---

### Menu Operations

#### Load Menu Data
```python
db.load_menu_data(df: pd.DataFrame) -> bool
```
**Purpose**: Load menu CSV data

**CSV Format**: Columns must include Date, Meal, Headcount, Menu Items

---

#### Get Menu
```python
db.get_menu(date: str, meal: str) -> Optional[Dict]
```
**Purpose**: Retrieve specific menu

**Returns**: Dictionary with keys:
- `date`: Date
- `meal`: Meal type
- `headcount`: Number of people
- `menu_items`: Menu description

---

#### Get All Dates
```python
db.get_all_dates() -> List[str]
```
**Purpose**: Get all unique dates from menus

---

#### Get Meals for Date
```python
db.get_meals_for_date(date: str) -> List[str]
```
**Purpose**: Get all meals for specific date

---

## Utility Functions (utils.py)

### UI Rendering Functions

#### Render Header
```python
from utils import render_header
render_header()
```
Displays the main header with app title and romantic styling.

---

#### Render Footer
```python
from utils import render_footer
render_footer()
```
Displays footer with celebration message.

---

#### Render Status Badge
```python
from utils import render_status_badge
html = render_status_badge(status: str) -> str
```
**Parameters**: "Completed" | "Incomplete" | "Not Started"

**Returns**: HTML string with colored badge

---

#### Render Alert
```python
from utils import render_alert
render_alert(message: str, alert_type: str = "info")
```
**Parameters**:
- `alert_type`: "success" | "error" | "warning" | "info"

---

#### Render Metric Box
```python
from utils import render_metric_box
render_metric_box(label: str, value: str, icon: str = "📊")
```
Displays metric in attractive box format.

---

#### Render Empty State
```python
from utils import render_empty_state
render_empty_state(message: str, icon: str = "📭")
```
Shows empty state UI when no data available.

---

### Validation Functions

#### Validate Ingredient Input
```python
from utils import validate_ingredient_input
is_valid, error_msg = validate_ingredient_input(
    name: str, quantity: str, unit: str
) -> Tuple[bool, str]
```

**Checks**:
- Name is not empty
- Quantity is valid positive number
- Unit is not empty

---

#### Validate Invitee Input
```python
from utils import validate_invitee_input
is_valid, error_msg = validate_invitee_input(
    name: str, lunch: str
) -> Tuple[bool, str]
```

**Checks**:
- Name is not empty
- Lunch (headcount) is valid positive integer

---

### Formatting Functions

#### Format Quantity Display
```python
from utils import format_quantity_display
display = format_quantity_display(quantity: float, unit: str) -> str
```

**Example**: `format_quantity_display(5.5, "kg")` → "5.5 kg"

---

#### Format Currency
```python
from utils import format_currency
formatted = format_currency(amount: float) -> str
```

**Example**: `format_currency(1000)` → "₹1,000.00"

---

### Search Functions

#### Search in List
```python
from utils import search_in_list
results = search_in_list(items: list, search_term: str, 
                        search_key: str = "item_name") -> list
```
**Purpose**: Filter items by search term

---

#### Group Data by Key
```python
from utils import group_data_by_key
grouped = group_data_by_key(items: list, group_key: str) -> dict
```
**Purpose**: Group items by specific key

---

## Configuration (config.py)

### Color Palette
```python
from config import COLORS

COLORS = {
    "primary": "#d4af37",        # Gold
    "secondary": "#fdf5e6",      # Cream
    "accent": "#c41e3a",         # Deep red
    "text": "#2c3e50",           # Dark blue-gray
    "light": "#f8f6f1",          # Off-white
    "success": "#27ae60",        # Green
    "warning": "#f39c12",        # Orange
    "error": "#e74c3c",          # Red
}
```

---

### List Configurations
```python
from config import INGREDIENT_LISTS, INVITEE_LISTS

INGREDIENT_LISTS = {
    "Local-List": "Local List",
    "Reception-Raasan": "Reception - Raasan",
    # ... 7 more
}

INVITEE_LISTS = {
    "Invitee-List-Poite-03.12.25": "Poite (03/12/25)",
    "Invitee-List-Barati-05.12.25": "Barati (05/12/25)",
    # ... 2 more
}
```

---

### Custom CSS
```python
from config import CUSTOM_CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
```

Applies romantic styling to entire app.

---

## Error Handling

### Database Errors
All database methods return boolean indicating success:
```python
success = db.add_ingredient(...)
if not success:
    print("Error adding ingredient")
```

### Input Validation Errors
Validation functions return tuple:
```python
is_valid, error_msg = validate_ingredient_input(...)
if not is_valid:
    print(f"Error: {error_msg}")
```

---

## Session State Management

### Initialize Database
```python
import streamlit as st
from database import WeddingDatabase
from config import SESSION_KEYS

if SESSION_KEYS["db_initialized"] not in st.session_state:
    st.session_state.db = WeddingDatabase()
```

---

## Example Usage

### Complete CRUD Example
```python
import streamlit as st
import pandas as pd
from database import WeddingDatabase
from config import INGREDIENT_LISTS

# Initialize
db = WeddingDatabase()

# Load initial data
df = pd.read_csv("Local-List.csv")
db.load_ingredient_list("Local-List", df)

# Retrieve
ingredients = db.get_ingredients("Local-List")

# Create
db.add_ingredient("Local-List", "New Item", 5, "kg")

# Update
db.update_ingredient("Local-List", "New Item", 10, "kg")

# Delete
db.delete_ingredient("Local-List", "New Item")

# Search
results = db.search_ingredients("salt")
```

---

## Performance Tips

1. **Use Session State**: Cache database connection
```python
if "db" not in st.session_state:
    st.session_state.db = WeddingDatabase()
```

2. **Batch Operations**: Load all CSVs at startup
3. **Minimize Queries**: Store results in session state
4. **Use Caching**: Apply `@st.cache_resource` decorator

---

## Troubleshooting

### "Table already exists" Error
- Normal behavior - tables created only if not exist
- Safe to ignore or catch exception

### Database Locked
- Ensure connections are closed properly
- `connection.close()` is called after operations

### CSV Not Loading
- Verify column names match expected format
- Check file encoding (UTF-8 recommended)

---

**For more information, refer to individual file documentation.**
