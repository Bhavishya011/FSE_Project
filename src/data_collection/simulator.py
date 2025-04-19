import json
import time
import random
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any
import os

class SensorSimulator:
    def __init__(self, num_sensors: int = 5):
        self.num_sensors = num_sensors
        self.sensor_locations = self._generate_sensor_locations()
        self.api_url = os.getenv('API_URL', 'http://localhost:5000/data')
        
    def _generate_sensor_locations(self) -> Dict[str, Dict[str, float]]:
        """Generate random locations for sensors."""
        locations = {}
        for i in range(self.num_sensors):
            sensor_id = f"sensor_{i}"
            locations[sensor_id] = {
                "lat": random.uniform(37.7, 37.8),  # Example: San Francisco area
                "lon": random.uniform(-122.5, -122.4)
            }
        return locations
    
    def _pseudonymize_sensor_id(self, sensor_id: str) -> str:
        """Create a pseudonymized version of the sensor ID."""
        return hashlib.sha256(sensor_id.encode()).hexdigest()[:8]
    
    def generate_record(self) -> Dict[str, Any]:
        """Generate a single sensor record."""
        sensor_id = random.choice(list(self.sensor_locations.keys()))
        location = self.sensor_locations[sensor_id]
        
        return {
            "sensor_id": self._pseudonymize_sensor_id(sensor_id),
            "lat": location["lat"],
            "lon": location["lon"],
            "value": random.uniform(0, 100),  # Example: traffic count
            "timestamp": datetime.now().isoformat()
        }
    
    def send_data(self, record: Dict[str, Any]):
        """Send data to the API endpoint."""
        try:
            response = requests.post(self.api_url, json=record)
            if response.status_code != 200:
                print(f"Error sending data: {response.text}")
        except Exception as e:
            print(f"Error connecting to API: {e}")
    
    def run(self, interval: float = 1.0):
        """Run the simulator, emitting records at regular intervals."""
        try:
            while True:
                record = self.generate_record()
                print(f"Generated record: {json.dumps(record)}")
                self.send_data(record)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nSimulator stopped.")

if __name__ == "__main__":
    simulator = SensorSimulator()
    simulator.run() 