import streamlit as st
import joblib
import pandas as pd
import time

# ------------------------
# Load Model
# ------------------------

model = joblib.load("placement_model.pkl")

# ------------------------
# Page Configuration
# ------------------------

st.set_page_config(
    page_title="Student Placement Prediction",
    page_icon="🎓",
    layout="wide"
)

# ------------------------
# CSS
# ------------------------

st.markdown("""
<style>

.main{
    background:#F8FAFF;
}

.block-container{
    padding-top:1rem;
}

.title{
    text-align:center;
    color:#1565C0;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.stButton>button{

width:100%;

height:55px;

background:#1565C0;

color:white;

font-size:18px;

font-weight:bold;

border-radius:12px;

}

.stButton>button:hover{

background:#0D47A1;

color:white;

}

div[data-testid="metric-container"]{

background:#EEF4FF;

padding:15px;

border-radius:12px;

box-shadow:0px 2px 8px rgba(0,0,0,.15);

}

</style>
""",unsafe_allow_html=True)

# ------------------------
# Sidebar
# ------------------------

st.sidebar.title("🎓 Student Placement")

st.sidebar.markdown("---")

st.sidebar.write("### Algorithm")

st.sidebar.success("Logistic Regression")

st.sidebar.write("### Prediction")

st.sidebar.info("Placed / Not Placed")

st.sidebar.write("### Features")

st.sidebar.info("10 Input Parameters")

st.sidebar.markdown("---")

st.sidebar.write("Enter student details and click Predict.")

# ------------------------
# Heading
# ------------------------

st.markdown(
"""
<p class='title'>
🎓 Student Placement Prediction
</p>

<p class='subtitle'>
Predict whether a student is likely to be placed based on academic performance and skills.
</p>
""",
unsafe_allow_html=True
)

st.divider()

# ------------------------
# Inputs
# ------------------------

col1,col2=st.columns(2)

with col1:

    cgpa=st.number_input(
        "CGPA",
        0.0,
        10.0,
        7.5
    )

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

    aptitude=st.slider(
        "Aptitude Test Score",
        0,
        100,
        70
    )

with col2:

    softskills=st.slider(
        "Soft Skills Rating",
        1,
        10,
        7
    )

    extracurricular=st.selectbox(
        "Extracurricular Activities",
        ["No","Yes"]
    )

    training=st.selectbox(
        "Placement Training",
        ["No","Yes"]
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

st.divider()
# ------------------------
# Prediction
# ------------------------

if st.button("🔍 Predict Placement"):

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

    with st.spinner("Analyzing student profile..."):

        time.sleep(1.5)

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)

    confidence = probability.max()*100

    st.divider()

    c1,c2 = st.columns(2)

    with c1:

        if prediction==1:

            st.balloons()

            st.metric(
                "Prediction",
                "Placed ✅"
            )

            st.success(
                "The student is likely to be placed."
            )

        else:

            st.metric(
                "Prediction",
                "Not Placed ❌"
            )

            st.error(
                "The student is less likely to be placed."
            )

    with c2:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.progress(int(confidence))

    st.subheader("Input Summary")

    st.dataframe(
        input_df,
        use_container_width=True
    )

    st.subheader("Career Suggestions")

    if prediction==1:

        st.success("""
✔ Maintain your CGPA

✔ Continue practicing coding

✔ Prepare for technical interviews

✔ Improve communication skills

✔ Keep building projects
""")

    else:

        if cgpa < 7:

            st.warning("Increase your CGPA.")

        if internships < 2:

            st.warning("Complete more internships.")

        if projects < 2:

            st.warning("Build additional projects.")

        if aptitude < 70:

            st.warning("Practice aptitude regularly.")

        if training=="No":

            st.warning("Attend placement training.")

        st.info("""
Focus on improving technical skills,
problem solving and communication.
""")

st.divider()

st.caption("Student Placement Prediction")