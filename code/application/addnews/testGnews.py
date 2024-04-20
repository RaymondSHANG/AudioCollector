import myGoogleNews
t = myGoogleNews.myGoogleNews()
news = t.getNews(max_words=200, N_news=10, verbose=False)
print(f"\n\n\n\nLength of all news: {len(news)}")
for one in news:
    print(one['title'])
