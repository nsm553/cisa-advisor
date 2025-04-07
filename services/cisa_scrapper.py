from bs4 import BeautifulSoup
from utils import get_page_content, get_anchors, get_element_text_with_links
import json
import re

def parse_advisory_page(url):
    """
    Parse a CISA advisory page and convert it to a structured markdown format.
    Returns a dictionary containing the parsed content and metadata.
    """
    # html page content
    html_content = ""
    
    # Initialize the advisory data structure
    advisory_data = {}

    # For testing, use the local file
    if url is None:
        soup = BeautifulSoup(open("data/cisa-advisory.html", 'r', encoding='utf-8'), 'html.parser')
        html_content = soup.contents
    else:
        html_content = get_page_content(url)
        if not html_content:
            return None
        soup = BeautifulSoup(html_content, 'html.parser')

    advisory_data.update(parse_advisory_page_header(soup, url))
    advisory_data.update(parse_advisory_page_main(soup, url))
    advisory_data.update(parse_advisory_page_footer(soup, url))
    # print("-----\n\n----")
    # print(json.dumps(advisory_data))

    # save markdown as json
    # save page html as a single page

    return advisory_data, html_content

'''
Parse header elements - title, date, alert_code, related_topics
'''
def parse_advisory_page_header(soup, url):
    # Extract title
    headers = {}
    header_elem = soup.find('h1')
    if header_elem:
        headers["title"] = header_elem.get_text(strip=True)

    title_elems = soup.find(class_='c-page-title__content')

    if title_elems:                
        # for child in title_elem.find_all(class_=lambda x: x and ('c-field__label' in x or 'c-field__content' in x)):
        eles = title_elems.find_all('div', class_='c-field')
        for ele in eles:
            lbl = ele.find(class_='c-field__label')
            val = ele.find(class_='c-field__content')
            if lbl and val:
                headers[lbl.getText(strip=True)] = val.getText(strip=True)
        # parse topics
        topic_elements = title_elems.find_all('div', class_='c-top__topics')
        if topic_elements:
            topics = []
            for topic_element in topic_elements:
                topics.extend(get_anchors(topic_element))

            headers['Related topics'] = topics

    # Extract advisory ID from URL or title
    if url:
        advisory_id = url.split('/')[-1]
        headers["advisory_id"] = advisory_id
    elif headers["title"]:
        # Try to extract ID from title (e.g., "ICSA-25-091-01")
        id_match = re.search(r'ICSA-\d{2}-\d{3}-\d{2}', headers["title"])
        if id_match:
            headers["advisory_id"] = id_match.group()    

    return headers

'''
Parse main content - h2, h3, h4 elements
'''
def parse_advisory_page_main(soup, url):
    # print(f'proc_content: {type} FROM {content.getText(strip=True)}')
    markup = {}
    # parse child elements and siblings 
    main_content = soup.find('div', class_='l-full__main')

    if main_content is None:
        return markup

    sections = main_content.find_all(['h2', 'h3', 'h4', 'p', 'li'])
    current_section = None

    markdown_content = []
    for elem in sections:
        if elem.name in ['h2', 'h3', 'h4']:
            new_section = elem.get_text(strip=True)
            if current_section is None or new_section != current_section:
                markdown_content = []
                current_section = new_section
            
            markup[current_section] = markdown_content
        
        elif elem.name in ['p', 'li']:
            if current_section:
                # Convert HTML to markdown
                markdown_text = get_element_text_with_links(elem) #elem.get_text(strip=True)                
                markup[current_section].append(markdown_text)
                
    return markup

def parse_advisory_page_footer(soup, url):
    markup = {}

    footer = soup.find('div', class_='l-full__footer')
    if not footer:
        return markup

    sections = footer.find_all(['h2', 'h3'])

    for section in sections:
        section_name = section.get_text(strip=True)
        markup[section_name] = []
        section_parent = section.parent
        if not section_parent:
            continue
        tag_elements = section_parent.find_all('div', class_='c-field')
        
        for tag_element in tag_elements:
            tag_text = get_element_text_with_links(tag_element)
            markup[section_name].append(tag_text)

    return markup
