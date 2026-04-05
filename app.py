from flask import Flask
from flask_socketio import SocketIO
from models import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_ttrpg_key' # In production, use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ttrpg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'maps'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'tokens'), exist_ok=True)

db.init_app(app)
socketio = SocketIO(app)

from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from models import Campaign, Adventure, Template, Scene, TokenInstance

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

@app.route('/campaign/<int:campaign_id>/edit_name', methods=['POST'])
def edit_campaign_name(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    name = request.form.get('name')
    if name:
        campaign.name = name
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    # We should handle template images if they are not used elsewhere.
    # A full robust implementation would check if image_path is used by templates in other campaigns.
    for template in Template.query.filter_by(campaign_id=campaign_id).all():
        if template.image_path:
            # Check if this image_path is used by any other template in ANY campaign
            other_uses = Template.query.filter(Template.image_path == template.image_path, Template.id != template.id).count()
            if other_uses == 0:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], template.image_path)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error removing token file: {e}")

    # Also delete scene backgrounds
    for adventure in campaign.adventures:
        for scene in adventure.scenes:
            if scene.background_image:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], scene.background_image)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error removing background file: {e}")

    db.session.delete(campaign)
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

@app.route('/adventure/<int:adventure_id>/edit_name', methods=['POST'])
def edit_adventure_name(adventure_id):
    adventure = Adventure.query.get_or_404(adventure_id)
    name = request.form.get('name')
    if name:
        adventure.name = name
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/adventure/<int:adventure_id>/delete', methods=['POST'])
def delete_adventure(adventure_id):
    adventure = Adventure.query.get_or_404(adventure_id)
    # Delete scene backgrounds
    for scene in adventure.scenes:
        if scene.background_image:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], scene.background_image)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing background file: {e}")

    db.session.delete(adventure)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/adventure/<int:adventure_id>/scene/create', methods=['POST'])
def create_scene(adventure_id):
    name = request.form.get('name')
    if name:
        new_scene = Scene(name=name, adventure_id=adventure_id)
        db.session.add(new_scene)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/scene/<int:scene_id>/edit_name', methods=['POST'])
def edit_scene_name(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    name = request.form.get('name')
    if name:
        scene.name = name
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/scene/<int:scene_id>/delete', methods=['POST'])
def delete_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)

    if scene.background_image:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], scene.background_image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing background file: {e}")

    db.session.delete(scene)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/scene/<int:scene_id>/activate', methods=['POST'])
def activate_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    if scene.is_active:
        # If it's already active, deactivate it
        scene.is_active = False
        db.session.commit()
        socketio.emit('scene_deactivated')
    else:
        # Deactivate all others
        Scene.query.update({Scene.is_active: False})
        scene.is_active = True
        db.session.commit()
        socketio.emit('scene_changed', {'scene_id': scene_id})
    return redirect(url_for('gm_scene', scene_id=scene_id))

@app.route('/scene/<int:scene_id>/gm')
def gm_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    adventure = Adventure.query.get(scene.adventure_id)
    campaign = Campaign.query.get(adventure.campaign_id)
    templates = Template.query.filter_by(campaign_id=campaign.id).all()
    tokens = TokenInstance.query.filter_by(scene_id=scene_id).order_by(TokenInstance.id).all()

    # Format tokens for JS
    tokens_data = []
    template_counts = {}

    for t in tokens:
        if t.template_id not in template_counts:
            template_counts[t.template_id] = 1
        else:
            template_counts[t.template_id] += 1

        display_name = t.template.name
        if template_counts[t.template_id] > 1:
            display_name = f"{t.template.name} {template_counts[t.template_id]}"

        tokens_data.append({
            'id': t.id,
            'template_id': t.template_id,
            'name': display_name,
            'type': t.template.type,
            'image_path': url_for('uploaded_file', filename=t.template.image_path) if t.template.image_path else None,
            'x': t.x,
            'y': t.y
        })

    return render_template('scene_gm.html', scene=scene, campaign=campaign, templates=templates, tokens=tokens_data)

@app.route('/scene/<int:scene_id>/upload_bg', methods=['POST'])
def upload_scene_bg(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    image = request.files.get('background')
    if image and image.filename:
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'maps', filename)
        image.save(path)
        scene.background_image = f'maps/{filename}'
        db.session.commit()
    return redirect(url_for('gm_scene', scene_id=scene_id))

@app.route('/scene/<int:scene_id>/delete_bg', methods=['POST'])
def delete_scene_bg(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    if scene.background_image:
        # Delete file physically
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], scene.background_image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing background file: {e}")
        scene.background_image = None
        db.session.commit()
        # Optionally, clear the FOW mask and grid sizes, tokens if we need to reset completely?
        # The prompt says: "Nach dem Löschen soll es wieder so sein, wie wenn die Szene neu angelegt wurde."
        scene.fow_mask = None
        scene.grid_size = 50
        scene.grid_offset_x = 0
        scene.grid_offset_y = 0
        scene.scale = 1.5
        scene.grid_color = 'rgba(255, 255, 255, 0.4)'
        scene.grid_thickness = 1

        # Delete tokens associated with the scene? "wie wenn die Szene neu angelegt wurde"
        # The scene would have no background and standard grid
        TokenInstance.query.filter_by(scene_id=scene_id).delete()

        db.session.commit()

        # We need to broadcast to clients that tokens are gone, fow is cleared, background is gone
        socketio.emit('scene_reset', {'scene_id': scene_id}, to=f"scene_{scene_id}")

    return redirect(url_for('gm_scene', scene_id=scene_id))

