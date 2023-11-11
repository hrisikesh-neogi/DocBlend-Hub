import streamlit as st

HOME_PAGE_DETAIL = """
# Document Utiliy

This is a utility for document summarization, video summarization and video transcript generation.

## Features

- 📃 Document Summarization
- 📼 Video Summarization
- 🎥🗒️ Video Transcript Generation
- 🤖 Chat With Document 

###  Use the sidebar to navigate to the menus



"""
st.markdown(
    HOME_PAGE_DETAIL,
    unsafe_allow_html=True
)