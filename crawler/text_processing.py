import os
import re
from bs4 import BeautifulSoup
import pymorphy3

PAGES_DIR = "data/pages"
TOKENS_DIR = "data/tokens"
LEMMAS_DIR = "data/lemmas"

morph = pymorphy3.MorphAnalyzer()

def extract_text_from_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

        # ищем основной текст произведения
        text_div = soup.find("div", id="text")

        if text_div:
            return text_div.get_text(separator=" ", strip=True)
        else:
            return ""

def tokenize(text):
    text = text.lower()

    raw_tokens = re.findall(r"[а-яё]+", text) # берем только русские слова

    tokens = []

    for token in raw_tokens:
        parsed = morph.parse(token)[0]
        pos = parsed.tag.POS

        # пропускаем предлоги, частицы, союзы и междометия
        if pos in {"PREP", "CONJ", "PRCL", "INTJ"}:
            continue

        tokens.append(token)

    return sorted(set(tokens)) # удаляем дубликаты


def lemmatize_tokens(tokens):
    lemma_dict = {}

    for token in tokens:
        parsed = morph.parse(token)[0]
        lemma = parsed.normal_form

        if lemma not in lemma_dict:
            lemma_dict[lemma] = []

        lemma_dict[lemma].append(token)

    return lemma_dict

def process_pages():
    os.makedirs(TOKENS_DIR, exist_ok=True)
    os.makedirs(LEMMAS_DIR, exist_ok=True)

    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".html"):
            continue

        page_path = os.path.join(PAGES_DIR, filename)
        page_number = filename.replace(".html", "")

        print(f"Обработка {filename}")

        text = extract_text_from_html(page_path)

        tokens = tokenize(text)
        lemma_dict = lemmatize_tokens(tokens)

        # сохраняем токены
        tokens_file = os.path.join(TOKENS_DIR, f"{page_number}_tokens.txt")
        with open(tokens_file, "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(token + "\n")

        # сохраняем леммы
        lemmas_file = os.path.join(LEMMAS_DIR, f"{page_number}_lemmas.txt")
        with open(lemmas_file, "w", encoding="utf-8") as f:
            for lemma, words in lemma_dict.items():
                line = lemma + " " + " ".join(words)
                f.write(line + "\n")

if __name__ == "__main__":
    process_pages()