@app.route('/player', methods=['GET', 'POST'])
def player_login():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        if player_name:
            # Find active scene
            active_scene = Scene.query.filter_by(is_active=True).first()
            if active_scene:
                return redirect(url_for('player_view', scene_id=active_scene.id, player_name=player_name))
            else:
                return redirect(url_for('waiting', player_name=player_name))
    return render_template('player_login.html')

@app.route('/player/waiting')
def waiting():
    player_name = request.args.get('player_name')
    # If a scene is active, redirect to it
    active_scene = Scene.query.filter_by(is_active=True).first()
    if active_scene:
        if player_name:
            return redirect(url_for('player_view', scene_id=active_scene.id, player_name=player_name))
        else:
            return redirect(url_for('display_view'))

    return render_template('waiting.html', player_name=player_name)

@app.route('/player/scene/<int:scene_id>')
def player_view(scene_id):
    player_name = request.args.get('player_name')
    if not player_name:
        return redirect(url_for('player_login'))

    scene = Scene.query.get_or_404(scene_id)
    if not scene.is_active:
        return redirect(url_for('waiting', player_name=player_name))

    tokens = TokenInstance.query.filter_by(scene_id=scene_id).order_by(TokenInstance.id).all()
    tokens_data = []
    template_counts = {}

    for t in tokens:
        if t.template_id not in template_counts:
            template_counts[t.template_id] = 1
        else:
            template_counts[t.template_id] += 1

        display_name = t.template.name
        if template_counts[t.template_id] > 1:
            display_name = f"{t.template.name} {template_counts[t.template_id]}"

        tokens_data.append({
            'id': t.id,
            'template_id': t.template_id,
            'name': display_name,
            'type': t.template.type,
            'image_path': url_for('uploaded_file', filename=t.template.image_path) if t.template.image_path else None,
            'x': t.x,
            'y': t.y
        })

    return render_template('scene_player.html', scene=scene, tokens=tokens_data, player_name=player_name, is_display=False)

@app.route('/display')
def display_view():
    active_scene = Scene.query.filter_by(is_active=True).first()
    if not active_scene:
        return redirect(url_for('waiting'))

    tokens = TokenInstance.query.filter_by(scene_id=active_scene.id).order_by(TokenInstance.id).all()
    tokens_data = []
    template_counts = {}

    for t in tokens:
        if t.template_id not in template_counts:
            template_counts[t.template_id] = 1
        else:
            template_counts[t.template_id] += 1

        display_name = t.template.name
        if template_counts[t.template_id] > 1:
            display_name = f"{t.template.name} {template_counts[t.template_id]}"

        tokens_data.append({
            'id': t.id,
            'template_id': t.template_id,
            'name': display_name,
            'type': t.template.type,
            'image_path': url_for('uploaded_file', filename=t.template.image_path) if t.template.image_path else None,
            'x': t.x,
            'y': t.y
        })

    return render_template('scene_player.html', scene=active_scene, tokens=tokens_data, player_name="DISPLAY", is_display=True)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/campaign/<int:campaign_id>/library')
def campaign_library(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    templates = Template.query.filter_by(campaign_id=campaign_id).all()
    other_campaigns = Campaign.query.filter(Campaign.id != campaign_id).all()
    return render_template('library.html', campaign=campaign, templates=templates, other_campaigns=other_campaigns)

@app.route('/campaign/<int:campaign_id>/library/template/create', methods=['POST'])
def create_template(campaign_id):
    name = request.form.get('name')
    type = request.form.get('type')
    image = request.files.get('image')

    image_path = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        # Store in tokens folder
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'tokens', filename)
        image.save(path)
        image_path = f'tokens/{filename}'

    if name and type:
        new_template = Template(name=name, type=type, image_path=image_path, campaign_id=campaign_id)
        db.session.add(new_template)
        db.session.commit()

    return redirect(url_for('campaign_library', campaign_id=campaign_id))

from flask import jsonify

@socketio.on('update_grid')
def handle_update_grid(data):
    scene_id = data.get('scene_id')
    scene = db.session.get(Scene, scene_id)
    if scene:
        scene.grid_size = data.get('grid_size', scene.grid_size)
        scene.grid_offset_x = data.get('grid_offset_x', scene.grid_offset_x)
        scene.grid_offset_y = data.get('grid_offset_y', scene.grid_offset_y)
        scene.grid_color = data.get('grid_color', scene.grid_color)
        scene.grid_thickness = data.get('grid_thickness', scene.grid_thickness)
        scene.scale = data.get('scale', scene.scale)
        db.session.commit()
        socketio.emit('grid_updated', data, to=f"scene_{scene_id}")

