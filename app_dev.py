import streamlit as st
from model import get_model_response

# Set the title of the app
st.title("AI Image and Text Analysis App")

# Text input for user prompt
prompt = st.text_input("Enter your prompt:", "")

# File uploader for images
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Text input for image-specific prompt (if needed)
image_prompt = st.text_input("Enter an image-specific prompt (optional):", "")

# Button to submit the inputs
if st.button("Submit"):
    # Check if there's a prompt or images uploaded
    if prompt or uploaded_files:
        # Get the model response
        response = get_model_response(prompt, image_prompt, uploaded_files)
        st.write("Model Response:")
        st.write(response)  # Display the response from the model
    else:
        st.error("Please provide either a prompt or upload images.")

# Optional: Add a footer or additional info about the app
st.markdown("---")
st.markdown("### About")
st.markdown("This app allows you to analyze images and text using an AI model.")
