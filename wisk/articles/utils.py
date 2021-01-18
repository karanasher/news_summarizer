# Reference.
#     https://pypi.org/project/sumy/
#     https://newsapi.org/docs/endpoints/top-headlines
import requests
from goose3 import Goose
from transformers import TFAutoModelWithLMHead, AutoTokenizer

def get_top_headlines():
    print('Entered get_top_headlines.')

    # Get top headlines from API.
    response_us = requests.get('https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey=d5d670dc694447868d28d02f551b7419')
    response_in = requests.get('https://newsapi.org/v2/top-headlines?country=in&pageSize=10&apiKey=d5d670dc694447868d28d02f551b7419')

    if response_us and response_in:
        print('Got some response from the API.')

        g = Goose()
        model = TFAutoModelWithLMHead.from_pretrained("t5-small")
        tokenizer = AutoTokenizer.from_pretrained("t5-small")

        # The list of articles that will be returned.
        articles = []

        # Convert the response in to a JSON array. This will make it easier to capture all the necessary details.
        json_response_us = response_us.json()['articles']
        json_response_in = response_in.json()['articles']
        json_response = json_response_us + json_response_in

        for article in json_response:
            try:
                print('Entered try.')

                url = article['url']
                extracted_article = g.extract(url=url)
                # Clean any \n that might exist in the article content.
                extracted_article_content = extracted_article.cleaned_text.replace('\n', ' ')
                print('Extracted article content.')

                inputs = tokenizer.encode("summarize: " + extracted_article_content, return_tensors="tf", max_length=512)
                outputs = model.generate(inputs, max_length=100, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
                summary = tokenizer.decode(outputs[0])

                # Remove the <pad> which is at the start of each sentence for some reason we do not know.
                summary = summary.lstrip("<pad> ")

                # Clean up the sentence, capitalize the first letter of each work of each sentence.
                sentences = summary.split(". ")
                intermediate_sentences = [sentence[0].capitalize() + sentence[1:] for sentence in sentences]
                summary = '. '.join(intermediate_sentences)

                # Do not use the article in case the length of the summary was less than 50 words.
                if len(summary.split()) < 40:
                    print('For some reason, the length of the summary was less than 40 words. So proceeding with the next item in the list.')
                    continue

                print(summary)

                print('Summarized article content.')
            except:
                print('An exception occurred while capturing the article content/summarizing the same. Continuing with the rest.')
                continue

            # Create the dict capturing all the details of the articles. This will eventually be added to the db.
            current_article = {
                'source': article['source']['name'],
                'title': article['title'],
                'url': article['url'],
                'url_to_img': article['urlToImage'],
                'ds': article['publishedAt'][:10],
                'summary': summary
            }

            articles.append(current_article)
            print('Added 1 article.')

        return articles
    else:
        return None

# To test things out.
# articles = get_top_headlines()

# for article in articles:
#     print(article['summary'])
