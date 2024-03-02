from flask import Flask, render_template, request
import pandas as pd
import pickle

df = pd.read_csv("data.csv")
similarity = pickle.load(open('cosineSimmilarity.pkl', 'rb'))

app =Flask(__name__)

@app.route('/')
def homePage():
    cities = sorted(df['city'])
    return(render_template("index.html",
                            cities = cities
                           ))

@app.route('/submit', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        name = str(request.form["cityName"])
        recommendcity = []
        url = []
        desc = []

        cityIndex = df[df['city'] == name].index[0]                 # FINDING INDEX OF SEARCED CITY IN DATAFRAME
        cosineSimillarity = list(enumerate(similarity[cityIndex]))  # FINDING COSINE SIMILARITY OF SEARCHED CITY WITH OTHER
        relatedCityDistance = sorted(cosineSimillarity, reverse=True, key=lambda x: x[1])[0:15]  # SORTING(DESCENDING) COSINE SIMILLARITY BASED
        for city in relatedCityDistance:
            j = city[0]
            recommendcity.append(df.iloc[j]['city'])
            url.append(df.iloc[j]['url'])
            desc.append(df.iloc[j]['desc'])
        return(render_template("result.html",
                               city = recommendcity,
                               url = url,
                               desc = desc))

if __name__ == "__main__":
    app.run(debug =True)