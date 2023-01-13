import requests
from datetime import datetime
from flask import Flask, render_template, request, session, flash, redirect, url_for,jsonify
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

# setting up the database
db = SQL(env.get("DATABASE_URL"))

@app.route("/")
def index():
    trending_endpoints = requests.get("https://kitsu.io/api/edge/trending/anime")
    trending = trending_endpoints.json()

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

    
    # db reviews
    myreview_db = db.execute("SELECT * FROM review review WHERE anime_id = ?", id)
    reviews = list()
    for item in myreview_db:
        user = db.execute("SELECT _name, picture from userdb where id = ?", item["sender_id"])

        reviews.append({
            "review": item["content"],
            "sender": user[0]["_name"],
            "sender_picture": user[0]["picture"],
            "rate": int(item["rate"]),
            "posted_at": item["posted_at"]
        })


    return render_template(
        "details.html", 
        anime = anime, 
        rating = rating, 
        total_avg = total_avg,
        review = review,
        reviews = reviews,
        session = session.get("user")
    )



@app.route("/send_review/<int:id>", methods = ["POST","GET"])
def send_review(id):

    if not request.method == "POST":
        return "Use /post method instead"

    review_sent = {
        "content": request.form.get("review"),
        "rate": request.form.get("rate"),
        "anime_id": id
    }

    # user id
    sender_id = db.execute(
        "SELECT id FROM userdb WHERE _email = ?",
        session.get("user")["userinfo"]["email"]
    )

    try:
        # check in the db
        reviewDB = db.execute(
            "SELECT * FROM review WHERE sender_id = ? AND anime_id = ?", 
            sender_id[0]['id'], 
            review_sent["anime_id"]
        )
    except:
        flash("Something went wrong during the operation")

    # check if user already left a review
    if len(reviewDB) > 0:
        flash("You already left a review")


    db.execute(
        "INSERT INTO review (sender_id, anime_id, rate, content, posted_at) VALUES (?,?,?,?,?)", 
        sender_id[0]['id'], 
        review_sent["anime_id"], 
        review_sent["rate"],
        review_sent["content"],
        datetime.now()
    )
   
    return render_template("message.html")



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


