from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Lansi'}
	games = [
		{
			'gameName': {'session': 'Game1'},
			'usersLeft': [
				{'username': 'Patrick'},
				{'username': 'Lansi'}
			]
		},
		{
			'gameName': {'session': 'Game2'},
			'usersLeft': [
				{'username': 'Polly'},
				{'username': 'Tony'}
			]
		}
	]
	return render_template('index.html', title='Home', user=user, games=games)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)