from gnews import GNews
import newspaper
from datetime import datetime
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# pip3 install newspaper3k
# Update Feb12,2025
# Google News RSS links often use JavaScript-based redirections, which requests alone cannot handle because it only follows HTTP redirects (3xx status codes) and doesn't execute JavaScript. To get the actual redirected URL, you need a browser automation tool like selenium.
# https://news.google.com/rss/articles/CBMiWkFVX3lxTE1KYmQyTGY4Sk12ejVrRUluM2UzVmY3Wmt6YjA1OG9DejRDUFN2NmVkLW1wclJZZF8zYkxwRm5GT3VNc2gySGcxNGRET0Ywa3ZqNm5PVElFQks4d9IBX0FVX3lxTE9rckhtOG9nXzF2dy1pdlg4MG9hbEhsZGRHc195bkwxWDk2WWJzTDFoZ0l6VlNIbWtnTVlWVHJoMUNiSW5lRmZWTE8xVG82MXdfUHZhRkRvN2dSbzRNRzc4?oc=5&hl=en-US&gl=US&ceid=US:en
# https://www.bbc.com/news/articles/c8ed3nk3n6ro
# pip install selenium
# pip install webdriver_manager
# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
service = Service(ChromeDriverManager().install())

class myGoogleNews():
    def __init__(self):
        pass

    def getNews(self, max_words: int = 200,  N_news=1, verbose=False):
        # level = 0?
        driver = webdriver.Chrome(service=service, options=options)

        google_news = GNews()
        newsCollect = []
        json_resp = google_news.get_top_news()
        if verbose:
            print(f"json length: {len(json_resp)}")
        N_currentNews = 0
        for news_index in range(len(json_resp)):
            original_url = json_resp[news_index]['url']
            redirected_url = driver.current_url  # Get the final redirected URL
            article = google_news.get_full_article(original_url)
            if not article:
                continue
            if not article.is_valid_url():
                driver.get(original_url)
                
                continue
            if verbose:
                print(f"Title:{article}")
            N_words = len(article.title.split())
            newsDisplay = []
            # print(f"N_word title: {N_words}")
            # newsDisplay.append(article.title)
            text_paras = [a for a in article.text.split("\n") if a != '']
            N_paragraph = len(text_paras)

            for i, para in enumerate(text_paras):
                N_word_i = len(para.split())
                if N_word_i <= 5:
                    continue
                # print(f"N_word current {N_word_i}: {para}")
                if N_words+N_word_i > max_words:
                    break
                N_words += N_word_i
                newsDisplay.append(para)
            newsDisplay = ''.join(newsDisplay)
            N_currentNews += 1
            newsCollect.append({"title": article.title,
                                "body": newsDisplay,
                                "date": datetime.utcnow(),
                                "length": N_words,
                                "hashtags": int(hashlib.sha1(newsDisplay.encode("utf-8")).hexdigest(), 16) % (10 ** 8),
                                "level": 5})
            if verbose:
                print(f"Title: {article.title}")
                print(f"Top News length: {len(article.text)}")
                print(f"N paragraph: {N_paragraph}")
                # print("\n\n".join(newsDisplay))
            # return {"N_words": N_words, "content": newsDisplay}
            if N_currentNews >= N_news:
                break
        driver.quit()
        return newsCollect

        # print(article.text)
if __name__ == "__main__":
    myNews = myGoogleNews()
    one_news = myNews.getNews(max_words=200, N_news=10, verbose=True)
    print(one_news)
