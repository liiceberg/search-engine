from flask import Flask, render_template, request
from vector_search import search, load_inverted_index, load_tfidf, load_urls

app = Flask(__name__)

inverted_index = load_inverted_index()
vectors, idf_dict = load_tfidf()
urls = load_urls()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        top_docs = search(query, inverted_index, vectors, idf_dict)
        results = [(urls.get(doc_id, doc_id), score) for doc_id, score in top_docs][:10]
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)