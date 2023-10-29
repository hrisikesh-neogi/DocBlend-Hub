import streamlit as st
import urllib.request
import moviepy.editor as mp
import pandas as pd

from src.pipeline.summarizer_pipeline import SummarizerPipeline


# Function to summarize a video
def summarize_video(video_url):
    st.write("Video Summarization is selected.")
    st.write("Summarizing the video...")
    pipeline = SummarizerPipeline(video_url)
    summary = pipeline.summarize()

    st.write("Video summarization completed.")
    st.write(summary["output_text"])







# Function to process a PDF
# def process_pdf(pdf_url):
#     st.write("PDF Processing is selected.")
#     st.write("Processing the PDF...")
#
#     # Download the PDF from the URL
#     pdf_filename = "document.pdf"
#     urllib.request.urlretrieve(pdf_url, pdf_filename)
#
#     # Extract text from the PDF and display it
#     doc = fitz.open(pdf_filename)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     st.write(text)


# Function to process a CSV
# def process_csv(csv_url):
#     st.write("CSV Processing is selected.")
#     st.write("Processing the CSV...")
#
#     # Download the CSV from the URL
#     csv_data = pd.read_csv(csv_url)
#
#     # Display the CSV data
#     st.dataframe(csv_data)


# Streamlit app
st.title("Document Summarizer App")

# URL input
url = st.text_input("Enter the URL:")

# Dropdown menu
task = st.selectbox("Select a task:", ["Video Summarization", "PDF Processing", "CSV Processing"])

if st.button("Process"):
    st.info(f"Processing {task}... This may take some time.")
    if task == "Video Summarization":
        summarize_video(url)
    # elif task == "PDF Processing":
    #     process_pdf(url)
    # elif task == "CSV Processing":
    #     process_csv(url)
    st.success(f"{task} processing completed.")
