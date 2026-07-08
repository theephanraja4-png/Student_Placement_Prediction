import streamlit as st
import joblib
import pandas as pd
import time

# =====================================
# Load Model
# =====================================

model = joblib.load("placement_model.pkl")

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="AI Career Readiness System",
    page_icon="🎓",
    layout="wide"
)

# =====================================
# Custom CSS
# =====================================

st.markdown("""
<style>

.main{
    background:#F5F7FB;
}

.block-container{
    padding-top:1.5rem;
}

.title{
    text-align:center;
    font-size:42px;
    color:#0D47A1;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.section{

    background:white;

    padding:20px;

    border-radius:15px;

    box-shadow:0px 2px 10px rgba(0,0,0,.15);

}

.

.metric-container{

    background:#EEF4FF;

    padding:18px;

    border-radius:12px;

}

.stButton>button{

width:100%;

height:55px;

font-size:18px;

font-weight:bold;

border-radius:12px;

background:#1565C0;

color:white;

}

.stButton>button:hover{

background:#0D47A1;

color:white;

}

</style>

""",unsafe_allow_html=True)

# =====================================
# Title
# =====================================

st.markdown("""

<p class="title">

🎓 AI Career Readiness & Placement Prediction System

</p>

<p class="subtitle">

Predict placement probability and analyze student career readiness.

</p>

""",unsafe_allow_html=True)

st.divider()

# =====================================
# Student Details
# =====================================

left,right=st.columns(2)

with left:

    st.subheader("🎓 Academic Details")

    cgpa=st.number_input(
        "CGPA",
        0.0,
        10.0,
        7.5
    )

    ssc=st.slider(
        "SSC Marks",
        0.0,
        100.0,
        80.0
    )

    hsc=st.slider(
        "HSC Marks",
        0.0,
        100.0,
        75.0
    )

    aptitude=st.slider(
        "Aptitude Test Score",
        0,
        100,
        70
    )

    softskills=st.slider(
        "Soft Skills Rating",
        1,
        10,
        7
    )

with right:

    st.subheader("💼 Career Profile")

    internships=st.number_input(
        "Internships",
        0,
        10,
        1
    )

    projects=st.number_input(
        "Projects",
        0,
        20,
        2
    )

    workshops=st.number_input(
        "Workshops / Certifications",
        0,
        20,
        2
    )

    extracurricular=st.selectbox(
        "Extracurricular Activities",
        ["No","Yes"]
    )

    training=st.selectbox(
        "Placement Training",
        ["No","Yes"]
    )

st.divider()
# =====================================
# Predict Button
# =====================================

predict = st.button(
    "🚀 Analyze Career Profile",
    use_container_width=True
)

# =====================================
# Prediction
# =====================================

