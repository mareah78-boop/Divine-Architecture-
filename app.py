import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="MetaMatrix Destiny Engine",
    page_icon="✨",
    layout="centered"
)

st.title("✨ METAMATRIX DESTINY ✨")

# ==========================================
# 2. ENERGY INTERPRETATIONS DICTIONARY
# ==========================================
ENERGY_DESCRIPTIONS = {
    1: "Energy of the Magician / Creator: Pioneer spirit, strong willpower, resourcefulness, and leadership.",
    2: "Energy of Harmony / Intuition: Receptivity, secret knowledge, deep intuition, and diplomacy.",
    3: "Energy of the Empress / Fertility: Creation, abundance, feminine power, nurture, and beauty.",
    4: "Energy of the Emperor / Structure: Authority, stability, order, discipline, and organization.",
    5: "Energy of the Teacher / Traditions: Wisdom, spiritual laws, guidance, family values, and learning.",
    6: "Energy of Relations / Choice: Love, harmony, decision-making, aesthetic sense, and deep connections.",
    7: "Energy of the Charioteer / Victory: Movement, drive, goal orientation, leadership, and triumph over obstacles.",
    8: "Energy of Justice / Balance: Karmic law, cause and effect, truth, integrity, and equilibrium.",
    9: "Energy of the Hermit / Wisdom: Deep introspection, spiritual knowledge, solitude, and inner guidance.",
    10: "Energy of the Wheel of Fortune / Destiny: Flow, luck, cycle changes, trust in life, and synchronicities.",
    11: "Energy of Strength / Potential: Great physical and inner vitality, passion, endurance, and power.",
    12: "Energy of the Visionary / Service: New perspectives, selfless service, compassion, and deep reflection.",
    13: "Energy of Transformation / Rebirth: Endings and beginnings, radical change, letting go, and regeneration.",
    14: "Energy of Temperance / Healing: Moderation, art, emotional equilibrium, patience, and balance.",
    15: "Energy of the Shadow / Passion: Charisma, material magnetism, uncovering illusions, and confronting shadows.",
    16: "Energy of the Tower / Awakening: Destruction of false structures, rapid spiritual growth, and breakthroughs.",
    17: "Energy of the Star / Inspiration: Creativity, hope, talent, public recognition, and higher intuition.",
    18: "Energy of the Moon / Subconscious: Imagination, overcoming fears, intuition, magic, and materialization.",
    19: "Energy of the Sun / Joy: Public influence, leadership, success, prosperity, and childlike happiness.",
    20: "Energy of the Resurrection / Family Karma: Ancestral rebirth, deep awakenings, system transformation, and legacy.",
    21: "Energy of the World / Expansion: Global vision, peace, freedom, completion, and limitless potential.",
    22: "Energy of Freedom / Fool: Unconditional freedom, trust in the universe, lightness, and new beginnings."
}

# ==========================================
# 3. USER INSTRUCTIONS & OVERVIEW
# ==========================================
with st.expander("📖 **How to Use & What This Analysis Means**", expanded=True):
    st.markdown("""
    ### Welcome to MetaMatrix Destiny
    This tool calculates your unique energy blueprint based on the **Destination Matrix** system, combining numerology and sacred geometry to map your core life energies, inherited ancestral patterns, and spiritual evolution.

    ---

    ### 🔮 How to Get Started:
    1. **Enter Your Birthdate:** Select your exact Day, Month, and Year of birth using the inputs below.
    2. **Calculate Your Matrix:** Click the **Calculate Matrix** button to process your blueprint.
    3. **Explore Your Energies:** Review your Life Synthesis, Core, Ancestral, Destiny, and Chakra maps directly on screen.
    4. **Download Your Detailed Report:** Click the **Download Complete Detailed PDF Report** button to generate a PDF with full energy interpretations.

    ---

    ### 🧬 Key Sections Overview:
    * **Life Purpose & Breakthrough Synthesis:** Highlights your higher goal, karmic block, and breakthrough solution.
    * **Core Matrix Energies:** Maps your primary Archetypes (Crown, Karma, Talent, Karmic Tail/Base, and Soul Center).
    * **Ancestral Lineage Channels:** Reveals inherited lineage energies along the Father and Mother diagonals.
    * **Destiny Purposes:** Breaks down your Personal (20–40), Social (40–60), and Lifetime Spiritual purpose.
    * **Chakra Energy Map:** Maps your numbers across the 7 primary energy centers.
    """)

