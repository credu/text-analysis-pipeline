import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]

GRAMMAR_CNF = {
    'O': [('SN', 'SV', 1.0)],
    'SN': [('DT', 'N', 1.0)],
    'SV': [('V', 'SAdv', 0.5), ('V', 'SN', 0.5)],
    'SP': [('Prep', 'SN', 1.0)],
    'DT': [('el', 0.25), ('la', 0.25), ('un', 0.25), ('los', 0.25)],
    'N': [
        ('señor', 0.2),
        ('mujer', 0.2),
        ('gato', 0.2),
        ('perros', 0.2),
        ('biblioteca', 0.2)
    ],
    'V': [('vino', 0.25), ('corre', 0.25), ('salta', 0.25), ('ladran', 0.25)],
    'Prep': [('en', 0.5), ('de', 0.5)],
    'SAdv': [('RB', 0.5), ('JJ', 0.5)],
    'RB': [('tarde', 0.33), ('rápido', 0.33), ('fuerte', 0.33)],
    'JJ': [('alto', 1.0)]
}

st.header("Analizador Sintactico", divider=True)
st.write("Gramática en CNF de entrenamiento")
st.json(body=GRAMMAR_CNF, expanded=False)

default_text = "Seleccione una opción"
text_input = st.selectbox(
    label="Oraciones permitidas",
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
