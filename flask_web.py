from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import db, AIModel
from config import Config
from openrouter_client import OpenRouterClient
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Admin password hash
    ADMIN_PASSWORD = os.getenv("UI_PASSWORD", "default_password")
    ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
    
    def login_required(f):
        """Decorator to require login for protected routes"""
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            password = request.form.get('password')
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if password_hash == ADMIN_PASSWORD_HASH:
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid password!', 'error')
                return redirect(url_for('login'))
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('Logged out successfully!', 'success')
        return redirect(url_for('login'))
    
    @app.route('/')
    def root():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def index():
        models = AIModel.query.all()
        return render_template('index.html', models=models)
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'Discord AI Bot is running'}, 200
    
    @app.route('/test_debug')
    def test_debug():
        """Simple debug endpoint to test if the app is working"""
        try:
            models = AIModel.query.all()
            model_info = []
            for model in models:
                model_info.append({
                    'id': model.id,
                    'name': model.name,
                    'official_name': model.official_name,
                    'is_active': model.is_active
                })
            return jsonify({
                'success': True,
                'models': model_info,
                'total_models': len(models)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @app.route('/test_model/<int:model_id>', methods=['POST'])
    @login_required
    def test_model(model_id):
        try:
            model = AIModel.query.get_or_404(model_id)
            test_message = request.form.get('test_message', 'Hello, how are you?')
            
            print(f"Testing model: {model.name}")
            print(f"Test message: {test_message}")
            print(f"Official name: {model.official_name}")
            
            # Test the model with OpenRouter
            client = OpenRouterClient(model.api_key)
            response = client.generate_response(model.official_name, test_message)
            
            print(f"Response received: {response is not None}")
            
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
            print(f"Error testing model: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @app.route('/add_model', methods=['GET', 'POST'])
    @login_required
    def add_model():
        if request.method == 'POST':
            name = request.form.get('name')
            official_name = request.form.get('official_name')
            api_key = request.form.get('api_key')
            
            if not all([name, official_name, api_key]):
                flash('All fields are required!', 'error')
                return redirect(url_for('add_model'))
            
            # Check if model name already exists
            existing_model = AIModel.query.filter_by(name=name).first()
            if existing_model:
                flash('A model with this name already exists!', 'error')
                return redirect(url_for('add_model'))
            
            new_model = AIModel(
                name=name,
                official_name=official_name,
                api_key=api_key
            )
            
            db.session.add(new_model)
            db.session.commit()
            
            flash('Model added successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('add_model.html')
    
    @app.route('/edit_model/<int:model_id>', methods=['GET', 'POST'])
    @login_required
    def edit_model(model_id):
        model = AIModel.query.get_or_404(model_id)
        
        if request.method == 'POST':
            model.name = request.form.get('name')
            model.official_name = request.form.get('official_name')
            model.api_key = request.form.get('api_key')
            model.is_active = 'is_active' in request.form
            
            db.session.commit()
            flash('Model updated successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('edit_model.html', model=model)
    
    @app.route('/delete_model/<int:model_id>', methods=['POST'])
    @login_required
    def delete_model(model_id):
        model = AIModel.query.get_or_404(model_id)
        db.session.delete(model)
        db.session.commit()
        flash('Model deleted successfully!', 'success')
        return redirect(url_for('index'))
    
    @app.route('/toggle_model/<int:model_id>', methods=['POST'])
    @login_required
    def toggle_model(model_id):
        model = AIModel.query.get_or_404(model_id)
        model.is_active = not model.is_active
        db.session.commit()
        return jsonify({'success': True, 'is_active': model.is_active})
    
    @app.route('/toggle_team_only/<int:model_id>', methods=['POST'])
    @login_required
    def toggle_team_only(model_id):
        model = AIModel.query.get_or_404(model_id)
        model.team_only = not model.team_only
        db.session.commit()
        return jsonify({'success': True, 'team_only': model.team_only})
    
    return app

# Create templates directory and HTML files
def create_templates():
    os.makedirs('templates', exist_ok=True)
    
    # Base template
    base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Discord AI Bot Manager{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .navbar-brand { font-weight: bold; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); }
        .btn-toggle { transition: all 0.3s ease; }
        .model-card { transition: transform 0.2s ease; }
        .model-card:hover { transform: translateY(-2px); }
    </style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-robot me-2"></i>Discord AI Bot Manager
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleModel(modelId) {
            fetch(`/toggle_model/${modelId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const btn = document.querySelector(`[data-model-id="${modelId}"]`);
                    const icon = btn.querySelector('i');
                    if (data.is_active) {
                        btn.classList.remove('btn-outline-secondary');
                        btn.classList.add('btn-success');
                        icon.className = 'fas fa-toggle-on';
                    } else {
                        btn.classList.remove('btn-success');
                        btn.classList.add('btn-outline-secondary');
                        icon.className = 'fas fa-toggle-off';
                    }
                }
            });
        }
    </script>
</body>
</html>'''
    
    # Index template
    index_html = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="fas fa-cogs me-2"></i>AI Models</h2>
            <a href="{{ url_for('add_model') }}" class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Add New Model
            </a>
        </div>
    </div>
</div>

{% if models %}
    <div class="row">
        {% for model in models %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card model-card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-brain me-2"></i>{{ model.name }}
                    </h5>
                    <div class="btn-group" role="group">
                        <button class="btn btn-sm {{ 'btn-success' if model.is_active else 'btn-outline-secondary' }}" 
                                onclick="toggleModel({{ model.id }})" 
                                data-model-id="{{ model.id }}"
                                title="{{ 'Active' if model.is_active else 'Inactive' }}">
                            <i class="fas {{ 'fa-toggle-on' if model.is_active else 'fa-toggle-off' }}"></i>
                        </button>
                        <a href="{{ url_for('edit_model', model_id=model.id) }}" 
                           class="btn btn-sm btn-outline-primary" title="Edit">
                            <i class="fas fa-edit"></i>
                        </a>
                        <button class="btn btn-sm btn-outline-danger" 
                                onclick="if(confirm('Are you sure you want to delete this model?')) document.getElementById('delete-form-{{ model.id }}').submit();"
                                title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        <strong>Official Name:</strong><br>
                        <code class="small">{{ model.official_name }}</code>
                    </p>
                    <p class="card-text">
                        <strong>API Key:</strong><br>
                        <code class="small">{{ model.api_key[:20] }}...</code>
                    </p>
                    <p class="card-text">
                        <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>
                            Created: {{ model.created_at.strftime('%Y-%m-%d %H:%M') }}
                        </small>
                    </p>
                </div>
            </div>
        </div>
        
        <form id="delete-form-{{ model.id }}" action="{{ url_for('delete_model', model_id=model.id) }}" method="POST" style="display: none;"></form>
        {% endfor %}
    </div>
{% else %}
    <div class="text-center py-5">
        <i class="fas fa-robot fa-3x text-muted mb-3"></i>
        <h4 class="text-muted">No AI Models Found</h4>
        <p class="text-muted">Get started by adding your first AI model.</p>
        <a href="{{ url_for('add_model') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Add Your First Model
        </a>
    </div>
{% endif %}
{% endblock %}'''
    
    # Add model template
    add_model_html = '''{% extends "base.html" %}

{% block title %}Add New Model - Discord AI Bot Manager{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">
                    <i class="fas fa-plus me-2"></i>Add New AI Model
                </h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="name" class="form-label">Model Name</label>
                        <input type="text" class="form-control" id="name" name="name" required 
                               placeholder="e.g., GPT-4, Claude-3, etc.">
                        <div class="form-text">A friendly name for the model (used in Discord commands)</div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="official_name" class="form-label">Official Model Name</label>
                        <input type="text" class="form-control" id="official_name" name="official_name" required 
                               placeholder="e.g., openai/gpt-4, anthropic/claude-3-sonnet">
                        <div class="form-text">The official model identifier from OpenRouter</div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="api_key" class="form-label">OpenRouter API Key</label>
                        <input type="password" class="form-control" id="api_key" name="api_key" required 
                               placeholder="sk-or-v1-...">
                        <div class="form-text">Your OpenRouter API key for this model</div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Add Model
                        </button>
                        <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Back to Models
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Edit model template
    edit_model_html = '''{% extends "base.html" %}

{% block title %}Edit Model - Discord AI Bot Manager{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">
                    <i class="fas fa-edit me-2"></i>Edit AI Model
                </h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="name" class="form-label">Model Name</label>
                        <input type="text" class="form-control" id="name" name="name" 
                               value="{{ model.name }}" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="official_name" class="form-label">Official Model Name</label>
                        <input type="text" class="form-control" id="official_name" name="official_name" 
                               value="{{ model.official_name }}" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="api_key" class="form-label">OpenRouter API Key</label>
                        <input type="password" class="form-control" id="api_key" name="api_key" 
                               value="{{ model.api_key }}" required>
                    </div>
                    
                    <div class="mb-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="is_active" name="is_active" 
                                   {{ 'checked' if model.is_active else '' }}>
                            <label class="form-check-label" for="is_active">
                                Active (available for use)
                            </label>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Update Model
                        </button>
                        <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Back to Models
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Write template files
    with open('templates/base.html', 'w') as f:
        f.write(base_html)
    
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    
    with open('templates/add_model.html', 'w') as f:
        f.write(add_model_html)
    
    with open('templates/edit_model.html', 'w') as f:
        f.write(edit_model_html)

# Don't overwrite existing templates
# create_templates() 