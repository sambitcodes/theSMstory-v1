# Tabu weds Mousumi - Wedding Management System

A beautifully designed, romantic Streamlit application for managing wedding ingredients tracking and guest lists.

## 🎉 Features

### 1. **Tracking Ingredients**
- Track 9 ingredient lists from different events (Reception, Home ceremonies)
- Mark items as Complete/Incomplete with delivery status
- Add, update, and delete ingredients
- Persistent data storage with SQLite
- Real-time status updates

### 2. **Tracking Invitees**
- Manage 4 guest lists across different events
- Track headcount and guest details
- Special fields for Barati event (Travel mode, Sakti count)
- Add, update, delete guest records
- Automatic headcount calculation

### 3. **Menu Planning**
- View menu by date and meal type
- Display headcount and detailed menu items
- Beautiful menu visualization

### 4. **Advanced Search**
- **Local Search**: Search within selected list
- **Global Search**: Search across all lists

## 📋 Project Structure

```
tabu-weds-mousumi/
├── app.py                 # Main Streamlit application
├── database.py            # Database initialization & management
├── config.py              # Configuration & constants
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── data/
│   ├── ingredients/       # Ingredient list CSVs
│   └── invitees/          # Guest list CSVs
└── README.md             # This file
```

## 🚀 Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tabu-weds-mousumi.git
   cd tabu-weds-mousumi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/tabu-weds-mousumi.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub repository
   - Select main branch and `app.py` as entry point
   - Deploy!

## 📦 Dependencies

- `streamlit` - Web framework
- `pandas` - Data manipulation
- `sqlite3` - Database (built-in)
- `Pillow` - Image processing

## 🎨 Design System

- **Colors**: Soft romantic palette with gold accents
- **Typography**: Elegant, wedding-themed
- **Visuals**: Floral patterns, subtle gradients, decorative elements
- **Layout**: Responsive, clean, intuitive

## 💾 Database

Uses **SQLite** (default Python DB) for:
- ✅ Streamlit Cloud compatibility
- ✅ No external server needed
- ✅ Persistent storage
- ✅ Easy backup

## 🔒 Data Persistence

All changes are automatically saved to SQLite database:
- ✅ Ingredient delivery status
- ✅ Guest updates
- ✅ Custom additions/deletions
- ✅ Headcount modifications

## 📱 Browser Compatibility

- Chrome/Chromium
- Firefox
- Safari
- Edge

## 👥 Contributors

Created for the wedding of Tabu and Mousumi

## 📄 License

This project is private and created for personal use.

---

**Happy Wedding! 💕**
