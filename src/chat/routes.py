from chat import app, db
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import text



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        print(f"[!] {username} tried to login with password '{password}'")

    return render_template("login.jinja")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template("register.jinja")


@app.route('/')
def chat_page():
    chat_id = request.args.get('chat', default=1, type=int)

    messages = [{"from_user": 1, "to": "Peter", "message": "Hallo Peter"},
                {"from_user": 2, "to": "Hans", "message": "Hi, was geht?"},
                {"from_user": 2, "to": "Hans", "message": "Hi, was geht?"},
                {"from_user": 1, "to": "Peter", "message": "Nix"}]

    chats = [
        { "username": "Hans", "status": "Lorem ipsum dolor sit.", "avatar": "img/default.jpeg", "active": True},
        { "username": "Frank", "status": "Lorem ipsum dolor sit.", "avatar": "img/default.jpeg"},
        { "username": "Martin", "status": "Lorem ipsum dolor sit.", "avatar": "img/default.jpeg"},
        { "username": "Klaus", "status": "Lorem ipsum dolor sit.", "avatar": "img/default.jpeg"},
    ]

    current_user = 1
    result = db.session.execute(text(f"SELECT * FROM chatusers WHERE id != {current_user};"))
    chats = result.fetchall()

    result = db.session.execute(text(f"SELECT * FROM messages WHERE (to_user = {chat_id} and from_user = {current_user}) OR (from_user = {chat_id} and to_user = {current_user});"))
    messages = result.fetchall()


    return render_template("chat.jinja", messages=messages, chats=chats, current_user=current_user, chat_id=chat_id)