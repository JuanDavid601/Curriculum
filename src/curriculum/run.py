from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from .models import User, CV, cvs, get_user, Users, get_cv_by_user_id, get_user_by_id
from urllib.parse import urlparse
from .forms import SignupForm, LoginForm, ExperienceForm, EducationForm, SkillForm, CVForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unaclave'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/", methods=["GET"])
def index():
    #renderizar la plantilla
    return render_template("index.html", cvs=cvs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form= LoginForm()

    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember= form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page= url_for('index')
            return redirect(next_page)
        return render_template("login.html", form=form)
    

@app.route("/logout", method=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))
            

@app.route("/signup", methods=["GET", "POST"])

def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form= SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = (User(len(Users)+1, name, email, password))
        Users.append(user)
        login_user(user, remember=True)
        next_page= request.args.get("next", None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page= url_for('index')
        return redirect(next_page)
    return render_template("admin/singup_form.html", form=form)



@app.route("/cv/<int:cv_id>", method=["GET"])
def view_cv():
    #Renderizar la plantilla
    return render_template("cv_view.html", CV=CV)


@app.route("/cv/create", methods=["GET", "POST"])
def create_cv():
    if get_cv_by_user_id(current_user.id):
        return redirect(url_for('edit_cv'))
    
    form = CVForm()

    if form.validate_on_submit():
        user_id = current_user.id
        full_name = form.full_name.data
        title = form.title.data
        about_me = form.about_me.data
        experience = form.experience.data
        education = form.education.data
        skills = form.skills.data
    
        cv = CV(len(cvs)+1,
                user_id, 
                full_name, 
                title, 
                about_me, 
                experience, 
                education, 
                skills)
        cvs.append(cv)
        next_page= request.args.get("next", None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page= url_for('index')
        return redirect(next_page)
    return render_template("admin/cv_form.html", form=form , is_new=True)


@app.route("/cv/edit", methods=["GET", "POST"])
def edit_cv():
    cv = get_cv_by_user_id(current_user.id)
    if not cv:
        return redirect(url_for('create_cv'))
    

    form = CVForm()

    if form.validate_on_submit():
        cv.full_name = form.full_name.data
        cv.title = form.title.data
        cv.about_me = form.about_me.data
        cv.experience = form.experience.data
        cv.education = form.education.data
        cv.skills = form.skills.data


        next_page= request.args.get("next", None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page= url_for('index')
        return redirect(next_page)
    return render_template("admin/cv_form.html", form=form, is_new=False)

@app.route("/api/cvs", methods=["GET"])
def api_get_cvs():
    return jsonify([cv.to_dict()for cv in cvs])
    #Renderizar template

@app.route("/api/cvs/<int:cv_id", methods=["GET"])
def api_get_cv(cv_id):
    cv= get_cv_by_user_id(cv_id)
    if not cv:
        return jsonify({"error": "CV not found"}), 404
    return jsonify(cv.to_dict)


@login_manager.user_loader
def load_user(user_id):
    if get_user_by_id(user_id):
        return User
    return None

def load_user(user_id):
    for u in Users:
        if str(u.id) == str(user_id):
            return u
    return None