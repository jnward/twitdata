from flask import Flask
app = Flask(__name__, template_folder='static/html')

import tweet_papers.views