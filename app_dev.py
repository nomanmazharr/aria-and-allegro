import streamlit as st
from model import get_model_response

# Set the title of the app
st.title("Rescure: Be the Help Until Help Arrives")

# Text input for user prompt
prompt = st.text_input("Enter your prompt:", "")

# File uploader for images
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Button to submit the inputs
if st.button("Submit"):
    # Check if there's a prompt or images uploaded
    if prompt or uploaded_files:
        # Get the model response
        response = get_model_response(prompt, uploaded_files)
        
        if isinstance(response, dict) and "error" in response:
            st.error(response["error"])
        else:
            st.write("Model Response:")
            st.write("Instructions:", response.get('instructions', 'Instructions not provided.'))
            video_prompt = response.get('video_prompt', 'Video prompt not provided.')
            st.write("Video Prompt:", video_prompt)
            # st.write(response)
    else:
        st.error("Please provide either a prompt or upload images.")

# Optional: Add a footer or additional info about the app
st.markdown("---")
st.markdown("### About")
st.markdown("This app allows you to analyze images and text using an AI model.")
