from flask import Flask, jsonify, render_template, request
from newspaper import Article
from textblob import TextBlob
from bardapi import Bard
import re

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

    sentiment_verdict = 'Neutral'
    if sentiment_polarity < -.25:
        sentiment_verdict = 'Polarizing Negative'
    elif sentiment_polarity > .25:
        sentiment_verdict = 'Polarizing Positive'

    # round polarity and subjectivity to 2 decimal places
    sentiment_polarity = round(sentiment_polarity, 2)
    sentiment_subjectivity = round(sentiment_subjectivity, 2)


    meaning = ''
    if sentiment_verdict == 'Polarizing Negative':
        meaning = 'The news article seems to convey strongly unfavorable news or express very negative views about the topic.'
    elif sentiment_verdict == 'Neutral':
        meaning = 'The news article seems to report the facts without expressing any strong positive or negative views about the topic.'
    else:  # sentiment_verdict == 'Polarizing Positive'
        meaning = 'The news article seems to convey strongly favorable news or express very positive views about the topic.'

    sentiment_details = f'Meaning: {meaning}'

    return sentiment_verdict, sentiment_details, sentiment_polarity, sentiment_subjectivity

def perform_narrative_consistency_check(link):
    # Define the initial prompt for narrative consistency checking
    narrative_consistency_prompt = '''I want you to act as a detective writing his blog. 
    I will provide you with a news article and you will critically assess it by cross-checking info about current events. 
    Throughly visit and go through relevent articles on the web, thoughtfully explain any discrepancies, 
    back up claims with facts, and provide the correct information for any inconsistencies detected in the article. 
    The format of your blog should be as follows: 'Article: ..., (And at the very beginning of the response) Final Verdict: ... , Score: .../100 (more is better),
    Verdict:(overall consistency level with global context) ... and so on,
    (And at the end of the response) Sources: ...'''

    # Reload Bard with the new initial prompt
    token = 'dQhIwV8k6dQHeZRqlECFXNx4CVtuq-5ZKGZjh8ui0MdsU8lhgBXfkVFacasWjDM4HeNDTQ.'
    bard3 = Bard(token=token)
    a = bard3.get_answer(narrative_consistency_prompt)['content']
    print('Initial Bard3 Narrative Consistency Prompt loaded')

    # Send the article link as the next prompt
    result = bard3.get_answer(link)['content']

    # Process and print the result
    result = result.replace('\n', '<br>')
    result = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result)
    print(result)

    # Extract the verdict from the Bard output
    verdict_match = re.search(r'Verdict:(.*?)(?=<br>|$)', result)
    verdict = 'Detailed Analysis' if verdict_match is None else verdict_match.group(1).strip()

    score_match = re.search(r'Score:(.*?)(?=<br>|$)', result)
    score = '0' if score_match is None else score_match.group(1).strip()
    print(score)
    return verdict, result, score

# def perform_global_context_crosscheck(link):
#     # Define the initial prompt for global context cross-checking
#     global_context_prompt = '''I want you to act as a detective writing his blog. 
#     I will provide you with a news article and you will critically assess it by cross-checking with other news sources and current events. 
#     Throughly visit and go through relevent articles on the web, thoughtfully explain any discrepancies, 
#     back up claims with facts, and provide the correct information for any inconsistencies detected in the article. 
#     The format of your blog should be as follows: 'Article: ..., (And at the very beginning of the response) Final Verdict: ... , Score: .../100 (more is better),,
#     Verdict:(overall consistency level with global context) ... and so on,
#     (And at the end of the response) Sources: ...'''

#     # Reload Bard with the new initial prompt
#     token = 'dQhIwV8k6dQHeZRqlECFXNx4CVtuq-5ZKGZjh8ui0MdsU8lhgBXfkVFacasWjDM4HeNDTQ.'
#     bard2 = Bard(token=token)
#     a = bard2.get_answer(global_context_prompt)['content']
#     print('Initial Bard2 Global Context Prompt loaded')

#     # Send the article link as the next prompt
#     result = bard2.get_answer(link)['content']

#     # Process and print the result
#     result = result.replace('\n', '<br>')
#     result = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result)
#     print(result)

#     # Extract the verdict from the Bard output
#     verdict_match = re.search(r'Verdict:(.*?)(?=<br>|$)', result)
#     verdict = 'Detailed Analysis' if verdict_match is None else verdict_match.group(1).strip()

#     return verdict, result

