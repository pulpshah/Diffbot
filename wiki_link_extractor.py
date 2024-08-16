import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

diff_token = 'YOUR_TOKEN'
url = 'YOUR_URL'

# Takes in a main webpage (string) and words to exclude (list of strings)
# Extracts all of the links from that webpage, ensuring that duplicates and any links with undesired words are excluded
# Returns the filtered links (list of strings)
def extract_links_from_webpage(webpage, exclude=None):
    if exclude is None:
        exclude = []
        
    response = requests.get(webpage)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set(urljoin(webpage, a['href']) for a in soup.find_all('a', href=True))
        filtered_links = [link for link in links if not any(pattern in link for pattern in exclude)]
        return filtered_links
    else:
        print(f"Couldn't get the source page {webpage}. Status code: {response.status_code}")
        return []

# Takes in links (list of strings)
# Initializes several new lists to store different types of links
# Uses Diffbot to determine the type of a link, and stores it in its corresponding list
# Returns the updated and sorted links (lists of strings) 
def sort_types(links):
    transcript_refs = []
    image_refs = []
    video_refs = []
    article_refs = []
    other_refs = []

    for index, link in enumerate(links):
        # print(f"Processing link {index + 1}/{len(links)}: {link}")  
        encoded_url = quote(link, safe='')
        diffbot_url = f'https://api.diffbot.com/v3/analyze?token={diff_token}&url={encoded_url}'
        try:
            response = requests.get(diffbot_url)
            response.raise_for_status()
        
            data = response.json()
        
            if 'objects' not in data:
                print(f"No results found for {link}. Response data: {data}")
                continue
        
            results = data['objects']
            if results:
                for result in results:
                    obj_type = result.get('type')
                    text_content = result.get('text', '').lower()
                    if 'transcript' in text_content:
                        transcript_refs.append(link)
                    elif obj_type == 'image':
                        image_refs.append(link)
                    elif obj_type == 'video':
                        video_refs.append(link)
                    elif obj_type == 'article':
                        article_refs.append(link)
                    else:
                        other_refs.append(link)
        
        except requests.RequestException as e:
            print(f"Request failed for {link}: {e}")

    return transcript_refs, image_refs, video_refs, article_refs, other_refs

# Common phrases that return irrelevant links from a Wikipedia page
# Can be adapted for any webpage
exclude_words = [
    'wikipedia',
    'Wikipedia',
    'Special:',   
    'User:',     
    'File:',
    'Category:',
    'Policy:',
    'Help:',
    'Portal:',
    'wikidata',
    'wiktionary'
]

links = extract_links_from_webpage(url, exclude_words)
print(f"Links extracted: {links}")
print(f"Number of links: {len(links)}")

transcript_refs, image_refs, video_refs, article_refs, other_refs = sort_types(links)
print(f"Transcript References: {transcript_refs}")
print(f"Image References: {image_refs}")
print(f"Video References: {video_refs}")
print(f"Article References: {article_refs}")
print(f"Other References: {other_refs}")
