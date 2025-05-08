""" wsgi hook """
from app import create_app

args = [
    '--http', ':9091',
    '--enable-threads'
]

if __name__ == "__main__":
    create_app().run(host="localhost", port=8080, debug=True)