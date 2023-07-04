from hydralit import HydraApp
import streamlit as st
import apps 

# st.set_page_config(page_title='UIApp',page_icon=":sweat_drops:",layout='wide',initial_sidebar_state='auto',
#                    )

if __name__=='_main_':
   over_theme = {'txc_inactive': '#FFFFFF'}
#this is the host applicatiion, we add children to it and that's it.
app = HydraApp(
   title="UIApp",
   favicon=":sweat_drops:",
   hide_streamlit_markers=False,
   use_navbar=True
)
#Home

#app.add_app("Home",icon=":house:",app=apps.HomeApp(title='Home'), is_home=True)
app.add_app("Trang chủ",icon=":email:",app=apps.HomeMainApp(title='Trang chủ'), is_home=True)
#app.add_app("About",icon=":house:",app=apps.AboutApp(title='About'))
#app.add_app("Tính năng",icon=":house:",app=apps.SpecApp(title='Tính năng'))
#app.add_app("Bảng giá",icon=":house:",app=apps.PriceApp(title='Bảng giá'))
#app.add_app("Hướng dẫn",icon=":house:",app=apps.GuideApp(title='Hướng dẫn'))
app.add_app("Q&A",icon=":house:",app=apps.QAApp(title='Q&A'))



#run the whole lot
app.run()