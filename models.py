from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    adventures = db.relationship('Adventure', backref='campaign', lazy=True, cascade="all, delete-orphan")

class Adventure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    scenes = db.relationship('Scene', backref='adventure', lazy=True, cascade="all, delete-orphan")

class Scene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    adventure_id = db.Column(db.Integer, db.ForeignKey('adventure.id'), nullable=False)
    tokens = db.relationship('TokenInstance', backref='scene', lazy=True, cascade="all, delete-orphan")
    background_image = db.Column(db.String(255), nullable=True)
    fow_mask = db.Column(db.Text, nullable=True) # Base64 encoded or path to mask
    grid_size = db.Column(db.Integer, default=50)
    grid_offset_x = db.Column(db.Integer, default=0)
    grid_offset_y = db.Column(db.Integer, default=0)
    scale = db.Column(db.Float, default=1.5) # meters per square
    is_active = db.Column(db.Boolean, default=False)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # 'Player', 'NPC', 'Item'
    image_path = db.Column(db.String(255), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class TokenInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scene_id = db.Column(db.Integer, db.ForeignKey('scene.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    x = db.Column(db.Float, default=0.0)
    y = db.Column(db.Float, default=0.0)

    template = db.relationship('Template')
