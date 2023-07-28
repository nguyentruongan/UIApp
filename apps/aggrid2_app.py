import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder,ColumnsAutoSizeMode,AgGridTheme,JsCode
#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class AGGrid2App(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
    
    def run(self):
        st.title('AG Grid 2 app demo')
        
        @st.cache_data()
        def load_data():
            data = pd.read_excel('file_pages/test-data3.xlsx')
            return data

        data = load_data()
        #AgGrid(data,height=400)
        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(data)

        #customize gridOptions
        gb.configure_default_column(
                                    filterable = True,
                                    sortable = True,  editable=False)
        gb.configure_column("ACCT_OPEN_DATE", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd/MM/yyyy', pivot=True)
        gb.configure_column("BRANCH", type=["textColumn","textColumnFilter","customTextFormat"],)

        gb.configure_column("ACTUAL_BAL", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2)
        # gb.configure_column("CCY", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
        # gb.configure_column("BRANCH", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

        #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value == 'A') {
                return {
                    'color': 'white',
                    'backgroundColor': 'darkred'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            }
        };
        """)
        #gb.configure_column("group", cellStyle=cellsytle_jscode)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()
        AgGrid(
                    data, 
                    gridOptions=gridOptions,
                    #height=grid_height, 
                    width='100%',
                    #data_return_mode=return_mode_value, 
                    #update_mode=update_mode_value,
                    #fit_columns_on_grid_load=fit_columns_on_grid_load,
                    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
                    #enable_enterprise_modules=enable_enterprise_modules
                    )
