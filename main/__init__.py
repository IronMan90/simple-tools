from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret_key_for_test'

from main import routes
