from flask import Flask, render_template, request
from newspaper import Article
from textblob import TextBlob


app = Flask(__name__)

def download_and_parse_article(article_link):
    article = Article(article_link)
    article.download()
    article.parse()
    return article.text


def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_subjectivity = blob.sentiment.subjectivity

    if sentiment_polarity < 0:
        sentiment_verdict = 'Negative'
    elif sentiment_polarity == 0:
        sentiment_verdict = 'Neutral'
    else:
        sentiment_verdict = 'Positive'

    sentiment_details = f'Polarity: {sentiment_polarity}, Subjectivity: {sentiment_subjectivity}'

    return sentiment_verdict, sentiment_details

def perform_narrative_consistency_check(text):
    # TODO: Implement narrative consistency check
    return None, None

def perform_global_context_crosscheck(text):
    # TODO: Implement global context crosscheck
    return None, None

def perform_bias_verdict(text):
    # TODO: Implement bias verdict
    return None, None

def bard_check(text):
    token = 'eQg5DwNw_DgKtSBI6WBJvbeAQza9zJEeDLDHoM-4bVcpUxkIlHhsh-lv25wFnAlVl0jnAw.'
    bard = Bard(token=token)
    a=bard.get_answer('''I want you to act as a detective writing his blog. 
    #                             I will provide you with news related stories or topics and you will 
    #                             critically assess the accuracy of the information. You should use your own experiences, 
    #                             thoughtfully explain why something is important, back up claims with facts, 
    #                             and provide the correct information for any inaccuracies presented in the given information. 
    #                             The format of your blog should be as follows: "Statement 1: ..., 
    #                             Verdict:(overall accuracy level) ... and so on, 
    #                             (And at the end of the response) Sources: ...".''')['content']
    
    print(a)
    b=bard.get_answer('https://www.hindustantimes.com/india-news/unemployment-price-rise-behind-parliament-security-breach-rahul-gandhi-101702731238803.html')['content']
    print(b)

@app.route('/', methods=['GET', 'POST'])
def collect_article():
    # Initialize a default article object
    article_details = {
        'global_context_crosscheck_result_verdict': None,
        'global_context_crosscheck_result_details': None,
        'bias_verdict_verdict': None,
        'bias_verdict_details': None,
        'sentiment_analysis_verdict': None,
        'sentiment_analysis_details': None,
        'narrative_consistency_result_verdict': None,
        'narrative_consistency_result_details': None,
    }

    if request.method == 'POST':
        article_link = request.form.get('article_link')
        article_text = download_and_parse_article(article_link)

        sentiment_verdict, sentiment_details = perform_sentiment_analysis(article_text)
        narrative_verdict, narrative_details = perform_narrative_consistency_check(article_text)
        global_context_verdict, global_context_details = perform_global_context_crosscheck(article_text)
        bias_verdict, bias_details = perform_bias_verdict(article_text)

        article_details.update({
            'text': article_text,
            'sentiment_analysis_verdict': sentiment_verdict,
            'sentiment_analysis_details': sentiment_details,
            'narrative_consistency_result_verdict': narrative_verdict,
            'narrative_consistency_result_details': narrative_details,
            'global_context_crosscheck_result_verdict': global_context_verdict,
            'global_context_crosscheck_result_details': global_context_details,
            'bias_verdict_verdict': bias_verdict,
            'bias_verdict_details': bias_details,
        })

    # Pass the article object to the template
    return render_template('index.html', article=article_details)

if __name__ == '__main__':
    app.run(debug=True)