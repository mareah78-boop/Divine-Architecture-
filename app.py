import streamlit as st
import datetime
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import ephem

# --- Title and Header ---
st.set_page_config(page_title="MetaMatrix Destiny", layout="wide")
st.title("MetaMatrix Destiny Engine")

# --- Arcana Dictionary / Reference Data ---
ARCANA_DICT = {
    1: ("The Magician", "Resourcefulness, action, power, manifestation capability."),
    2: ("The High Priestess", "Intuition, sacred knowledge, subconscious wisdom."),
    3: ("The Empress", "Abundance, creation, nurturing, material harmony."),
    4: ("The Emperor", "Structure, authority, stability, discipline."),
    5: ("The Hierophant", "Spiritual guidance, traditional wisdom, higher learning."),
    6: ("The Lovers", "Choice, harmony, alignment of dualities, relationships."),
    7: ("The Chariot", "Willpower, momentum, purpose-driven action, victory."),
    8: ("Justice", "Karma, cosmic balance, cause and effect, truth."),
    9: ("The Hermit", "Inner reflection, wisdom, soul-searching, solitude."),
    10: ("Wheel of Fortune", "Cycles, fate, turning points, alignment with flow."),
    11: ("Strength", "Inner resilience, passion, balance of spirit and instinct."),
    12: ("The Hanged Man", "New perspective, surrender, release of control."),
    13: ("Death", "Transformation, rebirth, shedding the obsolete."),
    14: ("Temperance", "Alchemy, moderation, spiritual integration."),
    15: ("The Devil", "Shadow integration, breaking attachments, material mastery."),
    16: ("The Tower", "Breakthrough, truth, shattering false foundations."),
    17: ("The Star", "Hope, cosmic connection, inspiration, vision."),
    18: ("The Moon", "Illusion, deep subconscious work, intuition, dreams."),
    19: ("The Sun", "Vitality, success, clarity, radiant self-expression."),
    20: ("Judgement", "Soul calling, awakening, ancestral clearing."),
    21: ("The World", "Completion, wholeness, cosmic integration."),
    22: ("The Fool", "Infinite potential, faith, new beginnings, freedom.")
}

EXPANDED_GRABOVOI = {
    "Financial Abundance": {"code": "318 798", "focus": "Wealth Flow & Opportunity Alignment", "protocol": "Visualize the numbers illuminated in golden light at the solar plexus during breathwork."},
    "Harmonization of Space": {"code": "14888948", "focus": "Energetic Clearing & Environmental Balance", "protocol": "Recite code mentally while walking through your living or working environment."},
    "Self-Healing & Vitality": {"code": "1814321", "focus": "Cellular Regeneration & Vital Energy", "protocol": "Focus on the heart space and project the sequence into a sphere of silver light."},
    "Transformation of Negative to Positive": {"code": "1888948", "focus": "Alchemical Transmutation of Shadow", "protocol": "Hold the sequence in mind during reflection, visualizing dense energy releasing into light."}
}

# --- Calculation Engines ---
def reduce_arcana(val):
    while val > 22:
        val = sum(int(digit) for digit in str(val))
    return val if val != 0 else 22

def calculate_destiny_matrix(dob):
    day = dob.day
    month = dob.month
    year = dob.year
    
    A = reduce_arcana(day)
    B = reduce_arcana(month)
    C = reduce_arcana(sum(int(d) for d in str(year)))
    D = reduce_arcana(A + B + C)
    E = reduce_arcana(A + B + C + D)
    
    # Ancestral Lineage Points
    F = reduce_arcana(A + B)
    G = reduce_arcana(B + C)
    H = reduce_arcana(C + D)
    I = reduce_arcana(D + A)
    
    return {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G, 'H': H, 'I': I}

def calculate_human_design(dob, tob):
    # Base calculation wrapper for ephem gate positions
    dt = datetime.datetime.combine(dob, tob)
    observer = ephem.Observer()
    observer.date = dt
    sun = ephem.Sun(observer)
    
    sun_lon = float(sun.hlon) * 180.0 / 3.141592653589793
    gate_num = int((sun_lon / 360.0) * 64) + 1
    return {"Sun Gate": gate_num, "Ecliptic Longitude": round(sun_lon, 2)}

