import os
import re
from collections import Counter, defaultdict
import pymorphy3
import math

INVERTED_INDEX_FILE = "data/index/inverted_index.txt"
INDEX_FILE = "index.txt"
TFIDF_DIR = "data/tfidf_lemmas"

morph = pymorphy3.MorphAnalyzer()

def load_inverted_index():
    index = defaultdict(set)

    with open(INVERTED_INDEX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            lemma = parts[0]
            docs = set(d.replace("page_", "") for d in parts[1].split())
            index[lemma] = docs
    return index

def load_tfidf():
    vectors = defaultdict(dict)
    idf_dict = {}

    for filename in os.listdir(TFIDF_DIR):

        doc_id = filename.replace("page_", "").replace(".txt", "")
        path = os.path.join(TFIDF_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                term, idf, tfidf = line.strip().split()

                vectors[doc_id][term] = float(tfidf)
                idf_dict[term] = float(idf)

    return vectors, idf_dict

def load_urls():
    mapping = {}

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            filename, url = line.strip().split()
            doc_id = filename.replace("page_", "").replace(".html", "")
            mapping[doc_id] = url

    return mapping

def lemmatize_query(query):
    tokens = re.findall(r"[а-яА-ЯёЁ]+", query.lower())
    return [morph.parse(t)[0].normal_form for t in tokens]

def build_query_vector(lemmas, idf_dict):
    tf = Counter(lemmas)
    total = sum(tf.values())

    vector = {}
    for term in tf:
        if term in idf_dict:
            vector[term] = (tf[term] / total) * idf_dict[term]

    return vector

def cosine_similarity(vec1, vec2):
    # скалярное произведение
    dot = 0
    for term in vec1:
        if term in vec2:
            dot += vec1[term] * vec2[term]

    # длины векторов
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (norm1 * norm2)

def search(query, index, vectors, idf_dict):
    lemmas = lemmatize_query(query)

    # кандидаты через индекс
    candidates = set()
    for lemma in lemmas:
        if lemma in index:
            candidates.update(index[lemma])

    if not candidates:
        return []

    query_vec = build_query_vector(lemmas, idf_dict)

    scores = {}
    for doc_id in candidates:
        if doc_id in vectors:
            doc_vec = vectors[doc_id]
            score = cosine_similarity(query_vec, doc_vec)
            if score > 0:
                scores[doc_id] = score
    # сортировка по убыванию релевантности
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def main():
    index = load_inverted_index()
    vectors, idf_dict = load_tfidf()
    urls = load_urls()

    print("Введите 'exit' для выхода")
    while True:
        query = input("Введите запрос: ")

        if query.lower() == "exit":
            break

        results = search(query, index, vectors, idf_dict)

        if not results:
            print("Ничего не найдено\n")
            continue

        print("\nРезультаты:")
        for doc_id, score in results[:10]:
            print(f"{urls.get(doc_id, doc_id)}  score={score:.4f}")
        print()

if __name__ == "__main__":
    main()