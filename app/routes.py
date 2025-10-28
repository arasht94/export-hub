from flask import Blueprint, render_template, send_file, jsonify
import os
import json
from pathlib import Path

main = Blueprint('main', __name__)

def get_models_dir():
    """Get the models directory path"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

def scan_model_cards():
    """Scan the models directory for model card JSON files"""
    models_dir = get_models_dir()
    model_cards = []
    
    if not os.path.exists(models_dir):
        return model_cards
    
    for item in os.listdir(models_dir):
        item_path = os.path.join(models_dir, item)
        if os.path.isdir(item_path):
            # Look for model_card.json in subdirectories
            card_file = os.path.join(item_path, 'model_card.json')
            if os.path.exists(card_file):
                try:
                    with open(card_file, 'r', encoding='utf-8') as f:
                        card_data = json.load(f)
                        card_data['model_id'] = item
                        model_cards.append(card_data)
                except Exception as e:
                    print(f"Error reading {card_file}: {e}")
    
    return model_cards

def get_model_card(model_id):
    """Get a specific model card by ID"""
    models_dir = get_models_dir()
    card_file = os.path.join(models_dir, model_id, 'model_card.json')
    
    if os.path.exists(card_file):
        try:
            with open(card_file, 'r', encoding='utf-8') as f:
                card_data = json.load(f)
                card_data['model_id'] = model_id
                return card_data
        except Exception as e:
            print(f"Error reading {card_file}: {e}")
    
    return None

@main.route('/')
def index():
    """Main page showing all model cards"""
    model_cards = scan_model_cards()
    return render_template('index.html', model_cards=model_cards)

@main.route('/model/<model_id>')
def model_page(model_id):
    """Individual model card page"""
    model_card = get_model_card(model_id)
    
    if not model_card:
        return render_template('404.html', message=f"Model card '{model_id}' not found"), 404
    
    return render_template('model_card.html', card=model_card)

@main.route('/download/<model_id>/<filename>')
def download_file(model_id, filename):
    """Download endpoint for model files"""
    models_dir = get_models_dir()
    file_path = os.path.join(models_dir, model_id, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

