from unittest.util import _MAX_LENGTH
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import math
import os
import requests

API_KEY = os.environ['API_KEY']

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
            new_user.calories = 0
            db.session.commit()
            login_user(new_user, remember=True)
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
        try:
            bench = int(float(request.form.get('bench')))
            squat = int(float(request.form.get('squat')))
            deadlift = int(float(request.form.get('deadlift')))
        except:
            bench = request.form.get('bench')
            squat = request.form.get('squat')
            deadlift = request.form.get('deadlift')

        user = current_user

        if user:
            if isinstance(bench, int) != True or isinstance(squat, int) != True or isinstance(deadlift, int) != True:
                flash('Please enter valid numbers for all lifts.', category='error')
            else:
                bch = bench
                sqt = squat
                dl = deadlift

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

                user.bench = bench
                user.squat = squat
                user.deadlift = deadlift
                db.session.commit()

                return render_template("weights.html", user=current_user, bench=bench, b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, b6=b6, squat=sqt, sq1=sq1, sq2=sq2, sq3=sq3, sq4=sq4, sq5=sq5, sq6=sq6, sq7=sq7, sq8=sq8, deadlift=dl, dl1=dl1, dl2=dl2, dl3=dl3, dl4=dl4, dl5=dl5, dl6=dl6, dl7=dl7, dl8=dl8,)

    return render_template("weights.html", user=current_user)


@auth.route('/running', methods=['GET', 'POST'])
@login_required
def running():
    if request.method == 'POST':
        try:
            mile = float(request.form.get('mile'))
            five_k = float(request.form.get('five_k'))
        except:
            mile = request.form.get('mile')
            five_k = request.form.get('five_k')

        user = current_user

        if user:
            if isinstance(mile, float) != True or isinstance(five_k, float) != True:
                flash('Please enter valid numbers for all runs.',
                      category='error')
            else:
                ml = float(mile)
                mlminsec = math.modf(ml)
                mlmin = mlminsec[1]
                mlsec = mlminsec[0]
                fivek = float(five_k)
                fivekminsec = math.modf(fivek)
                fivekmin = fivekminsec[1]
                fiveksec = fivekminsec[0]

                mlm = round((mlmin*2 + (.6*mlsec)), 2)
                mlt = round((mlmin*1.75 + (.6*mlsec)), 2)
                mlth = round((mlmin*1.25 + (.6*mlsec)), 2)

                fkm = round((fivekmin*1.5 + (.6*fiveksec)), 2)
                fkt = round((fivekmin*1.4 + (.6*fiveksec)), 2)
                fkth = round((fivekmin*1.25 + (.6*fiveksec)), 2)

                user.mile = mile
                user.five_k = five_k
                db.session.commit()

                return render_template("running.html", user=current_user, mlm=mlm, mlt=mlt, mlth=mlth, fkm=fkm, fkt=fkt, fkth=fkth)

    return render_template("running.html", user=current_user)


@ auth.route('/calories', methods=['GET', 'POST'])
@ login_required
def calories():
    if request.method == 'POST':
        if request.form['submit_button'] == 'log':
            user = current_user
            api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
            query = request.form.get('food')
            response = requests.get(
                api_url + query, headers={'X-Api-Key': API_KEY})

            if response.status_code == requests.codes.ok:
                print(response.text)
                food_nut = response.text
                item = request.form.get('food')
                split = food_nut.split(',')
                food_cal = split[8]
                split1 = food_cal.split(':')
                cals = float(split1[1])
                curr_cals = user.calories + cals

                user.calories = round(curr_cals, 2)
                db.session.commit()

                return render_template("calories.html", user=current_user, item=item, cals=cals)
            else:
                print("Error:", response.status_code, response.text)
        elif request.form['submit_button'] == 'reset_cals':
            user = current_user
            user.calories = 0
            db.session.commit()
            return render_template("calories.html", user=current_user)
        else:
            return render_template("calories.html", user=current_user)

    return render_template("calories.html", user=current_user)
