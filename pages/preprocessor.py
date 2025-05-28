import streamlit as st

pipeline = st.session_state.textAnalysisPipeline

st.header("Preprocesador", divider=True)

text_input = st.text_input(
    label="Texto a procesar:",
    autocomplete="off"
)

if text_input != "":
    tokens, lemmas = pipeline.preprocessor.process(text_input)
    st.write(f"Tokens: {tokens}")
    st.write(f"Lemas: {lemmas}")
