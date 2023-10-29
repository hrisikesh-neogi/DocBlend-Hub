import pathlib
from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    data_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_audio_file_path: str


@dataclass
class TranscriptionArtifact:
    transcript_store_dir: pathlib.Path
    transcript_file_type: str





