import pandas as pd

from src.pipeline.transcript_pipeline import TranscriptPipeline
import streamlit as st

st.set_page_config(layout="wide")


class Transcript:
    video_url = st.text_input("The Youtube video url")

    def generate_transcript(self):
        return_timestamp = st.selectbox("Return Timestamp", [True, False])
        if self.video_url and \
                st.button("Generate Transcript"):
            st.subheader("Generate Transcript")
            st.write("Please wait while we generate the transcript...")
            st.write("This might take a while depending on the length of the video")
            pipeline = TranscriptPipeline()
            pipeline.video_url = self.video_url 
            print(type(return_timestamp))
            transcripts = pipeline.get_transcripts(return_timestamp)
            if isinstance(transcripts, pd.DataFrame):
                st.dataframe(transcripts)
            else:
                st.subheader("Here's The Transcript")
                st.write(transcripts)

            st.session_state["transcripts"] = transcripts

            # return transcripts


if __name__ == "__main__":
    st.title("Transcript Summarizer")
    st.write("This is an application for summarizing the transcripts of a youtube video")
    st.write("Please enter the url of the youtube video")
    st.write("Please wait while we generate the transcript...")
    st.write("This might take a while depending on the length of the video")


    with st.spinner("Generating transcript"):

        transcript = Transcript()
        transcript.generate_transcript()
