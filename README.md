# DocBlend Hub
![image](https://github.com/hrisikesh-neogi/DocBlend-Hub/assets/78023847/83f528ce-365b-4c17-ac0e-902ed26ae7d1)

This project leverages the use of LLMs, langchain, openai and vectorstores. 

## Usage
- **Document Summarization**
- **Video Transcript generation** ( Supported only for youtube videos with english audio.)
- **Video Summarization** ( Supported only for youtube videos with english audio)
- **QnA on top of Documents**

## How to setup
1. Clone the repository

```bash
git clone https://github.com/hrisikesh-neogi/DocBlend-Hub.git
```

2. Create a conda environment and install required libraries
```bash
# use python version >=3.10
conda create -p ./env python=<python-version> -y
conda activate ./env
pip install -r requirements.txt 
```
3. Run the following command to open the streamlit app
```bash
streamlit run home.py
```
****************************************************************
#### Note: set the `open-ai api key` in the environment variable with the variable name as `OPENAI_API_KEY`

If you have any suggestions, please reach me at hrisikesh.neogi@gmail.com.
