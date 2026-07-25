import streamlit as st
import json
import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. HELPER FUNCTIONS & CALCULATIONS
# ==========================================

def reduce_to_22(n):
    """Reduces numbers greater than 22 by adding digits together, up to 22 max."""
    while n > 22:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_full_matrix(day, month, year):
    """Calculates all Core, Ancestral, Destiny, and Chakra energies."""
    # Core Primary Nodes
    top = reduce_to_22(day)
    left = reduce_to_22(month)
    right = reduce_to_22(sum(int(d) for d in str(year)))
    bottom = reduce_to_22(top + left + right)
    center = reduce_to_22(top + left + right + bottom)
    
    # Ancestral / Diagonal Lines
    father_line_1 = reduce_to_22(top + left)      # Top-Left Diagonal
    father_line_2 = reduce_to_22(right + bottom)  # Bottom-Right Diagonal
    mother_line_1 = reduce_to_22(top + right)     # Top-Right Diagonal
    mother_line_2 = reduce_to_22(left + bottom)   # Bottom-Left Diagonal
    
    # Destiny Purposes
    personal_destiny = reduce_to_22((top + bottom) + (left + right))
    social_destiny = reduce_to_22((father_line_1 + father_line_2) + (mother_line_1 + mother_line_2))
    spiritual_destiny = reduce_to_22(personal_destiny + social_destiny)
    
    # Chakra Energy Alignment
    chakras = {
        "Sahasrara (Crown)": reduce_to_22(top + center),
        "Ajna (Third Eye)": reduce_to_22(top + left + center),
        "Vishuddha (Throat)": reduce_to_22(left + center),
        "Anahata (Heart)": center,
        "Manipura (Solar Plexus)": reduce_to_22(bottom + center),
        "Svadhisthana (Sacral)": reduce_to_22(right + center),
        "Muladhara (Root)": reduce_to_22(bottom + right)
    }

    return {
        "core": {
            "top": top,
            "left": left,
            "right": right,
            "bottom": bottom,
            "center": center
        },
        "ancestral": {
            "Father Line (Top-Left to Bottom-Right)": f"{father_line_1} - {father_line_2}",
            "Mother Line (Top-Right to Bottom-Left)": f"{mother_line_1} - {mother_line_2}"
        },
        "destiny": {
            "personal": personal_destiny,
            "social": social_destiny,
            "spiritual": spiritual_destiny
        },
        "chakras": chakras
    }

# ==========================================
# 2. FULL PDF GENERATOR (REPORTLAB)
# ==========================================

def generate_full_pdf(matrix_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E1E1E'),
        spaceAfter=12
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=4
    )

    # Document Header
    story.append(Paragraph("MetaMatrix Destiny - Detailed Personal Analysis", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CCCCCC'), spaceAfter=12))

    # 1. Core Energies
    core = matrix_data['core']
    story.append(Paragraph("Core Matrix Energies", section_style))
    story.append(Paragraph(f"<b>Crown / Top Energy:</b> {core['top']}", body_style))
    story.append(Paragraph(f"<b>Left / Karma:</b> {core['left']}", body_style))
    story.append(Paragraph(f"<b>Right / Talent:</b> {core['right']}", body_style))
    story.append(Paragraph(f"<b>Karmic Tail / Base:</b> {core['bottom']}", body_style))
    story.append(Paragraph(f"<b>Center / Soul:</b> {core['center']}", body_style))
    story.append(Spacer(1, 8))

    # 2. Ancestral Lineage Channels
    story.append(Paragraph("Ancestral Lineage Channels", section_style))
    for line_name, value in matrix_data['ancestral'].items():
        story.append(Paragraph(f"<b>{line_name}:</b> {value}", body_style))
    story.append(Spacer(1, 8))

    # 3. Destiny Purposes
    destiny = matrix_data['destiny']
    story.append(Paragraph("Destiny Purposes", section_style))
    story.append(Paragraph(f"<b>Personal Destiny (20-40):</b> {destiny['personal']}", body_style))
    story.append(Paragraph(f"<b>Social Destiny (40-60):</b> {destiny['social']}", body_style))
    story.append(Paragraph(f"<b>Spiritual / Lifetime Purpose:</b> {destiny['spiritual']}", body_style))
    story.append(Spacer(1, 8))

    # 4. Chakra Alignment
    story.append(Paragraph("Chakra Energy Map", section_style))
    for chakra_name, val in matrix_data['chakras'].items():
        story.append(Paragraph(f"<b>{chakra_name}:</b> {val}", body_style))
    story.append(Spacer(1, 8))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#DDDDDD'), spaceBefore=12, spaceAfter=8))
    story.append(Paragraph("Generated via MetaMatrix Destiny Engine", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 3. STREAMLIT INTERFACE
# ==========================================

st.set_page_config(page_title="MetaMatrix Destiny", page_icon="✨", layout="wide")
st.title("✨ METAMATRIX DESTINY ✨")

# Sidebar Navigation
view_mode = st.sidebar.radio("Navigation", ["Matrix Generator", "Code Database Interface"])

if view_mode == "Matrix Generator":
    st.header("Matrix Calculation & Report Engine")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        day = st.number_input("Day of Birth", min_value=1, max_value=31, value=15)
    with col2:
        month = st.number_input("Month of Birth", min_value=1, max_value=12, value=8)
    with col3:
        year = st.number_input("Year of Birth", min_value=1900, max_value=2100, value=1990)
        
    if st.button("Calculate Matrix"):
        matrix_results = calculate_full_matrix(day, month, year)
        st.session_state['matrix_results'] = matrix_results
        
    if 'matrix_results' in st.session_state:
        res = st.session_state['matrix_results']
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.subheader("Core Energies")
            for k, v in res['core'].items():
                st.write(f"**{k.capitalize()}:** {v}")
                
        with c2:
            st.subheader("Ancestral Lines")
            for k, v in res['ancestral'].items():
                st.write(f"**{k}:** {v}")
                
            st.subheader("Destiny Purposes")
            for k, v in res['destiny'].items():
                st.write(f"**{k.capitalize()}:** {v}")
                
        with c3:
            st.subheader("Chakra Alignment")
            for k, v in res['chakras'].items():
                st.write(f"**{k}:** {v}")

        st.markdown("---")
        
        # Download PDF Button
        pdf_bytes = generate_full_pdf(res)
        st.download_button(
            label="📄 Download Complete Detailed PDF Report",
            data=pdf_bytes,
            file_name="MetaMatrix_Destiny_Full_Report.pdf",
            mime="application/pdf"
        )

elif view_mode == "Code Database Interface":
    st.header("Code Database Interface")
    
    if os.path.exists("codes.json"):
        with open("codes.json", "r") as f:
            codes_data = json.load(f)
        st.json(codes_data)
    else:
        st.info("codes.json file not found in current directory.")
    