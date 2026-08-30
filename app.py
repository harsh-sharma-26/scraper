from flask import Flask, render_template, request
import re

from parsing import process_words
from myscheme_api import fetch_matching_schemes

app = Flask(__name__)  # Flask app ka object bana rahe hain


# Home page route - jab user webpage kholega
@app.route('/')
def home():
    return render_template('index.html')  # index.html render karke bhejega


# Search route - form submit hone par (form mode ya text mode dono se) yaha data aayega
@app.route('/search', methods=['POST'])
def search():
    # request.form ek dictionary jaisa object hai
    # 'query' wahi naam hai jo templates/index.html ke <input name="query"> me diya gaya hai
    user_input = request.form.get('query', '').strip()

    # Agar prompt empty hai, to bina crash hue simple page wapas bhej do
    if not user_input:
        return render_template('index.html')

    print("\n==============================")
    print("USER INPUT:", user_input)
    print("==============================")

    # text ko words ki list me tokenize karo (punctuation clean karke)
    words_list = re.findall(r'\w+', user_input)

    # parsing.py ko bhejke structured data nikalwao
    user_data = process_words(words_list)
    print("USER DATA:", user_data)

    # myScheme API se matching schemes lao (already processed, "fields" wrapper ke saath)
    schemes = fetch_matching_schemes(user_data)
    print(f"TOTAL SCHEMES FOUND: {len(schemes)}")

    # results UI me bhejo
    return render_template('index.html', result=schemes)


if __name__ == '__main__':
    app.run(debug=True)  # debug=True se error dikhte hain aur auto-reload hota hai
