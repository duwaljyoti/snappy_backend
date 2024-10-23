from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, MBartTokenizer


model_name = "facebook/mbart-large-cc25"
model = MBartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
tokenizer = MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")
tokenizer.src_lang = "ne_NP"
tokenizer.tgt_lang = "ne_NP"

def my_vieww(request):
    online_portals = [
        'https://www.onlinekhabar.com/',
    ]
    # URL of the website
    url = 'https://ekantipur.com/'

    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section with the class 'main-news'
    main_news_section = soup.find_all('article', class_='normal')

    # Initialize an empty list to store the news
    news_list = []

    # Loop through the news items in the 'main-news' section
    for news in main_news_section:
        title_tag = news.find('a')
        description_tag = news.find('p')
        # time_tag = news.find('time')

        # Ensure tags are found before extracting text
        if title_tag and description_tag:
            # time_str = time_tag.get_text(strip=True)

            # Assuming the news are from the current date, you can modify this as needed
            # full_datetime = datetime.now().strftime('%Y-%m-%d ') + time_str

            # Append the news to the list
            news_list.append({
                "title": title_tag.get_text(strip=True),
                "description": description_tag.get_text(strip=True),
                "link": title_tag.get('href'),
                "whole_news": get_whole_news(title_tag.get('href'))
            })

    return JsonResponse(news_list, safe=False)


def test_punkt(request):
    # import nltk
    # nltk.download('punkt')  # Ensures punkt is downloaded before using any NLTK functionality
    # Your summarization or NLTK code goes here
    return JsonResponse({'message': 'Punkt downloaded successfully!'})

def get_whole_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main content container
    main_content = soup.find('div', class_='description current-news-block portrait')

    # Initialize a list to hold the text content
    news_text = []

    print('=>', main_content)
    # Loop through all the elements in the main content
    for element in main_content.children:
        # Check if the element is a paragraph tag (<p>)
        if element.name == 'p':
            # Add the paragraph text to the news_text list
            news_text.append(element.get_text(strip=True))
        # Skip <a> tags that might be ads
        elif element.name == 'a' and 'static-sponsor' in element.get('class', []):
            continue
        # Handle images or other content as needed
        elif element.name == 'img':
            # You can extract the image URL if needed
            img_url = element['src']
            news_text.append(f"[Image: {img_url}]")

    # Combine the text into a single string
    full_news_text = ' '.join(news_text)

    print(full_news_text)


def check_heath(request):
    return JsonResponse({'working': True, 'last_update_time': datetime.now()})


def my_view(request):
    text = '''दिल्लीबाट अवतरण भएलगत्तै भिस्ताराको जहाजमा आएका सबै यात्रु, लगेज, कार्गो चेकजाँच भइरहेको छ,’विमानस्थल स्रोतले भन्यो,‘प्रहरी र सेनाले जहाजलाई निगरानी गरेर जाँच गरिरहेका छन् ।’

जहाज अवतरण भएलगत्तै बम राखिएको खबर भिस्ताराको काठमाडौंस्थित कार्यालयमा कार्यरत भारतीय कर्मचारी सुमन शर्मालाई आएको थियो । स्रोतका अनुसार, शर्माले जहाज अवतरण भएलगत्तै दौडेर टर्मिनल कार्यालयलाई अज्ञात नम्बरबाट आफ्नो जहाजमा बम राखिएको फोन आएको जानकारी दिएका थिए ।

कुनै पनि वायुयानमा बमको हल्ला प्राप्त भएपछि जहाजलाई सुरक्षाकर्मीले नियन्त्रणमा लिई बम रहे नरहेको यकिन गर्ने अर्न्तराष्ट्रिय प्रोटोकल छ । त्यसैअनुसार, विमानस्थलको पार्किङ्गवेमा राखिएको जहाजलाई नेपाली सेना र प्रहरीले नियन्त्रण लिई जाँच गरिरहेको विमानस्थल कार्यालयले जनाएको छ ।'''
    summary = summarize_nepali_text(text)
    return JsonResponse({"summary": summary})


def my_view3(request):
    url = 'https://www.ratopati.com/'

    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve the webpage'}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []

    for article in soup.find_all('h2'):
        try:
            title = article.get_text(strip=True)
            if article.find('a'):
                link = article.find('a').get('href', None)
            else:
                link = ''

            if link and 'story' in link:
                news_data.append({
                    'title': title,
                    'link': link,
                    'full_news': scrape_article_content(link),
                    'summarized': summarize_nepali_text(scrape_article_content(link))
                })

        except AttributeError:
            continue

    return JsonResponse({'news': news_data})


def check_string_no_chars(s, forbidden_chars):
    # Check if the string `s` does not contain any of the characters in `forbidden_chars`
    return all(char not in s for char in forbidden_chars)

def scrape_article_content(url):
    # url = 'https://www.ratopati.com/story/449844/-security-personnel-operating-across-the-country-in-uddhar'
    response = requests.get(url)

    if response.status_code != 200:
        print('Failed to retrieve the webpage')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the heading of the article
    heading = soup.find('h2', class_='heading')  # Adjust based on the actual class
    if heading:
        print(f"Heading: {heading.get_text(strip=True)}")

    # Extract the main article body
    article_content = soup.find('div', class_='news-contentarea')  # Adjust based on actual class
    if article_content:
        return article_content.get_text(strip=True)
        # print(f"Content: {article_content.get_text(strip=True)}")
    else:
        print("Article content not found")


def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("nepali"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join(str(sentence) for sentence in summary)
    return summary_text


def summarize_nepali_text(text):
    print('testing')
    # Tokenize the input text (convert it into input IDs)
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate summary (you can control the length of the summary using max_length)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode the generated summary back to text
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return summary
