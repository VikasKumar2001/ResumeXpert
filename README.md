🤖 ResumeXpert: AI-Powered Resume Screening & Job Recommendation
ResumeXpert is an intelligent, end-to-end system for automating resume screening, categorization, and job role recommendation. Built using Python and machine learning, it provides fast, accurate insights into candidate profiles—perfect for recruiters, HR professionals, and job seekers.

🚀 Features
🔎 Resume Categorization: Instantly classifies resumes into job-relevant domains.

🧭 Job Role Recommendation: Suggests suitable job roles based on resume content.

📄 Resume Parsing: Automatically extracts name, phone, email, and skills from PDF or TXT files.

📈 ML Models with Confidence Scores: Robust predictions powered by trained ML models with top-N confidence scores.

📂 Supports PDF and TXT Resumes: Upload resumes in multiple formats.

⚡ Fast, User-Friendly Web App: Clean interface built with Flask and Jinja2.

📁 Project Structure
```
ResumeXpert/
├── app.py                          # Main Flask application
├── requirements.txt                # List of dependencies
├── models/                         # Trained ML models
│   ├── rf_classifier_categorization.pkl
│   ├── tfidf_vectorizer_categorization.pkl
│   ├── rf_classifier_job_recommendation.pkl
│   └── tfidf_vectorizer_job_recommendation.pkl
├── templates/
│   └── resume.html                 # HTML template (UI)
├── static/                         # Static files (CSS, JS, etc.)
├── README.md                       # This file
└── .gitignore                      # Ignore virtualenv, cache files, etc.
```
🛠️ Technologies Used
Python 3.x

Flask – Web application framework

scikit-learn – Machine Learning models

PyPDF2 – PDF parsing

Jinja2 – HTML templating

HTML5 & CSS3 – Frontend UI

(Optional) spaCy/pyresparser – For advanced NLP-based parsing

💻 Demo Screenshot
<!-- Replace with your screenshot or GIF -->

🖥️ How to Run
1. Clone the Repository
```
git clone https://github.com/yourusername/ResumeXpert.git
cd ResumeXpert
```
2. Create and Activate Virtual Environment (Recommended)
```
# Create
python -m venv venv
```
# Activate
# On Windows:
```
venv\Scripts\activate
```
# On macOS/Linux:
```
source venv/bin/activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. Run the Application
```
python app.py
Then open your browser at:
http://127.0.0.1:5000
```
📋 Example Output
```
Category: Engineering  
Recommended Job Role: Data Analyst
Extracted Information:
Name: John Doe  
Phone: 9876543210  
Email: john.doe@email.com  
Skills: Python, SQL, Tableau
```
🌐 Deployment
Want to deploy it on Heroku, AWS, or Render?
Follow instructions in the README_Deployment.md (coming soon) for easy cloud deployment.

📝 Citation
Vikas Kumar, ResumeXpert: AI-Powered Resume Screening and Job Recommendation, July 2025.
