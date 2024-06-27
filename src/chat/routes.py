from chat import app, db
from chat.models import Chatuser, Message
from flask import render_template, request, flash, redirect, url_for, session, send_file, escape
from werkzeug.utils import secure_filename
from sqlalchemy import text
import os
import subprocess

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = str(escape(request.form.get('username')))
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
        
        user = Chatuser.query.filter_by(username=username, password=password).first()

        if not user:
            flash(f"Benutzername oder Passwort falsch!", category='warning')
            return render_template ('login.jinja')
        
        session['userid'] = user.id

        return redirect(url_for("chat_page"))

    return render_template("login.jinja")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = str(escape(request.form.get('username')))
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

        user = Chatuser.query.filter_by(username=username).first()

        if user is not None:
            flash("Username exists, try again", category="danger")
            return render_template("register.jinja")
        
        default_status = "Lorem ipsum dolor sit."

        # Neuen Benutzer erstellen
        new_user = Chatuser(username=username, password=password1, status=default_status)
        db.session.add(new_user)
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

        new_message = Message(from_user=session['userid'], to_user=chat_id, message=str(escape(message)))
        db.session.add(new_message)
        db.session.commit()

    chats = Chatuser.query.filter(Chatuser.id != session['userid']).all()
    messages = Message.query.filter(
        ((Message.to_user == chat_id) & (Message.from_user == session['userid'])) | 
        ((Message.from_user == chat_id) & (Message.to_user == session['userid']))
    ).all()

    current_user = Chatuser.query.get(session['userid'])

    return render_template("chat.jinja", messages=messages, chats=chats, current_user=current_user, chat_id=chat_id)


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        username = str(escape(request.form.get('username')))
        status = request.form.get('status')

        if not username or len(username) < 3:
            flash("Username is not valid!", category='warning')
            return render_template('login.jinja')

        if not status or len(status) < 3:
            flash("Status is not valid!", category='warning')
            return render_template('login.jinja')

        current_user = Chatuser.query.get(session['userid'])

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file_path = os.path.join(app.config["UPLOAD_PATH"], str(current_user.id))
                file.save(file_path)
                current_user.avatar = f'/avatars/{current_user.id}'
                db.session.commit()
                flash("Avatar successfully updated!", category="success")

        if username != current_user.username:
            current_user.username = username
            db.session.commit()
            flash("Username successfully updated!", category="success")

        if status != current_user.status:
            current_user.status = str(escape(status))
            db.session.commit()
            flash("Status successfully updated!", category="success")

    current_user = Chatuser.query.get(session['userid'])
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

    current_user = Chatuser.query.get(session['userid'])

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