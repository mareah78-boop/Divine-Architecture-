import streamlit as st
import datetime

# Try importing pyswisseph safely for Streamlit Cloud deployment
try:
    import swisseph as swe
    HAS_SWISSEPH = True
except ImportError:
    HAS_SWISSEPH = False

# Set page configuration
st.set_page_config(
    page_title="MetaMatrix Destiny & Human Design",
    page_icon="🧬",
    layout="wide"
)

# ==============================================================================
# 1. MANIFESTATION / GRABOVOI CODES DATA
# ==============================================================================
MANIFESTATION_CODES = {
    "Money": {
        "Financial abundance": "318 798",
        "Unexpected money": "520 741 8",
        "Steady, long-term income": "9213140",
        "Cash flow abundance": "318 612 518 714",
        "Money knowledge": "964986583",
        "Money confidence": "87467894",
    },
    "Career": {
        "Manifest dream job": "493151 864 1491",
        "Get a job fast": "218 49451760",
        "Entrepreneurship": "71974131981",
    },
    "Love": {
        "Manifest love": "888 412 1289018",
        "Attract a partner": "197 023",
        "Self-love": "396815",
        "Eternal love": "888 912 818848",
        "Manifest romance": "401543512",
        "Reconnect with an ex": "89974476",
        "Reunite with a partner": "3856794",
    },
    "Well-Being": {
        "Good health": "80845700",
        "Healing of the body": "9187948181",
        "Weight management": "5343168",
        "Beauty and physical attraction": "83585179",
        "Spiritual Protection from Bullies": "55 16 987",
        "Addiction": "84 72 723",
        "Insomnia": "11 21 495",
        "Willpower": "35 31 798",
    },
    "Mind": {
        "Inner peace": "1001105010",
        "Cancel negativity": "4748132148",
        "Understanding": "39119488061",
        "Ideal future": "813791",
        "Positive Outlook": "25 67 993",
        "Gain Confidence": "45 32 246",
        "Focus": "45 88 623",
        "Fear": "42 58 735",
        "Anger": "66 82 121",
        "Betrayal": "53 14 80853",
    },
    "Health": {
        "Manifest Weight Loss": "5343168 31 22 778",
        "Hormonal Imbalance": "81 63 957",
        "Nourish Hair": "33 48 452",
        "Increased Muscle Flexibility & Strength": "81 21 596",
        "Wrinkles": "11112",
        "Cellulite": "2911",
    },
    "Other": {
        "Good luck": "817219738",
        "Fame": "8277237",
    },
}

# ==============================================================================
# 2. DESTINY MATRIX CALCULATION HELPERS
# ==============================================================================
def reduce_arcana(val: int) -> int:
    """Reduces numbers greater than 22 by summing their digits until <= 22."""
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return val

def calculate_destiny_matrix(dob: datetime.date):
    day = dob.day
    month = dob.month
    year = dob.year
    
    # Core Personal Square
    A = reduce_arcana(day)
    B = reduce_arcana(month)
    C = reduce_arcana(sum(int(d) for d in str(year)))
    D = reduce_arcana(A + B + C)
    E = reduce_arcana(A + B + C + D)  # Center/Comfort zone
    
    # Ancestral Cross
    F = reduce_arcana(A + B)  # Top-left (Father line)
    G = reduce_arcana(B + C)  # Top-right (Mother line)
    H = reduce_arcana(C + D)  # Bottom-right
    I = reduce_arcana(D + A)  # Bottom-left
    
    # Destinies
    sky = reduce_arcana(B + D)
    earth = reduce_arcana(A + C)
    personal_destiny = reduce_arcana(sky + earth)
    
    father_line = reduce_arcana(F + H)
    mother_line = reduce_arcana(G + I)
    social_destiny = reduce_arcana(father_line + mother_line)
    
    spiritual_destiny = reduce_arcana(personal_destiny + social_destiny)
    
    return {
        "A (Day/Personality)": A,
        "B (Month/Higher Self)": B,
        "C (Year/Karma)": C,
        "D (Bottom/Past Life)": D,
        "E (Center/Comfort Zone)": E,
        "F (Father Ancestral Top-Left)": F,
        "G (Mother Ancestral Top-Right)": G,
        "H (Ancestral Bottom-Right)": H,
        "I (Ancestral Bottom-Left)": I,
        "Sky Destiny": sky,
        "Earth Destiny": earth,
        "Personal Destiny": personal_destiny,
        "Social Destiny": social_destiny,
        "Spiritual Destiny": spiritual_destiny,
    }

# ==============================================================================
# 3. INTERFACE & NAVIGATION
# ==============================================================================
st.title("🧬 MetaMatrix Destiny & Quantum Portal")

tab1, tab2, tab3 = st.tabs(["🔮 Destiny Matrix Engine", "✨ Manifestation Codes", "🪐 Human Design / Ephemeris"])

# ------------------------------------------------------------------------------
# TAB 1: DESTINY MATRIX
# ------------------------------------------------------------------------------
with tab1:
    st.header("Destiny Matrix Calculator")
    st.write("Enter birth details to generate the core energy nodes and destiny points.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        name_input = st.text_input("Full Name", value="Princess Jasmine")
    with col_input2:
        dob_input = st.date_input("Date of Birth", value=datetime.date(1985, 1, 1), min_value=datetime.date(1900, 1, 1))
        
    if st.button("Calculate Matrix", type="primary"):
        matrix_results = calculate_destiny_matrix(dob_input)
        
        st.subheader(f"✨ Destiny Matrix Profile for {name_input}")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        keys = list(matrix_results.keys())
        for idx, key in enumerate(keys):
            target_col = [col_res1, col_res2, col_res3][idx % 3]
            with target_col:
                st.metric(label=key, value=f"Arcana {matrix_results[key]}")

# ------------------------------------------------------------------------------
# TAB 2: MANIFESTATION CODES
# ------------------------------------------------------------------------------
with tab2:
    st.header("Grabovoi & Quantum Frequency Codes")
    
    categories = list(MANIFESTATION_CODES.keys())
    selected_category = st.selectbox("Select a Category:", categories)
    
    st.markdown("---")
    
    if selected_category:
        codes = MANIFESTATION_CODES[selected_category]
        col1, col2 = st.columns(2)
        
        for idx, (intention, code) in enumerate(codes.items()):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                st.subheader(f"✨ {intention}")
                st.code(code, language="text")

# ------------------------------------------------------------------------------
# TAB 3: HUMAN DESIGN / EPHEMERIS
# ------------------------------------------------------------------------------
with tab3:
    st.header("Human Design & Swiss Ephemeris Module")
    if HAS_SWISSEPH:
        st.success("Swiss Ephemeris (`pyswisseph`) module is compiled and ready for planetary calculations.")
    else:
        st.warning("`pyswisseph` is loading or building in the environment.")