# --- PDF Generation Function ---
def generate_pdf_report(name, dob, tob, calc_data, hd_calc):
    pdf_filename = "MetaMatrix_Destiny_Report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor("#2C3E50"))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor("#16A085"))
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14)
    table_cell_style = ParagraphStyle('TableCellStyle', parent=styles['Normal'], fontSize=9, leading=12)
    
    # Title Section
    story.append(Paragraph(f"MetaMatrix Destiny Report: {name}", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Date of Birth:</b> {dob.strftime('%B %d, %Y')} | <b>Time of Birth:</b> {tob.strftime('%I:%M %p')}", body_style))
    story.append(Spacer(1, 14))
    
    # 1. Core Energy Section
    story.append(Paragraph("1. Core Energy Blueprint", heading_style))
    story.append(Spacer(1, 6))
    
    node_data = [["Node / Position", "Arcana", "Archetype", "Core Meaning"]]
    for key in ['A', 'B', 'C', 'D', 'E']:
        val = calc_data[key]
        label = f"Position {key}" if key != 'E' else "Center E (Core Soul)"
        t_title, t_desc = ARCANA_DICT.get(val, ("Unknown", "No description available."))
        node_data.append([
            Paragraph(label, table_cell_style),
            Paragraph(str(val), table_cell_style),
            Paragraph(f"<b>{t_title}</b>", table_cell_style),
            Paragraph(t_desc, table_cell_style)
        ])
        
    t_nodes = Table(node_data, colwidths=[110, 45, 125, 260])
    t_nodes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_nodes)
    story.append(Spacer(1, 10))

    # Integration Guidance for Core Energy (PDF)
    core_guide = "<b>Integration Guidance:</b> Use Center E as your primary 'North Star' baseline. Before making major life or career moves, audit whether you are acting from your Arcana's high-frequency gift or reacting out of its shadow pattern."
    story.append(Paragraph(core_guide, table_cell_style))
    story.append(Spacer(1, 14))

    # 2. Ancestral Lines
    story.append(Paragraph("2. Ancestral & Lineage Support", heading_style))
    story.append(Spacer(1, 6))
    anc_data = [["Lineage Node", "Arcana", "Archetype", "Lineage Focus"]]
    anc_map = [('F', 'Father Line (Spirit Top)'), ('I', 'Father Line (Material Bottom)'), ('G', 'Mother Line (Spirit Top)'), ('H', 'Mother Line (Material Bottom)')]
    for key, desc in anc_map:
        val = calc_data[key]
        t_title, t_desc = ARCANA_DICT.get(val, ("", ""))
        anc_data.append([
            Paragraph(desc, table_cell_style),
            Paragraph(str(val), table_cell_style),
            Paragraph(f"<b>{t_title}</b>", table_cell_style),
            Paragraph(t_desc, table_cell_style)
        ])
    t_anc = Table(anc_data, colwidths=[150, 45, 125, 220])
    t_anc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_anc)
    story.append(Spacer(1, 14))

    # 3. Grabovoi Manifestation Portal
    story.append(Paragraph("3. Grabovoi Quantum Portal", heading_style))
    story.append(Spacer(1, 6))
    g_data = [["Focus Area", "Sequence Code", "Activation Protocol"]]
    for title, info in EXPANDED_GRABOVOI.items():
        g_data.append([
            Paragraph(f"<b>{title}</b>", table_cell_style),
            Paragraph(info["code"], table_cell_style),
            Paragraph(info["protocol"], table_cell_style)
        ])
    t_g = Table(g_data, colwidths=[140, 90, 310])
    t_g.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_g)

    doc.build(story)
    return pdf_filename

# --- User Input Controls ---
col1, col2, col3 = st.columns(3)
with col1:
    user_name = st.text_input("Full Name", value="Princess Jasmine")
with col2:
    dob = st.date_input("Date of Birth", value=datetime.date(1985, 8, 15))
with col3:
    time_unknown = st.checkbox("Time of Birth Unknown")
    if time_unknown:
        tob = datetime.time(12, 0)
        st.caption("Using 12:00 PM (Noon) default for calculation.")
    else:
        tob = st.time_input("Time of Birth", value=datetime.time(12, 0))

# Execute Calculations
calc_data = calculate_destiny_matrix(dob)
hd_calc = calculate_human_design(dob, tob)

# --- Display Output on Web UI ---
st.header(f"Blueprint for {user_name}")

# Section 1: Core Energy
st.subheader("Core Energy Blueprint")
cols = st.columns(5)
cols[0].metric("Position A", calc_data['A'])
cols[1].metric("Position B", calc_data['B'])
cols[2].metric("Position C", calc_data['C'])
cols[3].metric("Position D", calc_data['D'])
cols[4].metric("Center E (Core)", calc_data['E'])

with st.expander("📖 How to Apply Your Core Energy Blueprint"):
    st.markdown("""
    * **Your Baseline Frequency:** Center E represents your primary soul frequency. Use this as your 'North Star' for big decisions.
    * **In Light vs. Shadow:** When making a decision, ask yourself if you are operating from your Arcana's core gift or its shadow fear response.
    * **Daily Action:** Notice where you feel friction today. Are you resisting your natural outward projection (Position A)?
    """)

# Section 2: Ancestral Lines
st.subheader("Ancestral & Lineage Support")
st.write(f"**Father Line:** Spirit Top = {calc_data['F']}, Material Bottom = {calc_data['I']}")
st.write(f"**Mother Line:** Spirit Top = {calc_data['G']}, Material Bottom = {calc_data['H']}")

with st.expander("📖 How to Apply Your Lineage Blueprint"):
    st.markdown("""
    * **Generational Gifts:** Identify inherited strengths from maternal and paternal lines to lean into.
    * **Pattern Breaking:** Distinguish between your personal emotional patterns and ancestral cycles that are ready to be cleared.
    """)

# Section 3: Grabovoi Manifestation Portal
st.subheader("Grabovoi Quantum Portal")
for title, info in EXPANDED_GRABOVOI.items():
    st.write(f"**{title}** (`{info['code']}`): {info['focus']}")

# --- PDF Generation Button ---
if st.button("Generate Downloadable PDF Report"):
    pdf_path = generate_pdf_report(user_name, dob, tob, calc_data, hd_calc)
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="MetaMatrix_Destiny_Report.pdf",
            mime="application/pdf"
        )