import sys
sys.path.append('.')

from apis import google_nlp
import os
import pytest

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/Google_API_Key.json" # local test
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/Google_API_Key.json" # actions test no need
nlp_client = google_nlp.init()

def analyze(comment):
    sentiment = google_nlp.analyze_sentiment(nlp_client, comment)
    return sentiment

def test_empty():  # empty text case
    sentiment = analyze("")
    assert sentiment == {} or (sentiment.score == 0 and sentiment.magnitude == 0)

def test_negative():  # test negative sentiments
    comments = ["Too bad!", "I don't like it", "太糟糕了"]
    for comment in comments:
        sentiment = analyze(comment)
        assert sentiment.score < 0

def test_positive():  # # test positive sentiments
    comments = ["excellent!", "brilliant", "can't be better"]
    for comment in comments:
        sentiment = analyze(comment)
        assert sentiment.score > 0

def test_magnitude():  # test different magnitudes
    comments = ["I have no feelings", "I kind of like it", "I extremely hate it"]
    mag = []
    for comment in comments:
        sentiment = analyze(comment)
        mag.append(sentiment.magnitude)
    assert sorted(mag) == mag

if __name__ == '__main__':
    pytest.main("test_google.py")