from flask import Flask, render_template, request
from utils.news_fetcher import fetch_news
from utils.summarizer import summarize_with_ollama

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        region = request.form.get("region")
        category = request.form.get("category")
        print(f"Fetching {region} news for {category}")  # Debug
        
        news_text = fetch_news(category, region)
        summary = summarize_with_ollama(news_text)
        
        return render_template(
            "news.html", 
            region=region,
            category=category,
            news_text=news_text, 
            summary=summary, 
        )
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)