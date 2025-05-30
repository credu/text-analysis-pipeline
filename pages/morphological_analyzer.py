import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]
corpus = st.session_state["CORPUS"]

st.header("Analizador morfologico")
st.write("Corpus de entrenamiento")
st.json(corpus)

word_input = st.text_input(
    label="Palabra desconocida a obtener su probabilidad basado en heurística:"
)
if " " in word_input:
    st.write("Error: Debe ingresar una palabra sin espacios")
elif word_input != "":
    heuristics = pipeline.morph_analyzer.handle_unknown_word(word_input)
    heuristics

default_text = "Seleccione una opción"
text_input = st.selectbox(
    label="Oraciones permitidas para etiquetar y viterbi",
    accept_new_options=True,
    options=[
        default_text,
        "El señor vino tarde",
        "La mujer corre rápido",
        "Un gato salta alto",
        "Los perros ladran fuerte",
    ]
)

if text_input != "" and text_input != default_text:
    tokens = pipeline.preprocessor.tokenize(text_input)

    st.write(f"tokens: {tokens}")
    st.write("Etiquetas")
    tags = pipeline.morph_analyzer.tag(tokens)
    tags
    st.write("Viterbi")
    viterbi = pipeline.morph_analyzer.viterbi(tokens)
    st.table(viterbi)
