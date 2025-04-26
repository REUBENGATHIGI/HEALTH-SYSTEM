# routes.py
from flask import jsonify, request, render_template
from services import ClientService, ProgramService, EnrollmentService
from models import db

def create_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/api/clients', methods=['POST'])
    def register_client():
        data = request.json
        required = ['first_name', 'last_name', 'email', 'date_of_birth']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing fields'}), 400

        try:
            client = ClientService.register_client(
                data['first_name'],
                data['last_name'],
                data['email'],
                data['date_of_birth']
            )
            return jsonify({
                'id': client.id,
                'name': f"{client.first_name} {client.last_name}"
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except RuntimeError:
            return jsonify({'error': 'Server error'}), 500

    @app.route('/api/clients/search', methods=['GET'])
    def search_clients():
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'error': 'Search term required'}), 400
        
        try:
            clients = ClientService.search_clients(search_term)
            return jsonify([{
                'id': c.id,
                'name': f"{c.first_name} {c.last_name}",
                'email': c.email
            } for c in clients])
        except RuntimeError:
            return jsonify({'error': 'Search failed'}), 500

    @app.route('/api/programs', methods=['POST'])
    def create_program():
        data = request.json
        if 'name' not in data:
            return jsonify({'error': 'Name required'}), 400
        
        try:
            program = ProgramService.create_program(
                data['name'],
                data.get('description', '')
            )
            return jsonify({'id': program.id, 'name': program.name}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except RuntimeError:
            return jsonify({'error': 'Server error'}), 500

    @app.route('/api/enrollments', methods=['POST'])
    def enroll_client():
        data = request.json
        required = ['client_id', 'program_id']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing IDs'}), 400
        
        try:
            enrollment = EnrollmentService.enroll_client(
                data['client_id'],
                data['program_id']
            )
            return jsonify({
                'id': enrollment.id,
                'client_id': enrollment.client_id,
                'program_id': enrollment.program_id
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except RuntimeError:
            return jsonify({'error': 'Server error'}), 500