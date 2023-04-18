import os

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session

from data.user import User
from data.trad import Trad
from data.article import Article

from data.trad_comments import TradComment
from data.article_comments import ArticleComment

from forms.registration_form import RegistrationForm
from forms.login_form import LoginForm

from forms.article_form import CreateArticleForm
from forms.trad_form import CreateTradForm

from forms.change_info_form import ChangeInfoForm
from forms.comment_form import CommentForm

from api.v1 import user_api
from api.v1 import trad_api

from werkzeug.security import check_password_hash

import uuid as uuid

'''
    ОБЪЯВЛЕНИЕ БАЗОВЫХ ПЕРЕМЕННЫХ И ПОДКЛЮЧЕНИЕ БИБЛИОТЕК
'''

app = Flask(__name__)
app.config["SECRET_KEY"] = "project_secret_key"
app.config["UPLOAD_FOLDER"] = ["static/profile pictures", "static/trads pictures", "static/article pictures"]
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

login_manager = LoginManager()
login_manager.init_app(app)


def upload_photo(photo, flag):
    if allowed_file(photo.filename):
        pic_name = f"{str(uuid.uuid1())}.webp"
        saver = request.files["photo"]
        saver.save(os.path.join(app.config["UPLOAD_FOLDER"][flag], pic_name))

        return [True, pic_name]
    return [False, None]


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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(f'зарегистрируйтесь, что бы просмотреть', 401)


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


@app.route("/account", methods=["GET"])  # обработчик аккаунта пользователя В сессии
@login_required
def account():
    db_sess = db_session.create_session()
    trads = db_sess.query(Trad).filter(Trad.author_id == current_user.id)
    articles = db_sess.query(Article).filter(Article.author_id == current_user.id)

    return render_template("account.html",
                           title="Аккаунт",
                           trads=trads,
                           articles=articles)


@app.route("/user/<int:user_id>", methods=["GET"])  # обработчик аккаунта пользователя НЕ в сессии
def user_account(user_id):
    if current_user.id == user_id:
        return redirect(f"/account/{current_user.id}")

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    trads = db_sess.query(Trad).filter(Trad.author_id == user_id)

    return render_template("another_user.html",
                           title=f"Аккаунт {user.username}",
                           user=user,
                           trads=trads)


@app.route("/trad/<int:trad_id>", methods=["GET", "POST"])
def look_trad(trad_id):
    db_sess = db_session.create_session()
    trad = db_sess.query(Trad).filter(Trad.id == trad_id).first()

    comments = db_sess.query(TradComment).filter(TradComment.trad_id == trad_id)

    form = CommentForm()

    if form.validate_on_submit():
        comment = TradComment()
        comment.trad_id = trad_id
        comment.author_id = current_user.id
        comment.content = form.comment_text.data

        db_sess.add(comment)

        db_sess.commit()
        return redirect(f"/trad/{trad_id}")

    return render_template("look_trad.html",
                           title=trad.title,
                           trad=trad,
                           form=form,
                           comments=comments)


@app.route("/article/<int:article_id>", methods=["GET", "POST"])
@login_required
def look_article(article_id):
    db_sess = db_session.create_session()
    article = db_sess.query(Article).filter(Article.id == article_id).first()
    comments = db_sess.query(ArticleComment).filter(ArticleComment.article_id == article_id)

    form = CommentForm()

    if form.validate_on_submit():
        comment = ArticleComment()
        comment.article_id = article_id
        comment.author_id = current_user.id
        comment.content = form.comment_text.data

        db_sess.add(comment)
        db_sess.commit()

        return redirect(f"/article/{article_id}")

    return render_template("look_article.html",
                           title=article.title,
                           article=article,
                           form=form,
                           comments=comments)


@app.route("/create_trad", methods=["GET", "POST"])
@login_required
def create_trad():  # обработчик для создания трэда (обсуждения)
    form = CreateTradForm()

    if form.validate_on_submit():
        if form.title.data and form.preview.data and form.content.data:
            if len(form.preview.data) > 70:
                return render_template("create_trad.html",
                                       form=form,
                                       message="Слишком длинное превью")

            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()

            trad = Trad()
            trad.title = form.title.data
            trad.preview = form.preview.data
            trad.content = form.content.data
            trad.is_private = form.is_private.data

            photo = request.files["photo"]
            if form.photo.data:
                if allowed_file(photo.filename):
                    uploaded_photo = upload_photo(photo, 1)
                    if uploaded_photo[0]:
                        trad.trad_photo = uploaded_photo[1]
                else:
                    return render_template("create_trad.html",
                                           title="создание обсуждения",
                                           form=form,
                                           message="Неккоректный файл")

            user.trads.append(trad)
            db_sess.commit()

            return redirect("/account")
        return render_template("crate_trad.html",
                               title="создание обсуждения",
                               form=form,
                               message="Одно из полей осталось пустым")
    return render_template("create_trad.html",
                           form=form)


@app.route("/create_article", methods=["GET", "POST"])
@login_required
def create_article():  # обработчик дл создания статьи
    form = CreateArticleForm()

    if form.validate_on_submit():
        if form.title.data and form.preview.data and form.content.data:
            if len(form.preview.data) > 70:
                return render_template("create_article.html",
                                       title="создание статьи",
                                       form=form,
                                       message="Слишком длинное превью")

            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()

            article = Article()
            article.title = form.title.data
            article.preview = form.preview.data
            article.content = form.content.data
            article.is_private = form.is_private.data

            photo = request.files["photo"]
            if form.photo.data:
                if allowed_file(photo.filename):
                    uploaded_photo = upload_photo(photo, 2)
                    if uploaded_photo[0]:
                        article.trad_photo = uploaded_photo[1]
                else:
                    return render_template("create_article.html",
                                           title="создание обсуждения",
                                           form=form,
                                           message="Неккоректный файл")

            user.article.append(article)
            db_sess.commit()

            return redirect("/account")
        return render_template("crate_trad.html",
                               title="создание обсуждения",
                               form=form,
                               message="Одно из полей осталось пустым")
    return render_template("create_trad.html",
                           title="создание статьи",
                           form=form)


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
            if form.photo.data:
                if allowed_file(photo.filename):
                    uploaded_photo = upload_photo(photo, 0)
                    if uploaded_photo[0]:
                        user.profile_photo = uploaded_photo[1]
                else:
                    return render_template("change_info.html",
                                           title="Изменение информации",
                                           form=form,
                                           message="Неккоректный файл")

            db_sess.commit()
            return redirect("/account")
        return render_template("change_info.html",
                               form=form,
                               title="Изменение информации",
                               message="Введён некорректный пароль")
    return render_template("change_info.html", title="Изменение информации", form=form)


@app.route("/")  # обработчик домашней страницы
def home():
    db_sess = db_session.create_session()
    trads = db_sess.query(Trad).filter(Trad.is_private != True)
    return render_template("base.html",
                           title="Главная",
                           trads=trads)


def main():
    db_session.global_init("db/forum.db")  # подключение к бд
    app.register_blueprint(user_api.blueprint)  # регистрация блюпринта API пользователя
    app.register_blueprint(trad_api.blueprint)
    app.run(host="127.0.0.1", port=5050)


if __name__ == '__main__':
    main()
