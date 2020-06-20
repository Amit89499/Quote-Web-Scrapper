import os

from bs4 import BeautifulSoup
import requests
from flask import Flask, request, render_template, redirect, jsonify
from flask_cors import CORS,cross_origin


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def home():
    return render_template('home.html')


@app.route('/result', methods = ['GET', 'POST'])
@cross_origin()
def result():
    if request.method == 'POST':
        searchString = request.form['quote'].replace(' ', '')
        print(searchString)

        url = 'https://www.brainyquote.com/search_results?q=' + searchString
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())

        quotes = soup.find('div', id='quotesList')
        # print(len(quotes))

        filename = 'happy' + '.csv'
        fw = open(filename, 'w+')
        headers = 'Quote, Written by \n'
        fw.write(headers)

        list_of_quotes = []

        for quote in quotes:
            try:
                Quote = quote.div.div.div.a.text
                # print(Quote)

                try:
                    Writer = quote.div.div.div.div.a.text
                    # print(Writer)
                except:
                    Writer = None

                # print()

                myDict = {'Quote': Quote, 'Writer': Writer}
                list_of_quotes.append(myDict)

            except:
                pass




        return render_template('result.html', list_of_quotes = list_of_quotes)
    else:
        return render_template('home.html')


# port = int(os.getenv("PORT"))
if __name__ == '__main__':
    app.run(debug=True)