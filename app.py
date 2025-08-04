from flask import Flask
import requests
import yaml
import urllib3

app = Flask(__name__)

@app.route("/")
def home():
    return "Dependency patched app running securely."

if __name__ == "__main__":
    app.run(debug=True)
