import pytesseract
from PIL import Image
import pdfplumber
import spacy
import re
import streamlit as st

# Loading spaCy NER model
nlp = spacy.load("en_core_web_sm")

# OCR function for images
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# PDF text extraction function
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# NER-based entity extraction
def extract_entities(text):
    doc = nlp(text)
    entities = {'PERSON': [], 'DATE': [], 'GPE': [], 'ORG': []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

# Regex-based additional info extraction (contact & LinkedIn)
def extract_additional_info(text):
    contact_pattern = r'(\+?\d[\d\s\-]{8,}\d)'
    linkedin_pattern = r'(https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+)'

    contact_numbers = re.findall(contact_pattern, text)
    linkedin_links = re.findall(linkedin_pattern, text)

    return {
        'CONTACT': contact_numbers,
        'LINKEDIN': linkedin_links
    }

# -----------------------------
# 📄 Streamlit Web App
# -----------------------------
st.set_page_config(page_title="AutoDocFill", page_icon="📄")
st.title("📄 Automated Document Filler")

file = st.file_uploader("📤 Upload your file (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

extracted_text = ""
entities = {}

if file is not None:
    # Process uploaded file
    if file.type == "application/pdf":
        with open("temp.pdf", "wb") as f:
            f.write(file.read())
        extracted_text = extract_text_from_pdf("temp.pdf")
    else:
        with open("temp_img.png", "wb") as f:
            f.write(file.read())
        extracted_text = extract_text_from_image("temp_img.png")

    # Extracting entities using NER
    entities = extract_entities(extracted_text)

    # Extracting additional info using Regex
    additional_info = extract_additional_info(extracted_text)

    # Combining all into one dictionary
    entities.update(additional_info)

    if st.checkbox("Show extracted entities and details"):
        st.subheader("📝 Extracted Entities & Details:")
        st.json(entities)

# -----------------------------
# 📋 Form Section
# -----------------------------
st.subheader("📝 Application Form")

with st.form("autofill_form"):
    name_value = entities.get('PERSON', [])
    contact_value = entities.get('CONTACT', [])
    linkedin_value = entities.get('LINKEDIN', [])

    name = st.text_input("Full Name", value=name_value[0] if name_value else "")
    contact = st.text_input("Contact Number", value=contact_value[0] if contact_value else "")
    linkedin = st.text_input("LinkedIn Profile Link", value=linkedin_value[0] if linkedin_value else "")

    submit = st.form_submit_button("Submit")

    if submit:
        st.success("✅ Form submitted successfully!")
        st.write("### 📋 Submitted Data:")
        st.write(f"**Name:** {name}")
        st.write(f"**Contact Number:** {contact}")
        st.write(f"**LinkedIn Profile:** {linkedin}")

# End of App

