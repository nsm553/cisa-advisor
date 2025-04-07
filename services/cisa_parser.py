from bs4 import BeautifulSoup
from utils import get_page_content, get_anchors, get_element_text_with_links
import json
import re

def parse_advisory_page(url):
    """
    Parse a CISA advisory page and convert it to a structured format optimized for LLM consumption.
    Returns a dictionary containing the parsed content and metadata.
    """
    # html page content
    html_content = ""
    
    # Initialize the advisory data structure
    advisory_data = {
        "metadata": {},
        "content": {},
        "references": [],
        "recommendations": [],
        "vulnerabilities": []
    }

    # For testing, use the local file
    if url is None:
        soup = BeautifulSoup(open("data/cisa-advisory.html", 'r', encoding='utf-8'), 'html.parser')
        html_content = soup.contents
    else:
        html_content = get_page_content(url)
        if not html_content:
            return None
        soup = BeautifulSoup(html_content, 'html.parser')

    # Parse headers and add to metadata
    headers = parse_advisory_page_header(soup, url)
    advisory_data["metadata"] = headers
    
    # Parse main content
    main_content = parse_advisory_page_main(soup, url)
    advisory_data["content"] = main_content
    
    # Parse footer content
    footer_content = parse_advisory_page_footer(soup, url)
    
    # Extract references from footer
    if "References" in footer_content:
        advisory_data["references"] = footer_content["References"]
    
    # Extract recommendations from content
    if "Recommendations" in main_content:
        advisory_data["recommendations"] = main_content["Recommendations"]
    
    # Extract vulnerabilities from content
    if "Vulnerability Details" in main_content:
        advisory_data["vulnerabilities"] = main_content["Vulnerability Details"]
    
    # Generate a structured summary for LLM consumption
    advisory_data["llm_summary"] = {
        "title": headers.get("title", ""),
        "advisory_id": headers.get("advisory_id", ""),
        "date": headers.get("date", ""),
        "advisory_type": headers.get("advisory_type", ""),
        "cvss_score": headers.get("cvss_score", ""),
        "affected_products": headers.get("affected_products", []),
        "vendors": headers.get("vendors", []),
        "summary": headers.get("summary", ""),
        "key_points": extract_key_points(main_content),
        "impact": extract_impact(main_content),
        "mitigation": extract_mitigation(main_content)
    }
    
    print("-----\n\n----")
    print(json.dumps(advisory_data))

    return advisory_data, html_content

def extract_key_points(content):
    """Extract key points from the content for LLM consumption"""
    key_points = []
    
    # Look for sections that might contain key points
    key_sections = ["Executive Summary", "Overview", "Summary"]
    for section in key_sections:
        if section in content:
            key_points.extend(content[section])
    
    return key_points

def extract_impact(content):
    """Extract impact information from the content"""
    impact = []
    
    # Look for sections that might contain impact information
    impact_sections = ["Impact", "Vulnerability Details", "Technical Details"]
    for section in impact_sections:
        if section in content:
            impact.extend(content[section])
    
    return impact

def extract_mitigation(content):
    """Extract mitigation information from the content"""
    mitigation = []
    
    # Look for sections that might contain mitigation information
    mitigation_sections = ["Mitigation", "Recommendations", "Workarounds"]
    for section in mitigation_sections:
        if section in content:
            mitigation.extend(content[section])
    
    return mitigation

'''
Parse header elements - title, date, alert_code, related_topics
'''
def parse_advisory_page_header(soup, url):
    headers = {}
    
    # Extract title
    header_elem = soup.find('h1')
    if header_elem:
        headers["title"] = header_elem.get_text(strip=True)
    
    # Extract date
    date_elem = soup.find('time')
    if date_elem:
        headers["date"] = date_elem.get_text(strip=True)
    
    # Extract advisory ID from URL or title
    if url:
        advisory_id = url.split('/')[-1]
        headers["advisory_id"] = advisory_id
    elif "title" in headers:
        # Try to extract ID from title (e.g., "ICSA-25-091-01")
        id_match = re.search(r'ICSA-\d{2}-\d{3}-\d{2}', headers["title"])
        if id_match:
            headers["advisory_id"] = id_match.group()
    
    # Extract advisory type
    advisory_type_elem = soup.find('div', class_='c-teaser__meta')
    if advisory_type_elem:
        headers["advisory_type"] = advisory_type_elem.get_text(strip=True)
    
    # Extract CVSS score if available
    cvss_elem = soup.find(string=re.compile('CVSS', re.IGNORECASE))
    if cvss_elem:
        cvss_parent = cvss_elem.find_parent()
        if cvss_parent:
            cvss_text = cvss_parent.get_text(strip=True)
            cvss_match = re.search(r'CVSS\s+v3\s+score:\s+(\d+\.\d+)', cvss_text, re.IGNORECASE)
            if cvss_match:
                headers["cvss_score"] = cvss_match.group(1)
    
    # Extract affected products
    affected_elem = soup.find(string=re.compile('Affected Products', re.IGNORECASE))
    if affected_elem:
        affected_section = affected_elem.find_parent()
        if affected_section:
            affected_list = affected_section.find_next('ul')
            if affected_list:
                headers["affected_products"] = [item.get_text(strip=True) for item in affected_list.find_all('li')]
    
    # Extract vendor information
    vendor_elem = soup.find(string=re.compile('Vendor', re.IGNORECASE))
    if vendor_elem:
        vendor_section = vendor_elem.find_parent()
        if vendor_section:
            vendor_list = vendor_section.find_next('ul')
            if vendor_list:
                headers["vendors"] = [item.get_text(strip=True) for item in vendor_list.find_all('li')]
    
    # Extract related topics
    topic_elements = soup.find_all('div', class_='c-top__topics')
    if topic_elements:
        topics = []
        for topic_element in topic_elements:
            topics.extend(get_anchors(topic_element))
        headers["related_topics"] = topics
    
    # Extract summary if available
    summary_elem = soup.find(string=re.compile('Summary', re.IGNORECASE))
    if summary_elem:
        summary_section = summary_elem.find_parent()
        if summary_section:
            summary_text = summary_section.find_next('p')
            if summary_text:
                headers["summary"] = summary_text.get_text(strip=True)
    
    return headers


def parse_advisory_page_head(soup, url):
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
