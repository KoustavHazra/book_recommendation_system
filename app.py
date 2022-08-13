from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
popular_df = pickle.load(open('popular.pkl', 'rb'))  # rb means, read it in read binary mode
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values))


@app.route('/recommendation')
def recommendation_ui():
    return render_template('recommendation.html')


@app.route('/recommended_books', methods=['POST'])
def recommended_books():
    user_input = request.form.get('user_input')
    # first it'll fetch book names from the index
    check = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[check])), key=lambda x: x[1], reverse=True)[1:6]

    data = list()
    for i in similar_items:
        item = list()
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]

        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        data.append(item)
    print(data)
    return render_template('recommendation.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
