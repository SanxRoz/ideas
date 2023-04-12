from flask import Flask, render_template, request, jsonify
import requests
import openai

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/submit', methods=['POST'])
def submit():

    getdata = request.json['inputValue']
    value, open_ai_cookie = getdata.split(';')

    if not open_ai_cookie:
        return jsonify({'message': 'No OpenAI key, check https://platform.openai.com/account/api-keys for your key'})
    else:
        try:
            openai.api_key = f"{open_ai_cookie}"
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": '''Generate a humorous and entertaining roast of ideas that the user provide, a roast that will make me laugh out loud and be rude!. No more than 400 characters. Give me 1 recommendation to improve the idea'''},{"role": "user", "content": f"{value}"}])

            return jsonify({'message': completion.choices[0].message.content})
        except requests.exceptions.RequestException as err:
            print('Something went wrong:', err)
            return jsonify({'message': 'Something went wrong'}), 500


if __name__ == '__main__':
    app.run(debug=True)