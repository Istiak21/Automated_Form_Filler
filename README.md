# 📄 AutoDocFill

A Streamlit web application that reads text from uploaded images or PDF documents using OCR, extracts important details using NLP Named Entity Recognition (NER) and Regex, and auto-fills an application form on the web interface with those extracted details.

---

## 📌 Features

- 📄 Extract text from images (`.png`, `.jpg`, `.jpeg`) and PDFs.
- 🧠 Perform entity extraction using spaCy NER for:
  - Full Name
- 🔍 Extract additional details like:
  - 📱 Contact Numbers (via Regex)
  - 🔗 LinkedIn Profile URLs (via Regex)
- 📝 Auto-fill an application form on the same web page with the extracted information.
- ✅ Submit the form and display the filled details.

---

## 📦 Tech Stack

- **Python 3**
- **Streamlit** — for the web application interface.
- **pytesseract** — for image-based OCR.
- **pdfplumber** — for text extraction from PDF files.
- **spaCy** — for Named Entity Recognition (NER).
- **Regex** — for pattern-based extraction (contact numbers & LinkedIn links).

---

