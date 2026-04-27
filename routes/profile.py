from flask import request, redirect, render_template, session, flash
from server import app
from db import get_users_connection, get_data_connection


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    if 'username' not in session:
        return redirect('/login')

    conn_u = get_users_connection()
    try:
        user = conn_u.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        conn_u.close()

    if not user:
        return render_template('errors/404.html'), 404

    conn_d = get_data_connection()
    try:
        comments = conn_d.execute(
            "SELECT comments.*, companies.name as company_name "
            "FROM comments "
            "JOIN companies ON comments.company_id = companies.id "
            "WHERE comments.user = ? "
            "ORDER BY comments.id DESC LIMIT 10",
            (user['username'],)
        ).fetchall()
    finally:
        conn_d.close()

    return render_template(
        'profile/view.html',
        profile_user=user,
        comments=comments
    )


@app.get('/profile/edit')
def edit_profile_form():
    if 'username' not in session:
        return redirect('/login')

    conn = get_users_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (session['username'],)
        ).fetchone()
    finally:
        conn.close()

    if not user:
        return render_template('errors/404.html'), 404

    return render_template('profile/edit.html', user=user)


@app.post('/profile/edit')
def update_profile():
    if 'username' not in session:
        return redirect('/login')

    new_username = request.form.get('username', '').strip()
    role = request.form.get('role', session.get('role'))

    if not new_username:
        flash("Username is required.", "danger")
        return redirect('/profile/edit')

    conn = get_users_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (session['username'],)
        ).fetchone()

        if not user:
            return render_template('errors/404.html'), 404

        conn.execute(
            "UPDATE users SET username = ?, role = ? WHERE username = ?",
            (new_username, role, session['username'])
        )
        conn.commit()
    finally:
        conn.close()

    session['username'] = new_username
    session['role'] = role

    flash("Profile updated successfully.", "success")
    return redirect('/dashboard')