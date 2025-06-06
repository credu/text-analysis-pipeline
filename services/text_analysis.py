# -*- coding: utf-8 -*-
"""pln_project_grupo_2_1p

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dMaqC_fLa9wHE2JWAq6N7bof61PZ20Qt

# Integrantes
- Jose Alejandro Alvarez Sanchez
- Justyn Gabriel Garcia Figueroa
- Jesus Jeampool Mendoza Navarro
- Daniel Moises Troya Riofrio

# Inicialización
"""

import re
from collections import defaultdict
import json
import matplotlib.pyplot as plt

# Corpus proporcionado para entrenamiento
CORPUS = [
    "<s> el/DT señor/NN vino/VBD tarde/RB </s>",
    "<s> la/DT mujer/NN corre/VBP rápido/RB </s>",
    "<s> un/DT gato/NN salta/VBP alto/JJ </s>",
    "<s> los/DT perros/NNS ladran/VBP fuerte/RB </s>"
]

# Gramática en CNF
GRAMMAR_CNF = {
    'O': [('SN', 'SV', 1.0)],
    'SN': [('DT', 'N', 1.0)],
    'SV': [('V', 'SAdv', 0.5), ('V', 'SN', 0.5)],
    'SP': [('Prep', 'SN', 1.0)],
    'DT': [('el', 0.25), ('la', 0.25), ('un', 0.25), ('los', 0.25)],
    'N': [('señor', 0.2), ('mujer', 0.2), ('gato', 0.2), ('perros', 0.2), ('biblioteca', 0.2)],
    'V': [('vino', 0.25), ('corre', 0.25), ('salta', 0.25), ('ladran', 0.25)],
    'Prep': [('en', 0.5), ('de', 0.5)],
    'SAdv': [('RB', 0.5), ('JJ', 0.5)],
    'RB': [('tarde', 0.33), ('rápido', 0.33), ('fuerte', 0.33)],
    'JJ': [('alto', 1.0)]
}

"""# Clase Preprocessor (Jesus Mendoza)
Responsable de tokenización, normalización, eliminación de stopwords y lematización básica.
## Recursos
[Archivo de StopWords](https://raw.githubusercontent.com/stopwords-iso/stopwords-es/refs/heads/master/stopwords-es.txt)
"""

class Preprocessor:
    def __init__(self, *args):
        """Inicializa el preprocesador con una lista de stopwords (opcional)."""
        stopwords_file = args[0] if args else None
        self.stopwords = self.load_stopwords(stopwords_file) if stopwords_file else set([
            'el', 'la', 'los', 'un', 'de', 'en', 'y', 'a', 'que'  # Ejemplo básico
        ])
        self.lemmatization_rules = [
            (r'ando$', 'ar'),  # corriendo -> correr
            (r'iendo$', 'er'),  # comiendo -> comer
            (r's$', '')  # gatos -> gato
        ]

    def load_stopwords(self, *args):
        """Carga stopwords desde un archivo de texto (una por línea)."""
        filepath = args[0] if args else None
        with open(filepath, "r", encoding="UTF-8") as file:
            content = file.read().splitlines()
            return set(content)

    def tokenize(self, *args):
        """Divide el texto en tokens, eliminando puntuación básica."""
        text = args[0] if args else ""

        words = re.findall(r"([().]|['\w]+)", text)
        return [word for word in words if word not in "!\"'(),-.:;¿?`_{}"]

    def normalize(self, *args):
        """Convierte tokens a minúsculas y elimina caracteres no alfanuméricos."""
        tokens = args[0] if args else []

        return [word.lower() for word in tokens if word not in "#$%&*+<=>@[\\/]^|~"]

    def remove_stopwords(self, *args):
        """Elimina stopwords de la lista de tokens."""
        tokens = args[0] if args else []

        return [word for word in tokens if word not in self.stopwords]

    def lemmatize(self, *args):
        """Aplica reglas morfológicas simples para lematización."""
        tokens = args[0] if args else []

        lemmas = []
        for word in tokens:
            for rule in self.lemmatization_rules:
                regex, replacement = rule
                if re.search(regex, word):
                    lemma = re.sub(regex, replacement, word)
                    lemmas.append(lemma)
                    break

        return lemmas

    def process(self, *args):
        """Ejecuta el pipeline completo: tokenización, normalización, eliminación de stopwords, lematización."""
        text = args[0] if args else ""

        tokenized_text = self.tokenize(text)
        normalized_tokens = self.normalize(tokenized_text)
        tokens = self.remove_stopwords(normalized_tokens)
        lemmas = self.lemmatize(tokens);

        return tokens, lemmas  # Retorna (tokens, lemas)

