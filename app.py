import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="MetaMatrix Destiny Engine",
    page_icon="✨",
    layout="wide"
)

st.title("✨ METAMATRIX DESTINY ✨")

# ==========================================
# 2. ENERGY INTERPRETATIONS & POSITION MAPS
# ==========================================
ENERGY_DESCRIPTIONS = {
    1: "The Magician / Creator: Pioneer spirit, strong willpower, resourcefulness, and leadership. You are a natural manifestor with the ability to turn thoughts into physical reality.",
    2: "Harmony / Intuition: Receptivity, secret knowledge, deep intuition, and diplomacy. You thrive when balancing dualities and listening to your inner voice.",
    3: "The Empress / Fertility: Creation, abundance, feminine power, nurture, and beauty. Represents growth, financial flow, and bringing projects to fruition.",
    4: "The Emperor / Structure: Authority, stability, order, discipline, and organization. Demands leadership, personal accountability, and building lasting foundations.",
    5: "The Teacher / Traditions: Wisdom, spiritual laws, guidance, family values, and learning. You are called to acquire knowledge and share truth with integrity.",
    6: "Relations / Choice: Love, harmony, decision-making, aesthetic sense, and deep connections. Focuses on accepting yourself and making choices alignment with your heart.",
    7: "The Charioteer / Victory: Movement, drive, goal orientation, leadership, and triumph over obstacles. Demands clear direction and active momentum.",
    8: "Justice / Balance: Karmic law, cause and effect, truth, integrity, and equilibrium. Reminds you that every action brings an equal reaction; seek systemic clarity.",
    9: "The Hermit / Wisdom: Deep introspection, spiritual knowledge, solitude, and inner guidance. Encourages taking time away from noise to access deep inner truths.",
    10: "The Wheel of Fortune / Destiny: Flow, luck, cycle changes, trust in life, and synchronicities. Teaches you to ride the waves of change without resisting the current.",
    11: "Strength / Potential: Great physical and inner vitality, passion, endurance, and power. Shows the ability to master raw impulses through gentleness and self-belief.",
    12: "The Visionary / Service: New perspectives, selfless service, compassion, and deep reflection. Asks you to reframe sacrifices and look at the world from new angles.",
    13: "Transformation / Rebirth: Endings and beginnings, radical change, letting go, and regeneration. Clears out dead weight so true transformation can take place.",
    14: "Temperance / Healing: Moderation, art, emotional equilibrium, patience, and balance. Brings steady emotional synthesis, creative flow, and inner peace.",
    15: "The Shadow / Passion: Charisma, material magnetism, uncovering illusions, and confronting shadows. A test of spiritual power over material temptation.",
    16: "The Tower / Awakening: Destruction of false structures, rapid spiritual growth, and breakthroughs. Shatters outdated illusions to build on absolute truth.",
    17: "The Star / Inspiration: Creativity, hope, talent, public recognition, and higher intuition. Encourages shining your unique light brightly without fear.",
    18: "The Moon / Subconscious: Imagination, overcoming fears, intuition, magic, and materialization. Unlocks deep psychic awareness while mastering subconscious fears.",
    19: "The Sun / Joy: Public influence, leadership, success, prosperity, and childlike happiness. Radiates warmth, abundance, and generous, confident expression.",
    20: "The Resurrection / Family Karma: Ancestral rebirth, deep awakenings, system transformation, and legacy. Calls you to heal bloodline patterns and awaken spiritual gifts.",
    21: "The World / Expansion: Global vision, peace, freedom, completion, and limitless potential. Represents cosmic alignment, international connections, and wholeness.",
    22: "Freedom / Fool: Unconditional freedom, trust in the universe, lightness, and new beginnings. Step into the unknown with childlike trust and total openness."
}

POSITION_EXPLANATIONS = {
    "Crown / Top Energy": "Your spiritual connection, inspiration, and highest vibration. This shows how you express your highest potential and divine inspiration.",
    "Left / Karma": "Your primary karmic lesson and challenge. This represents the hurdle or debt brought into this lifetime that requires active awareness to balance.",
    "Right / Talent": "Your practical talent and engine for manifestation. This energy powers your material achievements, career success, and creative output.",
    "Karmic Tail / Base": "Your subconscious root foundation. This is unhealed baggage or deeply ingrained habits that pull you down if left unaddressed.",
    "Center / Soul": "The core of your psyche. Represents what brings your soul deep peace, emotional comfort, and central alignment when you operate authentically.",
    "Father Line (Top-Left to Bottom-Right)": "Top-Left reveals inherited paternal strengths; Bottom-Right reveals unhealed male bloodline karma and subconscious patterns.",
    "Mother Line (Top-Right to Bottom-Left)": "Top-Right reveals inherited maternal talents; Bottom-Left reveals passed-down female bloodline beliefs, traditions, and lessons.",
    "Personal Destiny (20-40)": "Your core developmental phase (ages 20 to 40). Focuses on building self-mastery, personal identity, and emotional independence.",
    "Social Destiny (40-60)": "Your mid-life expansion (ages 40 to 60). Focuses on your contribution to community, relationship dynamics, and societal impact.",
    "Spiritual / Lifetime Purpose": "Your overarching soul mission across this entire incarnation—the ultimate synthesis of your personal and social growth."
}

