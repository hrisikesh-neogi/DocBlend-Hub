import os, sys

from typing import List, Dict

import pandas as pd

from src.constant import TRANSCRIPTION_STORAGE_FILE_NAME
from src.logger import logging as lg
import librosa
from transformers import AutoTokenizer, pipeline
import torch

from src.exception import SummarizerException
from src.utils import download_video_from_url
from src.entity.config_entity import TranscriptionConfig
from src.entity.artifact_entity import DataTransformationArtifact, TranscriptionArtifact


class GenerateTranscript:
    """
    Creates transcript from a video file.

    """

    def __init__(self,
                 data_transformation_artifact: DataTransformationArtifact,
                 transcription_config: TranscriptionConfig):

        self.data_transformation_artifact = data_transformation_artifact
        self.transcription_config = transcription_config

    def load_audio(self):
        try:
            audio, rate = librosa.load(
                self.data_transformation_artifact.transformed_audio_file_path,
                sr=16000)

            return audio, rate

        except Exception as e:
            raise SummarizerException(e, sys)

    def generate_transcript(self, return_timestamp: bool = True):
        try:

            model = "openai/whisper-base"
            tokenizer = AutoTokenizer.from_pretrained(model)

            model = pipeline(
                "automatic-speech-recognition",  # task
                model=model,
                tokenizer=tokenizer,
                chunk_length_s=10,
            )

            audio, _ = self.load_audio()

            prediction = model(
                audio,
                batch_size=8,
                return_timestamps=return_timestamp
            )

            os.makedirs(self.transcription_config.transcription_dir, exist_ok=True)
            if return_timestamp:
                transcript = prediction["chunks"]  # list[timestamp, text]
                texts = [text["text"] for text in transcript["chunks"]]
                times = [text["timestamp"] for text in transcript["chunks"]]

                data = pd.DataFrame()
                data["timestamp"] = times
                data["text"] = texts

                transcript_file_ext = "csv"
                transcript_store_dir = os.path.join(
                    self.transcription_config.transcription_dir,
                    TRANSCRIPTION_STORAGE_FILE_NAME + f".{transcript_file_ext}"
                )
                data.to_csv(transcript_store_dir, index=False)

            else:
                transcript = prediction["text"]
                transcript_file_ext = "txt"
                transcript_store_dir = os.path.join(
                    self.transcription_config.transcription_dir,
                    TRANSCRIPTION_STORAGE_FILE_NAME + f".{transcript_file_ext}")

                with open(transcript_store_dir, "w") as file:
                    file.writelines(transcript)

            transcription_artifact = TranscriptionArtifact(
                transcript_store_dir=self.transcription_config.transcription_dir,
                transcript_file_type=transcript_file_ext
            )

            return transcription_artifact

        except Exception as e:
            raise SummarizerException(e, sys)
