from flask import Flask, render_template, request
import re

from parsing import process_words
from myscheme_api import fetch_matching_schemes

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():

    print("🔥 SEARCH ROUTE HIT")

    user_input = request.form.get('query', '').strip()

    # Agar prompt empty hai
    if not user_input:
        return render_template('index.html')

    print("\n==============================")
    print("USER INPUT:")
    print(user_input)
    print("==============================")

    # Words ko parser ke format mein convert karo
    words_list = re.findall(r'\w+', user_input)

    # User ki details extract karo
    user_data = process_words(words_list)

    print("\nUSER DATA:")
    print(user_data)

    # MyScheme API se matching schemes lao
    schemes_response = fetch_matching_schemes(user_data)

    # API response ke andar se actual schemes nikalo
    schemes = schemes_response.get("data", {}).get("hits", {}).get("items", [])

    print("\nACTUAL SCHEMES:")
    print(schemes)

    # Results UI mein bhejo
    return render_template(
        'index.html',
        result=schemes
    )


if __name__ == '__main__':
    app.run(debug=True)