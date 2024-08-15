# Importing all necessary libraries
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from collections import Counter
import matplotlib.pyplot as plt
import io

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

def calculate_keyword_density(text):
    words = text.split()
    word_count = Counter(words)
    total_words = len(words)
    density = {word: (count / total_words) * 100 for word, count in word_count.items()}
    return density

def extract_skills(text):
    skills = ['Python', 'SQL', 'Java', 'C++', 'JavaScript', 'R', 'Tableau', 'Power BI']
    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return found_skills

def calculate_resume_score(jd_match, missing_keywords, profile_summary):
    score = (float(jd_match.replace('%', '')) / 100) * 50
    if not missing_keywords:
        score += 20
    if profile_summary:
        score += 30
    return min(score, 100)

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and provide 
the best assistance for improving the resumes. Assign the percentage matching based 
on JD and identify the missing keywords with high accuracy.
Also, provide specific areas of improvement for the resume tailored to the job description.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[], "Profile Summary":"", "Areas of Improvement":[]}}
"""

# Streamlit app
st.set_page_config(page_title="Smart ATS", page_icon=":robot:", layout="wide")

# Apply custom styles
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f4f9f9;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #e9f5f5;
    }
    .title {
        color: #009688;
        font-size: 2rem;
        font-weight: bold;
    }
    .text-area, .stButton>button {
        background-color: #00bcd4;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0097a7;
    }
    .subheader {
        color: #00796b;
    }
    .stWrite {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Use custom HTML title
st.markdown('<h1 class="title">Smart ATS</h1>', unsafe_allow_html=True)

st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description", key="job_description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if 'report' not in st.session_state:
    st.session_state.report = None

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Parse the response
        try:
            result = json.loads(response)
            jd_match = result.get("JD Match", "N/A")
            missing_keywords = result.get("MissingKeywords", [])
            profile_summary = result.get("Profile Summary", "")
            areas_of_improvement = result.get("Areas of Improvement", [])

            # Save the report to session state
            st.session_state.report = {
                'jd_match': jd_match,
                'missing_keywords': missing_keywords,
                'profile_summary': profile_summary,
                'areas_of_improvement': areas_of_improvement,
                'text': text
            }

        except json.JSONDecodeError:
            st.error("Error decoding response. Please ensure the response is in valid JSON format.")

# Display the report if available
if st.session_state.report:
    report = st.session_state.report
    jd_match = report['jd_match']
    missing_keywords = report['missing_keywords']
    profile_summary = report['profile_summary']
    areas_of_improvement = report['areas_of_improvement']
    text = report['text']

    st.subheader("Evaluation Result")

    # Display JD Match
    st.markdown(f'<div class="stWrite"><strong>JD Match:</strong> {jd_match}</div>', unsafe_allow_html=True)

    # Display Missing Keywords in a single line
    st.markdown(f'<div class="stWrite"><strong>Missing Keywords:</strong> {", ".join(missing_keywords) if missing_keywords else "None"}</div>', unsafe_allow_html=True)

    # Display Profile Summary as bullet points
    st.markdown(f'<div class="stWrite"><strong>Profile Summary:</strong></div>', unsafe_allow_html=True)
    profile_summary_points = profile_summary.split('\n')
    for point in profile_summary_points:
        if point.strip():
            st.markdown(f'<div class="stWrite">• {point.strip()}</div>', unsafe_allow_html=True)

    # Display Areas of Improvement as bullet points
    st.markdown(f'<div class="stWrite"><strong>Areas of Improvement:</strong></div>', unsafe_allow_html=True)
    if areas_of_improvement:
        for point in areas_of_improvement:
            st.markdown(f'<div class="stWrite">• {point.strip()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="stWrite">• None</div>', unsafe_allow_html=True)

    # Keyword Density Analysis
    density = calculate_keyword_density(text)
    st.subheader("Keyword Density Analysis")
    
    # Limit number of keywords displayed
    top_keywords = dict(sorted(density.items(), key=lambda item: item[1], reverse=True)[:10])
    
    # Create and display bar chart for top keywords
    fig, ax = plt.subplots(figsize=(6, 6))  # Set size to 600x600 pixels
    bars = ax.barh(list(top_keywords.keys()), list(top_keywords.values()), color='#00bcd4')
    ax.set_xlabel('Density (%)')
    ax.set_title('Top 10 Keywords by Density')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest density on top

    # Add value annotations to bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.2f}%', 
                va='center', ha='left', color='black', fontsize=10)

    # Convert plot to PNG image and display
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    st.image(buf, use_column_width=False, width=600)
    plt.close()

    # Skill Matching
    skills_found = extract_skills(text)
    st.subheader("Skill Matching")
    st.write(f"Skills found in resume: {', '.join(skills_found) if skills_found else 'None'}")

    # Resume Scoring
    score = calculate_resume_score(jd_match, missing_keywords, profile_summary)
    st.subheader("Resume Scoring")
    
    # Create and display donut chart with specific size
    fig, ax = plt.subplots(figsize=(5, 5))  # Set size to 500x500 pixels
    sizes = [score, 100 - score]
    labels = ['Resume Score', 'Remaining']
    colors = ['#00bcd4', '#e0e0e0']
    wedges, texts = ax.pie(sizes, labels=labels, colors=colors, startangle=90, wedgeprops=dict(width=0.3))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add score percentage annotation
    for i, text in enumerate(texts):
        text.set_text(f'{sizes[i]:.1f}%')

    # Convert plot to PNG image and display
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    st.image(buf, use_column_width=False, width=600)
    plt.close()

    # Feedback section
    st.subheader("Feedback")
    feedback = st.text_area("Provide feedback for further improvements")
    feedback_submitted = st.button("Submit Feedback")
    if feedback_submitted:
        if feedback:
            # Handle feedback submission logic
            st.success("Thank you for your feedback!")
        else:
            st.error("Please enter your feedback before submitting.")
