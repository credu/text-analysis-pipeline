import re
import streamlit as st
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]

st.header("Analizador morfologico")

corpus_input = st.text_area(
    label="Corpus de entrenamiento",
    value="<s> el/DT señor/NN vino/VBD tarde/RB </s>\n" +
    "<s> la/DT mujer/NN corre/VBP rápido/RB </s>\n" +
    "<s> un/DT gato/NN salta/VBP alto/JJ </s>\n" +
    "<s> los/DT perros/NNS ladran/VBP fuerte/RB </s>",
    height=120
)


corpus = re.findall(r"^<s>[\w\s/]+</s>$", corpus_input, flags=re.MULTILINE)
pipeline.morph_analyzer.train(corpus)
corpus

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
