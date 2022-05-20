from flask import Blueprint, session
from sqlalchemy import false, true
from .forms import LoginForm, RegistrationFrom
from app.lib.db_actions import *
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = get_user_by_email(form.email.data)

        if(not user):
            flash("Account non registrato", 'danger')
            return redirect(url_for('main.login'))
        
        #! HARDCODED LOGIN (creare utente)
        if(user.email == 'fake_prof@gmail.com' or user.email == 'visconti373@gmail.com' or user.email == 'stefano.calzavara@unive.it'):
            login_user(user, remember=form.rememberMe.data)
            session['role'] = 'teacher'
            flash("Accesso come professore", 'success')
            return redirect(url_for('teachers.profile'))
        #! ---------------

        student = get_student_by_id(user.id_user)
        
        if bcrypt.check_password_hash(student.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)
            session['role'] = 'student'

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('students.dashboard')) # ternary operator
        else:
            flash('Accesso negato', 'danger')

    return render_template('login.html', form = form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Accesso già effettuato", 'danger')
        return redirect(url_for('main.index'))
    form = RegistrationFrom()
    if form.validate_on_submit():

        insert_user(form)

        flash(f'Account creato, {form.firstName.data}', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form = form)

@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.index'))


@main.route('/<path>/<id_course>/lessons', methods = ['GET','POST'])
def lessons(id_course,path):
    isTeacher = False
    if path == 'teacher':
        isTeacher = True
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))

    lessons = get_course_lessons(id_course)
    
    hasLessons = True
    if len(lessons) == 0:
        hasLessons = False
    return render_template('lesson_list.html', teacher = isTeacher, course = get_course_by_id(id_course), lessons = lessons, no_lessons = not hasLessons)