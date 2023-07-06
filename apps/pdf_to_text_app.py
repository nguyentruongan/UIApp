import streamlit as st
import pdf2image
from PIL import Image

import pytesseract
from pytesseract import Output, TesseractError
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class PDF2TextApp(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        st.header('PDFText')
        
        languages = {
            'English': 'eng',
            'Vietnamese': 'vie'
        }
        with st.sidebar:
            st.title("PDF to Text")
            textOutput = st.selectbox("Which output?",('One text file (.txt)','Text file per page (.zip)'))
            ocr_box = st.checkbox('Enable OCR (scanned document)')
        pdf_file = st.file_uploader('Load your pdf', type=['pdf','png','jpg','jpeg'])
        if pdf_file:
            path = pdf_file.read()
            file_extension = pdf_file.name.split(".")[-1]
            if file_extension == "pdf":
                    #display document
                    with st.expander("Display document"):
                        displayPDF(path)
                    if ocr_box:
                        option = st.selectbox('Select the document language', list(languages.keys))
                    #pdf to text
                    if textOutput =='One text file (.txt)':
                        if ocr_box:
                            texts, nbPages = images_to_txt(path, languages[option])
                            totalPages = "Total pages:" + str(nbPages) 
                            text_data_f = "\n\n".join(texts)
                        else:
                            text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                            totalPages = "Total pages:" + str(nbPages) 
                        st.info(totalPages)
                        st.download_button("Download file", text_data_f)
                    else:
                        if ocr_box:
                            texts, nbPages = images_to_txt(path, languages[option])
                            totalPages = "Total pages:" + str(nbPages) 
                           
                        else:
                            text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
                            totalPages = "Total pages:" + str(nbPages) 
                        st.info(totalPages)
                        zipPath = save_pages(text_data)
                        #download text data
                        with open(zipPath, "rb") as fp:
                            btn = st.download_button(
                                label ="Download ZIP (txt)",
                                data =fp,
                                file_name ="pdf_to_txt.zip",
                                mime="application/zip"
                            )
            else:
                    option = st.selectbox("What's language of the text in the image?",list(languages.keys()))
                    pil_image = Image.open(pdf_file)
                    text = pytesseract.image_to_string(pil_image, lang=languages[option])
                    col1, col2 = st.columns(s)
                    with col1:
                        with st.expander("Display Image"):
                            st.image(pdf_file)
                    with col2:
                        with st.expander("Display Text"):
                            st.info(text)
                    st.download_button("Download txt file", text)


        
