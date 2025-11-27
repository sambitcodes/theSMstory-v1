"""
Utility functions for Tabu weds Mousumi application
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from config import COLORS, CUSTOM_CSS

def render_header():
    """Render the header section with custom styling"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown("""
<div class="header-main">
     <h1>
        💕the<span style="color: red; font-size: 1.3em;">S</span>oul<span style="color: red; font-size: 1.3em;">M</span>atestory💕
    </h1>
    <p>A Beautiful Journey of Love & Celebration</p>
    <div class="flower-divider"></div>
    <p style="color: #2c3e50; font-size: 0.95em;">
        <strong><span style="color: red;">S</span>UBHANKAR</strong> weds <strong><span style="color: red;">M</span>OUSMI</strong>
    </p>
</div>
""", unsafe_allow_html=True)

def render_footer():
    """Render the footer section"""
    st.markdown("""
    <div class="footer-romantic">
        <p>✨ Wishing a lifetime of love, happiness, and cherished moments ✨</p>
        <p style="font-size: 0.85em; margin-top: 10px;">December 5th, 2025 • A celebration of love</p>
    </div>
    """, unsafe_allow_html=True)

def render_decorative_line():
    """Render decorative line"""
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

def render_status_badge(status: str) -> str:
    """Render colored status badge"""
    if status == "Completed":
        return f'<span style="color: #27ae60; font-weight: 600;">✓ Completed</span>'
    elif status == "Incomplete":
        return f'<span style="color: #e74c3c; font-weight: 600;">✗ Incomplete</span>'
    else:
        return f'<span style="color: #95a5a6; font-weight: 600;">○ Not Started</span>'

def render_info_badge(text: str, color: str = "primary") -> str:
    """Render info badge"""
    badge_color = COLORS.get(color, COLORS["primary"])
    return f'<span class="info-badge" style="background-color: {badge_color};">{text}</span>'

def render_summary_card(title: str, value: str, icon: str = ""):
    """Render summary card"""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <div style="font-size: 0.9em; margin-bottom: 10px;">{icon} {title}</div>
            <div style="font-size: 2em; font-weight: bold;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

def create_dataframe_from_dict_list(data: list) -> pd.DataFrame:
    """Convert list of dictionaries to DataFrame"""
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def safe_convert_to_float(value) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def safe_convert_to_int(value) -> int:
    """Safely convert value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def format_quantity_display(quantity: float, unit: str) -> str:
    """Format quantity for display"""
    if quantity == int(quantity):
        return f"{int(quantity)} {unit}"
    else:
        return f"{quantity} {unit}"

def confirm_action(action_text: str) -> bool:
    """Show confirmation dialog"""
    st.warning(f"⚠️ {action_text}")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("✓ Confirm", key=f"confirm_{action_text}"):
            return True
    
    with col2:
        if st.button("✗ Cancel", key=f"cancel_{action_text}"):
            return False
    
    return False

def render_metric_box(label: str, value: str, icon: str = "📊"):
    """Render metric box"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fdf5e6 0%, #fff9f0 100%);
                padding: 15px; border-radius: 10px; text-align: center;
                border-left: 4px solid #d4af37;">
        <div style="font-size: 0.85em; color: #2c3e50; font-weight: 600; margin-bottom: 5px;">
            {icon} {label}
        </div>
        <div style="font-size: 1.8em; color: #c41e3a; font-weight: bold;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_alert(message: str, alert_type: str = "info"):
    """Render custom alert"""
    if alert_type == "success":
        icon = "✓"
        color = "#27ae60"
    elif alert_type == "error":
        icon = "✗"
        color = "#e74c3c"
    elif alert_type == "warning":
        icon = "⚠"
        color = "#f39c12"
    else:
        icon = "ℹ"
        color = "#3498db"
    
    st.markdown(f"""
    <div style="background-color: {color}20; border-left: 4px solid {color};
                padding: 12px; border-radius: 6px; margin: 10px 0;">
        <span style="color: {color}; font-weight: 600; font-size: 0.95em;">
            {icon} {message}
        </span>
    </div>
    """, unsafe_allow_html=True)

def get_csv_download_link(df: pd.DataFrame, filename: str) -> bytes:
    """Generate CSV download link"""
    csv = df.to_csv(index=False)
    return csv.encode()

def search_in_list(items: list, search_term: str, search_key: str = "item_name") -> list:
    """Search items in list by term"""
    search_term = search_term.lower()
    return [item for item in items if search_term in str(item.get(search_key, "")).lower()]

def group_data_by_key(items: list, group_key: str) -> dict:
    """Group items by key"""
    grouped = {}
    for item in items:
        key = item.get(group_key)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    return grouped

def render_loading_animation():
    """Show loading animation"""
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 2em; animation: spin 2s linear infinite;">💫</div>
        <p style="color: #2c3e50; margin-top: 10px;">Processing...</p>
    </div>
    """, unsafe_allow_html=True)

def render_empty_state(message: str, icon: str = "📭"):
    """Show empty state"""
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: #95a5a6;">
        <div style="font-size: 3em; margin-bottom: 15px;">{icon}</div>
        <p style="font-size: 1.1em;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def render_statistics_row(stat1: tuple, stat2: tuple, stat3: tuple):
    """Render statistics in a row"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_box(stat1[0], stat1[1], stat1[2] if len(stat1) > 2 else "📊")
    
    with col2:
        render_metric_box(stat2[0], stat2[1], stat2[2] if len(stat2) > 2 else "📊")
    
    with col3:
        render_metric_box(stat3[0], stat3[1], stat3[2] if len(stat3) > 2 else "📊")

def validate_ingredient_input(name: str, quantity: str, unit: str) -> tuple:
    """Validate ingredient input - returns (is_valid, error_message)"""
    if not name or not name.strip():
        return False, "Item name cannot be empty"
    
    try:
        qty = float(quantity)
        if qty <= 0:
            return False, "Quantity must be greater than 0"
    except ValueError:
        return False, "Quantity must be a valid number"
    
    if not unit or not unit.strip():
        return False, "Unit cannot be empty"
    
    return True, ""

def validate_invitee_input(name: str, lunch: str) -> tuple:
    """Validate invitee input - returns (is_valid, error_message)"""
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    try:
        headcount = int(lunch)
        if headcount <= 0:
            return False, "Headcount must be greater than 0"
    except ValueError:
        return False, "Headcount must be a valid number"
    
    return True, ""

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"

def get_time_based_greeting() -> str:
    """Get greeting based on time"""
    from datetime import datetime
    hour = datetime.now().hour
    
    if hour < 12:
        return "Good Morning 🌅"
    elif hour < 18:
        return "Good Afternoon ☀️"
    else:
        return "Good Evening 🌙"

def render_wedding_theme_background():
    """Add wedding theme background"""
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #fdf5e6 0%, #fff9f0 50%, #fdf5e6 100%);
        }
    </style>
    """, unsafe_allow_html=True)
