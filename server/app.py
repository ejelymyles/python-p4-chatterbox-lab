from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_dict = [message.to_dict() for message in messages]
        return jsonify(messages_dict), 200
    
    elif request.method == 'POST':
        request_data = request.json
        new_message = Message(
            body=request_data.get("body"),
            username=request_data.get("username"),
        )

        db.session.add(new_message)
        db.session.commit()
        new_message_dict = new_message.to_dict()
        return jsonify(new_message_dict), 201
    

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        return make_response(message.to_dict(), 200)

    elif request.method == 'PATCH':
        request_data = request.json
        for attr, value in request_data.items():
            setattr(message, attr, value)
        
        db.session.commit()
        message_dict = message.to_dict()
        return jsonify(message_dict), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response({'message':'record successfully deleted'}, 200)

    

if __name__ == '__main__':
    app.run(port=5555)
