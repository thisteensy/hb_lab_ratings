"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """view homepage"""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():    
    """getting all movies"""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """get movie by id"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def show_all_users():
    """get user profile"""
    
    users = crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def user_profile(user_id):
    """display user profile"""

    user = crud.show_user_profile(user_id)

    return render_template("user_profile.html", user=user)

@app.route('/users', methods=['POST'])
def register_user():
    """create a new user"""

    email = request.form.get('email')
    password =  request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else: 
        crud.create_user(email, password)
        flash('Account created! Please log in.')
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def login_user():
    """add and check for user login"""

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)

    if user:
        if password == user.password:
            flash("You've logged in!")
            return redirect('/')
        else:
            flash("Incorrect password. Try again.")
            return redirect('/')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
