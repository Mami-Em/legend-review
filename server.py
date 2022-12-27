import json
import requests
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for, request

from cs50 import SQL


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# setting up the database
db = SQL(env.get("DATABASE_URL"))


# Controllers auth0 API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


# SEARCH
@app.route("/search")
def search():
    query = request.args.get("q")

    # listen to the user input
    if len(query) >= 3:
        show = db.execute(
            "SELECT * FROM anime WHERE LOWER(en_title) LIKE ?",
            "%" + query.lower() + "%"
        )

        # return any data from the db that match the user input
        if len(show) > 0:
            return render_template("search.html", show=show)

        return "No data found"

    # if input less than 3 char
    return ""


# ANIME DETAILS
@app.route("/details/<int:id>")
def details(id):
    anime_details_api = requests.get("https://kitsu.io/api/edge/anime/" + id)
    anime_details = anime_details_api.json()

    review_api = requests.get(anime_details['data']['relationships']['reviews']['links']['related'])
    anime_reviews = review_api.json()

    all_reviews = list()

    for i in range(3):
        review = anime_reviews['data'][i]

        reviews = review['attributes']['content']

        user_api = requests.get(review['relationships']['user']['links']['related'])
        user = user_api.json()

        try:
            all_reviews.append({
                "review": reviews,
                "user": user['data']['attributes']['name'],
                "profile": user['data']['attributes']['avatar']['original'],
                "publish_date": user['data']['attributes']['updatedAt']
            })
        except:
            ...


    mdb = db.execute("SELECT * FROM anime WHERE kitsu_id = ?", id)

    # return anime
    return render_template(
        "detail.html", 
        mdb = mdb,
        session=session.get("user"),
        all_reviews=all_reviews,
        anime=anime_details
    )

# /** TODO **/
# SEND REVIEW
# PROFILE


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
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run()