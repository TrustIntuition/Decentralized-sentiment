import requests
import os
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

api_key = os.getenv('NEWS_API_KEY')
to_date = datetime.utcnow()
from_date = to_date - timedelta(days=1)
url = f'https://newsapi.org/v2/everything?q=decentralized+compute&from={from_date.isoformat()}&to={to_date.isoformat()}&apiKey={api_key}'
response = requests.get(url)
articles = response.json().get('articles', [])

keywords = ['decentralized compute', 'blockchain', 'distributed computing']
relevant_articles = [article for article in articles if any(keyword.lower() in (article['title'] or '').lower() or keyword.lower() in (article['content'] or '').lower() for keyword in keywords)]

sia = SentimentIntensityAnalyzer()
sentiments = [sia.polarity_scores(article['content'])['compound'] for article in relevant_articles if article['content']]

if sentiments:
    average_sentiment = sum(sentiments) / len(sentiments)
    label = 'Positive' if average_sentiment > 0.05 else 'Negative' if average_sentiment < -0.05 else 'Neutral'
    sentiment_text = f'Average sentiment score: {average_sentiment:.2f} ({label}) based on {len(relevant_articles)} articles.'
else:
    sentiment_text = 'No relevant articles found in the past 24 hours.'

with open('index.html', 'w') as f:
    f.write(f'<html><body><h1>News Sentiment Tracker</h1><p>{sentiment_text}</p></body></html>')
