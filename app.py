# %%
import streamlit as st
from google import genai
from google.genai import types
import os

# %%
# To run this code, make sure to install the following dependencies:
# pip install google-genai streamlit

# Load the API key from a separate `apikey.py` file
from apikey import google_gemini_api_key

# %%
def generate_blog(title, keywords, num_words):
    # Initialize the client
    client = genai.Client(api_key=google_gemini_api_key)

    # Model to use
    model = "gemini-2.0-flash-lite"

    # Prepare the input content
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
Title: {title}
Word Limit: {num_words}
Keywords: {keywords}
Tone: informative, persuasive
Audience: general public, students
"""),
            ],
        )
    ]

    # Configuration for generating content
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    # Generate content stream
    blog_content = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        blog_content += chunk.text

    return blog_content

# %%
# Streamlit page settings
st.set_page_config(layout="wide")

# Title of the application
st.title("BLOG-FROG: YOUR PERSONAL AI BLOGGING COMPANION")
st.subheader("Express your thoughts with the help of AI. \nREMEMBER: IT'S you, just better!")

# %%
# Sidebar for user inputs
with st.sidebar:
    st.title("INPUT YOUR BLOG PARAMETERS")
    st.subheader("Input the details about your blog you want to generate.")

    # User input fields
    blog_title = st.text_input("Blog Title")
    keywords = st.text_area("Keywords (comma-separated)")
    num_words = st.slider("Number of words", min_value=100, max_value=1500, step=100)

    # Button to generate the blog
    submit_button = st.button("Generate Blog")

# %%
# Main content
blog = ""

if submit_button:
    if blog_title.strip() == "" or keywords.strip() == "":
        st.error("Please fill in both the Blog Title and Keywords.")
    else:
        # Generate the blog using the Google GenAI API
        with st.spinner("Generating your blog..."):
            try:
                blog = generate_blog(blog_title, keywords, num_words)
                st.success("Your blog has been generated successfully!")
                st.write(blog)
            except Exception as e:
                st.error(f"An error occurred: {e}")
# %%
