from flask import Blueprint, request, jsonify
import spacy
from .utils import extract_text_from_pdf, extract_gpa, score_skills, calculate_experience_years

main = Blueprint('main', __name__)

# Load the trained spaCy model once when the app starts
nlp = spacy.load("app/model/model-best")

@main.route('/process-pdf', methods=['POST'])
def process_pdf():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    text = extract_text_from_pdf(file)
    doc = nlp(text)

    # Calculate score (example implementation)
    gpa = extract_gpa(text)
    skills_score = 0
    experience_years = calculate_experience_years(text)
    
    for ent in doc.ents:
        if ent.label_ == "TECHNICAL SKILLS":
            skills_score += score_skills(ent.text, {"python": 2, "machine learning": 3, "java": 5, "sql": 2})
        elif ent.label_ == "NON TECHNICAL SKILLS":
            skills_score += score_skills(ent.text, {"leadership": 1, "teamwork": 1})
    
    total_score = skills_score + experience_years
    if gpa:
        total_score += 5 if 2.0 <= gpa <= 4.0 else 0

    return jsonify({
        "gpa": gpa,
        "skills_score": skills_score,
        "experience_years": experience_years,
        "total_score": total_score
    })
