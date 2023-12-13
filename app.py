import streamlit as st
from multiapp import MultiApp
import home, result, data_col # import your app modules here



st.set_page_config(
    layout="centered", page_title="RBF Sim", page_icon="♨"
)


app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
#app.add_app("Theory", theory.app)
app.add_app("Data Collection", data_col.app)
app.add_app("Results", result.app)



# The main app
app.run()
