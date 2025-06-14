from urllib.parse import unquote

from django.http import JsonResponse, HttpResponse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import urljoin

BASE_URL = 'https://ekantipur.com/'  # Define the base URL globally

def get_image_url_updated(news):
    img_src = 'https://www.shutterstock.com/image-vector/newspaper-icon-theme-symbol-vector-260nw-2490697095.jpg'
    img_class = news.find('div', class_='image')
    if img_class:
        img_tag = img_class.find('img')
        if img_tag and ('src' in img_tag.attrs or 'data-src' in img_tag.attrs):
            img_src = img_tag.get('src') or img_tag.get('data-src', '')
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
    return img_src


def another_method():
    test_tesxt = """
    राजविराज — सप्तरीको मलेकपुरमा शनिबार दिउँसो ट्र्याक्टरको पछाडि भागमा मोटरसाइकल ठोक्किँदा मृत्यु भएका दुईजना र घाइतेको परिचय खुलेको छ ।\n\n\n\nसप्तरी प्रहरी प्रमुख एसपी ढकेन्द्र खतिवडाका अनुसार घटनामा मृत्यु हुनेहरुमा विष्णुपुर गाउँपालिका-१ जमुनि मध्यपुराका १९ वर्षीय सन्तोष यादव र २२ वर्षीय सागर मण्डल रहेका छन् । उनीहरुको शव गजेन्द्रनारायाण सिंह अस्पताल राजविराज सप्तरीको शव गृहमा राखिएको छ । घटनामा सोही स्थानका १८ वर्षीय धनञ्जय यादवको अवस्था गम्भीर छ । उनलाई थप उपचारका लागि विराटनगर पठाइएको छ ।\n\nपत्थरगाढाबाट राजविराजतर्फ आउँदै गरेको इट्टा लोड भएको स १ त ५४४२ नं. को ट्र्याक्टर र विपरीत दिशाबाट जाँदै गरेको म.प्र.०२-०१९ प ९६२६ नं. को मोटरसाइकल ट्र्याक्टरको पछाडिको भागमा ठोकिँदा दुईजनाको मृत्यु भएको हो ।,
    """

    something = summarise_with_mistral_ai(test_tesxt)
    print(something.json())
    return something
    # return JsonResponse({'data': something}, status=500)


def my_view(request):
    another_method()
    return JsonResponse({'status': 'ok'})
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
    for index, news in enumerate(main_news_section):
        title_tag = news.find('a')
        description_tag = news.find('p')
        # time_tag = news.find('time')

        # Ensure tags are found before extracting text
        if title_tag and description_tag:
            relative_url = title_tag.get('href')  # This might be relative
            full_link = urljoin(BASE_URL, relative_url)  #
            # time_str = time_tag.get_text(strip=True)

            # Assuming the news are from the current date, you can modify this as needed
            # full_datetime = datetime.now().strftime('%Y-%m-%d ') + time_str
            # Append the news to the list
            extracted_news = extract_article_content(full_link)
            news_list.append({
                "id": index,
                "title": title_tag.get_text(strip=True),
                "description": description_tag.get_text(strip=True),
                "link": full_link,
                "image_url": get_image_url_updated(news),
                # "whole_news": get_whole_news(full_link),
                "extracted_news": extracted_news,
                "summarised_news": summarise_with_mistral_ai(extracted_news),
            })


    return JsonResponse(news_list, safe=False)


def summarise_with_mistral_ai(dynamic_content):
    if "Content div not found." in dynamic_content:
        return {
            "success": False,
            "summary": "",
            "error": "No content to summarise – content div not found."
        }

    try:
        url = "https://api.mistral.ai/v1/chat/completions"
        api_key = "GNlXNSgk6TX2moXptFNhqh4U3RYxEfIw"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": "mistral-large-latest",
            "messages": [{"role": "user", "content": 'summarise the following text in 60 words in nepali language: ' + dynamic_content}],
        }
        response = requests.post(url, headers=headers, json=payload)
    except requests.RequestException as e:
        response = {
            "success": False,
            "error": "Invalid JSON response"
        }
    return response

def get_image_urls(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({  # Changed from [] to proper response
            'status': 'error',
            'message': 'No URL provided'
        }, status=400)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error fetching URL: {str(e)}'
        }, status=400)

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tags = soup.find_all("div", class_="image")

        if not div_tags:
            return JsonResponse({
                'status': 'error',
                'message': 'No image divs found'
            }, status=404)

        for div_tag in div_tags:
            print("Found <div> with class 'image':", div_tag)
            figure_tag = div_tag.find("figure")

            if figure_tag:
                img_tag = figure_tag.find("img")
                if img_tag and img_tag.has_attr("data-src"):
                    return JsonResponse({
                        'status': 'success',
                        'url': unquote(img_tag["data-src"]),
                        'message': 'URL received successfully'
                    })

        # If we've gone through all div tags and found nothing
        return JsonResponse({
            'status': 'error',
            'message': 'No valid image found in the page'
        }, status=404)

    except Exception as e:
        print(f"Error parsing the HTML content: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error parsing content: {str(e)}'
        }, status=500)


def extract_article_content(url = ''):
    # url = 'https://ekantipur.com/en/news/2025/02/21/what-happened-in-the-world-today-53-50.html'
    if not url:
        url = 'https://ekantipur.com/news/2025/02/23/the-state-government-plays-an-effective-role-in-solving-the-land-problem-chief-minister-acharya-34-52.html'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the div with the specified class
        content_div = soup.find('div', class_='col-md-12 desc-content')
        content_div = soup.find('div', class_='current-news-block')
        if content_div:
            # Extract text from all <p> tags within the div
            # paragraphs = content_div.find_all('p')
            paragraphs = [p for p in content_div.find_all('p') if "warningMessage" not in p.get("class", [])]
            article_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
            return article_text
        else:
            return "Content div not found."
    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}"


def get_whole_news(url):
    # Validate the URL
    if not url:
        return ''

    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ''

    try:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to remove ad container if it exists
        ad_element = soup.find('i', class_='icon-close')
        if ad_element:
            ad_div = ad_element.find_parent('div')
            if ad_div:
                ad_div.decompose()  # Removes the ad div completely from soup

        # Find the main content container
        # main_content = soup.find('div', class_='description current-news-block portrait')
        # main_content = soup.select_one('div.description.current-news-block.portrait')
        main_content = soup.find('div', class_=['description', 'current-news-block', 'portrait'])

        if not main_content:
            print("Main content block not found.")
            return ''

        # Initialize a list to hold the text content
        news_text = []

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
                # Extract the image URL if needed
                img_url = element.get('src', '')
                if img_url:
                    news_text.append(f"[Image: {img_url}]")

        # Combine the text into a single string
        full_news_text = ' '.join(news_text)
        return full_news_text

    except Exception as e:
        print(f"Error parsing the HTML content: {e}")
        return ''


def check_heath(request):
    return JsonResponse({'working': True, 'last_update_time': datetime.now()})

