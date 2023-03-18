from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_API_KEY="996a924cdc6b3524f6e93703f4a204a4"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my-movies.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(100), nullable=True)
    img_url = db.Column(db.String(200), nullable=False)
db.create_all()


class RateMovieForm(FlaskForm):
    rating = StringField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class FindMovie(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


# new_movie = Movie(
#     id=1,
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=["GET", "POST"])
def rate_movie():
    edit_form = RateMovieForm()
    movie_id = request.args.get('id')
    movie_selected = Movie.query.get(movie_id)
    if edit_form.validate_on_submit():
        # movie_selected.rating = request.form['rating']
        # movie_selected.review = request.form['review']
        movie_selected.rating = float(edit_form.rating.data)
        movie_selected.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("rate_movie.html", form=edit_form, movie=movie_selected)


@app.route('/delete')
def delete_movie():
    movie_id  = request.args.get('id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/find", methods=["GET", "POST"])
def find():
    form = FindMovie()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()['results']
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route('/select')
def select():
    movie_id = request.args.get('id')
    print(movie_id)
    url = "https://api.themoviedb.org/3/movie"
    movie_api_url = f"{url}/{movie_id}"
    response = requests.get(movie_api_url, params={'api_key': MOVIE_DB_API_KEY, 'language': 'en-US'})
    data = response.json()
    print(data)
    MOVIE_DB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500/'
    new_movie = Movie(
        title = data['original_title'],
        year = data['release_date'].split('-')[0],
        img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        description = data['overview']
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('rate_movie', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
