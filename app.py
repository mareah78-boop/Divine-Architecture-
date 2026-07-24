import streamlit as st
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Page Configuration
st.set_page_config(
    page_title="MetaMatrix Destiny",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #1e222d;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #313745;
        margin-bottom: 1rem;
    }
    .metric-label {
        color: #8b9bb4;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Helper: Major Arcana Rule of 22 Reduction
def reduce_to_arcana(val: int) -> int:
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return val if val > 0 else 22

# Helper: Load Grabovoi Codes
def load_grabovoi_codes():
    if os.path.exists("codes.json"):
        try:
            with open("codes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Default fallback data if codes.json is missing
    return [
        {"code": "888 71294714", "category": "Abundance", "purpose": "Financial freedom"},
        {"code": "519 7148", "category": "Health", "purpose": "Overall wellness"},
        {"code": "1487210", "category": "Harmonization", "purpose": "Inner peace"}
    ]

# Helper: Generate PDF Report
def generate_pdf_report(top, left, right, base, center):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 750, "MetaMatrix Destiny - Personal Analysis Report")
    c.line(100, 740, 500, 740)
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Crown / Top Energy: {top}")
    c.drawString(100, 675, f"Left / Karma: {left}")
    c.drawString(100, 650, f"Right / Talent: {right}")
    c.drawString(100, 625, f"Karmic Tail / Base: {base}")
    c.drawString(100, 600, f"Center / Soul: {center}")
    
    c.drawString(100, 550, "Generated via MetaMatrix Destiny Engine")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.markdown("## ✨ MetaMatrix Navigation")

# UNIQUE KEY "main_app_navigation_radio" prevents the duplicate ID error
view_mode = st.sidebar.radio(
    "Select View:",
    ["Grabovoi Database", "Matrix of Destiny"],
    key="main_app_navigation_radio"
)

# ----------------------------------------------------
# VIEW 1: GRABOVOI DATABASE
# ----------------------------------------------------
if view_mode == "Grabovoi Database":
    st.markdown("<h1 class='main-title'>✨ METAMATRIX DESTINY ✨</h1>", unsafe_allow_html=True)
    st.subheader("Grabovoi Code Database Interface")

    codes_data = load_grabovoi_codes()
    categories = sorted(list(set(c["category"] for c in codes_data)))

    # UNIQUE KEY for view selector tabs
    db_tab = st.radio(
        "Navigation Mode:",
        ["Browse Categories", "Keyword Search", "View All"],
        horizontal=True,
        key="grabovoi_view_mode_tab_radio"
    )

    if db_tab == "Browse Categories":
        selected_cat = st.selectbox(
            "Choose a category from the list:", 
            categories,
            key="grabovoi_category_select_box"
        )
        filtered = [c for c in codes_data if c["category"] == selected_cat]
        st.success(f"Found {len(filtered)} code(s) in '{selected_cat}'")
        st.table(filtered)

    elif db_tab == "Keyword Search":
        query = st.text_input("Enter search phrase:", key="grabovoi_search_text_input")
        if query:
            filtered = [
                c for c in codes_data 
                if query.lower() in c["code"].lower() or query.lower() in c["purpose"].lower()
            ]
            st.write(f"Search Results for '{query}':")
            st.table(filtered)

    else:
        st.write("Full Grabovoi Code Database")
        st.table(codes_data)

# ----------------------------------------------------
# VIEW 2: MATRIX OF DESTINY
# ----------------------------------------------------
elif view_mode == "Matrix of Destiny":
    st.markdown("<h1 class='main-title'>✨ MetaMatrix Destiny ✨</h1>", unsafe_allow_html=True)

    with st.expander("Calculate New Chart", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            day = st.number_input("Day of Birth", min_value=1, max_value=31, value=12, key="dob_day_input")
            month = st.number_input("Month of Birth", min_value=1, max_value=12, value=9, key="dob_month_input")
        with col2:
            year = st.number_input("Year of Birth", min_value=1900, max_value=2100, value=1988, key="dob_year_input")

    # Core Calculations
    top_energy = reduce_to_arcana(month)
    left_energy = reduce_to_arcana(day)
    right_energy = reduce_to_arcana(sum(int(d) for d in str(year)))
    base_energy = reduce_to_arcana(top_energy + left_energy + right_energy)
    center_energy = reduce_to_arcana(top_energy + left_energy + right_energy + base_energy)

    st.subheader("Core Energy Breakdown")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>CROWN / TOP ENERGY</div>
            <div class='metric-val'>{top_energy}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>LEFT / KARMA</div>
            <div class='metric-val'>{left_energy}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>CENTER / SOUL</div>
            <div class='metric-val'>{center_energy}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>RIGHT / TALENT</div>
            <div class='metric-val'>{right_energy}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
            <div class='metric-label'>KARMIC TAIL / BASE</div>
            <div class='metric-val'>{base_energy}</div>
        </div>
        """, unsafe_allow_html=True)

    # UNIQUE KEY for sub-breakdown selection
    sub_view = st.radio(
        "Select Detailed Matrix View:",
        ["Overview", "Ancestral Channels", "Chakra Health"],
        horizontal=True,
        key="matrix_detailed_sub_view_radio"
    )

    if sub_view == "Overview":
        st.info(f"Primary Core Matrix centered around Arcana {center_energy}.")
    elif sub_view == "Ancestral Channels":
        st.write("Ancestral Diagonals:")
        st.json({
            "Male Lineage Top-Left": reduce_to_arcana(top_energy + left_energy),
            "Female Lineage Top-Right": reduce_to_arcana(top_energy + right_energy),
            "Male Lineage Bottom-Left": reduce_to_arcana(base_energy + left_energy),
            "Female Lineage Bottom-Right": reduce_to_arcana(base_energy + right_energy)
        })
    elif sub_view == "Chakra Health":
        st.write("Chakra Alignment Breakdown active.")

    st.markdown("---")
    pdf_data = generate_pdf_report(top_energy, left_energy, right_energy, base_energy, center_energy)
    st.download_button(
        label="📄 Download Narrative PDF Report",
        data=pdf_data,
        file_name="MetaMatrix_Destiny_Report.pdf",
        mime="application/pdf",
        key="pdf_download_button_key"
    )