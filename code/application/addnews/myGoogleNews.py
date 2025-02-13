from gnews import GNews
import newspaper
from datetime import datetime
import hashlib
from googlenewsdecoder import new_decoderv1


class myGoogleNews():
    def __init__(self):
        pass

    def getNews(self, max_words: int = 200,  N_news=1, verbose=False):
        interval_time = 5 # this can change to any time, but 5 is recommended
        google_news = GNews()
        newsCollect = []
        json_resp = google_news.get_top_news()
        if verbose:
            print(f"json length: {len(json_resp)}")
        N_currentNews = 0
        for news_index in range(len(json_resp)):
            original_url = json_resp[news_index]['url']
            decoded_url = new_decoderv1(original_url, interval=interval_time)
            article = google_news.get_full_article(decoded_url['decoded_url'])

            if not article:
                continue
            if not article.is_valid_url():                
                continue
            if verbose:
                #print(f"Title:{article}")
                print(f"url:{decoded_url['decoded_url']}")
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
        return newsCollect

        # print(article.text)
if __name__ == "__main__":
    myNews = myGoogleNews()
    one_news = myNews.getNews(max_words=200, N_news=10, verbose=True)
    print(one_news)
