from db import get_users_connection, verify_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse

# Constantes de rutas
DASHBOARD_URL = '/dashboard'
LOGIN_URL = '/login'

# Constantes de templates
LOGIN_TEMPLATE = 'auth/login.html'


# Validación de redirecciones seguras (evita open redirect)
def is_safe_redirect(target):
    if not target:
        return False

    parsed = urlparse(target)

    # Solo permite rutas relativas internas
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

    # Validación básica de entrada
    if not username or not password:
        flash("Username and password are required.", "danger")
        return render_template(LOGIN_TEMPLATE, next_url=next_url)

    # Conexión a base de datos
    conn = get_users_connection()

    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
    finally:
        conn.close()

    # 🔒 Validación segura de contraseña (evita 500)
    is_valid_password = False

    try:
        if user:
            is_valid_password = verify_password(user['password'], password)
    except ValueError as e:
        # Error típico: hash incompatible (ej: scrypt)
        app.logger.error("Password verification failed: %s", e)
        is_valid_password = False
    except Exception as e:
        # Cualquier otro error inesperado
        app.logger.error("Unexpected login error: %s", e)
        is_valid_password = False

    # Login exitoso
    if user and is_valid_password:
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['company_id'] = user['company_id']
        session.permanent = True

        return redirect(next_url)

    # Respuesta controlada (evita enumeración de usuarios)
    flash("Invalid username or password", "danger")
    return render_template(LOGIN_TEMPLATE, next_url=next_url)


@app.post('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(LOGIN_URL)