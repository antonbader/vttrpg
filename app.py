from flask import Flask
from flask_socketio import SocketIO
from models import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_ttrpg_key' # In production, use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ttrpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)

from flask import render_template, request, redirect, url_for
from models import Campaign, Adventure

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    campaigns = Campaign.query.all()
    return render_template('index.html', campaigns=campaigns)

@app.route('/campaign/create', methods=['POST'])
def create_campaign():
    name = request.form.get('name')
    description = request.form.get('description')
    if name:
        new_campaign = Campaign(name=name, description=description)
        db.session.add(new_campaign)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/campaign/<int:campaign_id>/adventure/create', methods=['POST'])
def create_adventure(campaign_id):
    name = request.form.get('name')
    if name:
        new_adventure = Adventure(name=name, campaign_id=campaign_id)
        db.session.add(new_adventure)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
