import streamlit as st
import requests

URL = "https://job-assistant-production-386a.up.railway.app"
st.title("🎯 Job Assistant")
st.subheader("Upload your resume and paste a job description to find skill gaps")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=200)

if st.button("Analyze"):
    if resume_file and jd_text:
        with st.spinner("Analyzing..."):
            response = requests.post(
                f"{URL}/api/analyze",
                files={"resume": resume_file},
                data={"jd_text": jd_text},
            )
            result = response.json()

        st.subheader("Missing Skills")
        skills = result["missing_skills"]
        st.write(" | ".join([f"**{skill}**" for skill in skills]))

        st.subheader("Recommended Videos")
        for video in result["recommended_videos"]:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(video["thumbnail"])
                with col2:
                    st.markdown(f"**[{video['title']}]({video['url']})**")
                    st.caption(f"📺 {video['channel']} | 🎯 {video['skill']}")
    else:
        st.warning("Please upload a resume and paste a job description")
