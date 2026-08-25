from flask import Flask, render_template, request
import re

app = Flask(__name__)  # Flask app ka object bana rahe hain

# Home page route - jab user webpage kholega
@app.route('/')
def home():
    return render_template('index.html')  # index.html render karke bhejega

# Search route - form submit hone par yaha data aayega
@app.route('/search', methods=['POST'])
def search():
    # request.form ek dictionary jaisa object hai
    # 'query' wahi naam hai jo humne <input name="query"> me diya tha
    user_input = request.form.get('query')

    print("User ne search kiya:", user_input)  # terminal me check karne ke liye

    # yaha tum apna processing kar sakte ho
    # e.g. database search, filtering, API call, etc.
    #processed_result = user_input.upper()  # example: uppercase kar diya
    words_list = re.findall(r'\w+', user_input)
    # wapas same page render karo, result variable ke saath
    return render_template('index.html', result=words_list)

if __name__ == '__main__':
    app.run(debug=True)  # debug=True se error dikhte hain aur auto-reload hota hai