# ==========================================
# 3. USER INSTRUCTIONS & OVERVIEW
# ==========================================
with st.expander("📖 **How to Read & Interpret Your Destiny Matrix**", expanded=True):
    st.markdown("""
    ### Welcome to MetaMatrix Destiny
    This is not just a calculation engine—it is a comprehensive map of your soul's architecture using sacred geometry and numerology.

    #### How to Navigate Your Analysis:
    1. **Life Purpose Synthesis:** Your quick-start guide. Identifies your primary goal, your biggest roadblock, and the exact energy needed to overcome it.
    2. **Core Matrix Energies:** Defines the 5 key pillars of your personality, soul comfort, gifts, and primary karmic test.
    3. **Ancestral Lineage:** Explains inherited bloodline dynamics passed down through your mother's and father's sides.
    4. **Destiny Eras:** Shows how your focus evolves from self-building (ages 20–40) to social contribution (40–60) and ultimate spiritual mastery.
    5. **Chakra Alignment:** Maps your energies across the physical and subtle body centers.
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
        "ancestral_raw": {
            "Father Line Top-Left (Strengths)": father_tl,
            "Father Line Bottom-Right (Unhealed Karma)": father_br,
            "Mother Line Top-Right (Gifts)": mother_tr,
            "Mother Line Bottom-Left (Lessons/Beliefs)": mother_bl
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
# 5. EXPANDED READABLE PDF GENERATOR
# ==========================================
def generate_pdf(results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    # Custom Palette & Typography
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, spaceAfter=8, textColor=colors.HexColor("#1A252C"))
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=12, textColor=colors.HexColor("#555555"))
    section_heading = ParagraphStyle('SecHead', parent=styles['Heading2'], fontSize=14, leading=18, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor("#2C3E50"))
    position_title = ParagraphStyle('PosTitle', parent=styles['Heading3'], fontSize=11, leading=14, spaceBefore=6, spaceAfter=2, textColor=colors.HexColor("#16A085"))
    body_text = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, leading=13.5, spaceAfter=4)
    italic_note = ParagraphStyle('Note', parent=styles['Italic'], fontSize=8.5, leading=11, spaceAfter=6, textColor=colors.HexColor("#666666"))

    elements = []

    # Header
    elements.append(Paragraph("MetaMatrix Destiny — Comprehensive Soul Analysis", title_style))
    elements.append(Paragraph("Personalized Energetic Blueprint, Ancestral Mapping & Destiny Timeline", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2C3E50"), spaceAfter=14))

    # 1. Life Purpose Synthesis
    elements.append(Paragraph("1. Life Purpose & Breakthrough Synthesis", section_heading))
    elements.append(Paragraph("This synthesis outlines your highest aspiration, the primary energetic friction keeping you from it, and the golden key needed to unlock balance.", body_text))
    elements.append(Spacer(1, 4))

    synthesis = calculate_life_synthesis(results)
    for label, val in synthesis.items():
        desc = ENERGY_DESCRIPTIONS.get(val, "")
        elements.append(Paragraph(f"<b>{label}:</b> Energy {val}", position_title))
        elements.append(Paragraph(desc, body_text))
        elements.append(Spacer(1, 2))

    elements.append(Spacer(1, 10))

    # 2. Core Matrix Energies
    elements.append(Paragraph("2. Core Matrix Energies", section_heading))
    for pos, val in results['core'].items():
        pos_expl = POSITION_EXPLANATIONS.get(pos, "")
        energy_desc = ENERGY_DESCRIPTIONS.get(val, "")
        
        elements.append(Paragraph(f"<b>{pos}</b> — Energy {val}", position_title))
        elements.append(Paragraph(f"<i>Position Meaning:</i> {pos_expl}", italic_note))
        elements.append(Paragraph(f"<i>Active Archetype:</i> {energy_desc}", body_text))
        elements.append(Spacer(1, 4))

    # Page Break for clean reading structure
    elements.append(PageBreak())

    # 3. Ancestral Lineage Channels
    elements.append(Paragraph("3. Ancestral Lineage Channels", section_heading))
    elements.append(Paragraph("Your matrix contains two major diagonal channels carrying genetic and spiritual information passed down through bloodlines.", body_text))
    elements.append(Spacer(1, 4))

    for line_pos, val in results['ancestral_raw'].items():
        energy_desc = ENERGY_DESCRIPTIONS.get(val, "")
        elements.append(Paragraph(f"<b>{line_pos}</b> — Energy {val}", position_title))
        elements.append(Paragraph(f"<i>Active Archetype:</i> {energy_desc}", body_text))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 8))

    # 4. Destiny Purposes Timeline
    elements.append(Paragraph("4. Destiny Purpose Timeline", section_heading))
    for dest_pos, val in results['destiny'].items():
        pos_expl = POSITION_EXPLANATIONS.get(dest_pos, "")
        energy_desc = ENERGY_DESCRIPTIONS.get(val, "")
        
        elements.append(Paragraph(f"<b>{dest_pos}</b> — Energy {val}", position_title))
        elements.append(Paragraph(f"<i>Timeline Meaning:</i> {pos_expl}", italic_note))
        elements.append(Paragraph(f"<i>Guiding Energy:</i> {energy_desc}", body_text))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 8))

    # 5. Chakra Energy Alignment Map
    elements.append(Paragraph("5. Chakra Energy Alignment Map", section_heading))
    elements.append(Paragraph("Shows how your core energies map across your physical and energetic centers:", body_text))
    elements.append(Spacer(1, 4))

    for ch_name, val in results['chakra'].items():
        energy_desc = ENERGY_DESCRIPTIONS.get(val, "")
        elements.append(Paragraph(f"<b>{ch_name}:</b> Energy {val}", position_title))
        elements.append(Paragraph(f"<i>Expression:</i> {energy_desc}", body_text))

    # Footer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceBefore=16, spaceAfter=8))
    elements.append(Paragraph("Generated via MetaMatrix Destiny Engine • All Rights Reserved", italic_note))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==========================================
# 6. USER INPUT & APPLICATION UI
# ==========================================
st.markdown("### 🗓️ Enter Birth Information")
col1, col2, col3 = st.columns(3)

with col1:
    day = st.number_input("Day of Birth", min_value=1, max_value=31, value=19)
with col2:
    month = st.number_input("Month of Birth", min_value=1, max_value=12, value=12)
with col3:
    year = st.number_input("Year of Birth", min_value=1900, max_value=2100, value=1978)

if st.button("Calculate Matrix & Generate Reading", type="primary"):
    st.session_state['results'] = calculate_full_matrix(day, month, year)

if 'results' in st.session_state:
    res = st.session_state['results']
    st.markdown("---")

    # Life Purpose Synthesis
    st.markdown("### 🎯 Life Purpose & Breakthrough Synthesis")
    synthesis = calculate_life_synthesis(res)
    
    syn_col1, syn_col2, syn_col3 = st.columns(3)
    with syn_col1:
        g_val = synthesis["Goal (Highest Potential)"]
        st.info(f"**Goal (Highest Potential)**\n\n**Energy {g_val}**\n\n_{ENERGY_DESCRIPTIONS.get(g_val, '')}_")
    with syn_col2:
        o_val = synthesis["Obstacle (Karmic Block)"]
        st.error(f"**Obstacle (Karmic Block)**\n\n**Energy {o_val}**\n\n_{ENERGY_DESCRIPTIONS.get(o_val, '')}_")
    with syn_col3:
        s_val = synthesis["Solution (How to Overcome)"]
        st.success(f"**Solution (How to Overcome)**\n\n**Energy {s_val}**\n\n_{ENERGY_DESCRIPTIONS.get(s_val, '')}_")

    st.markdown("---")

    # Detailed Interactive View Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Core Energies", 
        "🧬 Ancestral Lines", 
        "⏳ Destiny Eras", 
        "🌈 Chakra Map"
    ])

    with tab1:
        st.subheader("Core Matrix Pillars")
        for k, v in res['core'].items():
            with st.container():
                st.markdown(f"#### **{k}** — Energy {v}")
                st.caption(f"**Position Role:** {POSITION_EXPLANATIONS.get(k, '')}")
                st.write(ENERGY_DESCRIPTIONS.get(v, ""))
                st.markdown("---")

    with tab2:
        st.subheader("Ancestral Bloodline Channels")
        for k, v in res['ancestral_raw'].items():
            with st.container():
                st.markdown(f"#### **{k}** — Energy {v}")
                st.write(ENERGY_DESCRIPTIONS.get(v, ""))
                st.markdown("---")

    with tab3:
        st.subheader("Destiny Eras & Lifetime Purpose")
        for k, v in res['destiny'].items():
            with st.container():
                st.markdown(f"#### **{k}** — Energy {v}")
                st.caption(f"**Timeline Context:** {POSITION_EXPLANATIONS.get(k, '')}")
                st.write(ENERGY_DESCRIPTIONS.get(v, ""))
                st.markdown("---")

    with tab4:
        st.subheader("Chakra Energy Map")
        for k, v in res['chakra'].items():
            st.markdown(f"**{k}** (Energy {v}): _{ENERGY_DESCRIPTIONS.get(v, '')}_")

    st.markdown("---")

    # PDF Generator Action Button
    pdf_data = generate_pdf(res)
    st.download_button(
        label="📄 Download Complete Detailed PDF Report",
        data=pdf_data,
        file_name="MetaMatrix_Destiny_Comprehensive_Analysis.pdf",
        mime="application/pdf"
    )