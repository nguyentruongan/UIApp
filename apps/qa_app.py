import streamlit as st
import sys
from langchain.llms import OpenAI

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class QAApp(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        self._cs_sidebar()
        self._cs_body()

     # sidebar
    def _cs_sidebar(self):
        openai_api_key = st.sidebar.text_input('OpenAI API Key')

    def _cs_body(self):
        def generate_response(input_text):
            llm = OpenAI(temperature=0.7, openai_api_key='sk-4hIAPiNm17uzanA1f8shT3BlbkFJMxxxxTSkodzgva7w1u3a')
            st.info(llm(input_text))

        with st.form('my_form'):
                text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
                submitted = st.form_submit_button('Submit')
        # if not openai_api_key.startswith('sk-'):
        #     st.warning('Please enter your OpenAI API key!', icon='⚠')
                if submitted:
                    generate_response(text)
