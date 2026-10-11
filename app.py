
from flask import Flask, render_template, request

app = Flask(__name__)


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

    return render_template(
        "index.html",
        success=f"Спасибо, {name}! Ваша заявка принята."
    )


if __name__ == "__main__":
    app.run(debug=True)