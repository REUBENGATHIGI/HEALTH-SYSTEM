# test_app.py
import pytest
from app import create_app
from models import db, Client, Program

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_client_registration(client):
    # Test valid registration
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'date_of_birth': '1990-01-01'
    }
    response = client.post('/api/clients', json=data)
    assert response.status_code == 201
    assert b'id' in response.data

def test_program_creation(client):
    # Test valid program creation
    data = {'name': 'Diabetes Care', 'description': 'Management program'}
    response = client.post('/api/programs', json=data)
    assert response.status_code == 201
    assert b'Diabetes Care' in response.data

def test_enrollment(client):
    # Setup test data
    client_data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice@example.com',
        'date_of_birth': '1985-05-05'
    }
    program_data = {'name': 'Malaria Prevention'}
    
    client.post('/api/clients', json=client_data)
    client.post('/api/programs', json=program_data)
    
    # Test enrollment
    enrollment_data = {'client_id': 1, 'program_id': 1}
    response = client.post('/api/enrollments', json=enrollment_data)
    assert response.status_code == 201
    assert b'client_id' in response.data