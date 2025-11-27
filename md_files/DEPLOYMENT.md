# Streamlit Cloud Deployment Guide

## 📋 Pre-Deployment Checklist

- [ ] All code files are present (`app.py`, `database.py`, `config.py`, `utils.py`)
- [ ] `requirements.txt` is up to date
- [ ] `.streamlit/config.toml` is configured
- [ ] CSV data files are in the repository root
- [ ] `.gitignore` includes database and cache files
- [ ] No hardcoded API keys or secrets

## 🚀 Steps to Deploy on Streamlit Cloud

### 1. Prepare GitHub Repository

```bash
# Initialize git if not done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Tabu weds Mousumi Wedding Management System"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/tabu-weds-mousumi.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://share.streamlit.io/deploy)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and branch (`main`)
5. Set the main file path to `app.py`
6. Click "Deploy"

### 3. Configure Streamlit Cloud

After deployment:

1. Go to app settings (⚙️ menu)
2. Configure if needed:
   - Python version: 3.9+
   - Client error details: On
   - Manage secrets: Add any sensitive data here

### 4. Verify Deployment

- [ ] App loads successfully
- [ ] All tabs work correctly
- [ ] Database operations (CRUD) work
- [ ] Search functionality works
- [ ] Data persists across reloads

## 📊 File Structure Expected in Cloud

```
tabu-weds-mousumi/
├── app.py                         ← Main entry point
├── database.py                    ← Database operations
├── config.py                      ← Configuration
├── utils.py                       ← Utility functions
├── requirements.txt               ← Dependencies
├── .streamlit/
│   └── config.toml               ← Streamlit config
├── .gitignore                     ← Git ignore rules
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
├── Menus-List.csv
└── README.md
```

## 🔧 Troubleshooting

### Database Issues
- SQLite works fine on Streamlit Cloud
- Database file (`wedding_management.db`) is created automatically
- Data persists between sessions

### CSV Loading Issues
- Ensure CSV files are in repository root
- Check file paths match exactly in `app.py`
- CSV column names must match code expectations

### Slow Performance
- Database caching with `@st.cache_resource` is implemented
- CSV loading happens only once on app restart

### Memory Issues
- Large CSV files are loaded into SQLite (memory efficient)
- Session state is cleared on page refresh

## 📱 Browser Compatibility

Tested and working on:
- Chrome/Chromium (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)

## 💾 Database Persistence

SQLite database persists data across:
- Page refreshes
- App reruns
- Streamlit Cloud restarts (within session)

**Note:** For production, consider using a cloud database like PostgreSQL or Firebase if permanent storage across app restarts is critical.

## 🔐 Security Notes

- No sensitive data is hardcoded
- CSV files contain public wedding information
- Database is local to app instance
- Consider adding authentication if deploying publicly

## 📞 Support

For issues with:
- **Streamlit:** Visit [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub:** Check GitHub documentation
- **SQLite:** Check [sqlite.org](https://sqlite.org)

---

**Happy Deployment! 🎉**
