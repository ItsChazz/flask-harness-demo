#Unit tests
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data

def test_health(client):
    """Test the health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_info(client):
    """Test the info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == 'Python Flask Demo'
    assert data['version'] == '1.0.0'
