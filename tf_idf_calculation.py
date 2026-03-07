import os
import math
from collections import Counter, defaultdict

TOKENS_DIR = "data/tokens"
LEMMAS_DIR = "data/lemmas"

TFIDF_TERMS_DIR = "data/tfidf_terms"
TFIDF_LEMMAS_DIR = "data/tfidf_lemmas"


def load_tokens():
    docs = {}
    for filename in os.listdir(TOKENS_DIR):
        doc_id = filename.replace("_tokens.txt", "")
        path = os.path.join(TOKENS_DIR, filename)
        tokens = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                tokens.extend(parts)

        docs[doc_id] = tokens

    return docs


def load_lemmas():
    docs = {}
    for filename in os.listdir(LEMMAS_DIR):
        doc_id = filename.replace("_lemmas.txt", "")
        path = os.path.join(LEMMAS_DIR, filename)

        lemmas = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                lemmas.extend(parts)

        docs[doc_id] = lemmas
    return docs


def compute_idf(docs):
    N = len(docs) # число документов
    df = defaultdict(int) # в скольких документах встречается термин

    for tokens in docs.values():
        unique_terms = set(tokens) # учитываем каждый термин только один раз в документе
        for term in unique_terms:
            df[term] += 1

    idf = {}
    for term, freq in df.items():
        idf[term] = math.log(N / freq)
    return idf


def compute_tf(tokens):
    total = len(tokens) # кол-во терминов в документе
    counts = Counter(tokens) # сколько раз встречается каждый термин

    tf = {}
    for term, count in counts.items():
        tf[term] = count / total
    return tf


def save_tfidf(docs, idf, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for doc_id, tokens in docs.items():
        tf = compute_tf(tokens)
        path = os.path.join(output_dir, f"{doc_id}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for term in sorted(tf.keys()):
                tfidf = tf[term] * idf.get(term, 0)
                f.write(f"{term} {idf.get(term,0)} {tfidf}\n")


def main():
    print("Загрузка терминов...")
    token_docs = load_tokens()
    print("Подсчёт IDF терминов...")
    idf_terms = compute_idf(token_docs)
    print("Сохранение TF-IDF терминов...")
    save_tfidf(token_docs, idf_terms, TFIDF_TERMS_DIR)

    print("Загрузка лемм...")
    lemma_docs = load_lemmas()
    print("Подсчёт IDF лемм...")
    idf_lemmas = compute_idf(lemma_docs)
    print("Сохранение TF-IDF лемм...")
    save_tfidf(lemma_docs, idf_lemmas, TFIDF_LEMMAS_DIR)


if __name__ == "__main__":
    main()