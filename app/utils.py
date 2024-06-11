import pdfplumber
import re
from datetime import datetime

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_gpa(text):
    """Extract GPA using regex from provided text."""
    gpa_pattern = r"\b(?:GPA|CGPA)[:\s]*([\d\.]+)\b"
    match = re.search(gpa_pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def score_skills(entity_text, skills_dict):
    """Calculate the score for given skills in a case-insensitive manner."""
    entity_text_lower = entity_text.lower()
    return sum(points for skill, points in skills_dict.items() if skill.lower() in entity_text_lower)

def calculate_experience_years(text):
    """Calculate total experience by finding all years mentioned in the text."""
    current_year = datetime.now().year
    years = re.findall(r'\b(20\d{2})\b', text)
    years = list(map(int, years))
    if not years:
        return 0
    years.sort()
    total_experience = max(years) - min(years) + 1
    return total_experience