@socketio.on('add_token')
def handle_add_token(data):
    scene_id = data.get('scene_id')
    template_id = data.get('template_id')
    x = data.get('x', 0)
    y = data.get('y', 0)

    if scene_id and template_id:
        new_token = TokenInstance(scene_id=scene_id, template_id=template_id, x=x, y=y)
        db.session.add(new_token)
        db.session.commit()

        t = new_token

        # Check if there are other tokens of the same template in this scene to auto-increment name
        existing_tokens_count = TokenInstance.query.filter_by(scene_id=scene_id, template_id=template_id).count()
        display_name = t.template.name
        if existing_tokens_count > 1:
            display_name = f"{t.template.name} {existing_tokens_count}"

        token_data = {
            'id': t.id,
            'template_id': t.template_id,
            'name': display_name,
            'type': t.template.type,
            'image_path': url_for('uploaded_file', filename=t.template.image_path) if t.template.image_path else None,
            'x': t.x,
            'y': t.y
        }
        socketio.emit('token_added', token_data, to=f"scene_{scene_id}")

@socketio.on('move_token')
def handle_move_token(data):
    token_id = data.get('token_id')
    x = data.get('x')
    y = data.get('y')

    token = db.session.get(TokenInstance, token_id)
    if token:
        token.x = x
        token.y = y
        db.session.commit()
        socketio.emit('token_moved', {'token_id': token_id, 'x': x, 'y': y}, to=f"scene_{token.scene_id}")

@socketio.on('delete_token')
def handle_delete_token(data):
    token_id = data.get('token_id')
    token = db.session.get(TokenInstance, token_id)
    if token:
        scene_id = token.scene_id
        db.session.delete(token)
        db.session.commit()
        socketio.emit('token_deleted', {'token_id': token_id}, to=f"scene_{scene_id}")

@socketio.on('update_fow')
def handle_update_fow(data):
    scene_id = data.get('scene_id')
    mask = data.get('mask')

    scene = db.session.get(Scene, scene_id)
    if scene:
        scene.fow_mask = mask
        db.session.commit()
        socketio.emit('fow_updated', {'mask': mask}, to=f"scene_{scene_id}", include_self=False)

from flask_socketio import join_room, leave_room

@socketio.on('join')
def on_join(data):
    room = f"scene_{data['scene_id']}"
    join_room(room)

@app.route('/template/<int:template_id>/edit_name', methods=['POST'])
def edit_template_name(template_id):
    template = Template.query.get_or_404(template_id)
    name = request.form.get('name')
    if name:
        template.name = name
        db.session.commit()
    return redirect(url_for('campaign_library', campaign_id=template.campaign_id))

@app.route('/template/<int:template_id>/delete', methods=['POST'])
def delete_template(template_id):
    template = Template.query.get_or_404(template_id)
    campaign_id = template.campaign_id

    # Check if this image_path is used by any other template in ANY campaign
    if template.image_path:
        other_uses = Template.query.filter(Template.image_path == template.image_path, Template.id != template.id).count()
        if other_uses == 0:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], template.image_path)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing token file: {e}")

    # Delete all tokens instances of this template
    TokenInstance.query.filter_by(template_id=template_id).delete()

    db.session.delete(template)
    db.session.commit()

    return redirect(url_for('campaign_library', campaign_id=campaign_id))

@app.route('/api/reorder', methods=['POST'])
def reorder_items():
    data = request.json
    item_type = data.get('type')
    items = data.get('items', [])

    if item_type == 'adventure':
        for idx, item_id in enumerate(items):
            adventure = Adventure.query.get(item_id)
            if adventure:
                adventure.order = idx
        db.session.commit()
    elif item_type == 'scene':
        for idx, item_id in enumerate(items):
            scene = Scene.query.get(item_id)
            if scene:
                scene.order = idx
        db.session.commit()

    return jsonify({'success': True})

@app.route('/api/campaign/<int:campaign_id>/templates')
def get_campaign_templates(campaign_id):
    templates = Template.query.filter_by(campaign_id=campaign_id).all()
    return jsonify([{'id': t.id, 'name': t.name, 'type': t.type} for t in templates])

@app.route('/campaign/<int:campaign_id>/library/import', methods=['POST'])
def import_template(campaign_id):
    source_campaign_id = request.form.get('source_campaign_id')
    template_id = request.form.get('template_id')

    if source_campaign_id and template_id:
        source_template = Template.query.get(template_id)
        if source_template and str(source_template.campaign_id) == str(source_campaign_id):
            new_template = Template(
                name=source_template.name,
                type=source_template.type,
                image_path=source_template.image_path,
                campaign_id=campaign_id
            )
            db.session.add(new_template)
            db.session.commit()

    return redirect(url_for('campaign_library', campaign_id=campaign_id))

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
