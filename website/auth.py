from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Run, Lift, Food
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 8:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/weights', methods=['GET', 'POST'])
@login_required
def weights():
    if request.method == 'POST':
        bench = request.form.get('bench')
        squat = request.form.get('squat')
        deadlift = request.form.get('deadlift')

        lifts = User(bench=bench, squat=squat, deadlift=deadlift)
        if bench is None or squat is None or deadlift is None:
            flash('Please enter valid numbers.', category='error')
        else:
            bch = int(float(bench))
            sqt = int(float(squat))
            dl = int(float(deadlift))

            b1 = 5*(round(bch*.333/5))
            b2 = 5*(round(bch*.58/5))
            b3 = 5*(round(bch*.777/5))
            b4 = 5*(round(bch*.85/5))
            b5 = 5*(round(bch*.938271/5))
            b6 = 5*(round(bch*.96296/5))

            sq1 = 5*(round(sqt*.2967/5))
            sq2 = 5*(round(sqt*.4945/5))
            sq3 = 5*(round(sqt*.6044/5))
            sq4 = 5*(round(sqt*.6923/5))
            sq5 = 5*(round(sqt*.8022/5))
            sq6 = 5*(round(sqt*.8462/5))
            sq7 = 5*(round(sqt*.9121/5))
            sq8 = 5*(round(sqt*.9780/5))

            dl1 = 5*(round(dl*.2967/5))
            dl2 = 5*(round(dl*.4945/5))
            dl3 = 5*(round(dl*.6044/5))
            dl4 = 5*(round(dl*.6923/5))
            dl5 = 5*(round(dl*.8022/5))
            dl6 = 5*(round(dl*.8462/5))
            dl7 = 5*(round(dl*.9121/5))
            dl8 = 5*(round(dl*.9780/5))

            db.session.add(lifts)
            db.session.commit()

            return render_template("weights.html", user=current_user, bench=bench, b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, b6=b6, squat=sqt, sq1=sq1, sq2=sq2, sq3=sq3, sq4=sq4, sq5=sq5, sq6=sq6, sq7=sq7, sq8=sq8, deadlift=dl, dl1=dl1, dl2=dl2, dl3=dl3, dl4=dl4, dl5=dl5, dl6=dl6, dl7=dl7, dl8=dl8,)

    return render_template("weights.html", user=current_user)


@auth.route('/calories', methods=['GET', 'POST'])
@login_required
def calories():
    return render_template("calories.html", user=current_user)


@auth.route('/running', methods=['GET', 'POST'])
@login_required
def running():
    return render_template("running.html", user=current_user)
