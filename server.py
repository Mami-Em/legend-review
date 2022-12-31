import json
import requests
from datetime import datetime
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for, request, flash

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

    if session:
        # collect user data
        user = {
            "name": session.get('user')['userinfo']['name'],
            "email": session.get('user')['userinfo']['email'],
            "picture": session.get('user')['userinfo']['picture']
        }

        userInDb = db.execute("SELECT * FROM userdb WHERE _email = ?", user['email'])


        registration = datetime.now()

        # if user not in db yet
        if len(userInDb) == 0:
            db.execute(
                "INSERT INTO userdb (_name, _email, first_login, picture) VALUES (?,?,?,?)", 
                user['name'], 
                user['email'],
                registration.strftime("%B %d, %Y %I:%M %p"),
                user['picture']
            )

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
    show = db.execute(
        "SELECT * FROM anime WHERE LOWER(en_title) LIKE ?",
        "%" + query.lower() + "%"
    )

    # return any data from the db that match the user input
    if len(show) > 0:
        return render_template("search.html", show=show)

    return "No data found"



# ANIME DETAILS
@app.route("/details/<int:id>")
def details(id):
    anime_details_api = requests.get(f"https://kitsu.io/api/edge/anime/{id}")
    anime_details = anime_details_api.json()

    review_api = requests.get(anime_details['data']['relationships']['reviews']['links']['related'])
    anime_reviews = review_api.json()

    all_reviews = list()

    for i in range(4):

        try:
            review = anime_reviews['data'][i]

            reviews = review['attributes']['content']

            user_api = requests.get(review['relationships']['user']['links']['related'])
            user = user_api.json()

            all_reviews.append({
                "review": reviews,
                "user": user['data']['attributes']['name'],
                "profile": user['data']['attributes']['avatar']['original'],
                "publish_date": user['data']['attributes']['updatedAt']
            })
        except:
            ...


    myreview_db = db.execute("SELECT * FROM review review WHERE anime_id = ?", id)
    reviews = list()
    for review in myreview_db:
        user = db.execute("SELECT _name, picture from userdb where id = ?", myreview_db[0]["sender_id"])

        reviews.append({
            "review": myreview_db[0]["content"],
            "sender": user[0]["_name"],
            "sender_picture": user[0]["picture"],
            "posted_at": myreview_db[0]["posted_at"]
        })

    # return anime
    return render_template(
        "details.html", 
        session=session.get("user"),
        all_reviews=all_reviews,
        db_reviews=reviews,
        anime=anime_details
    )


# SEND REVIEW
@app.route("/send_review/<int:anime_id>", methods=["GET","POST"])
def send_review(anime_id):

    # if method not post
    if not request.method == "POST":
        flash("Please use correct method", "error")
        return render_template("message.html")

    review = request.form.get("review")
    sender_id = db.execute("SELECT id FROM userdb WHERE _email = ?", session.get("user")["userinfo"]["email"])

    # check in the db
    reviewDB = db.execute(
        "SELECT * FROM review WHERE sender_id = ? AND anime_id = ?", 
        sender_id[0]['id'], 
        anime_id
    )

    # check if user already left a review
    if len(reviewDB) > 0:
        flash("You left a comment already!")
        return render_template("message.html")


    db.execute(
        "INSERT INTO review (sender_id, anime_id, content, posted_at) VALUES (?,?,?,?)", 
        sender_id[0]['id'], 
        anime_id, 
        review,
        datetime.now()
    )

    flash("Review added!", "success")
    return render_template("message.html")



# /** TODO **/
# PROFILE
@app.route("/profile")
def profile():
    if not session:
        return "Please Login first"

    return json.dumps(session.get("user"), indent=4)


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