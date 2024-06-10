import streamlit as st
import google.generativeai as genai
import os
import tempfile

# Set up Google Generative AI key
os.environ['GOOGLE_API_KEY'] = 'YOUR_GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

st.title("Video Analysis with Google Generative AI")

video_file = st.file_uploader("Upload a video file", type=["mp4", "mpeg", "mov", "avi", "flv", "mpg", "webm", "wmv", "3gpp"])

if video_file is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
    temp_file.close()

    st.write("Uploading video file...")
    uploaded_file = genai.upload_file(path=temp_file.name, mime_type=video_file.type)

    prompt = "Describe this video."
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    st.write("Making LLM inference request...")
    try:
        response = model.generate_content([prompt, uploaded_file])
    except Exception as e:
        st.exception(e)
    st.write(response.text)
