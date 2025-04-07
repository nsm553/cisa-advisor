import os
import requests

def create_output_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    
'''
Get anchors with text and uri
'''  
def get_anchors(element):
    links_with_text = []
    sub_elements = element.find_all('a')
    for sub_element in sub_elements:
        link_text = f"[{sub_element.getText(strip=True)}]({sub_element.get('href')})"
        links_with_text.append(link_text)

    return links_with_text    


'''
Get text, text including uri
'''    
def get_element_text_with_links(element):
    """Get element text while preserving hyperlinks in markdown format"""
    if not element:
        return ""
    
    text_parts = []
    for content in element.contents:
        if content.name == 'a':
            # Convert link to markdown format [text](url)
            text_parts.append(f"[{content.get_text(strip=True)}]({content.get('href', '')})")
        elif content.name is None:  # Text node
            text_parts.append(content.string.strip() if content.string else '')
        else:  # Other HTML elements
            text_parts.append(content.get_text(strip=True))
    
    return ' '.join(text_parts)