# ==========================================
# 4. CALCULATION ENGINE LOGIC
# ==========================================
def reduce_to_22(n):
    n = abs(int(n))
    while n > 22:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_full_matrix(day, month, year):
    top = reduce_to_22(day)
    left = reduce_to_22(month)
    year_sum = sum(int(d) for d in str(year))
    right = reduce_to_22(year_sum)
    bottom = reduce_to_22(top + left + right)
    center = reduce_to_22(top + left + right + bottom)
    
    father_tl = reduce_to_22(top + left)
    father_br = reduce_to_22(right + bottom)
    mother_tr = reduce_to_22(top + right)
    mother_bl = reduce_to_22(left + bottom)

    personal_destiny = reduce_to_22(top + bottom)
    social_destiny = reduce_to_22(left + right)
    spiritual_destiny = reduce_to_22(personal_destiny + social_destiny)

    sahasrara = reduce_to_22(top + left)
    ajna = reduce_to_22(top + center)
    vishuddha = reduce_to_22(left + center)
    anahata = center
    manipura = reduce_to_22(right + center)
    svadhisthana = reduce_to_22(bottom + center)
    muladhara = reduce_to_22(bottom + right)

    return {
        "core": {
            "Crown / Top Energy": top,
            "Left / Karma": left,
            "Right / Talent": right,
            "Karmic Tail / Base": bottom,
            "Center / Soul": center
        },
        "ancestral": {
            "Father Line (Top-Left to Bottom-Right)": f"{father_tl} - {father_br}",
            "Mother Line (Top-Right to Bottom-Left)": f"{mother_tr} - {mother_bl}"
        },
        "destiny": {
            "Personal Destiny (20-40)": personal_destiny,
            "Social Destiny (40-60)": social_destiny,
            "Spiritual / Lifetime Purpose": spiritual_destiny
        },
        "chakra": {
            "Sahasrara (Crown)": sahasrara,
            "Ajna (Third Eye)": ajna,
            "Vishuddha (Throat)": vishuddha,
            "Anahata (Heart)": anahata,
            "Manipura (Solar Plexus)": manipura,
            "Svadhisthana (Sacral)": svadhisthana,
            "Muladhara (Root)": muladhara
        }
    }

def calculate_life_synthesis(res):
    goal_energy = res['core']['Crown / Top Energy']
    obstacle_energy = res['core']['Left / Karma']
    center_energy = res['core']['Center / Soul']
    solution_energy = reduce_to_22(obstacle_energy + center_energy)
    
    return {
        "Goal (Highest Potential)": goal_energy,
        "Obstacle (Karmic Block)": obstacle_energy,
        "Solution (How to Overcome)": solution_energy
    }

