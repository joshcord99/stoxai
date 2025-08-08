import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'Stock Analyst API is running' in data['message']

def test_available_assets(client):
    """Test the available assets endpoint"""
    response = client.get('/api/available-assets')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'assets' in data
    assert len(data['assets']) > 0

def test_available_stocks(client):
    """Test the available stocks endpoint"""
    response = client.get('/api/available-stocks')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'stocks' in data
    assert len(data['stocks']) > 0 