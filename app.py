import json
import streamlit as st

# Page Configuration for Mobile
st.set_page_config(
    page_title="MetaMatrix Destiny",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load data
@st.cache_data
def load_matrix():
    try:
        with open('codes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading codes.json: {e}")
        return []

data = load_matrix()

# Title Header
st.title("✨ METAMATRIX DESTINY ✨")
st.caption("Grabovoi Code Database Interface")

if data:
    # Navigation Tabs for Mobile Touch
    tab1, tab2, tab3 = st.tabs(["📁 Browse Categories", "🔍 Keyword Search", "📜 View All"])

    # TAB 1: BROWSE BY CATEGORY (Touch Dropdown)
    with tab1:
        st.subheader("Select Category")
        categories = sorted(list(set(item.get('category', 'Uncategorized') for item in data if item.get('category'))))
        
        selected_cat = st.selectbox("Choose a category from the list:", categories)
        
        if selected_cat:
            cat_results = [item for item in data if item.get('category') == selected_cat]
            st.success(f"Found {len(cat_results)} code(s) in '{selected_cat}'")
            st.dataframe(cat_results, use_container_width=True, hide_index=True)

    # TAB 2: KEYWORD SEARCH
    with tab2:
        st.subheader("Search Codes")
        search_query = st.text_input("Enter search term (e.g., love, wealth, health):").strip().lower()
        
        if search_query:
            search_results = [
                item for item in data 
                if search_query in item.get('purpose', '').lower() 
                or search_query in item.get('code', '').lower() 
                or search_query in item.get('category', '').lower()
            ]
            if search_results:
                st.success(f"Found {len(search_results)} match(es)")
                st.dataframe(search_results, use_container_width=True, hide_index=True)
            else:
                st.warning(f"No codes found matching '{search_query}'.")

    # TAB 3: VIEW ALL CODES
    with tab3:
        st.subheader("Complete Database")
        st.dataframe(data, use_container_width=True, hide_index=True)