from flask import Flask
from utils.logging_config import setup_logging

setup_logging()
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