# Tes del pipeline completo
# preprocessor = Preprocessor("stopwords-es.txt")
# preprocessor.process("Un elefante corriendo se balanceaba sobre la tela de una araña.")

"""# Clase MorphologicalAnalyzer

---


Implementa POS tagging con HMM y Viterbi, y soporte para lematización.
"""

class MorphologicalAnalyzer:
    def __init__(self, *args):
        """Inicializa el analizador con datos de entrenamiento"""
        corpus = args[0] if args else []
        self.tags = {'DT', 'NN', 'NNS', 'VBD', 'VBP', 'RB', 'JJ', '<s>', '</s>'}
        self.transition_probs = defaultdict(lambda: defaultdict(float))
        self.emission_probs = defaultdict(lambda: defaultdict(float))

        # Entrenamos el modelo si hay corpus
        if corpus:
            self.train(corpus)

    def train(self, *args):
        """Calcula probabilidades de transición y emisión a partir del corpus."""
        corpus = args[0] if args else []

        # Procesado del corpus si viene en formato texto
        if corpus and isinstance(corpus[0], str):
            corpus_procesado = []
            for linea in corpus:
                palabras_etiquetas = []
                for parte in linea.split():
                    if '/' in parte and parte not in ('<s>', '</s>'):
                        palabra, etiqueta = parte.rsplit('/', 1)
                        palabras_etiquetas.append((palabra.lower(), etiqueta))
                corpus_procesado.append(palabras_etiquetas)
            corpus = corpus_procesado

        # Contadores para transiciones y emisiones
        trans_counts = defaultdict(lambda: defaultdict(int))
        emis_counts = defaultdict(lambda: defaultdict(int))

        # Contamos ocurrencias en el corpus
        for oracion in corpus:
            oracion_con_marcadores = [('<s>', '<s>')] + oracion + [('</s>', '</s>')]

            for i in range(1, len(oracion_con_marcadores)):
                palabra_actual, etiqueta_actual = oracion_con_marcadores[i]
                _, etiqueta_anterior = oracion_con_marcadores[i-1]

                # Contamos transiciones
                trans_counts[etiqueta_anterior][etiqueta_actual] += 1

                # Contamos emisiones (excepto para marcadores)
                if etiqueta_actual not in ('<s>', '</s>'):
                    emis_counts[etiqueta_actual][palabra_actual] += 1

        # Convertimos conteos a probabilidades
        self._convertir_a_probabilidades(trans_counts, emis_counts)

    def _convertir_a_probabilidades(self, trans_counts, emis_counts):
        """Helper para convertir conteos en probabilidades"""
        # Probabilidades de transición
        for etiqueta_origen, destinos in trans_counts.items():
            total = sum(destinos.values())
            for etiqueta_destino, conteo in destinos.items():
                self.transition_probs[etiqueta_origen][etiqueta_destino] = conteo / total if total > 0 else 0.0

        # Probabilidades de emisión
        for etiqueta, palabras in emis_counts.items():
            total = sum(palabras.values())
            for palabra, conteo in palabras.items():
                self.emission_probs[etiqueta][palabra] = conteo / total if total > 0 else 0.0

    def viterbi(self, *args):
        """Implementa el algoritmo de Viterbi para POS tagging."""
        tokens = args[0] if args else []
        if not tokens:
            return [], []

        n = len(tokens)
        tags = [t for t in self.tags if t not in {'<s>', '</s>'}]

        # Matrices para probabilidades y backpointers
        V = [{} for _ in range(n)]  # Probabilidades
        B = [{} for _ in range(n)]  # Mejores etiquetas anteriores

        # Paso inicial
        primera_palabra = tokens[0].lower()
        for t in tags:
            # Probabilidad = P(t|<s>) * P(palabra|t)
            prob_trans = self.transition_probs['<s>'].get(t, 0.000001)
            prob_emis = self._get_emission_prob(t, primera_palabra)
            V[0][t] = prob_trans * prob_emis
            B[0][t] = '<s>'

        # Pasos siguientes
        for i in range(1, n):
            palabra = tokens[i].lower()
            for t in tags:
                # Buscamos la mejor etiqueta anterior
                mejor_prob = -1
                mejor_etiqueta = None

                for t_prev in tags:
                    prob = V[i-1][t_prev] * self.transition_probs[t_prev].get(t, 0.000001)
                    if prob > mejor_prob:
                        mejor_prob = prob
                        mejor_etiqueta = t_prev

                # Multiplicamos por probabilidad de emisión
                prob_emis = self._get_emission_prob(t, palabra)
                V[i][t] = mejor_prob * prob_emis
                B[i][t] = mejor_etiqueta

        # Encontrar la mejor secuencia
        mejor_etiqueta = max(V[-1], key=lambda t: V[-1][t] * self.transition_probs[t].get('</s>', 0.000001))
        path = [mejor_etiqueta]

        # Reconstruir el camino
        for i in reversed(range(1, n)):
            path.insert(0, B[i][path[0]])

        return path, [V[i][tag] for i, tag in enumerate(path)]

    def _get_emission_prob(self, tag, word):
        """Obtiene probabilidad de emisión, manejando palabras desconocidas"""
        if word in self.emission_probs[tag]:
            return self.emission_probs[tag][word]
        else:
            # Usar heurísticas para palabras desconocidas
            return self.handle_unknown_word(word).get(tag, 0.000001)

    def tag(self, *args):
        """Etiqueta una lista de tokens con sus categorías morfosintácticas."""
        tokens = args[0] if args else []
        tags, _ = self.viterbi(tokens)
        return tags

    def handle_unknown_word(self, *args):
        """Asigna probabilidades bajas a palabras desconocidas basadas en heurísticas."""
        word = args[0] if args else ''
        word = word.lower()
        heuristics = {}

        # Basado en sufijos comunes en español
        if word.endswith("mente"):
            heuristics["RB"] = 0.9  # Adverbio
        elif word.endswith(("ado", "ido")):
            heuristics["VBD"] = 0.8  # Participio pasado
        elif word.endswith(("ar", "er", "ir")):
            heuristics["VB"] = 0.8   # Infinitivo verbal
        elif word.endswith(("os", "as", "es")):
            heuristics["NNS"] = 0.7  # Plural
        elif word.endswith(("o", "a", "e")):
            heuristics["NN"] = 0.6   # Singular
        else:
            heuristics["NN"] = 0.5   # Valor por defecto

        return heuristics

