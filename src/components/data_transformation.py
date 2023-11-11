import os
import sys

from moviepy.editor import VideoFileClip

from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.exception import SummarizerException


class DataTransformation:

    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):

        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def convert_video_to_audio(
            video_file,
            output_ext="wav"):

        """Converts video to audio using MoviePy library
                       that uses `ffmpeg` under the hood"""

        try:

            filename, ext = os.path.splitext(video_file)
            clip = VideoFileClip(video_file)
            audio_file_path = f"{filename}.{output_ext}"
            clip.audio.write_audiofile(audio_file_path)

            return audio_file_path

        except Exception as e:
            raise SummarizerException(e, sys)

    def __get_video_file_name(self):
        try:
            files = os.listdir(self.data_ingestion_artifact.data_file_path)
            video_file_name = "".join([file for file in files if file.endswith(".mp4")])

            return video_file_name

        except Exception as e:
            raise SummarizerException(e, sys)

    def initiate_data_transformation(self):
        try:
            video_file_name = self.__get_video_file_name()
            video_file_path = os.path.join(
                self.data_ingestion_artifact.data_file_path,
                video_file_name
            )
            audio_file_path = DataTransformation.convert_video_to_audio(
                video_file=video_file_path,
            )

            data_transformation_artifact = DataTransformationArtifact(
                transformed_audio_file_path=audio_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise SummarizerException(e, sys)
