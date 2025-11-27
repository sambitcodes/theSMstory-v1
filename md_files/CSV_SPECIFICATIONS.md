# 📋 CSV File Specifications

## Expected CSV Format & Structure

All CSV files should be placed in the project root directory.

---

## Ingredient List CSV Format

### Required Columns
- **Index**: Sequential number (1, 2, 3, ...)
- **Item Name**: Name of the ingredient/item
- **Quantity**: Numerical value
- **Unit**: Unit of measurement (kg, g, pc, ltr, etc.)

### Example Structure
```csv
Index,Item Name,Quantity,Unit
1,Rice White Platinum,30,kg
2,Salt,5,kg
3,Oil,20,ltr
4,Spices Mix,500,g
```

### Valid Units
- kg, g, mg (weight)
- ltr, ml (volume)
- pc, pieces (count)
- box, packet, dabba (containers)
- tin, bottle, pouch (packaging)

### Important Notes
- **Case Sensitive**: Column names must match exactly
- **No Empty Rows**: Avoid blank rows in CSV
- **Encoding**: Use UTF-8 encoding
- **Delimiter**: Comma (,)

---

## Ingredient Lists (9 Files)

### 1. Local-List.csv
- **Items**: 43
- **Description**: General local items (rice, flour, spices, oils, milk products)
- **Expected Columns**: Index, Item Name, Quantity, Unit

### 2. Reception-Raasan.csv
- **Items**: 58
- **Description**: Comprehensive reception cooking ingredients
- **Expected Columns**: Sl No., Item Name, Quantity, Unit
- **Note**: Uses "Sl No." instead of "Index"

### 3. Reception-Tent.csv
- **Items**: 16 (note: has duplicate index 6)
- **Description**: Kitchen equipment for reception
- **Expected Columns**: Index, Item Name, Quantity, Unit
- **Contents**: Balti, sauce pan, gas chula, kadhai, etc.

### 4. Reception-Extras.csv
- **Items**: 26
- **Description**: Vegetables, proteins, fruits
- **Expected Columns**: Index, Item Name, Quantity, Unit

### 5. Reception-Pakoda.csv
- **Items**: 17
- **Description**: Snack preparation ingredients
- **Expected Columns**: Index, Item Name, Quantity, Unit

### 6. Reception-Coffee.csv
- **Items**: 3
- **Description**: Coffee service items
- **Expected Columns**: Index, Item Name, Quantity, Unit
- **Contents**: Milk, Coffee, Sugar

### 7. Home-Raasan.csv
- **Items**: 68
- **Description**: Home ceremony cooking items
- **Expected Columns**: Index, Item Name, Quantity, Unit
- **Note**: Largest ingredient file

### 8. Home-Dessert.csv
- **Items**: 11
- **Description**: Dessert ingredients
- **Expected Columns**: Index, Item Name, Quantity, Unit

### 9. Home-Tent.csv
- **Items**: 16
- **Description**: Home ceremony equipment
- **Expected Columns**: Index, Item Name, Quantity, Unit

---

## Invitee List CSV Format

### Required Columns (Basic)
- **Index**: Sequential number
- **Name**: Guest name
- **Lunch**: Headcount (number)

### Optional Columns (Barati Only)
- **To SAKTI**: Sakti count (for Barati event)
- **Travel By**: Transportation mode (Bus/Car/Not)

### Example Structure (Basic)
```csv
Index,Name,Lunch
1,Tabu Family,4
2,Minti Di Family,5
3,Rubi Di,2
```

### Example Structure (Barati)
```csv
Index,Name,Lunch,To SAKTI,Travel By
1,Tabu family,4,4,Car
2,Minti Di family,5,5,Bus
3,Rubi Di family,2,2,Car
```

### Valid Travel Options
- "Bus"
- "Car"
- "Not" (not applicable)

### Important Notes
- **Headcount**: Must be positive integer
- **To SAKTI**: Optional, must be non-negative integer
- **Travel By**: Only for Barati event
- **Total Row**: Optional summary row at end (ignored by app)

---

## Invitee Lists (4 Files)

### 1. Invitee-List-Poite-03.12.25.csv
- **Type**: Basic (Name + Lunch)
- **Guests**: 43
- **Date**: 03/12/25 (Pre-wedding ceremony)
- **Total Headcount**: 117

