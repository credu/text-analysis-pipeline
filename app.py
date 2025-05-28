import streamlit as st
from services.text_analysis import TextAnalysisPipeline

# TextAnalysisPipeline
if "preprocessor" not in st.session_state:
    st.session_state.textAnalysisPipeline = TextAnalysisPipeline(
        stopwords_path="data/stopwords-es.txt"
    )

# Define the pages
home_page = st.Page("pages/home.py", title="Inicio")
preprocessor_page = st.Page("pages/preprocessor.py", title="Preprocesador")

# Set up navigation
pg = st.navigation([home_page, preprocessor_page])

# Run the selected page
pg.run()
