from flask import Flask, render_template, request
import os
from google import genai

app = Flask(__name__)

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_skill_gap(student_skills, target_role, job_description):
    """
    AI Skill Gap Agent
    Compares the student's current skills with the
    skills required for the target job role.
    """

    if not client:
        return """
Gemini API key is not configured.

Please set the environment variable:

GEMINI_API_KEY

If you are using Render, add it under:
Environment Variables → GEMINI_API_KEY
"""

    prompt = f"""
You are an AI Skill Gap Analysis Agent for college students.

Analyze the student's current skills against the requirements
of their target job.

STUDENT'S CURRENT SKILLS:
{student_skills}

TARGET JOB ROLE:
{target_role}

JOB DESCRIPTION / REQUIRED SKILLS:
{job_description}

Provide the analysis using the following format:

1. CURRENT SKILLS
List the skills the student already has.

2. MATCHING SKILLS
List the skills that match the target role.

3. MISSING SKILLS
List the important skills required for the role that the student
does not currently mention.

4. SKILL GAP ANALYSIS
Explain the major gaps in simple language.

5. LEARNING PRIORITY
Divide the missing skills into:
- High Priority
- Medium Priority
- Low Priority

6. LEARNING ROADMAP
Give a simple step-by-step learning roadmap.

7. PROJECT SUGGESTIONS
Suggest 3 practical projects that can help the student
develop the missing skills.

8. JOB READINESS
Give a brief explanation of what the student should improve
before applying for the target role.

Keep the response simple, clear, and suitable for a college student.
Do not invent skills that the student has not mentioned.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text

        return "The AI did not return a response. Please try again."

    except Exception as e:
        return f"""
Error while generating AI response:

{str(e)}

Please check:
1. GEMINI_API_KEY is correct.
2. The API key is active.
3. Internet connection is available.
4. The Gemini model is available for your API key.
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        student_skills = request.form.get(
            "student_skills", ""
        ).strip()

        target_role = request.form.get(
            "target_role", ""
        ).strip()

        job_description = request.form.get(
            "job_description", ""
        ).strip()

        # Check empty fields
        if not student_skills or not target_role or not job_description:

            result = """
Please fill in all three fields:

1. Your Current Skills
2. Target Job Role
3. Job Description / Required Skills
"""

        else:

            result = analyze_skill_gap(
                student_skills,
                target_role,
                job_description
            )

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    # Render provides the PORT environment variable.
    # Local testing uses port 5000.
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