### 2. Invitee-List-Barati-05.12.25.csv
- **Type**: Special (Name + Lunch + To SAKTI + Travel By)
- **Guests**: 23
- **Date**: 05/12/25 (Barati - Groom's procession)
- **Special Features**: 
  - Sakti count tracking
  - Transportation planning (Bus/Car)
- **Note**: Has "Workers" entry with travel mode "Not"

### 3. Invitee-List-Boubhaat-07.12.25.csv
- **Type**: Basic (Name + Lunch)
- **Guests**: 20+
- **Date**: 07/12/25 (Reception)

### 4. Invitee-List-Return-06.12.25.csv
- **Type**: Basic (Name + Lunch)
- **Guests**: 26
- **Date**: 06/12/25 (Return journey day)

---

## Menu List CSV Format

### Required Columns
- **Date**: Date in DD/MM/YY format (e.g., "03/12/25")
- **Meal**: Meal type (Breakfast, Lunch, or Dinner)
- **Headcount**: Number of people
- **Menu Items**: Detailed menu description

### Example Structure
```csv
Date,Meal,Headcount,Menu Items
03/12/25,Breakfast,40,"Luchi, Aloo Chochori"
03/12/25,Lunch,120,"Bhaat, Saag, Dal, Maacher Jhal"
03/12/25,Dinner,40,"Roti, Matar Paneer"
```

### Meal Types
- "Breakfast"
- "Lunch"
- "Dinner"

### Important Notes
- **Date Format**: DD/MM/YY (e.g., "03/12/25" for December 3, 2025)
- **Empty Rows**: Use empty row to separate dates visually
- **Menu Items**: Can contain dish names separated by commas
- **Multi-line Menus**: Use "\n" for line breaks (will display as-is in app)

---

## Menus-List.csv Structure

### File Specifications
- **Dates**: 5 unique dates (03, 04, 05, 06, 07 Dec 2025)
- **Meals**: Total 11 meal entries
- **Format**: Rows separated by empty lines for visual organization

### Date Distribution
```
03/12/25 → Breakfast, Lunch, Dinner (40, 120, 40 people)
04/12/25 → Breakfast, Lunch, Dinner (25, 40, 40 people)
05/12/25 → Lunch only (65 people)
06/12/25 → Lunch only (70 people)
07/12/25 → Breakfast, Lunch, Dinner (30, 140, 500 people)
```

### Special Note on 07/12/25 Dinner
- **Largest Event**: 500 people
- **Comprehensive Menu**: Includes Main Course, Desserts, Sides, Snacks
- **Multi-line Format**: Uses "\n" separator for organization

---

## Data Validation Rules

### Ingredient CSVs
✅ Item Name: Non-empty string
✅ Quantity: Positive number (can be decimal)
✅ Unit: Non-empty string
❌ No empty rows
❌ No missing columns

### Invitee CSVs
✅ Name: Non-empty string
✅ Lunch/Headcount: Positive integer
✅ To SAKTI: Non-negative integer (optional)
✅ Travel By: One of allowed values (optional)
❌ No negative headcounts
❌ No invalid travel modes

### Menu CSVs
✅ Date: DD/MM/YY format
✅ Meal: One of (Breakfast, Lunch, Dinner)
✅ Headcount: Positive integer
✅ Menu Items: Non-empty string
❌ No invalid dates
❌ No invalid meal types

---

## Troubleshooting CSV Issues

### "Column name mismatch" Error
**Problem**: CSV columns don't match expected names
**Solution**: 
- Check exact spelling (case-sensitive)
- Common mistakes:
  - "Item Name" not "ItemName" or "Item_Name"
  - "Lunch" not "lunch" or "Headcount"
  - "Unit" not "unit"

### "No data loaded" Error
**Problem**: CSV file not found or not in root directory
**Solution**:
- Verify file is in project root
- Check filename exactly matches configuration
- Ensure file has .csv extension

### "Invalid quantity" Error
**Problem**: Quantity contains non-numeric value
**Solution**:
- Use numbers only: 5, 5.5, 10
- Don't include units in quantity column
- Units go in separate "Unit" column

### "Duplicate entries" Error
**Problem**: Same item appears twice in list
**Solution**:
- Check for exact duplicates (including spaces)
- First occurrence is kept, duplicates are skipped
- Combine quantities if needed

---

## CSV Best Practices

1. **Use UTF-8 Encoding**
   - Supports special characters
   - Default in most applications

2. **No Extra Spaces**
   - Trim spaces in names
   - "Tabu Family" not " Tabu Family "

3. **Consistent Formatting**
   - Use same date format throughout
   - Use same unit abbreviations

4. **Backup Original CSVs**
   - Keep copies before importing
   - Database can be reset by re-importing

5. **Validate Before Import**
   - Check columns
   - Check data types
   - Check for duplicates

---

## Example Valid CSVs

### Valid Ingredient CSV
```csv
Index,Item Name,Quantity,Unit
1,Rice,30,kg
2,Salt,5,kg
3,Oil,20,ltr
4,Spices,500,g
```

### Valid Invitee CSV (Basic)
```csv
Index,Name,Lunch
1,Tabu,4
2,Mousumi,3
3,Guest 1,2
```

### Valid Invitee CSV (Barati)
```csv
Index,Name,Lunch,To SAKTI,Travel By
1,Tabu,4,4,Car
2,Guest,2,2,Bus
```

### Valid Menu CSV
```csv
Date,Meal,Headcount,Menu Items
03/12/25,Breakfast,40,Luchi and Aloo Chochori
03/12/25,Lunch,120,Bhaat Dal Maacher Jhal
```

---

## Data Import Process

1. App reads CSV file
2. Validates structure
3. Extracts data rows
4. Inserts into SQLite database
5. Skips invalid rows
6. Reports success/failure

---

**For questions about specific CSV formats, see the actual CSV files in the project.**
