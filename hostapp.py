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
app.add_app("Home",icon=":email:",app=apps.HomeMainApp(title='Home'), is_home=True)
#app.add_app("About",icon=":house:",app=apps.AboutApp(title='About'))
#app.add_app("Tính năng",icon=":house:",app=apps.SpecApp(title='Tính năng'))
#app.add_app("Bảng giá",icon=":house:",app=apps.PriceApp(title='Bảng giá'))
#app.add_app("Hướng dẫn",icon=":house:",app=apps.GuideApp(title='Hướng dẫn'))
app.add_app("PDF2Text",icon=":house:",app=apps.PDF2TextApp(title='PDF2Text'))
app.add_app("ChatGpt",icon=":house:",app=apps.ChatGptApp(title='ChatGpt'))
app.add_app("Dashboard",icon=":house:",app=apps.DashboardApp(title='Dashboard'))
#app.add_app("AG Grid",icon=":house:",app=apps.AGGridApp(title='AG Grid'))
app.add_app("AG Grid v2",icon=":house:",app=apps.AGGrid2App(title='AG Grid 2'))



#run the whole lot
app.run()