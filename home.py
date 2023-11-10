import streamlit as st
from src.pipeline.summarizer_pipeline import SummarizerPipeline
from langchain.llms import OpenAI


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
            summarizer = SummarizerPipeline(url)

            output = summarizer.summarize()

            if output:
                st.subheader("Summary of the Video")
                st.write(output["output_text"])
                st.success("Summarization Completed")

    def pdf_summarizer(self):
        st.subheader("PDF Summarizer")
        pdf_url = st.text_input("Enter PDF URL")
        if st.button("Summarize"):
            print("pdff")
            st.info("Summarizing te PDF...")
            st.write(pdf_url)
            # summarizer = SummarizerPipeline(url)
            #
            # output = summarizer.summarize()
            # st.write(output)



    def run(self):
        if self.document_type == "Youtube Video":
            self.youtube_summarizer()

        if self.document_type == "PDF":
            self.pdf_summarizer()


if __name__ == "__main__":
    Summarizer().run()
