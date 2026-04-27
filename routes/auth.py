from db import get_users_connection, verify_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse

# Constantes de rutas
DASHBOARD_URL = '/dashboard'
LOGIN_URL = '/login'

# Constantes de templates
LOGIN_TEMPLATE = 'auth/login.html'


# Función para validar que la URL de redirección es segura
def is_safe_redirect(target):
    if not target:
        return False

    parsed = urlparse(target)

    # Solo permite redirecciones internas relativas
    return not parsed.netloc and target.startswith('/')


@app.get('/login')
def login_form():
    if 'username' in session:
        return redirect(DASHBOARD_URL)

    next_url = request.args.get('next', DASHBOARD_URL)

    if not is_safe_redirect(next_url):
        next_url = DASHBOARD_URL

    return render_template(LOGIN_TEMPLATE, next_url=next_url)


@app.post('/login')
def login_submit():
    if 'username' in session:
        return redirect(DASHBOARD_URL)

    next_url = request.form.get('next', DASHBOARD_URL)

    if not is_safe_redirect(next_url):
        next_url = DASHBOARD_URL

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        flash("Username and password are required.", "danger")
        return render_template(LOGIN_TEMPLATE, next_url=next_url)

    conn = get_users_connection()

    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
    finally:
        conn.close()

    if user and verify_password(user['password'], password):
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['company_id'] = user['company_id']
        session.permanent = True

        return redirect(next_url)

    flash("Invalid username or password", "danger")
    return render_template(LOGIN_TEMPLATE, next_url=next_url)


@app.post('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(LOGIN_URL)