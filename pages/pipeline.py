import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]

initial_sentences = [
    "el gato salta alto",
    "la mujer corre rápido",
    "los perros ladran fuerte",
    "el señor vino tarde",
    "un gato en la biblioteca"
]

st.header("Demostración", divider=True)

test_sentences = st.multiselect(
    label="Oraciones",
    options=initial_sentences,
    default=initial_sentences,
    accept_new_options=True,
)

for sentence in test_sentences:
    st.write(f"\nProcesando: {sentence}")
    results = pipeline.process(sentence)
    pipeline.visualize_results(results)

    st.write("Tokens:", results.get('tokens', []))
    st.write("Lemas:", results.get('lemmas', []))
    st.write("POS Tags:", results.get('pos_tags', []))
    st.write("Árbol Sintáctico:")
    parse_tree = results.get('parse_tree', {})
    if parse_tree[1] == "Not Found" or parse_tree[1] == "Invalid":
        st.write(
            "Error: Programa no capacitado para representar esta oración"
        )
    else:
        fig = pipeline.synt_analyzer.visualize_tree(parse_tree)
        st.pyplot(fig)
