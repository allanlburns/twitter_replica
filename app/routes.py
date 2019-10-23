from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, ContactForm, LoginForm, RegisterForm, PostForm
from app.models import Post

@app.route('/')
@app.route('/index')
@app.route('/index/<word>', methods=['GET'])
def index(word=''):
    products = [
        {
            'id': 1001,
            'title': 'Twitter Bot',
            'price': 150,
            'desc': 'This Twitter bot will destroy your enemies!!!!!!!!!!!!!!!!!!!!!!!!!'
        },
        {
            'id': 1002,
            'title': 'Twitter T-Shirt',
            'price': 15,
            'desc': 'You\'ll look pretty okay in this.'
        },
        {
            'id': 1003,
            'title': 'Stickers',
            'price': 5,
            'desc': 'These stickers will stick to anything with their stickiness.'
        },
        {
            'id': 1004,
            'title': '100k Follower Account',
            'price': 5000,
            'desc': 'Be an influencer today! Christiano Ronaldo gets paid $950,000 for every post he makes.'
        },
    ]

    return render_template('index.html', title="Home", products=products, word=word)

@app.route('/title', methods=['GET', 'POST'])
def title():
    form = TitleForm()

    # handle form submission
    if form.validate_on_submit():
        text = form.title.data

        return redirect(url_for('index', word=text))

    return render_template('form.html', title="Title", form=form)

@app.route('/contact', methods={'GET', 'POST'})
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash(f"Thanks {form.name.data}, your message has been received. We have sent a copy of the submission to {form.email.data}.")

        return redirect(url_for('index'))

    return render_template('form.html', form=form, title='Contact Us')

@app.route('/login', methods={'GET', 'POST'})
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f"You have been logged in.")

        return redirect(url_for('index'))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods={'GET', 'POST'})
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        flash(f"You have been registered.")

        return redirect(url_for('index'))

    return render_template('form.html', form=form, title='Register')

@app.route('/profile')
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=''):
    # if username is empty
    if not username:
        return redirect(url_for('login'))
    form = PostForm()
    people = [
        {
            'id' : 1,
            'first_name' : 'John',
            'last_name' : ' Jingle',
            'username' : 'heimerschmidt',
            'bio' : 'His name is my name too.',
            'age' : 180
        },
        {
            'id' : 2,
            'first_name' : 'Max',
            'last_name' : 'Smith',
            'username' : 'maxsmith',
            'bio' : 'I\'m sure Max has a bio, too.',
            'age' : 180
        }
    ]

    for p in people:
        if p['username'] == username:
            person = p
            break

    tweets = Post.query.all()

    if form.validate_on_submit():

        tweet = form.tweet.data
        post = Post(user_id=person['id'], tweet=tweet)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('profile', username=username))

    return render_template('profile.html', title='Profile', person=person, tweets=tweets, form=form)
