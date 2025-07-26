import fileinput
import pickle
from PyPDF2 import PdfReader, PdfFileReader

from flask import Flask, request, render_template
import pickle
app = Flask(__name__)

# load model---------------------------------

rf_classifier_categorization = pickle.load(open('models/rf_classifier_categorization.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('models/tfidf_vectorizer_categorization.pkl', 'rb'))
rf_job_recommendation=pickle.load(open('models/rf_classifier_job_recommendation.pkl', 'rb'))
tfidf_job_recommendation=pickle.load(open('models/tfidf_vectorizer_job_recommendation.pkl', 'rb'))

#helper function ----------------------------

def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

import re;
def cleanResume(resumeText):
    resumeText = re.sub(r'http\S+\s*', ' ', resumeText)  # Remove URLs
    resumeText = re.sub(r'RT|cc', ' ', resumeText)       # Remove RT and cc
    resumeText = re.sub(r'#\S+', ' ', resumeText)        # Remove hashtags
    resumeText = re.sub(r'@\S+', ' ', resumeText)        # Remove mentions
    punctuation_pattern = r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
    resumeText = re.sub(punctuation_pattern, ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)  # Remove non-ASCII characters
    resumeText = re.sub(r'\s+', ' ', resumeText)         # Clean multiple spaces
    return resumeText.lower()                         # Convert to lowercase

def predict_category(resume_text):
    resume_text =  cleanResume(resume_text)
    resume_tfidf= tfidf_vectorizer.transform([resume_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category

def job_recommendation(resume_text):
    resume_text = cleanResume(resume_text)
    resume_tfidf= tfidf_job_recommendation.transform([resume_text])
    predicted_job_recommendation = rf_job_recommendation.predict(resume_tfidf)[0]
    return predicted_job_recommendation

import re

def extract_phone_numbers_standardized(text):
    # Regex to find phone number-like patterns (international, brackets, dashes, spaces)
    phone_pattern = re.compile(r'''
        (\+?\d{1,3}[\s\-\.])?           # Optional country code (+91, +1 etc)
        (\(?\d{3,4}\)?[\s\-\.]?)?       # Optional area code (3-4 digits)
        \d{3,4}                         # First part of number (3-4 digits)
        [\s\-\.]?                      # Separator
        \d{3,4}                        # Second part (3-4 digits)
    ''', re.VERBOSE)

    matches = phone_pattern.findall(text)
    results = []

    # Since `findall` returns tuples (because of groups), we extract full strings via finditer instead:
    for match in re.finditer(phone_pattern, text):
        phone = match.group()
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Take last 10 digits (to standardize)
        if len(digits) >= 10:
            return (digits[-10:])

    return None

def extract_first_email(text):
    # Regex pattern for matching most common email formats
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')

    match = email_pattern.search(text)
    if match:
        return match.group(0)
    return None  # Return None if no email found


# Example: Define a list of known skills (expand as needed)
skills_list = [
    'python', 'java', 'c++', 'sql', 'machine learning', 'deep learning',
    'project management', 'tableau', 'excel', 'powerpoint', 'linux',
    'data analysis', 'communication', 'git', 'tensorflow', 'keras', 'aws',
    'leadership', 'html', 'css', 'javascript'
]
def extract_skills(text, skills_list):
    # Lowercase and tokenize the text for matching
    text = text.lower()
    # Optional: improve with word boundaries, but keep simplicity for phrases
    found_skills = set()
    for skill in skills_list:
        # Use regex to find skill as a whole word or phrase, case-insensitive
        pattern = r'(?i)\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    return list(found_skills)

def extract_name_simple(text):
    # Consider first 2-3 lines for name extraction (usually name is at start)
    lines = text.strip().split('\n')
    for line in lines[:3]:  # first 3 lines
        # Extract capitalized words sequences (likely a name)
        match = re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b', line)
        if match:
            # Return the longest match (e.g. full name)
            name = max(match, key=len)
            return name
    return None


#routes ------------------------------------

@app.route("/")
def resume():
    return render_template('resume.html')


@app.route("/pred", methods=['POST'])
def predict():
    if 'resume' in request.files:
        file = request.files['resume']
        filename = file.filename
        print(f"Received file: {filename}")  # Debug log

        if filename.lower().endswith('.pdf'):
            text = pdf_to_text(file)
        elif filename.lower().endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return render_template('resume.html', message='Please upload a pdf or txt file')

        print(f"Extracted text snippet: {text[:100]}")  # Debug log
        predicted_category = predict_category(text)
        recommended_job_recommendation = job_recommendation(text)
        phone=extract_phone_numbers_standardized(text)
        skills=extract_skills(text, skills_list)
        name_simple=extract_name_simple(text)
        email=extract_first_email(text)
        print(f"Predicted category: {predicted_category}")  # Debug log

        return render_template('resume.html', predicted_category=predicted_category, predicted_job_recommendation=recommended_job_recommendation,phone=phone, extracted_skills=skills, name_simple=name_simple, email=email)

    return render_template('resume.html', message='No file uploaded')



if __name__ == "__main__":
    app.run(debug=True)