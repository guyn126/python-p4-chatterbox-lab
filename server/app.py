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

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

@app.route('/messages/<int:id>', methods = ['GET'])
def messages_by_id(id):
    msg = Message.query.get_or_404(id)
    return jsonify(msg.to_dict()), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    username = data.get('username')
    body = data.get('body')

    if not username or not body:
        return jsonify({"error": "Both 'username' and 'body' are required."}), 400

    new_msg = Message(username=username, body=body)
    db.session.add(new_msg)
    db.session.commit()

    return jsonify(new_msg.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' not in data:
        return jsonify({'error': 'Body field is required for update.'}), 400

    msg.body = data['body']
    db.session.commit()

    return jsonify(msg.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get_or_404(id)

    db.session.delete(msg)
    db.session.commit()

    return '', 204



if __name__ == '__main__':
    app.run(port=5555)
