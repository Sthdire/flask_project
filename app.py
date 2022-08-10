from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from model import users, db, App

HEX_SEC_KEY = 'd5fb8c4fa8bd46638dadc4e751e0d68d'
App.config['SECRET_KEY'] = HEX_SEC_KEY


@App.route('/')
def hello_world():
    return render_template('index.html')


@App.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = users(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')


@App.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = users.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if request.path == '/login':
                return redirect(url_for('profile'))
            return redirect(next_page)
        else:
            flash('login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@App.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@App.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@App.after_request
def after_request(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@App.route('/anim')
def anim():
    return render_template('animation.html')



if __name__ == '__main__':
    App.run(debug=True)
