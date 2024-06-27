from chat import app, db

class Chatuser(db.Model):
    __tablename__ = "chatusers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)

    # Beziehung zu gesendeten Nachrichten
    sent_messages = db.relationship('Message', foreign_keys='Message.from_user', backref='sender', lazy=True)
    # Beziehung zu empfangenen Nachrichten
    received_messages = db.relationship('Message', foreign_keys='Message.to_user', backref='recipient', lazy=True)
    

    def __repr__(self):
        return f'<Chatuser {self.id}: {self.username}>'


class Message(db.Model):
    __tablename__  = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1024), nullable=False)

    # Fremdschlüssel für den Sender
    from_user = db.Column(db.Integer, db.ForeignKey('chatusers.id'), nullable=False)
    # Fremdschlüssel für den Empfänger
    to_user = db.Column(db.Integer, db.ForeignKey('chatusers.id'), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}: {self.message}>'