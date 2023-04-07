import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.user import User

from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm
from forms.trad_form import CreateTradForm
from forms.change_info_form import ChangeInfoForm

from werkzeug.security import check_password_hash

import uuid as uuid


'''
    ОБЪЯВЛЕНИЕ БАЗОВЫХ ПЕРЕМЕННЫХ И ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
'''

app = Flask(__name__)
app.config["SECRET_KEY"] = "project_secret_key"
app.config["UPLOAD_FOLDER"] = "static/profile pictures"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/forum.db")  # подключение к бд


# сохранения пользователя в "сессии"
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")  # обработчик выхода пользователя из аккаунта
@login_required
def logout():
    logout_user()
    return redirect("/")


def allowed_file(filename):  # функция проверки расширения файла
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''
        ВИДИМАЯ НА САЙТЕ ЧАСТЬ
'''


@app.route("/registration", methods=["GET", "POST"])  # обработчик для регистрации пользователя
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


@app.route("/login", methods=["GET", "POST"])  # обработчик для входа в аккаунт пользователя
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
    return render_template("login.html",
                           title="вход",
                           form=form)


@app.route("/account/<int:user_id>", methods=["GET"])  # обработчик аккаунта пользователя
@login_required
def account(user_id):
    return render_template("account.html",
                           title="Аккаунт",
                           id=user_id)


@app.route("/create_trad", methods=["GET", "POST"])
@login_required
def create_trad():  # обработчик для создания трэда (обсуждения)
    form = CreateTradForm()

    if form.validate_on_submit():
        if form.title.data and form.preview.data and form.content.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.title = form.title.data
            user.preview = form.preview.data
            user.content = form.content.data
            user.is_private = form.is_private.data
            return redirect(f"/account/{current_user.id}")
        return render_template("crate_trad.html",
                               form=form,
                               message="Одно из полей осталось пустым")
    return render_template("create_trad.html",
                           form=form)


@app.route("/create_article", methods=["GET", "POST"])
def create_article():  # обработчик дл создания статьи
    ...


@app.route("/change_info", methods=["GET", "POST"])
def change_info():
    form = ChangeInfoForm()

    if form.validate_on_submit():
        if check_password_hash(current_user.hashed_password, form.password.data):
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()

            if form.username.data:
                user.username = form.username.data
            if form.email.data:
                user.email = form.email.data

            photo = request.files["photo"]
            if form.photo.data
                if allowed_file(photo.filename):
                    pic_name = f"{str(uuid.uuid1())}.webp"
                    user.profile_photo = pic_name

                    saver = request.files["photo"]
                    saver.save(os.path.join(app.config["UPLOAD_FOLDER"], pic_name))
                else:
                    return render_template("change_info.html",
                               form=form,
                               message="Некорректный файл")

            db_sess.commit()
            return redirect(f"/account/{current_user.id}")
        return render_template("change_info.html",
                               form=form,
                               message="Введён некорректный пароль")
    return render_template("change_info.html", form=form)


@app.route("/")  # обработчик домашней страницы
def home():
    return render_template("base.html", title="Главная")


def main():
    app.run(host="127.0.0.1", port=5050)


if __name__ == '__main__':
    main()
