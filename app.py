import requests
from flask import Flask, render_template, request, session, flash, redirect, url_for
from helpers import rating_percentage, avg_rating, avg_rating2
from cs50 import SQL

from functools import wraps
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app = Flask("__app__")
app.secret_key = env.get("APP_SECRET_KEY")

# auth0
oauth = OAuth(app)

# first time user
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)



@app.route("/")
def index():
    trending_endpoints = requests.get("https://kitsu.io/api/edge/trending/anime")
    trending = trending_endpoints.json()
    return render_template("index.html", trending = trending, session = session.get("user"))


@app.route("/about")
def about():
    return render_template("about.html", session = session.get("user"))



@app.route("/profile")
def profile():
    return render_template("profile.html", session = session.get("user"))


@app.route("/search")
def search():
    query = request.args.get("q")
    enpoints = requests.get(f"https://kitsu.io/api/edge/anime?filter[text]={query.replace(' ','%20')}&page[limit]=20")
    anime = enpoints.json()

    # json format
    return render_template("result.html", anime = anime)


@app.route("/details/<int:id>")
def details(id):
    endpoints = requests.get(f"https://kitsu.io/api/edge/anime/{id}")
    anime = endpoints.json()

    # format percentage of ratings and reviews
    rating = rating_percentage(anime['data']['attributes']['ratingFrequencies'])
    total_avg = avg_rating(anime['data']['attributes']['averageRating'])

    # comments and users
    comments_ep = requests.get(f"https://kitsu.io/api/edge/anime/{id}/reviews?sort=-updatedAt&include=user")
    comments = comments_ep.json()    


    # fetch all reviews
    review = list()
    for item in comments['data']:


        try:
            # fetch user name & avatar
            user_id = item['relationships']['user']['data']['id']
            user_ep = requests.get(f"https://kitsu.io/api/edge/users/{user_id}?fields[users]=name,avatar")
            user = user_ep.json()

            review.append({
                "review": item['attributes']['content'],
                "rate": avg_rating2(item['attributes']['rating']),
                "username": user['data']['attributes']['name'],
                "avatar": user['data']['attributes']['avatar']['original']
            })

        except:
            ...


    return render_template(
        "details.html", 
        anime = anime, 
        rating = rating, 
        total_avg = total_avg,
        review = review,
        session = session.get("user")
    )



@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


