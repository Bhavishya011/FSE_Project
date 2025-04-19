import pytest
from src.data_collection.simulator import SensorSimulator

def test_sensor_simulator_initialization():
    simulator = SensorSimulator(num_sensors=3)
    assert len(simulator.sensor_locations) == 3
    
def test_pseudonymization():
    simulator = SensorSimulator()
    sensor_id = "test_sensor"
    pseudonym = simulator._pseudonymize_sensor_id(sensor_id)
    
    # Check that pseudonym is different from original
    assert pseudonym != sensor_id
    
    # Check that pseudonym is consistent
    assert simulator._pseudonymize_sensor_id(sensor_id) == pseudonym
    
def test_record_generation():
    simulator = SensorSimulator()
    record = simulator.generate_record()
    
    # Check required fields
    assert 'sensor_id' in record
    assert 'lat' in record
    assert 'lon' in record
    assert 'value' in record
    assert 'timestamp' in record
    
    # Check value ranges
    assert 0 <= record['value'] <= 100
    assert 37.7 <= record['lat'] <= 37.8
    assert -122.5 <= record['lon'] <= -122.4 