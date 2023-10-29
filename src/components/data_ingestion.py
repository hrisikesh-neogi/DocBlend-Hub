import os, sys
from urllib.parse import urlparse

from src.logger import logging as lg
from src.exception import SummarizerException
from src.utils import download_video_from_url
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    """
    Collecting and storing data.

    This class initiates the data ingestion steps. It understands the type of the data needed for this
    problem statement.

    Attributes:


    """

    def __init__(self,
                 data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    @staticmethod
    def is_url_youtube_related(url):
        """
           Check if a given URL is related to YouTube.

           Args:
               url (str): The URL to check.

           Returns:
               bool: True if the URL is YouTube-related, False otherwise.
       """
        try:
            # Parse the URL
            parsed_url = urlparse(url)

            # Check if the domain is youtube.com or youtu.be
            if parsed_url.netloc.endswith("youtube.com") or parsed_url.netloc == "youtu.be":
                return True
            else:
                return False

        except Exception as e:
            raise SummarizerException(e, sys)

    def initiate_data_ingestion(self,
                                url: str):
        try:
            if DataIngestion.is_url_youtube_related(url):
                download_video_from_url(
                    url=url,
                    file_path=self.data_ingestion_config.data_ingestion_dir
                )

            data_ingestion_artifact = DataIngestionArtifact(
                data_file_path=self.data_ingestion_config.data_ingestion_dir
            )

            return data_ingestion_artifact

        except Exception as e:
            raise SummarizerException(e, sys)
