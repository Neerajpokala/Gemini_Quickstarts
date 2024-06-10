import streamlit as st
import google.generativeai as genai
import os
import time

os.environ['GOOGLE_API_KEY'] = 'YOUR_GOOGLE_API_KEY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

st.title("Audio Summarization with Google Generative AI")

uploaded_file = st.file_uploader("Upload an audio file", type=['mp3', 'wav'])

if uploaded_file is not None:
    file_path = "uploaded_audio.mp3"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(file_path)

    generate_summary = st.button("Generate Summary")

    if generate_summary:
        def upload_file_to_google(file_path):
            try:
                with st.spinner('Uploading file...'):
                    response = genai.upload_file(path=file_path)
                return response
            except Exception as e:
                st.error(f"Failed to upload file: {e}")
                return None

        uploaded_file_response = upload_file_to_google(file_path)

        if uploaded_file_response:
            st.success("File uploaded successfully to Google Generative AI")

            prompt = "Listen carefully to the following audio file. Provide a brief summary."
            max_retries = 5  # Maximum number of retries
            retry_delay = 10  # Delay in seconds between retries

            for retry in range(max_retries):
                try:
                    with st.spinner('Generating summary...'):
                        model = genai.GenerativeModel('models/gemini-1.5-flash')
                        response = model.generate_content([prompt, uploaded_file_response])
                    st.success("Summary generated successfully")
                    st.markdown(f"**Summary:**\n\n{response.text}")
                    break
                except Exception as e:
                    if retry == max_retries - 1:
                        st.error(f"Error generating content: {e}")
                        st.exception(e)
                    else:
                        st.warning(f"Error generating content: {e}. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)

        else:
            st.error("Failed to upload file to Google Generative AI")

else:
    st.info("Please upload an audio file to get started.")
