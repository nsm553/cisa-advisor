from dotenv import load_dotenv
import os
from flask import Flask, current_app
from markupsafe import Markup
from flask_cors import CORS

load_dotenv()
Markup()
Markup('')

"""
CISA Advisor project.
""" 

def create_app():
    
    app = Flask(__name__)
    cors = CORS(app)

    vars = ["FIRECRAWL_API_KEY"]
    # Note: Every module in this app assumes the app context is available and initialized.
    with app.app_context():
        for var in vars:
            if var not in os.environ:
                raise Exception(f"Environment variable {var} is not set")
    
    from app.services.cisa_advisory import adv

    app.register_blueprint(adv)
    
    with app.app_context():
        current_app.route('/')

    return app
