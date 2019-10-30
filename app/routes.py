from app import app, db
from flask import render_template, url_for, redirect, flash, jsonify, request
from app.forms import TitleForm, ContactForm, LoginForm, RegisterForm, PostForm
from app.models import Post, User, Contact
from flask_login import login_user, logout_user, login_required, current_user
import datetime

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
# @app.route('/contact/<contacts>', methods={'GET', 'POST'})
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash(f"Thanks {form.name.data}, your message has been received. We have sent a copy of the submission to {form.email.data}.")

        contact = Contact(
            name = form.name.data,
            email = form.email.data,
            message = form.message.data
        )

        # add to stage and commit
        db.session.add(contact)
        db.session.commit()

        # contacts = Contact.query.all()
        contacts = Contact.query.all()

        return redirect(url_for('contact', contacts=contacts))

    return render_template('form.html', form=form, title='Contact Us')









@app.route('/login', methods={'GET', 'POST'})
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # qurey the db for the user information and log them in if everything is valid.
        user = User.query.filter_by(email=form.email.data).first()

        # if user doesn't exsit, reload page and flash message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials')
            return redirect(url_for('login'))

        #if user exists and credentials are correct, log them in
        login_user(user)
        flash(f"You have been logged in.")
        return redirect(url_for('profile', username=current_user.username))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods={'GET', 'POST'})
def register():
    # if user is already logged in , redirect them.
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('profile', username=current_user.username))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            age = form.age.data,
            bio = form.bio.data,
        )

        # include password
        user.set_password(form.password.data)

        # add to stage and commit
        db.session.add(user)
        db.session.commit()

        flash(f"You have been registered.")
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title='Register')

@app.route('/profile')
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=''):
    # if username is empty
    if not username:
        return redirect(url_for('login'))
    form = PostForm()

    person = User.query.filter_by(username=username).first()

    if form.validate_on_submit():

        tweet = form.tweet.data
        post = Post(user_id=current_user.id, tweet=tweet)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('profile', username=username))

    return render_template('profile.html', title='Profile', person=person, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


################################################################################
################################################################################# API section
################################################################################################################################################################


# Create an API that handles getting tweets
@app.route('/api/posts/retrieve/', methods=['GET'])
def api_posts_retrieve():
# try:
    # get variables passed into api
    username = request.args.get('username')
    month = request.args.get('month')

    if username and month:
        user = User.query.filter_by(username=username).first()
        posts = user.posts

        data = []

        for post in posts:

            if post.date_posted.month == int(month):
                data.append({
                    'post_id': post.post_id,
                    'user_id': post.user_id,
                    'tweet': post.tweet,
                    'date_posted': post.date_posted
                })

        return jsonify({ 'code' : 200, 'data' : data})


    if username:
        user = User.query.filter_by(username=username).first()
        posts = user.posts

        data = []

        # d = datetime.datetime(2019, 1, 1, 1, 00)
        # post = Post(user_id=1, tweet='Happy New Year!', date_posted=d)
        # db.session.add(post)
        # db.session.commit()

        # d = datetime.datetime(2019, 10, 24, 11, 00)
        # post = Post(user_id=1, tweet='Hello from today!', date_posted=d)
        # db.session.add(post)
        # db.session.commit()

        for post in posts:
            data.append({
                'post_id': post.post_id,
                'user_id': post.user_id,
                'tweet': post.tweet,
                'date_posted': post.date_posted
            })

        return jsonify({ 'code' : 200, 'data' : data})
    return jsonify({ 'code' : 200, 'message': 'Invalid params' })

# except:
    return jsonify({
        'message': 'Error #1001: Something went wrong',
        'code': 1001
    })

# create an API that handles posting tweets
@app.route('/api/posts/save/', methods=['POST'])
def api_posts_save():
    '''
        This API route should take in two arguments,
        username, tweet, and save the twee into the database,
        then return a success or fail message. Be sure to set date_posted
        to current time.
    '''
    # user_id
    username = request.args.get('username')
    # tweet
    tweet = request.args.get('tweet')

    user = User.query.filter_by(username=username).first()

    if user:

        post = Post(username=username, tweet=tweet)
        db.session.add(post)
        db.session.commit()

        return jsonify({ 'code' : 200, 'message': 'Tweet saved.' })

    # try:
    #     # get variables passed into api
    #     username = request.args.get('username')
    #     print(username)
    #
    #     return jsonify({ 'code' : 200 })
    #
    # except:
    #     return jsonify({
    #         'message': 'Error #1002: Something went wrong',
    #         'code': 1002
    #     })

# api to delete posts, take in a post id and delete
@app.route('/api/posts/delete/', methods=['DELETE'])
def api_posts_delete():
    try:
        post_id = request.args.get('post_id')

        post = Post.query.get(int(post_id))

        db.session.delete(post)
        db.session.commit()
        return jsonify({ 'code': 200, 'message': 'Tweet deleted'})
    except:
        return jsonify({ 'code': 1004, 'message': 'Couldn\'t find post to delete' })
# this api should accept info through headers securely, and pass back infor of user

@app.route('/api/users/retrieve/', methods=['GET', 'POST'])
def api_users_retrieve():
    try:
        # get headers first
        username = request.headers.get('username')
        API_KEY = request.headers.get('API_KEY')

        if API_KEY == 'secret':
            # query the user based on username, get info, return it
            user = User.query.filter_by(username=username).first()

            info = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'username': user.username,
                'email': user.email
            }
            return jsonify({ 'code': 200, 'data':info })
        return jsonify({ 'code': 200, 'message': 'Invalid key'})
    except:
        return jsonify({
            'message': 'Error #1003: Please dont\' be mad at me.',
            'code': 1003
        })
