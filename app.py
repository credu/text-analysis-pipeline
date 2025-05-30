import streamlit as st
from services.text_analysis import TextAnalysisPipeline

if "preprocessor" not in st.session_state:
    # Corpus proporcionado para entrenamiento
    st.session_state["CORPUS"] = [
        "<s> el/DT señor/NN vino/VBD tarde/RB </s>",
        "<s> la/DT mujer/NN corre/VBP rápido/RB </s>",
        "<s> un/DT gato/NN salta/VBP alto/JJ </s>",
        "<s> los/DT perros/NNS ladran/VBP fuerte/RB </s>"
    ]

    # Gramática en CNF
    st.session_state["GRAMMAR_CNF"] = {
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
        'V': [
            ('vino', 0.25),
            ('corre', 0.25),
            ('salta', 0.25),
            ('ladran', 0.25)
        ],
        'Prep': [('en', 0.5), ('de', 0.5)],
        'SAdv': [('RB', 0.5), ('JJ', 0.5)],
        'RB': [('tarde', 0.33), ('rápido', 0.33), ('fuerte', 0.33)],
        'JJ': [('alto', 1.0)]
    }

    st.session_state["textAnalysisPipeline"] = TextAnalysisPipeline(
        st.session_state["CORPUS"],
        st.session_state["GRAMMAR_CNF"],
        stopwords_path="data/stopwords-es.txt"
    )

# Define the pages
home_page = st.Page("pages/home.py", title="Inicio")
preprocessor_page = st.Page("pages/preprocessor.py", title="Preprocesador")
morphological_analyzer_page = st.Page(
    "pages/morphological_analyzer.py", title="Analizador Morfologico"
)
syntactic_analyzer_page = st.Page(
    "pages/syntactic_analyzer.py", title="Analizador Sintactico"
)
pipeline_page = st.Page("pages/pipeline.py", title="Demostración de pipeline")

# Set up navigation
pg = st.navigation([
    home_page,
    preprocessor_page,
    morphological_analyzer_page,
    syntactic_analyzer_page,
    pipeline_page,
])

# Run the selected page
pg.run()
