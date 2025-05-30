import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]

st.header("Analizador Sintactico", divider=True)
st.write("Gramática en CNF de entrenamiento")
st.json(body=st.session_state["GRAMMAR_CNF"], expanded=False)

default_text = "Seleccione una opción"
text_input = st.selectbox(
    label="Oraciones permitidas",
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
    tokens = pipeline.preprocessor.tokenize(text_input.lower())
    st.write(f"Tokens: {tokens}")
    backpointers = pipeline.synt_analyzer.cky_parse(tokens)
    st.write("Backpointers:")
    st.table(backpointers)

    tree = pipeline.synt_analyzer.build_tree(
        backpointers, 0, len(tokens) - 1, 'O'
    )
    fig = pipeline.synt_analyzer.visualize_tree(tree)
    st.pyplot(fig)
