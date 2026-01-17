from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import db, Hero, Power, HeroPower
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Superheroes API"}), 200

# Get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes]), 200

# Get a specific hero
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    # Serialize 
    hero_dict = hero.to_dict(only=(
        'id', 
        'name', 
        'super_name', 
        'hero_powers.id',
        'hero_powers.hero_id',
        'hero_powers.power_id',
        'hero_powers.strength',
        'hero_powers.power.id',
        'hero_powers.power.name',
        'hero_powers.power.description'
    ))
    
    return jsonify(hero_dict), 200

# Get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict(only=('id', 'name', 'description')) for power in powers]), 200

#  Get a specific power
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    return jsonify(power.to_dict(only=('id', 'name', 'description'))), 200

# Update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data['description']
        
        db.session.commit()
        
        return jsonify(power.to_dict(only=('id', 'name', 'description'))), 200
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# Create a new HeroPower
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        # Validate that hero and power exist
        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))
        
        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found"]}), 404
        
        # Create new HeroPower
        new_hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        
        db.session.add(new_hero_power)
        db.session.commit()
        
        # Return the created HeroPower with nested hero and power data
        response = new_hero_power.to_dict(only=(
            'id',
            'hero_id',
            'power_id',
            'strength',
            'hero.id',
            'hero.name',
            'hero.super_name',
            'power.id',
            'power.name',
            'power.description'
        ))
        
        return jsonify(response), 201
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# Email route 
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        
        msg = Message(
            subject=data.get('subject', 'Superheroes API Notification'),
            recipients=[data.get('recipient')],
            body=data.get('body', 'This is a test email from Superheroes API')
        )
        
        mail.send(msg)
        
        return jsonify({"message": "Email sent successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)