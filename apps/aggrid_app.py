import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder,ColumnsAutoSizeMode,AgGridTheme

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class AGGridApp(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):
        st.title('AG Grid app demo')
        @st.cache_data()
        def load_data():
            data = pd.read_excel('file_pages/test-data.xls',parse_dates=['ACCT_OPEN_DATE'])
            return data

        data = load_data()
        #AgGrid(data,height=400)
        gb = GridOptionsBuilder()
        #make columns resiable, sortable and filterable by default
        gb.configure_default_column(resizable = True,
                                    filterable = True,
                                    sortable = True,
                                    editable = False,
                                    )
        #configures xx column to have a 80px initial width
        gb.configure_column(field='string',header_name="BRANCH", width=5)
        gb.configure_column(field='string',header_name="CCY", width=5)
        gb.configure_column(field='string',header_name="CLIENT_NO", width=5)
        gb.configure_column(field='string',header_name="ACCT_NO", width=5)
        gb.configure_column(field='string',header_name="ACCT_TYPE", width=5)
        #gb.configure_column(field='ACCT_OPEN_DATE',header_name="ACCT_OPEN_DATE", width=10)
        #configures xx column to have a tooltip
        # gb.configure_column(field="ACCT_OPEN_DATE",header_name="Acct Open Date", flex=1,tooltipField="Ngày mở TK")
        # #apply format
        # gb.configure_column(field="ACCT_OPEN_DATE",header_name="Acct Open Date",
        #                     valueFormatter="value !=undefined ? new Date(value).toLocaleString('en-US',{dateStyle:'medium'}):''",)
        gb.configure_column(field='ACCT_OPEN_DATE',type=['customDateTimeFormat'],custom_format_string ='dd/mm/yyyy')
        gb.configure_default_column(cellStyle={'color': 'black', 'font-size': '10px'}, suppressMenu=True, wrapHeaderText=True, autoHeaderHeight=True)

        custom_css = {".ag-header-cell-text": {"font-size": "10px", 'text-overflow': 'revert;', 'font-weight': 700},
                        ".ag-theme-streamlit": {'transform': "scale(0.8)", "transform-origin": '0 0'}}

        #make tooltip apprear instanly
        other_options = {'suppressColumnVirtualisation':True}
        gb.configure_grid_options(tooltipShowDelay = 0,**other_options)
        go = gb.build()
        AgGrid (data,
                gridOption = go, 
                custom_css= custom_css,
                height=400, 
                #width='100%',
                fit_columns_on_grid_load=True,
                #allow_unsafe_jscode=True,
                enable_enterprise_modules=False,
                theme=AgGridTheme.BALHAM,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)