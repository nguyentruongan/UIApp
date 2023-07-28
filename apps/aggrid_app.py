import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder,ColumnsAutoSizeMode,AgGridTheme,JsCode
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
            data = pd.read_excel('file_pages/test-data3.xlsx')
            return data

        data = load_data()
        #AgGrid(data,height=400)
        AG_GRID_PERCENT_FORMATTER = JsCode(
            """
            function customPercentFormatter(params) {
                let n = Number.parseFloat(params.value) * 100;
                let precision = params.column.colDef.precision ?? 0;

                if (!Number.isNaN(n)) {
                return n.toFixed(precision).replace(/\B(?=(\d{3})+(?!\d))/g, ',')+'%';
                } else {
                return '-';
                }
            }
            """
        )

        AG_GRID_STRING_FORMATTER = JsCode(
            """
            function stringFormatter(params) {
               var s = params.value;
              
               return s.toLowerCase();
            }
            """
        )
        gb = GridOptionsBuilder()
        #make columns resiable, sortable and filterable by default
        gb.configure_default_column(resizable = True,
                                    filterable = True,
                                    sortable = True,
                                    editable = False,
                                    )
        #configures xx column to have a 80px initial width
        gb.configure_column(field="BRANCH", header_name="BRANCH", 
                          type=["stringColumn","customStringFormat"],valueFormatter = AG_GRID_STRING_FORMATTER)
        # gb.configure_column(field='CCY',header_name="CCY", width=5,
        #                     type=["stringColumn","customStringFormat"],valueFormatter = AG_GRID_STRING_FORMATTER)
        
        gb.configure_column(field='CLIENT_NO',header_name="CLIENT_NO", valueFormatter = AG_GRID_STRING_FORMATTER)
        gb.configure_column(field='ACCT_NO',header_name="ACCT_NO", width=5)
        gb.configure_column(field='ACCT_TYPE',header_name="ACCT_TYPE", width=5)
        

        gb.configure_column(field="PERCENT",header_name="PERCENT",
                            type = ["numberColumnFilter", "customNumericFormat", "numericColumn"],
                            valueFormatter = AG_GRID_PERCENT_FORMATTER,
                            precision=2)
        gb.configure_column("ACCT_OPEN_DATE", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd/MM/yyyy', pivot=True)
        #gb.configure_column(field='ACCT_OPEN_DATE',header_name="ACCT_OPEN_DATE", width=10)
        #configures xx column to have a tooltip
        # gb.configure_column(field="ACCT_OPEN_DATE",header_name="Acct Open Date", flex=1,tooltipField="Ngày mở TK")
        # #apply format
        # gb.configure_column(field="ACCT_OPEN_DATE",header_name="Acct Open Date",
        #                     valueFormatter="value !=undefined ? new Date(value).toLocaleString('en-US',{dateStyle:'medium'}):''",)
        #gb.configure_default_column(cellStyle={'color': 'black', 'font-size': '10px'}, suppressMenu=True, wrapHeaderText=True, autoHeaderHeight=True)

        custom_css = {".ag-header-cell-text": {"font-size": "10px", 'text-overflow': 'revert;', 'font-weight': 700},
                        ".ag-theme-streamlit": {'transform': "scale(0.8)", "transform-origin": '0 0'}}

        #make tooltip apprear instanly
      
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()
        gridOptions['columnDefs'].append({
            "field": "CCY",
            "header": "ccY",
            "cellRenderer": AG_GRID_STRING_FORMATTER,
            "cellRendererParams": {
                "color": "red",
                "background_color": "black",
            },
        })
        AgGrid (
                data,
                gridOption = gridOptions, 
                custom_css= custom_css,
                height=800, 
                #width='100%',
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True,
                theme=AgGridTheme.BALHAM,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)