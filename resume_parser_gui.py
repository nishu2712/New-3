
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import docx2txt
import spacy
from pdfminer.high_level import extract_text

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from file
def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    else:
        return ""

# Function to extract name using NLP
def extract_name(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names[0] if names else "Not found"

# Extract email
def extract_email(text):
    match = re.search(r'\b[\w.-]+?@\w+?\.\w+?\b', text)
    return match.group(0) if match else "Not found"

# Extract phone number
def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-().]{8,15}\d', text)
    return match.group(0) if match else "Not found"

# Extract skills
def extract_skills(text):
    SKILLS = ['python', 'java', 'c++', 'machine learning', 'deep learning',
              'nlp', 'sql', 'html', 'css', 'javascript', 'pandas', 'numpy']
    text = text.lower()
    return [skill for skill in SKILLS if skill in text]

# Process resume
def process_resume(file_path):
    text = extract_text_from_file(file_path)
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    return f"""
    ✅ Resume Parsed Successfully!

    👤 Name: {name}
    📧 Email: {email}
    📞 Phone: {phone}
    💼 Skills: {', '.join(skills) if skills else 'Not found'}
    """

# GUI App
def upload_file():
    file_path = filedialog.askopenfilename(
        title="Select Resume File",
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")]
    )
    if file_path:
        try:
            output = process_resume(file_path)
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{e}")

# Set up GUI
app = tk.Tk()
app.title("Resume Parser - NLP Based")
app.geometry("600x400")
app.resizable(False, False)

title_label = tk.Label(app, text="📄 Upload Resume to Parse", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

upload_btn = tk.Button(app, text="Upload Resume", command=upload_file, font=("Arial", 12), bg="#4CAF50", fg="white")
upload_btn.pack(pady=10)

text_box = tk.Text(app, height=15, width=70, font=("Arial", 10))
text_box.pack(padx=10, pady=10)

app.mainloop()
