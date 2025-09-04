from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import db, AIModel
from config import Config
from openrouter_client import OpenRouterClient
import os
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Setup configuration file
    SETUP_FILE = 'setup_config.json'

    def get_setup_config():
        if os.path.exists(SETUP_FILE):
            with open(SETUP_FILE, 'r') as f:
                return json.load(f)
        return None

    def save_setup_config(config):
        with open(SETUP_FILE, 'w') as f:
            json.dump(config, f)

    def is_setup_complete():
        config = get_setup_config()
        return config is not None and config.get('setup_complete', False)

    def login_required(f):
        """Decorator to require login for protected routes"""
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    def setup_required(f):
        """Decorator to require setup completion"""
        def decorated_function(*args, **kwargs):
            if not is_setup_complete():
                return redirect(url_for('setup'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function

    # OpenRouter model definitions - updated with new free models
    OPENROUTER_MODELS = {
        'free': [
            {'id': 'cognitivecomputations/dolphin-mistral-24b-venice-edition:free', 'name': 'Dolphin Mistral 24B', 'description': 'High-quality uncensored conversational model', 'price': '$0.00/M'},
            {'id': 'deepseek/deepseek-r1-0528-qwen3-8b:free', 'name': 'DeepSeek R1 Qwen3 8B', 'description': 'Fast reasoning model with 8B parameters', 'price': '$0.00/M'},
            {'id': 'deepseek/deepseek-r1-0528:free', 'name': 'DeepSeek R1', 'description': 'Advanced reasoning model with strong performance', 'price': '$0.00/M'},
            {'id': 'mistralai/devstral-small-2505:free', 'name': 'Devstral Small', 'description': 'Code-optimized model for development tasks', 'price': '$0.00/M'},
            {'id': 'meta-llama/llama-4-maverick:free', 'name': 'Llama 4 Maverick', 'description': 'Meta\'s latest Llama 4 variant with enhanced capabilities', 'price': '$0.00/M'},
            {'id': 'meta-llama/llama-4-scout:free', 'name': 'Llama 4 Scout', 'description': 'Lightweight Llama 4 model for exploration', 'price': '$0.00/M'},
            {'id': 'google/gemini-2.5-flash-image-preview:free', 'name': 'Gemini 2.5 Flash Image', 'description': 'Google\'s multimodal model with image generation capabilities', 'price': '$0.00/M'}
        ],
        'paid': []
    }

    @app.route('/')
    def root():
        if not is_setup_complete():
            return redirect(url_for('setup'))
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return redirect(url_for('dashboard'))

    @app.route('/setup')
    def setup():
        if is_setup_complete():
            return redirect(url_for('root'))
        return render_template('setup.html')

    @app.route('/setup_step/<int:step>')
    def setup_step(step):
        if is_setup_complete():
            return redirect(url_for('root'))
        return render_template('setup.html', step=step)

    @app.route('/complete_setup', methods=['POST'])
    def complete_setup():
        try:
            data = request.json
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            api_key = data.get('api_key')
            selected_models = data.get('selected_models', [])

            if not password or not confirm_password or not api_key:
                return jsonify({'success': False, 'error': 'All fields are required'})

            if password != confirm_password:
                return jsonify({'success': False, 'error': 'Passwords do not match'})

            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            # Save setup configuration
            config = {
                'setup_complete': True,
                'password_hash': password_hash,
                'api_key': api_key
            }
            save_setup_config(config)

            # Create database tables
            with app.app_context():
                db.create_all()

                # Add selected models to database
                for model_data in selected_models:
                    if model_data.get('enabled', False):
                        existing_model = AIModel.query.filter_by(official_name=model_data['id']).first()
                        if not existing_model:
                            new_model = AIModel(
                                name=model_data['name'],
                                official_name=model_data['id'],
                                api_key=api_key,
                                is_active=True
                            )
                            db.session.add(new_model)

                db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/login', methods=['GET', 'POST'])
    @setup_required
    def login():
        if session.get('logged_in'):
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            password = request.form.get('password')

            config = get_setup_config()
            if not config:
                flash('Setup not completed', 'error')
                return redirect(url_for('setup'))

            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if password_hash == config.get('password_hash'):
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password!', 'error')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('Logged out successfully!', 'success')
        return redirect(url_for('login'))

    @app.route('/forgot_password', methods=['POST'])
    @setup_required
    def forgot_password():
        # Delete setup config and all models
        if os.path.exists(SETUP_FILE):
            os.remove(SETUP_FILE)

        with app.app_context():
            try:
                AIModel.query.delete()
                db.session.commit()
            except:
                pass

        session.clear()
        return jsonify({'success': True, 'message': 'All data has been reset. You can now start the setup process again.'})

    @app.route('/dashboard')
    @setup_required
    @login_required
    def dashboard():
        models = AIModel.query.all()

        # Categorize models
        free_models = []
        paid_models = []

        for model in models:
            # Check if model is in free list
            is_free = any(free_model['id'] == model.official_name for free_model in OPENROUTER_MODELS['free'])
            if is_free:
                free_models.append(model)
            else:
                paid_models.append(model)

        return render_template('dashboard.html',
                             free_models=free_models,
                             paid_models=paid_models,
                             available_models=OPENROUTER_MODELS)

    @app.route('/settings')
    @setup_required
    @login_required
    def settings():
        config = get_setup_config()
        return render_template('settings.html', config=config)

    @app.route('/update_password', methods=['POST'])
    @setup_required
    @login_required
    def update_password():
        try:
            data = request.json
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not all([current_password, new_password, confirm_password]):
                return jsonify({'success': False, 'error': 'All fields are required'})

            if new_password != confirm_password:
                return jsonify({'success': False, 'error': 'New passwords do not match'})

            config = get_setup_config()
            current_hash = hashlib.sha256(current_password.encode()).hexdigest()

            if current_hash != config.get('password_hash'):
                return jsonify({'success': False, 'error': 'Current password is incorrect'})

            # Update password
            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
            config['password_hash'] = new_hash
            save_setup_config(config)

            return jsonify({'success': True, 'message': 'Password updated successfully'})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/update_api_key', methods=['POST'])
    @setup_required
    @login_required
    def update_api_key():
        try:
            data = request.json
            new_api_key = data.get('api_key')

            if not new_api_key:
                return jsonify({'success': False, 'error': 'API key is required'})

            config = get_setup_config()
            config['api_key'] = new_api_key
            save_setup_config(config)

            # Update all model API keys
            models = AIModel.query.all()
            for model in models:
                model.api_key = new_api_key
            db.session.commit()

            return jsonify({'success': True, 'message': 'API key updated successfully'})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/add_model', methods=['POST'])
    @setup_required
    @login_required
    def add_model():
        try:
            data = request.json
            model_id = data.get('model_id')
            model_name = data.get('model_name')

            if not model_id or not model_name:
                return jsonify({'success': False, 'error': 'Model ID and name are required'})

            # Check if model already exists
            existing_model = AIModel.query.filter_by(official_name=model_id).first()
            if existing_model:
                return jsonify({'success': False, 'error': 'Model already exists'})

            config = get_setup_config()
            api_key = config.get('api_key')

            new_model = AIModel(
                name=model_name,
                official_name=model_id,
                api_key=api_key,
                is_active=True
            )

            db.session.add(new_model)
            db.session.commit()

            return jsonify({'success': True, 'message': f'Model {model_name} added successfully'})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/toggle_model/<int:model_id>', methods=['POST'])
    @setup_required
    @login_required
    def toggle_model(model_id):
        try:
            model = AIModel.query.get_or_404(model_id)
            model.is_active = not model.is_active
            db.session.commit()
            return jsonify({'success': True, 'is_active': model.is_active})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/delete_model/<int:model_id>', methods=['POST'])
    @setup_required
    @login_required
    def delete_model(model_id):
        try:
            model = AIModel.query.get_or_404(model_id)
            db.session.delete(model)
            db.session.commit()
            return jsonify({'success': True, 'message': f'Model {model.name} deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/test_model/<int:model_id>', methods=['POST'])
    @setup_required
    @login_required
    def test_model(model_id):
        try:
            model = AIModel.query.get_or_404(model_id)
            test_message = request.json.get('message', 'Hello, how are you?')

            client = OpenRouterClient(model.api_key)
            response = client.generate_response(model.official_name, test_message)

            if response:
                return jsonify({
                    'success': True,
                    'response': response,
                    'model_name': model.name
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to get response from model'
                })

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'Discord AI Bot is running'}, 200

    @app.route('/api/models')
    @setup_required
    @login_required
    def api_models():
        """API endpoint for getting available OpenRouter models"""
        return jsonify(OPENROUTER_MODELS)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
