import os
from collections import defaultdict

LEMMAS_DIR = "data/lemmas"
INDEX_DIR = "data/index"
INDEX_FILE = "inverted_index.txt"

def build_inverted_index():
    inverted_index = defaultdict(set)

    for filename in os.listdir(LEMMAS_DIR):
        doc_id = filename.replace("_lemmas.txt", "")

        filepath = os.path.join(LEMMAS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue

                lemma = parts[0]
                inverted_index[lemma].add(doc_id)

    return inverted_index

def save_index(index):
    os.makedirs(INDEX_DIR, exist_ok=True)
    path = os.path.join(INDEX_DIR, INDEX_FILE)

    with open(path, "w", encoding="utf-8") as f:
        for lemma in sorted(index.keys()):
            docs = sorted(index[lemma])
            f.write(lemma + " " + " ".join(docs) + "\n")

def main():
    index = build_inverted_index()
    save_index(index)
    print(f"Индекс построен. Терминов: {len(index)}")

if __name__ == "__main__":
    main()