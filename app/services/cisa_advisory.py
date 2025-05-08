# Install with pip install firecrawl-py
import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp, ScrapeOptions
from datetime import datetime
from flask import jsonify, request, Blueprint, Response
from .utils import toInt
from app.models import cisa_model

adv = Blueprint("advisories", __name__)

BASE_URL="https://www.cisa.gov/news-events/cybersecurity-advisories"

@adv.route("/advisories", methods=["GET"])
def advisories():
    """
    Search for cyber security advisories
    [GET] /advisories
    
    Request Body:
    {
        "limit_matches" : Number of matches
        "max_depth" : Maximum pages to search
    }
    
    Response:
    {
        "{message}": [.. results ..]
    }
    """
        
    limit = request.args.get('limit')
    if limit:
        limit = toInt(limit)
    else:
        limit = 1
    max_depth = request.args.get('max_depth')
    if max_depth:
        max_depth = toInt(max_depth) 
    else:
        max_depth = 1

    data = []
    try:
        app = FirecrawlApp()

        sc = ScrapeOptions(
            formats=[ 'markdown'],
            onlyMainContent=False,
            excludeTags=[ 'script' ]    
        )

        # result = "<html><title>Cyber Security Advisories AI Agent</title></html>"
        # return {result: "ok"}, 200
        result = app.crawl_url(
            url=BASE_URL, 
            limit=limit,
            max_depth=max_depth,
            exclude_paths=[ 'news-events/alerts/.+' ],
            include_paths=[ 'news-events/cybersecurity-advisories/.+' ],            
            scrape_options=sc,
        )

        res_json_schema = result.model_json_schema()
        res_json = result.model_dump_json()
        print(f"status: {result.status}")

        for d in result.data:
            print(f"data: {d.markdown}") 
            data.append(d.markdown)          # print(f"data markdown: {d.markdown['data']['markdown']['markdown']['markdown']['markdown']}")          
        return Response(data, mimetype='text/plain', status=200)

    except Exception as e:
        return jsonify(error=str(e)), 500


@adv.route("/search", methods=["GET"])
def scrape_advisories():
    """
    Search for cyber security advisories
    [GET] /search
    
    Request Body:
    {
        "search_term" : Search term
        "limit_matches" : Number of matches
        "max_depth" : Maximum pages to search
    }
    
    Response:
    {
        "{message}": [.. results ..]
    }
    """

    search_term = request.args.get('search_term')
    if not search_term:
        return jsonify(error="Required argument: search_term is not available"), 400

    # Implement search logic here
    # ...
    try:
        app = FirecrawlApp()

        params={
            "formats": ["markdown"],
            "extract": {
                # "schema": cisa_model.Advisory.model_json_schema(),
                "prompt": "Extract information based on the schema provided",
                "systemPrompt": f"You are a cybersecurity expert. Extract information from the advisory that matches with {search_term}.",
            },
        }

        result = app.scrape_url(
            url=BASE_URL,
            extract=params,  
            includeTags=["h1", "h2", "h3", "p", "ul", "li"],
            excludeTags=["script", "style"],
            formats= ["markdown"],
        )

        res_json_schema = result.model_json_schema()
        res_json = result.model_dump_json()
        data = []
        for d in result.data:
            print(f"data: {d.markdown}") 
            data.append(d.markdown)          # print(f"data markdown: {d.markdown['data']['markdown']['markdown']['markdown']['markdown']}")      
        return Response(result.markdown, mimetype='text/plain', status=200)

    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    advisories()