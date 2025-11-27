# 🚀 Quick Start Guide

## Installation & Setup

### Option 1: Local Development

#### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

#### Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/tabu-weds-mousumi.git
cd tabu-weds-mousumi
```

2. **Create Virtual Environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Place CSV Files**
Ensure all CSV files are in the project root:
- `Local-List.csv`
- `Reception-Raasan.csv`
- `Reception-Tent.csv`
- `Reception-Extras.csv`
- `Reception-Pakoda.csv`
- `Reception-Coffee.csv`
- `Home-Raasan.csv`
- `Home-Dessert.csv`
- `Home-Tent.csv`
- `Invitee-List-Poite-03.12.25.csv`
- `Invitee-List-Barati-05.12.25.csv`
- `Invitee-List-Boubhaat-07.12.25.csv`
- `Invitee-List-Return-06.12.25.csv`
- `Menus-List.csv`

5. **Run the Application**
```bash
streamlit run app.py
```

6. **Access the App**
Open your browser and go to: `http://localhost:8501`

---

### Option 2: Streamlit Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed cloud deployment instructions.

---

## 📖 User Guide

### Tab 1: 📦 Track Ingredients

#### View Ingredients
1. Select a list from the dropdown
2. View all items with quantities and status
3. See statistics: Total, Completed, Incomplete

#### Update Delivery Status
- **✓ Button**: Mark item as Completed
- **✗ Button**: Mark as Incomplete (enter not-delivered quantity)
- **⋮ Menu**: Edit, delete, or manage item

#### Add New Ingredient
1. Enter item name
2. Enter quantity (number)
3. Enter unit (kg, g, pc, etc.)
4. Click "Add Item"

#### Delete Ingredient
1. Click ⋮ menu on item
2. Click 🗑️ Delete
3. Click again to confirm

---

### Tab 2: 👥 Track Invitees

#### View Guests
1. Select a guest list from dropdown
2. View all guests with headcount
3. See total headcount statistics

#### Manage Headcount
- **➖ Button**: Decrease headcount by 1
- **➕ Button**: Increase headcount by 1

#### Special Barati Features (05/12/25)
- **Sakti Count**: Separate tracking
- **Transport Mode**: Select Bus/Car/Not
- Change travel mode from dropdown

#### Add New Guest
1. Enter guest name
2. Enter headcount
3. If Barati: Enter Sakti count and transport mode
4. Click "Add Guest"

#### Delete Guest
1. Click 🗑️ button
2. Click again to confirm

---

### Tab 3: 🍽️ Menu Planning

#### View Menu
1. Select a date
2. Select a meal (Breakfast/Lunch/Dinner)
3. View headcount and detailed menu items
4. Download menu as text file

---

### Tab 4: 🔍 Global Search

#### Search Ingredients
1. Select "Ingredients" tab
2. Enter search term
3. Results show across all lists
4. Grouped by list for easy viewing

#### Search Guests
1. Select "Guests" tab
2. Enter search term
3. Results show across all lists
4. Grouped by list for easy viewing

---

## 🎨 Features

✅ **Beautiful UI**
- Romantic color scheme (Gold, Cream, Deep Red)
- Elegant typography
- Smooth animations
- Responsive design

✅ **Full CRUD Operations**
- Create: Add ingredients and guests
- Read: View all items and search
- Update: Modify quantities and details
- Delete: Remove items with confirmation

✅ **Persistent Storage**
- SQLite database (no external server needed)
- Data persists across sessions
- Automatic backups

✅ **Advanced Search**
- Local search within selected list
- Global search across all lists
- Instant filtering

✅ **Real-time Updates**
- Changes reflect immediately
- Status tracking for deliveries
- Live headcount calculations

---

## 🔧 Troubleshooting

### App Won't Start
```bash
# Verify Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with debug info
streamlit run app.py --logger.level=debug
```

### Database Issues
- Database file creates automatically
- If corrupted, delete `wedding_management.db` and restart
- All CSV data will be reloaded

### CSV Not Loading
- Check file names match exactly (case-sensitive on Linux/Mac)
- Verify CSV columns: `Item Name`, `Quantity`, `Unit` for ingredients
- Verify CSV columns: `Name`, `Lunch` for guests

### Slow Performance
- Clear browser cache: Ctrl+Shift+Del (Cmd+Shift+Delete on Mac)
- Restart Streamlit: Press R in terminal
- Check CSV file sizes (large files may be slow)

---

## 📞 Support & Help

### Common Questions

**Q: Where is my data stored?**
A: Locally in `wedding_management.db` (SQLite). On Streamlit Cloud, it's stored in the app's filesystem.

**Q: Can I backup my data?**
A: Yes! Download the `wedding_management.db` file for backup.

**Q: How do I update an item quantity?**
A: Use Edit mode (⋮ → 📝 Edit) or delete and re-add with new quantity.

**Q: Can multiple people use this simultaneously?**
A: On Streamlit Cloud, each user gets their own session. For shared data, deploy on a server.

---

## 🎉 Ready to Use!

Your wedding management system is now ready. Enjoy organizing your special day! 💕

---

**Questions or Issues?**
- Check documentation in individual files
- Review config.py for configuration options
- See DEPLOYMENT.md for cloud setup

**Made with ❤️ for Tabu & Mousumi**
