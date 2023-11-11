import streamlit as st
from src.pipeline.summarizer.video_summarizer_pipeline import SummarizerPipeline
from src.pipeline.summarizer.pdf_summarizer_pipeline import PDFSummarizerPipeline

class Summarizer:
    st.set_page_config(
        page_title="Summarizer",
        page_icon="🤖",
        layout="centered",
        # menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        #             'Report a bug': "https://www.extremelycoolapp.com/bug",
        #             'About': "# This is a header. This is an *extremely* cool app!"}

    )

    st.title("Summarizer")
    document_type = st.sidebar.selectbox("Document Type", ["Youtube Video", "PDF"])

    def youtube_summarizer(self):
        st.subheader("Youtube Video Summarizer")
        url = st.text_input("Enter Youtube Video URL")
        if st.button("Summarize"):
            print(url)
            st.info("Summarizing...")
            summarizer = SummarizerPipeline()
            summarizer.video_url = url

            output = summarizer.summarize()

            if output:
                st.subheader("Summary of the Video")
                st.write(output["output_text"])
                st.success("Summarization Completed")

            return output

    def pdf_summarizer(self):
        st.subheader("PDF Summarizer")
        with st.sidebar:
            pdf_file = st.file_uploader("Upload the PDF")


        if st.button("Summarize"):
            print("pdff")
            st.info("Summarizing te PDF...")
            pipeline = PDFSummarizerPipeline()
            output = pipeline.summarize_pdf(pdf_file)
            st.write(output["output_text"])
            # summarizer = SummarizerPipeline(url)
            #
            # output = summarizer.summarize()
            # st.write(output)

    def run(self):
        output = None
        if self.document_type == "Youtube Video":

            output = self.youtube_summarizer()

        if self.document_type == "PDF":
            self.pdf_summarizer()

        st.session_state["summary"] = output


if __name__ == "__main__":
    if "transcripts" not in st.session_state:
        Summarizer().run()
    else:
        transcript_selector = st.selectbox("Do you wanna summarize the video that you generated the transcript of?",
                                           ["Yes", "No"])
        if transcript_selector == "Yes":
            transcript = st.session_state["transcripts"]
            st.markdown(
                f"""
                ### Your transcript was 
                `{transcript}`
                
                """
            )
            output = SummarizerPipeline().summarize_transcript(transcript)
            if output:
                st.subheader("Summary of the Transcript")
                st.write(output["output_text"])
        if transcript_selector == "No":
            Summarizer().run()
