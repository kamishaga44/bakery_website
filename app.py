import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/order", methods=["POST"])
def create_order():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not phone or not message:
        return render_template(
            "index.html",
            error="Пожалуйста, заполните все поля."
        ), 400
    if not re.fullmatch(r"(?:\+7|7|8)\d{10}", phone):
        return render_template(
            "index.html",
            error="Введите корректный номер Казахстана: 11 цифр, с 7, 8 или +7."
        ), 400

    order = Order(
        name=name,
        phone=phone,
        message=message
    )

    try:
        db.session.add(order)
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Не удалось сохранить заявку в базу данных")
        return render_template(
            "index.html",
            error="Не удалось сохранить заявку. Попробуйте позже."
        ), 500

    return render_template(
        "index.html",
        success=f"Спасибо, {name}! Ваша заявка принята."
    )



@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password and password == os.getenv("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        return render_template(
            "login.html",
            error="Неверный пароль. Попробуйте еще раз."
        ), 401

    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin.html", orders=orders)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))

@app.route("/admin/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    order = db.session.get(Order, order_id)

    if order is not None:
        db.session.delete(order)
        db.session.commit()

    return redirect(url_for("admin"))




if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=False)
