from pytube import YouTube
from langchain.callbacks.base import BaseCallbackHandler

from src.exception import SummarizerException
from src.logger import logging as lg
import os, sys

# Provide the path to your ffprobe executable
YouTube.ffprobe_path = "/path/to/ffprobe"


def download_video_from_url(url, file_path):
    try:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video.download(output_path=file_path)
        lg.info("Video downloaded successfully!")
    except Exception as e:
        raise SummarizerException(e, sys)