"""# Clase SyntacticAnalyzer
Implementa análisis sintáctico con el algoritmo CKY.
"""

# No olviden prender la gramatica cnf que esta arriba
# Tampoco olviden usar el pip install para que muestre grafico
# El codigo tiene un error que aun no decifro pero en esencia ya esta T-T
# no le crean
# confien
# no le crean v2
# YA SIRVE, la fe señores, lo mas lindo de la vida


class SyntacticAnalyzer:
    def __init__(self, *args):
        grammar = args[0] if args else {}
        self.grammar = grammar
        self.non_terminals = set(grammar.keys())
        self.terminals = set()
        self.build_terminal_set()

    def build_terminal_set(self):
        for values in [value for values in self.grammar.values() for value in values]:
            for value in values:
                if not isinstance(value, float) and value not in self.non_terminals:
                    self.terminals.add(value)

    def cky_parse(self, *args):
        tokens = args[0] if args else []
        n = len(tokens)
        backpointers = []
        table = []

        for i in range(n):
            fila_table = []
            fila_back = []
            for j in range(n):
                fila_table.append({})
                fila_back.append({})
            table.append(fila_table)
            backpointers.append(fila_back)

        for i in range(n):
            token = tokens[i]
            for etiqueta in self.grammar:
                for resultado in self.grammar[etiqueta]:
                    if len(resultado) == 2 and resultado[0] == token:
                        table[i][i][etiqueta] = resultado[1]
                        backpointers[i][i][etiqueta] = token
            added = True
            while added:
                added = False
                for A in self.grammar:
                    for prod in self.grammar[A]:
                        if len(prod) == 2 and prod[0] in table[i][i] and isinstance(prod[0], str) and prod[0] in self.non_terminals:
                            B = prod[0]
                            prob = prod[1] * table[i][i][B]
                            if A not in table[i][i] or prob > table[i][i][A]:
                                table[i][i][A] = prob
                                backpointers[i][i][A] = (i, B)
                                added = True

        for longitud in range(2, n + 1):
            for inicio in range(n - longitud + 1):
                fin = inicio + longitud - 1
                for division in range(inicio, fin):
                    izquierda = table[inicio][division]
                    derecha = table[division + 1][fin]
                    for etiqueta in self.grammar:
                        for resultado in self.grammar[etiqueta]:
                            if len(resultado) == 3:
                                B, C, prob = resultado
                                if B in izquierda and C in derecha:
                                    prob_total = izquierda[B] * derecha[C] * prob
                                    if etiqueta not in table[inicio][fin] or prob_total > table[inicio][fin][etiqueta]:
                                        table[inicio][fin][etiqueta] = prob_total
                                        backpointers[inicio][fin][etiqueta] = (division, B, C)

        return backpointers


    def build_tree(self, *args):
        """Construye el árbol sintáctico a partir de los backpointers del CKY."""
        backpointers, start, end, symbol = args[:4] if len(args) >= 4 else ({}, 0, 0, '')
        if symbol not in backpointers[start][end]:
            return (symbol, "Not Found")

        data = backpointers[start][end][symbol]

        if isinstance(data, str):
            return (symbol, data)
        elif isinstance(data, tuple) and len(data) == 2:
            tipo, hijo = data
            return (symbol, self.build_tree(backpointers, start, end, hijo))
        elif isinstance(data, tuple) and len(data) == 3:
            division, izquierdo, derecho = data
            izquierda = self.build_tree(backpointers, start, division, izquierdo)
            derecha = self.build_tree(backpointers, division + 1, end, derecho)
            return (symbol, izquierda, derecha)
        else:
            return (symbol, "Invalid")

    def visualize_tree(self, tree):
        def build_lines(node, indent=""):
            lines = []
            if isinstance(node, tuple):
                label = node[0]
                lines.append(indent + label)
                for child in node[1:]:
                    lines.extend(build_lines(child, indent + "  "))
            else:
                lines.append(indent + str(node))
            return lines

        lines = build_lines(tree)

        fig, ax = plt.subplots()
        ax.axis('off')
        text = '\n'.join(lines)
        ax.text(0, 1, text, ha='left', va='top', family='monospace')
        plt.title('Árbol Sintáctico')
        plt.tight_layout()
        plt.show()

        # Nota de Jesus
        # Es necesario retornar la figura su renderizacion en streamlit
        return fig

