from chat import app, db
from flask import render_template, request
from sqlalchemy import text


@app.route('/')
def home_page():
    return render_template('home.jinja')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        print(f"[!] {username} tried to login with password '{password}'")

    return render_template("login.jinja")


@app.route('/chat')
def tickets_page():
    items = [{ "id": 1, "prio": 2, "user": "Mark", "title":"Backend broken"},
             { "id": 2, "prio": 2, "user": "Peter", "title":"GUI not working"},
             { "id": 3, "prio": 1, "user": "Mark", "title":"Nothing works"}]

    users = [{ "username": "Hans Peter", "avatar_path": "default.jpeg"}]

    messages = [{ "from": 1, "message": "Hallo" }]

    '''
    query_stmt = f"select * from bugitems"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()
    '''

    return render_template("chat.jinja")#, items=itemsquery)