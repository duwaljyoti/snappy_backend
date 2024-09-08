from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def my_view(request):
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
