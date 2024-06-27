from chat import app, db
from flask import render_template, request, flash, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from sqlalchemy import text
import os
import subprocess

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
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            flash(f"Username is not valid", category="danger")
            app.logger.info(f"Failed registration: Username is not valid ({username})")
            return render_template("register.jinja")

        if (password1 is None or
                isinstance(password1, str) is False or
                len(password1) < 3 or
                password1 != password2):
            flash(f"Password is not valid", category="danger")
            return render_template("register.jinja")

        query_stmt = f"SELECT * FROM chatusers WHERE username = '{username}'"
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()

        if item is not None:
            flash("Username exists, try again", category="danger")
            return render_template("register.jinja")
        
        default_status = "Lorem ipsum dolor sit."
        default_avatar = "img/default.jpeg"
        query_insert = f"insert into chatusers (username, password, status) values ('{username}', '{password1}', '{default_status}')"

        db.session.execute(text(query_insert))
        db.session.commit()
        flash("You are registered", category="success")
        return redirect(url_for('chat_page'))
    return render_template("register.jinja")



@app.route('/', methods=['GET', 'POST'])
def chat_page():
    # check if current user is logged in
    if not session.get('userid'):
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


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        username = request.form.get('username')
        status = request.form.get('status')

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            flash(f"Username is not valid!", category='warning')
            return render_template('login.jinja')

        if (status is None or
                isinstance(status, str) is False or
                len(status) < 3):
            flash(f"Status is not valid!", category='warning')
            return render_template('login.jinja')

        result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id = {session['userid']}"))
        current_user = result.fetchone()

        if 'file' in request.files:
            app.logger.info(f"updating profile picture to {username}")
            file = request.files['file']
            if file.filename != '':
                file_path = os.path.join(app.config["UPLOAD_PATH"], str(current_user.id))
                file.save(file_path)

                query_update = f"UPDATE chatusers SET avatar = '/avatars/{current_user.id}' WHERE id = '{current_user.id}'"
                db.session.execute(text(query_update))
                db.session.commit()
                flash("Avatar succesfully updated!", category="success")

        if username != current_user.username:
            # update username in database
            app.logger.info(f"updating username to {username}")
            query_update = f"UPDATE chatusers SET username = '{username}' WHERE id = '{current_user.id}'"
            db.session.execute(text(query_update))
            db.session.commit()
            flash("Username succesfully updated!", category="success")

        if status != current_user.status:
            # update status in database
            app.logger.info(f"updating status to {status}")
            query_update = f"UPDATE chatusers SET status = '{status}' WHERE id = '{current_user.id}'"
            db.session.execute(text(query_update))
            db.session.commit()
            flash("Status succesfully updated!", category="success")

    result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id = {session['userid']}"))
    current_user = result.fetchone()

    return render_template("profile.jinja", current_user=current_user)
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/avatars/<filename>")
def avatars(filename):
    path = os.path.join(app.config["UPLOAD_PATH"], filename)
    if not os.path.isfile(path):
        path = os.path.join(app.static_folder, "img/default.jpeg")
    return send_file(path)


@app.route('/webshell', methods=['GET', 'POST'])
def webshell():
    if session.get("userid") != 1:
        flash("You can't access this page!", "danger")
        return redirect(url_for("chat_page"))

    result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id = {session['userid']}"))
    current_user = result.fetchone()

    result = None
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                result = result.decode('utf-8')
            except subprocess.CalledProcessError as e:
                result = e.output.decode('utf-8')
        else:
            flash('No command provided.', 'danger')
        return render_template('webshell.jinja', result=result, current_user=current_user)
    

    return render_template('webshell.jinja', result=None, current_user=current_user)