if predict:

    input_df = pd.DataFrame({

        "CGPA":[cgpa],

        "Internships":[internships],

        "Projects":[projects],

        "Workshops/Certifications":[workshops],

        "AptitudeTestScore":[aptitude],

        "SoftSkillsRating":[softskills],

        "ExtracurricularActivities":[1 if extracurricular=="Yes" else 0],

        "PlacementTraining":[1 if training=="Yes" else 0],

        "SSC_Marks":[ssc],

        "HSC_Marks":[hsc]

    })

    with st.spinner("Analyzing Student Profile..."):

        time.sleep(2)

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    placement_probability = probability * 100

    # =====================================
    # Resume Strength
    # =====================================

    resume_score = 0

    resume_score += (cgpa / 10) * 25

    resume_score += min(projects,5) * 5

    resume_score += min(internships,3) * 10

    resume_score += min(workshops,5) * 3

    if training=="Yes":
        resume_score += 10

    resume_score = min(100, round(resume_score))

    # =====================================
    # Career Readiness
    # =====================================

    if placement_probability >= 80:

        readiness = "🟢 Excellent"

    elif placement_probability >= 60:

        readiness = "🟡 Moderate"

    else:

        readiness = "🔴 Needs Improvement"

    st.divider()

    st.subheader("📊 Career Analysis")

    c1,c2,c3 = st.columns(3)

    with c1:

        st.metric(

            "Placement Probability",

            f"{placement_probability:.2f}%"

        )

        st.progress(
            float(probability)
        )

    with c2:

        st.metric(

            "Resume Strength",

            f"{resume_score}/100"

        )

    with c3:

        st.metric(

            "Career Readiness",

            readiness

        )

    st.divider()

    # =====================================
    # Prediction Result
    # =====================================

    st.subheader("🎯 Prediction Result")

    if prediction == 1:

        st.success(f"""
### ✅ Likely to Get Placed

**Placement Probability:** {placement_probability:.2f}%

The student's academic performance and overall profile indicate a strong chance of getting placed.

Continue improving technical skills and prepare for interviews.
""")

    else:

        st.error(f"""
### ⚠ Placement Chances are Low

**Placement Probability:** {placement_probability:.2f}%

The student's current profile indicates a lower chance of placement.

Focus on improving projects, internships, aptitude, communication skills, and technical knowledge.
""")

    st.divider()

    # =====================================
    # Personalized Recommendations
    # =====================================

    st.subheader("💡 Personalized Career Recommendations")

    recommendations = []

    if cgpa < 7.5:
        recommendations.append("📚 Improve your CGPA to 7.5 or above.")

    if internships < 2:
        recommendations.append("💼 Complete at least one more internship.")

    if projects < 3:
        recommendations.append("💻 Build 2–3 real-world projects and upload them to GitHub.")

    if workshops < 3:
        recommendations.append("📜 Earn industry certifications (Python, Java, SQL, Cloud).")

    if aptitude < 70:
        recommendations.append("🧠 Practice aptitude and logical reasoning daily.")

    if softskills < 7:
        recommendations.append("🗣 Improve communication and presentation skills.")

    if training == "No":
        recommendations.append("🎯 Attend placement training and mock interviews.")

    if extracurricular == "No":
        recommendations.append("🏆 Participate in hackathons, coding contests, or technical clubs.")

    if len(recommendations) == 0:

        st.success("""
🎉 Excellent Profile!

Keep improving your coding skills, continue practicing DSA,
and prepare for company-specific interviews.
""")

    else:

        for item in recommendations:
            st.warning(item)

    st.divider()

    # =====================================
    # Skill Analysis
    # =====================================

    st.subheader("📈 Skill Analysis")

    technical = round((projects*10 + internships*15 + workshops*5)/2)
    technical = min(100, technical)

    communication = softskills * 10

    academics = round(((ssc + hsc)/2))

    aptitude_score = aptitude

    st.write("**Academic Performance**")
    st.progress(academics/100)

    st.write(f"{academics}%")

    st.write("**Technical Skills**")
    st.progress(technical/100)

    st.write(f"{technical}%")

    st.write("**Communication Skills**")
    st.progress(communication/100)

    st.write(f"{communication}%")

    st.write("**Aptitude**")
    st.progress(aptitude_score/100)

    st.write(f"{aptitude_score}%")

    st.divider()

    # =====================================
    # 30-Day Career Roadmap
    # =====================================

    st.subheader("🗓 30-Day Career Roadmap")

    st.info("""

### Week 1
✅ Improve Aptitude

✅ Practice Communication

### Week 2
✅ Learn SQL

✅ Revise DBMS & OOP

### Week 3
✅ Solve DSA Problems

✅ Build One Mini Project

### Week 4
✅ Resume Preparation

✅ Mock Interviews

✅ Apply for Companies

""")

    st.divider()

    # =====================================
    # Student Summary
    # =====================================

    st.subheader("📋 Career Summary")

    summary = pd.DataFrame({

        "Placement Probability":[f"{placement_probability:.2f}%"],

        "Resume Strength":[f"{resume_score}/100"],

        "Career Readiness":[readiness]

    })

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.caption(
"""
AI Career Readiness & Placement Prediction System

Built using Streamlit • Scikit-Learn • Machine Learning
"""
)