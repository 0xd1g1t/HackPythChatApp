from chat import app, db
from flask import render_template, request, flash, redirect, url_for, session
from sqlalchemy import text


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            flash(f"Username is not valid", category='warning')
            return render_template('login.jinja')

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            flash(f"Password is not valid", category='warning')
            return render_template('login.jinja')
        
        query_stmt = f"select id from chatusers where username = '{username}' and password = '{password}'"
        result = db.session.execute(text(query_stmt))
        user = result.fetchone()

        if not user:
            flash(f"Benutzername oder Passwort falsch!", category='warning')
            return render_template ('login.jinja')
        
        session['userid'] = user.id

        return redirect(url_for("chat_page"))

    return render_template("login.jinja")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template("register.jinja")


@app.route('/', methods=['GET', 'POST'])
def chat_page():
    # check if current user is logged in
    if not session['userid']:
        flash("Bitte einloggen", category='warning')
        return redirect(url_for("login_page"))

    chat_id = request.args.get('chat')
    if chat_id == None:
        return redirect(url_for('chat_page', chat=1 if session['userid'] != 1 else 2))

    if request.method == "POST":
        message = request.form.get('message-input')
        if (message is None or 
            isinstance(message, str) is False or
            len(message) == 0):
            flash(f"Message was empty! {message}", category='info')
            return redirect(url_for('chat_page', chat=chat_id))
        query_send_message = f"INSERT INTO messages (from_user, to_user, message) VALUES ({session['userid']}, '{chat_id}', '{message}')"
        db.session.execute(text(query_send_message))
        db.session.commit()

    result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id != {session['userid']};"))
    chats = result.fetchall()

    result = db.session.execute(text(f"SELECT * FROM messages WHERE (to_user = {chat_id} and from_user = {session['userid']}) OR (from_user = {chat_id} and to_user = {session['userid']});"))
    messages = result.fetchall()

    result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id = {session['userid']}"))
    current_user = result.fetchone()

    return render_template("chat.jinja", messages=messages, chats=chats, current_user=current_user, chat_id=chat_id)