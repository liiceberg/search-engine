import requests
import os
import time

OUTPUT_DIR = "data/pages"
INDEX_FILE = "index.txt"

# электронная библиотека с произведениями русских писателей
def generate_urls():
    works = {
        1199: 97, # И. С. Тургенев. Братья Карамазовы (97 страниц)
        1198: 13  # И. С. Тургенев. Рудин (13 страниц)
    }

    urls = []

    for work_id, pages_count in works.items():
        for page in range(1, pages_count + 1):
            urls.append(
                f"https://ilibrary.ru/text/{work_id}/p.{page}/index.html"
            )

    return urls

def download_page(url, file_number):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        filename = f"page_{file_number}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)

        return filename

    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    urls = generate_urls()

    with open(INDEX_FILE, "w", encoding="utf-8") as index_file:
        for i, url in enumerate(urls, start=1):
            print(f"Скачивание {i}: {url}")

            filename = download_page(url, i)

            if filename:
                index_file.write(f"{filename} {url}\n")

            time.sleep(1) # пауза между запросами

if __name__ == "__main__":
    main()
