from gnews import GNews
import newspaper
import requests

url = "https://www.reuters.com/world/europe/kremlin-says-after-trump-putin-call-there-is-political-will-both-sides-end-2025-02-13/"

#google_news = GNews()
#article = newspaper.Article(url="%s" % url)
#article.download()
#article.parse()


url = "https://www.reuters.com/world/europe/kremlin-says-after-trump-putin-call-there-is-political-will-both-sides-end-2025-02-13/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    article = newspaper.Article(url)
    article.download(input_html=response.text)
    article.parse()
    print(article.text)
else:
    print(f"Failed to fetch article. Status Code: {response.status_code}")