"""# Pipeline Completo
Integra las clases anteriores en un pipeline unificado.
"""


class TextAnalysisPipeline:
    def __init__(self, *args, stopwords_path=None):
        """Inicializa el pipeline con los componentes necesarios."""
        corpus, grammar = args[:2] if len(args) >= 2 else ([], {})

        self.preprocessor = Preprocessor(stopwords_path)
        self.morph_analyzer = MorphologicalAnalyzer(corpus)
        self.synt_analyzer = SyntacticAnalyzer(grammar)

    def process(self, *args):
        """Procesa un texto a través del pipeline completo."""
        text = args[0] if args else ""
        # Preprocesamiento
        tokens, lemmas = self.preprocessor.process(text)
        tokens_with_stopwords = self.preprocessor.tokenize(text.lower())

        # Análisis morfológico
        tagged_tokens = self.morph_analyzer.tag(tokens)

        # Análisis sintáctico
        backpointers = self.synt_analyzer.cky_parse(tokens_with_stopwords)
        parse_tree = pipeline.synt_analyzer.build_tree(
            backpointers, 0, len(tokens_with_stopwords) - 1, 'O'
        )

        return {
            'tokens': tokens,
            'lemmas': lemmas,
            'pos_tags': tagged_tokens,
            'parse_tree': parse_tree
        }

    def visualize_results(self, *args):
        """Visualiza los resultados del pipeline."""
        results = args[0] if args else {}
        print("Tokens:", results.get('tokens', []))
        print("Lemas:", results.get('lemmas', []))
        print("POS Tags:", results.get('pos_tags', []))
        print("Árbol Sintáctico:")
        parse_tree = results.get('parse_tree', {})
        if parse_tree[1] == "Not Found" or parse_tree[1] == "Invalid":
            print("Error: Este programa no esta capacitado para representar esta oración")
        else:
            self.synt_analyzer.visualize_tree(parse_tree)


"""# Demostración
Prueba el pipeline con oraciones de ejemplo.
"""

# Inicializar el pipeline
pipeline = TextAnalysisPipeline(CORPUS, GRAMMAR_CNF)

# Oraciones de prueba
test_sentences = [
    "el gato salta alto",
    "la mujer corre rápido",
    "los perros ladran fuerte",
    "el señor vino tarde",
    "un gato en la biblioteca"
]

# Procesar y visualizar resultados
# for sentence in test_sentences:
#     print(f"\nProcesando: {sentence}")
#     results = pipeline.process(sentence)
#     pipeline.visualize_results(results)

"""# Script de Demostración
Script para procesar un archivo de texto y generar resultados.
"""

def process_file(*args) -> None:
    """Procesa un archivo de texto con oraciones y guarda los resultados."""
    input_file, output_file = args[:2] if len(args) >= 2 else ('', '')
    pipeline = TextAnalysisPipeline(CORPUS, GRAMMAR_CNF)
    results = []

    # Leer oraciones
    with open(input_file, 'r', encoding='utf-8') as f:
        sentences = f.readlines()

    # Procesar cada oración
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            result = pipeline.process(sentence)
            results.append({
                'sentence': sentence,
                **result
            })

    # Guardar resultados
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# Ejemplo de uso
# process_file('input_sentences.txt', 'output_results.json')
