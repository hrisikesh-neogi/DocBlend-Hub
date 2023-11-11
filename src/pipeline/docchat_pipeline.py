import os
import pickle
import sys

import requests
from langchain import OpenAI
from langchain.schema import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

from src.exception import SummarizerException
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, CSVLoader
from src.entity.config_entity import ChatWithDocsConfig, VectorDbConfig
from langchain.chains import RetrievalQA
from src.logger import logging as lg


class DocChatPipeline:
    def __init__(self,
                 uploaded_doc: UploadedFile,
                 ):
        self.model = OpenAI()
        self.config = ChatWithDocsConfig()
        self.vectordb_config = VectorDbConfig()
        self.uploaded_doc = uploaded_doc

    def save_uploaded_doc(self):
        try:
            file_path = os.path.join(self.config.chat_with_docs_dir,
                                     self.uploaded_doc.name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(self.uploaded_doc.getvalue())

            return file_path
        except SummarizerException as e:
            lg.error(e)
            raise SummarizerException(e, sys)

    def load_docs(self, file_path: str):
        try:
            file_extension = self.uploaded_doc.name.split(".")[-1]
            if file_extension == "pdf":
                doc_loader = PyPDFLoader(file_path)
            elif file_extension == "csv":
                doc_loader = CSVLoader(file_path)

            else:
                raise Exception(f"File extension {file_extension} not supported")

            docs = doc_loader.load()
            return docs

        except Exception as e:
            raise SummarizerException(e, sys)

    def split_documents(self, docs: List[Document]):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )

            chunks = text_splitter.split_documents(docs)
            return chunks

        except SummarizerException as e:
            lg.error(e)
            raise SummarizerException(e, sys)

    def build_vectorstore(self, chunks: List[Document]):
        try:

            temp_embedding_file_name = self.uploaded_doc.name.split(".")[0]. \
                                           lower().replace(" ", "").strip() + \
                                       "_embedding"

            temp_embedding_store = os.path.join(
                self.vectordb_config.vector_db_dir,
                temp_embedding_file_name
            )

            os.makedirs(os.path.dirname(temp_embedding_store), exist_ok=True)
            vectorstore = Chroma.from_documents(chunks,
                                                embedding=OpenAIEmbeddings(),
                                                persist_directory=temp_embedding_store)

            # if not os.path.exists(temp_embedding_store):
            #     with open(temp_embedding_store, "wb") as store:
            #         pickle.dump(vectorstore, store)
            #         lg.info(f"Vector store saved to {temp_embedding_store}")
            # else:
            #     lg.info(f"Vector store already exists at {temp_embedding_store}")
            #     with open(temp_embedding_store, "rb") as store:
            #         vectorstore = pickle.load(store)

            return vectorstore
        except Exception as e:
            lg.error(e)
            raise SummarizerException(e, sys)

    def run(self):
        try:
            if self.uploaded_doc:
                saved_file_path = self.save_uploaded_doc()

                docs = self.load_docs(saved_file_path)
                chunks = self.split_documents(docs)
                vectorstore = self.build_vectorstore(chunks)

                qa_chain = RetrievalQA.from_chain_type(
                    retriever=vectorstore.as_retriever(),
                    llm=self.model,
                    chain_type="stuff"
                )

                return qa_chain


        except SummarizerException as e:
            lg.error(e)
            raise SummarizerException(e, sys)

        # try:
        #     self.model.load(self.config.chat_with_docs_dir)
        # except Exception as e:
        #     lg.error(e.message)
        #     raise SummarizerException(e, sys)