# ==========================================
# 5. DETAILED PDF REPORT GENERATOR
# ==========================================
def generate_pdf(results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=36, 
        leftMargin=36, 
        topMargin=36, 
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, spaceAfter=10, textColor=colors.HexColor("#1A1A1A"))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=13, leading=16, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#2C3E50"))
    label_style = ParagraphStyle('LabelStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=2)
    desc_style = ParagraphStyle('DescStyle', parent=styles['Italic'], fontSize=9, leading=12, spaceAfter=8, textColor=colors.HexColor("#555555"))

    elements = []

    elements.append(Paragraph("MetaMatrix Destiny - Detailed Personal Analysis", title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceAfter=12))

    def append_section(title, data_dict):
        elements.append(Paragraph(title, heading_style))
        for label, val in data_dict.items():
            elements.append(Paragraph(f"<b>{label}:</b> {val}", label_style))
            if isinstance(val, int) and val in ENERGY_DESCRIPTIONS:
                elements.append(Paragraph(f"└ <i>{ENERGY_DESCRIPTIONS[val]}</i>", desc_style))
        elements.append(Spacer(1, 6))

    # Add Synthesis First in PDF for impact
    synthesis_data = calculate_life_synthesis(results)
    append_section("1. Life Purpose & Breakthrough Synthesis", synthesis_data)

    append_section("2. Core Matrix Energies", results['core'])

    elements.append(Paragraph("3. Ancestral Lineage Channels", heading_style))
    for line, numbers in results['ancestral'].items():
        elements.append(Paragraph(f"<b>{line}:</b> {numbers}", label_style))
    elements.append(Spacer(1, 6))

    append_section("4. Destiny Purposes", results['destiny'])
    append_section("5. Chakra Energy Map", results['chakra'])

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceBefore=12, spaceAfter=8))
    elements.append(Paragraph("Generated via MetaMatrix Destiny Engine", desc_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==========================================
# 6. USER INPUT & APPLICATION UI
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    day = st.number_input("Day of Birth", min_value=1, max_value=31, value=19)
with col2:
    month = st.number_input("Month of Birth", min_value=1, max_value=12, value=12)
with col3:
    year = st.number_input("Year of Birth", min_value=1900, max_value=2100, value=1978)

if st.button("Calculate Matrix", type="primary"):
    st.session_state['results'] = calculate_full_matrix(day, month, year)

if 'results' in st.session_state:
    res = st.session_state['results']
    st.markdown("---")

    # Life Purpose & Breakthrough Synthesis UI
    st.markdown("### 🎯 Life Purpose & Breakthrough Synthesis")
    synthesis = calculate_life_synthesis(res)
    
    syn_col1, syn_col2, syn_col3 = st.columns(3)
    with syn_col1:
        g_val = synthesis["Goal (Highest Potential)"]
        st.info(f"**Goal (Highest Potential)**\n\nEnergy {g_val}\n\n_{ENERGY_DESCRIPTIONS.get(g_val, '')}_")
    with syn_col2:
        o_val = synthesis["Obstacle (Karmic Block)"]
        st.error(f"**Obstacle (Karmic Block)**\n\nEnergy {o_val}\n\n_{ENERGY_DESCRIPTIONS.get(o_val, '')}_")
    with syn_col3:
        s_val = synthesis["Solution (How to Overcome)"]
        st.success(f"**Solution (How to Overcome)**\n\nEnergy {s_val}\n\n_{ENERGY_DESCRIPTIONS.get(s_val, '')}_")

    st.markdown("---")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.subheader("Core Energies")
        for k, v in res['core'].items():
            st.write(f"**{k}:** {v}")
            st.caption(ENERGY_DESCRIPTIONS.get(v, ""))

    with col_b:
        st.subheader("Ancestral Lines")
        for k, v in res['ancestral'].items():
            st.write(f"**{k}:** {v}")

        st.subheader("Destiny Purposes")
        for k, v in res['destiny'].items():
            st.write(f"**{k}:** {v}")
            st.caption(ENERGY_DESCRIPTIONS.get(v, ""))

    with col_c:
        st.subheader("Chakra Alignment")
        for k, v in res['chakra'].items():
            st.write(f"**{k}:** {v}")
            st.caption(ENERGY_DESCRIPTIONS.get(v, ""))

    st.markdown("---")

    pdf_data = generate_pdf(res)
    st.download_button(
        label="📄 Download Complete Detailed PDF Report",
        data=pdf_data,
        file_name="MetaMatrix_Destiny_Full_Report.pdf",
        mime="application/pdf"
    )