from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.user import User

from forms.registration import RegistrationForm
from forms.login import LoginForm

from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "project_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/forum.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("registration.html",
                                   title="Регистрация",
                                   message="Пароли не совпадают",
                                   form=form)
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(str(User.email) == form.email.data).first():
            return render_template("registration.html",
                                   title="Регистрация",
                                   message="Пользователь с такой почтой уже существует",
                                   form=form)

        if db_sess.query(User).filter(str(User.username) == form.username.data).first():
            return render_template("registration.html",
                                   title="Регистрация",
                                   message="Пользователь с таким именем уже существует",
                                   form=form)

        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        login_user(user)

        return redirect("/")
    return render_template("registration.html",
                           title="Регистрация",
                           form=form)


@app.route("/login", methods=["GET", "POST"])  # функция для входа в аккаунт пользователя
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               title="",
                               message="",
                               form=form)
    return render_template("login.html", title="вход", form=form)


@app.route("/redirect_account")
@login_required
def redirect_account():
    user_id = current_user.id
    return redirect(f"/account/{user_id}")


@app.route("/account/<int:user_id>", methods=["GET"])
@login_required
def account(user_id):
    return f"{user_id}"


@app.route("/")
def home():
    return render_template("base.html", title="home page")


def main():
    app.run(host="127.0.0.1", port=5050)


if __name__ == '__main__':
    main()
