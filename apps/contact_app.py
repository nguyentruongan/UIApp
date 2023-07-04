import streamlit as st

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class ContactApp(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.title('Contact app')
        
