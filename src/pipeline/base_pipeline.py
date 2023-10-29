import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.transcript import GenerateTranscript

from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig, TranscriptionConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, TranscriptionArtifact

from src.logger import logging as lg
from src.exception import SummarizerException


class BasePipeline:
    def __init__(self, video_url: str):
        self.video_url = video_url

    @property
    def data_ingestion_artifact(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=DataIngestionConfig())
            return data_ingestion.initiate_data_ingestion(self.video_url)
        except Exception as e:
            raise SummarizerException(e, sys)

    @property
    def data_transformation_artifact(self) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_transformation_config=DataTransformationConfig()
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise SummarizerException(e, sys)

    def transcription_artifact(self, return_timestamp: bool = False):
        try:
            transcription = GenerateTranscript(
                data_transformation_artifact=self.data_transformation_artifact,
                transcription_config=TranscriptionConfig())

            transcript_artifact = transcription.generate_transcript(
                return_timestamp=return_timestamp
            )

            return transcript_artifact

        except Exception as e:
            raise SummarizerException(e, sys)
