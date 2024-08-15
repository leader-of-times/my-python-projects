
---

# Smart ATS - Resume Evaluation System

## Overview

**Smart ATS** is a web application designed to evaluate and enhance resumes based on a provided job description. This application uses advanced AI technology to analyze resumes, match them against job descriptions, and provide detailed feedback on improvements. It also includes keyword density analysis, skill matching, and a resume scoring system to help users optimize their resumes for better chances in a competitive job market.

## Features

- **Job Description Analysis**: Input a job description to evaluate how well a resume matches it.
- **Resume Upload**: Upload a PDF resume for analysis.
- **AI-Powered Evaluation**: Get a detailed evaluation of your resume from an AI model, including JD match percentage, missing keywords, profile summary, and areas of improvement.
- **Keyword Density Analysis**: View a bar chart showing the density of keywords in your resume.
- **Skill Matching**: Identify relevant skills present in the resume.
- **Resume Scoring**: See a donut chart depicting the overall score of your resume.
- **Feedback Section**: Provide feedback on the evaluation for further improvements.

## Installation

To run this application locally, you need to set up your environment and install the required dependencies.

### Prerequisites

- Python 3.8 or higher
- Streamlit
- `google-generativeai` (for AI model)
- `PyPDF2` (for PDF processing)
- `matplotlib` (for plotting)
- `python-dotenv` (for environment variable management)

### Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**

   Create a `.env` file in the project root directory and add your Google Generative AI API key:

   ```
   GOOGLE_API_KEY=<your-api-key>
   ```

5. **Run the Application**

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Navigate to the Application**

   Open your web browser and go to `http://localhost:8501` to access the Smart ATS application.

2. **Input Job Description**

   Paste the job description into the provided text area.

3. **Upload Resume**

   Upload your resume in PDF format using the file uploader.

4. **Submit for Evaluation**

   Click the "Submit" button to analyze your resume.

5. **View Results**

   After submission, you will see:

   - JD Match percentage
   - Missing Keywords
   - Profile Summary (formatted as bullet points)
   - Areas of Improvement (formatted as bullet points)
   - Keyword Density Analysis (bar chart)
   - Skill Matching
   - Resume Scoring (donut chart)

6. **Provide Feedback**

   Use the feedback section to submit your comments and suggestions.

## Code Explanation

- **`app.py`**: The main Streamlit application script. It includes:
  - Input handling for job descriptions and resume uploads.
  - API interaction with Google Generative AI for resume evaluation.
  - Data processing functions for keyword density, skill extraction, and resume scoring.
  - Visualization components for keyword density and resume scoring.

- **`requirements.txt`**: Contains all the Python packages required for the project.

- **`.env`**: Used for storing sensitive environment variables like API keys.

## Contributing

Contributions to this project are welcome! If you have suggestions or improvements, please create a pull request or open an issue.

## Contact

For questions or support, please contact:

- [Mohammad Noufal](mailto:mohammadnoufalctr@gmail.com)

---
