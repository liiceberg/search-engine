import re

INDEX_PATH = "data/index/inverted_index.txt"

def load_index():
    index = {}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) > 1:
                index[parts[0]] = set(parts[1:])
            else:
                index[parts[0]] = set()
    return index

def tokenize_query(query):
    query = query.lower()
    tokens = re.findall(r"\w+|[()]", query)
    return tokens

def boolean_search(query, index):
    all_docs = set()
    for docs in index.values():
        all_docs |= docs

    tokens = tokenize_query(query)

    expr = []

    for token in tokens:
        if token == "and":
            expr.append("&")
        elif token == "or":
            expr.append("|")
        elif token == "not":
            expr.append("all_docs -")
        elif token in ("(", ")"):
            expr.append(token)
        else:
            docs = index.get(token, set())
            expr.append(f"set({docs})")

    expression = " ".join(expr)

    try:
        result = eval(expression)
        return result
    except Exception as e:
        print("Ошибка в запросе:", e)
        return set()

def main():
    index = load_index()

    print("Введите булев запрос (AND, OR, NOT, скобки):")
    print("Для выхода введите exit или q\n")

    while True:
        query = input("> ").strip()

        if not query:
            continue

        if query.lower() in {"exit", "q"}:
            print("Выход из программы.")
            break

        result = boolean_search(query, index)

        if result:
            print("Найденные документы:")
            for doc in sorted(result):
                print(" ", doc)
        else:
            print("Ничего не найдено.")

        print()

if __name__ == "__main__":
    main()