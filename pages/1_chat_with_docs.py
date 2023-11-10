import streamlit as st
from src.utils.chatbot_utils import StreamHandler
from src.utils.chatbot_utils import *
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Basic Chatbot')

class Chatbot:

    def __init__(self):
        # utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"

    def setup_chain(self):
        llm = OpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        chain = ConversationChain(llm=llm, verbose=True)
        return chain

    @enable_chat_history
    def chat(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                response = chain.run(user_query, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    obj = Chatbot()
    obj.chat()