from flask import Flask, render_template
from datetime import timedelta
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")
app.permanent_session_lifetime = timedelta(minutes=30)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403