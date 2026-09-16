from flask import Flask, render_template, request
import os
from google import genai

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def analyze_skill_gap(student_skills, target_role, job_description):
    if not client:
        return "Gemini API key is not configured."

    prompt = f"""
You are an AI Skill Gap Analysis Agent.

Student's current skills:
{student_skills}

Target job role:
{target_role}

Job description / required skills:
{job_description}

Analyze the student's skill gap.

Give the response in this format:

1. Current Skills
- List the skills the student already has.

2. Missing Skills
- List important skills required for the target role that the student does not have.

3. Skill Gap Analysis
- Briefly explain the major gaps.

4. Learning Priority
- Give the skills in the order the student should learn them.

5. Learning Roadmap
- Give a simple step-by-step roadmap.

6. Project Suggestions
- Suggest 2 or 3 projects that can help improve the missing skills.

7. Final Advice
- Give short practical advice for becoming job-ready.

Keep the explanation simple and suitable for a college student.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error while generating AI response: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        student_skills = request.form.get("student_skills", "")
        target_role = request.form.get("target_role", "")
        job_description = request.form.get("job_description", "")

        result = analyze_skill_gap(
            student_skills,
            target_role,
            job_description
        )

    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
