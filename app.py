import streamlit as st

# Page setup
st.set_page_config(page_title="MetaMatrix Destiny", page_icon="✨", layout="wide")

# Custom CSS for high-definition spacing on Matrix displays
st.markdown("""
    <style>
    /* Styling for large, spaced number cards */
    .number-card {
        background-color: #1e1e2e;
        border: 2px solid #313244;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Monospaced numbers with explicit letter and word spacing */
    .matrix-number {
        font-family: 'Courier New', monospace;
        font-size: 36px;
        font-weight: bold;
        color: #f5e0dc;
        letter-spacing: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation Sidebar
st.sidebar.title("✨ MetaMatrix Navigation")
app_mode = st.sidebar.radio("Select View:", ["Grabovoi Database", "Matrix of Destiny"])

# ==========================================
# VIEW 1: GRABOVOI DATABASE
# ==========================================
if app_mode == "Grabovoi Database":
    st.title("✨ METAMATRIX DESTINY ✨")
    st.subheader("Grabovoi Code Database Interface")

    # Sample Database
    grabovoi_data = [
        {"code": "493151 864 1491", "category": "Career", "purpose": "Manifest dream business"},
        {"code": "218 49451760", "category": "Career", "purpose": "Get a job fast"},
        {"code": "71974131981", "category": "Career", "purpose": "Entrepreneurship success"},
        {"code": "888 71294714", "category": "Abundance", "purpose": "Financial freedom"},
        {"code": "519 7148", "category": "Health", "purpose": "Overall wellness"}
    ]

    tab1, tab2, tab3 = st.tabs(["📁 Browse Categories", "🔍 Keyword Search", "📋 View All"])

    with tab1:
        st.markdown("### Select Category")
        categories = sorted(list(set(item["category"] for item in grabovoi_data)))
        selected_cat = st.selectbox("Choose a category from the list:", categories)
        
        filtered = [item for item in grabovoi_data if item["category"] == selected_cat]
        st.success(f"Found {len(filtered)} code(s) in '{selected_cat}'")
        st.table(filtered)

    with tab2:
        search_query = st.text_input("Enter keyword (e.g., job, health):")
        if search_query:
            results = [item for item in grabovoi_data if search_query.lower() in item["purpose"].lower() or search_query.lower() in item["category"].lower()]
            st.table(results)

    with tab3:
        st.table(grabovoi_data)

# ==========================================
# VIEW 2: MATRIX OF DESTINY
# ==========================================
elif app_mode == "Matrix of Destiny":
    st.title("MetaMatrix Destiny")
    st.subheader("Core Energy Breakdown")

    # Top Energy
    st.markdown("#### CROWN / TOP ENERGY")
    st.markdown('<div class="number-card"><div class="matrix-number">0 9</div></div>', unsafe_allow_html=True)

    # Middle Row: Karma, Soul, Talent
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### LEFT / KARMA")
        st.markdown('<div class="number-card"><div class="matrix-number">1 2</div></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("#### CENTER / SOUL")
        st.markdown('<div class="number-card"><div class="matrix-number">1 8</div></div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown("#### RIGHT / TALENT")
        st.markdown('<div class="number-card"><div class="matrix-number">0 3</div></div>', unsafe_allow_html=True)

    # Bottom Row: Karmic Tail
    st.markdown("#### KARMIC TAIL / BASE")
    tail1, tail2, tail3 = st.columns(3)
    
    with tail1:
        st.markdown('<div class="number-card"><div class="matrix-number">0 6</div></div>', unsafe_allow_html=True)
    with tail2:
        st.markdown('<div class="number-card"><div class="matrix-number">1 8</div></div>', unsafe_allow_html=True)
    with tail3:
        st.markdown('<div class="number-card"><div class="matrix-number">1 2</div></div>', unsafe_allow_html=True)