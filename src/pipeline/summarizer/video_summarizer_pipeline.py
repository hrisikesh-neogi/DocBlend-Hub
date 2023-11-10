import os.path
import sys
from typing import List

from langchain.schema import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.pipeline.docchat_pipeline import DocChatPipeline
from src.exception import SummarizerException
from src.constant import *
from src.pipeline.summarizer.base_pipeline import BasePipeline
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter


class SummarizerPipeline(BasePipeline):
    video_url = None
    model = OpenAI()

    def load_transcript_as_docs(self) -> List[Document]:
        try:
            transcript_artifact = self.transcription_artifact()
            transcript_store_dir = transcript_artifact.transcript_store_dir
            transcript_file_ext = transcript_artifact.transcript_file_type

            loader = TextLoader(
                os.path.join(
                    transcript_store_dir,
                    TRANSCRIPTION_STORAGE_FILE_NAME + f".{transcript_file_ext}")
            )

            documents = loader.load()

            return documents

        except Exception as e:
            raise SummarizerException(e, sys)

    @staticmethod
    def get_map_reduce_chain(model: OpenAI):

        try:

            map_template = """The following is a set of documents containing a transcript of an youtube video.
            {docs}
            Based on this list of docs, please generate the summary of the transcripts.
            Helpful Answer:"""

            map_prompt = PromptTemplate.from_template(map_template)

            map_chain = LLMChain(llm=model, prompt=map_prompt)

            reduce_template = """The following is set of summaries of a transcripted video:
            {doc_summaries}
            Take these and distill it into a final, consolidated summary of that particular video transcript. 
            Helpful Answer:"""

            reduce_prompt = PromptTemplate.from_template(reduce_template)

            reduce_chain = LLMChain(llm=model, prompt=reduce_prompt)

            combine_documents_chain = StuffDocumentsChain(
                llm_chain=reduce_chain, document_variable_name="doc_summaries"
            )

            reduce_documents_chain = ReduceDocumentsChain(
                combine_documents_chain=combine_documents_chain,
                collapse_documents_chain=combine_documents_chain,
                token_max=4000,
            )

            map_reduce_chain = MapReduceDocumentsChain(
                llm_chain=map_chain,
                reduce_documents_chain=reduce_documents_chain,
                document_variable_name="docs",
                return_intermediate_steps=False,
            )

            return map_reduce_chain

        except Exception as e:
            raise SummarizerException(e, sys)

    def summarize(self):
        try:

            chain = SummarizerPipeline.get_map_reduce_chain(model=self.model)

            transcript_doc = self.load_transcript_as_docs()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

            transcript_docs = text_splitter.split_documents(transcript_doc)
            output = chain(transcript_docs)

            return output

        except Exception as e:
            raise SummarizerException(e, sys)

    @staticmethod
    def summarize_transcript(transcript: str):
        try:
            chain = SummarizerPipeline.get_map_reduce_chain(model=OpenAI())

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
            transcript_docs = text_splitter.create_documents([transcript])
            print("transcript docs", transcript_docs)
            output = chain(transcript_docs)

            return output

        except Exception as e:
            raise SummarizerException(e, sys)


    def summarize_pdf(self,uploaded_doc: UploadedFile):
        if uploaded_doc:
            doc_pipeline = DocChatPipeline(uploaded_doc=uploaded_doc)
            saved_file_path = doc_pipeline.save_uploaded_doc()

            docs = doc_pipeline.load_docs(saved_file_path)
            chunks = doc_pipeline.split_documents(docs)

            chain = SummarizerPipeline.get_map_reduce_chain(model=OpenAI())
            output = chain(chunks)
            return output




