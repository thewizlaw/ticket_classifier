from flask import Flask, request, jsonify, request, render_template, send_from_directory, redirect
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ticket', methods=['POST'])
def ticket_process():
    ticket = request.form.get('ticket')
    nlp = spacy.load("en_core_web_sm")
    analyzer = SentimentIntensityAnalyzer()
    doc = nlp(ticket)
    
    tockens = []
    
    for token in doc:
        if not token.is_stop and not token.is_punct:
            tockens.append(token.lemma_.lower())
    
    URGENT_KEYWORDS = {"outage", "down", "failure", "urgent", "critical", "immediately", "unreachable", "broken"}
    
    keyword_critic = 0
    
    for token in tockens:
        if token in URGENT_KEYWORDS:
            keyword_critic += 1
    # print(f"Number of critical keywords found: {keyword_critic}")
    
    if keyword_critic > 1:
        print("Priority: High")
    elif keyword_critic == 1:
        print("Priority: Medium")
    else:
        print("Priority: Low")
    
    sentiment = analyzer.polarity_scores(ticket)
    score = sentiment['compound']
    print(sentiment)
    print(f"Sentiment Score: {score}")
    
    response = {
        'priority': 'High' if keyword_critic > 1 else 'Medium' if keyword_critic == 1 else 'Low',
        'sentiment_score': score
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)