def perform_bias_verdict(link):
    # Define the initial prompt for bias detection
    bias_prompt = '''I want you to act as a detective writing his blog. 
    I will provide you with a news article and you will critically assess it for potential bias. 
    You should consider both the perspective of the news organization and the individual writer.
    Especially consider the ideological leanings of the news organization and the writer's history.
    Throughly visit and go through relevent articles on the web to gather the info, thoughtfully explain why something might be biased, 
    back up claims with facts, and provide the correct information for any biases detected in the article. 
    The format of your blog should be as follows: 'Article: ..., (And at the very beginning of the response) Final Verdict: ... , Score: .../100 (more is better),
    Verdict:(overall bias level) ... and so on,
    (And at the end of the response) Sources: ...'''

    # Reload Bard with the new initial prompt
    token = 'dQhIwV8k6dQHeZRqlECFXNx4CVtuq-5ZKGZjh8ui0MdsU8lhgBXfkVFacasWjDM4HeNDTQ.'
    bard1 = Bard(token=token)
    a = bard1.get_answer(bias_prompt)['content']
    print('Initial Bard1 Bias Prompt loaded')
    print(a)
    
    # Send the article link as the next prompt
    result = bard1.get_answer(link)['content']

    # Process and print the result
    result = result.replace('\n', '<br>')
    result = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result)
    print(result)
    
    # Extract the verdict from the Bard output
    verdict_match = re.search(r'Verdict:(.*?)(?=<br>|$)', result)
    verdict = 'Detailed Analysis' if verdict_match is None else verdict_match.group(1).strip()

    score_match = re.search(r'Score:(.*?)(?=<br>|$)', result)
    score = '0' if score_match is None else score_match.group(1).strip()


    return verdict, result, score

def bard_setup(setup_prompt='''I want you to act as a detective writing his blog. 
    #                             I will provide you with news related stories or topics and you will 
    #                             critically assess the accuracy of the information. You should use your own experiences, 
    #                             thoughtfully explain why something is important, back up claims with facts, 
    #                             and provide the correct information for any inaccuracies presented in the given information. 
    #                             The format of your blog should be as follows: "Statement 1: ...,  (And at the very beginning of the response) Final Verdict: ... , Score: .../100
    #                             Verdict:(overall accuracy level) ... and so on, 
    #                              (And at the end of the response) Sources: ...".'''):
    token = 'dQhIwV8k6dQHeZRqlECFXNx4CVtuq-5ZKGZjh8ui0MdsU8lhgBXfkVFacasWjDM4HeNDTQ.'
    bard = Bard(token=token)    
    a=bard.get_answer(setup_prompt)['content']

    print('Initial Bard Prompt loaded')
    print(a)
    return bard

def bard_analysis(link):
    bard = bard_setup()
    result = bard.get_answer(link)['content']
    print(result)
    result = result.replace('\n', '<br>')
    result = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', result)

    score_match = re.search(r'Score:(.*?)(?=<br>|$)', result)
    score = '0' if score_match is None else score_match.group(1).strip()

    return result, score

def calculate_total_score(score1a,score1b, score2, score3, score4):
    
    print("SCORES BEFORE PROCESSING")
    print(score1a)
    print(score1b)
    print(score2)
    print(score3)
    print(score4)
    
    try:
        score2=score2.split('</b>')[1]
    except:
        pass
    try:
        score3=score3.split('</b>')[1]
    except:
        pass
    try:
        score4=score4.split('</b>')[1]
    except:
        pass


    # take first integer values until
    score2=score2.split('/')[0]
    score3=score3.split('/')[0]
    score4=score4.split('/')[0]

    print("SCORES AFTER PROCESSING")
    print(score1a)
    print(score1b)
    print(score2)
    print(score3)
    print(score4)

    # round score 1
    score1a = round(float(score1a))
    score1b = round(float(score1b))
    return {
        'polarity_score': int(score1a),
        'subjectivity_score': int(score1b),
        'narrative_score': int(score2),
        'bard_score': int(score3),
        'bias_score': int(score4),
    }

@app.route('/', methods=['GET', 'POST'])
def collect_article():
    global article_details
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
        'bard_analysis_result': None,
        'total_score': None,  # Add this line
    }
    if request.method == 'POST':
        article_link = request.form.get('article_link')
        article_text = download_and_parse_article(article_link)
        sentiment_verdict, sentiment_details, sentiment_polarity, sentiment_subjectivity = perform_sentiment_analysis(article_text)
        narrative_verdict, narrative_details, narrative_score = perform_narrative_consistency_check(article_link)
        bard_result, bard_score = bard_analysis(article_link)  # Update this line
        bias_verdict, bias_details,bias_score = perform_bias_verdict(article_link)
        scores = calculate_total_score(sentiment_polarity, sentiment_subjectivity, narrative_score, bard_score, bias_score)
        article_details.update({
            'text': article_text,
            'scores': scores,
            'sentiment_analysis_verdict': sentiment_verdict,
            'sentiment_analysis_details': sentiment_details,
            'narrative_consistency_result_verdict': narrative_verdict,
            'narrative_consistency_result_details': narrative_details,
            'bard_analysis_result': bard_result,
            'bias_verdict_verdict': bias_verdict,
            'bias_verdict_details': bias_details,
        })
    # Pass the article object to the template
    return render_template('index.html', article=article_details)

@app.route('/get_scores')
def get_scores():
    # Assuming article_details is globally accessible
    return jsonify(article_details['scores'])
if __name__ == '__main__':
    app.run(debug=True)