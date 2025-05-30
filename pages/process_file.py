import streamlit as st
import json
from services.text_analysis import TextAnalysisPipeline

pipeline: TextAnalysisPipeline = st.session_state["textAnalysisPipeline"]

st.header("Procesar archivo TXT", divider=True)
input_file = st.file_uploader(
    label="Suba sus oraciones en un .txt separadas por saltos de linea:",
    type="txt"
)

if input_file is not None:
    try:
        results = []

        sentences = input_file.getvalue().decode("UTF-8").splitlines()
        if len(sentences) == 0:
            raise ValueError("Archivo vacio")

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                result = pipeline.process(sentence)
                results.append({
                    'sentence': sentence,
                    **result
                })

        file = json.dumps(results, ensure_ascii=False, indent=4)
        st.download_button(
            label="Descargar archivo procesado",
            data=file,
            file_name="output_results.json"
        )
    except ValueError:
        st.write("Error: No se encontro valores en su archivo")
    except IndexError:
        st.write("Error: Fallo IndexError al procesar su archivo")
    except Exception:
        st.write("Error: Se genero un error desconocido")
else:
    st.download_button(
        label="Descargar archivo de prueba",
        data="https://raw.githubusercontent.com/credu/text-analysis-pipeline/refs/heads/main/data/input_sentences.txt",
        icon="🧪"
    )
