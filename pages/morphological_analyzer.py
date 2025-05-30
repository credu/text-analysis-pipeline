import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]
corpus = st.session_state["CORPUS"]

st.header("Analizador morfologico")
st.write("Corpus de entrenamiento")
st.json(corpus)
pipeline.morph_analyzer.train(corpus)

text_input = st.text_input(
    label="Texto a analizar para etiquetar y viterbi:",
    autocomplete="off"
)
if text_input != "":
    tokens, lemmas = pipeline.preprocessor.process(text_input)

    st.write("Etiquetas")
    tags = pipeline.morph_analyzer.tag(tokens)
    tags
    st.write("Viterbi")
    viterbi = pipeline.morph_analyzer.viterbi(tokens)
    viterbi


word_input = st.text_input(
    label="Palabra desconocida a obtener su probabilidad basado en heurística:"
)
if " " in word_input:
    st.write("Error: Debe ingresar una palabra sin espacios")
elif word_input != "":
    heuristics = pipeline.morph_analyzer.handle_unknown_word(word_input)
    heuristics
