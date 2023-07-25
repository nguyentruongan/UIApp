import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
)
import numpy as np
#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class DashboardApp(HydraHeadApp):
    
    def __init__(self, title = '', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def filter_dataframe(self,df: pd.DataFrame) -> pd.DataFrame:
        modify = st.checkbox("Add filters")
        if not modify:
            return df
        df = df.copy()
        #try to convert datetimes into standart format(datetime,no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass
            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
            for column in to_filter_columns:
                left, right = st.columns((1,20))
                left.write("--->")
                #Treat cols with < 10 unique values as cate
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min)/100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min,_max),
                        step = step,
                    )
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value =(
                            df[column].min(),
                            df[column].max(),
                          ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime,user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date,end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].str.contains(user_text_input)]
                    
        return df    
    
    def run(self):
        st.subheader("======================Display Excel file======================")
        
        df = pd.read_excel('file_pages/test-data.xls')
   
        st.dataframe(self.filter_dataframe(df))

   
    
        # st.write(df.shape)
        # # df.info()
        # st.write(df.head(10))
        # st.subheader("======================Filter by EUR======================")
        # st.write(df[df.CCY=='EUR'])

        #a list of strings
        # pd.Series(['apple','lemon','cook'])
        # #st.write(pd)
        # #creating a dataframe from a NumPy array
        # n1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
        # df1 = pd.DataFrame(n1,columns=['Teo','Ti','Cu Ti'],index=['Row1','Row2','Row3'])
        # st.write(df1)
        # #creating a series from a list
        # l2 = [1,2,3,4,5]
        # s2 = pd.Series(l2,name='A')
        # st.write(s2)
        # #Rows names in a DF can be renamed by altering the .index
        # df4 = df1.copy()
        # df4.index = ['John','Tom','Jerry']
        # st.write(df4)
        # #creating a DF from a dict
        # st.subheader("==================df5======================")
        # d = {'col1':[1,2,3], 'col2':[4,5,6],'col3':[7,8,9]}
        # df5 = pd.DataFrame(d)
        # st.write(df5)
        # #creating a DF from a dict with index
        # st.subheader("==================df6======================")
        # d = {'col1':[1,2,3], 'col2':[4,5,6],'col3':[7,8,9]}
        # df6 = pd.DataFrame(d,index =['John','Jerry','Tom'])
        # st.write(df6)

        # st.subheader("==================df7======================")
        # df7 = pd.DataFrame(d)
        # df7.index = ['Tom','Jerry','Sally']
        # st.write(df7)
