# app.py

from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
import requests


Final_df = pickle.load(open('Top.pkl', 'rb'))
Final_df1 = pickle.load(open('Final.pkl', 'rb'))

Rating = pickle.load(open('Rating.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
Pivot = pickle.load(open('pivot.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',

                           book_name=list(Final_df['Book-Title'].values),
                           author=list(Final_df['Book-Author'].values),
                           url=list(Final_df['Image-URL-M'].values),
                           rating=list(Rating['Mean-Rating'].values),
                           #    recomend=recomend(text)
                           #    year=list(Final_df['Year-Of-Publication'].values)
                           )

@app.route('/search', methods=['POST'])
def recomend():
    user_req = request.form.get("user_input")
    index = np.where(Pivot.index == user_req)[0]
    if len(index) == 0:
        # If no match found, display a message and any 5 images
        data = None
        return render_template('nofile.html')
    else:
        index = index[0]
        distances = similarity[index]
        Top5 = sorted(list(enumerate(distances)),
                      key=lambda x: x[1], reverse=True)[1:10]

        data = []
        for i in Top5:
            item = []
            temp_df = Final_df1[Final_df1['Book-Title'] == Pivot.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render_template('search.html', data=data)

app.run(debug=True)
