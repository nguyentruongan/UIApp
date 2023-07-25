import streamlit as st

from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

from hugchat import hugchat
from langchain.chains import ConversationChain
from hugchat.login import Login
import os.path

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class ChatGptApp(HydraHeadApp):
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        
    def run(self):
        st.title('Chatgpt app')
        
        # with st.sidebar:
        #     st.header('Hugging Face Login')
        #     hf_email = st.text_input('Enter E-mail:', type='password')
        #     hf_pass = st.text_input('Enter password:', type='password')
        #     # Store AI generated responses
        #     if "messages" not in st.session_state.keys():
        #         st.session_state.messages = [{"role": "assistant", "content": "I'm HugChat, How may I help you?"}]
        #Store AI generated responses
        if "messages" not in st.session_state.keys():
                st.session_state.messages = [{"role": "assistant", "content": "I'm an assistant, How may I help you?"}]

        # Display existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Function for generating LLM response
        def generate_response(prompt, email, passwd):
            # Hugging Face Login
            sign = Login(email, passwd)
            #st.write('sign:',sign)
            cookies = sign.login()
            #st.write('cookies:',cookies)
            cookie_path_dir= "./usercookies" + f"/{email}.json"
            sign.saveCookiesToDir(cookie_path_dir)

            # load cookies from usercookies/<email>.json
            sign = Login(email, None)
            cookies = sign.loadCookiesFromDir(cookie_path_dir)
            #st.write('self cookie path:',cookie_path_dir)
            
            #st.write('cookies.get_dict():',cookies.get_dict())
           
            # Create ChatBot                        
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            chain = ConversationChain(llm=chatbot)
            response = chain.run(input=prompt)
            return response

         # Prompt for user input and save
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # If last message is not from assistant, we need to generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
                # Call LLM
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    hf_email =st.secrets.hug_chat.username
                    hf_pass  =st.secrets.hug_chat.password
                    # st.write('email:', hf_email)
                    # st.write('pass:', hf_pass)
                    response = generate_response(prompt, hf_email, hf_pass)
                    st.write(response)
                        
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)