import functools

from flask import render_template, Blueprint, request, flash, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from comments.db import get_db

bp = Blueprint("auth", __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # 正常应该返回带状态码 json 格式错误提示，前端弹窗
            flash('请登录后留言')
            return redirect(url_for("index"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone())


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not email:
            error = "Email is required."
        elif not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (email, username, password) VALUES (?, ?, ?)",
                    (email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/signup.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form["password"]
        remember = request.form.get("remember", False)
        error = None

        if not username and not email:
            error = "Username or Email must has one."
        elif username and email:
            error = "Username or Email just need one"
        if error is None:
            db = get_db()
            if username:
                user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
            else:
                user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
            if not user:
                error = "Incorrect username."
            elif not check_password_hash(user["password"], password):
                error = "Incorrect password."
            if error is None:
                session.clear()
                session["user_id"] = user["id"]
                if remember:
                    session.permanent = True
                return redirect(url_for("index"))

        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
