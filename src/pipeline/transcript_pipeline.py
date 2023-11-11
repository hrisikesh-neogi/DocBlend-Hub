import os
import sys
import pandas as pd

from langchain import OpenAI

from src.constant import TRANSCRIPTION_STORAGE_FILE_NAME
from src.pipeline.summarizer.base_pipeline import BasePipeline
from src.exception import SummarizerException


class TranscriptPipeline(BasePipeline):
    video_url = None
    model = OpenAI()


    def get_transcripts(self, return_timestamp: bool = False):
        try:

            transcript_artifact = self.transcription_artifact(return_timestamp=return_timestamp)
            transcript_store_dir = transcript_artifact.transcript_store_dir
            transcript_file_ext = transcript_artifact.transcript_file_type

            transcript_file_path = os.path.join(transcript_store_dir,
                                                TRANSCRIPTION_STORAGE_FILE_NAME + f".{transcript_file_ext}")
            transcripts = None
            if transcript_file_ext == "txt":
                with open(transcript_file_path, "r") as transcript:
                    transcripts = transcript.read()

            elif transcript_file_ext == "csv":
                transcripts = pd.read_csv(transcript_file_path)

            return transcripts


        except Exception as e:
            raise SummarizerException(e, sys)


