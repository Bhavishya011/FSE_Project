from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from typing import List, Dict, Any
import json
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.analytics.aggregate import DataAggregator

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'),
            static_url_path='')

aggregator = DataAggregator(epsilon=1.0)

# In-memory storage for demo purposes
sensor_data: List[Dict[str, Any]] = []

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Get privacy-protected metrics for a given time range.
    
    Query parameters:
    - type: metric type (e.g., 'traffic')
    - start: ISO format start timestamp
    - end: ISO format end timestamp
    """
    try:
        metric_type = request.args.get('type', 'traffic')
        start_time = datetime.fromisoformat(request.args.get('start'))
        end_time = datetime.fromisoformat(request.args.get('end'))
        
        # Filter data for the requested time range
        filtered_data = [
            record for record in sensor_data
            if start_time <= datetime.fromisoformat(record['timestamp']) <= end_time
        ]
        
        if not filtered_data:
            return jsonify({'error': 'No data available for the specified time range'}), 404
        
        # Get hourly aggregates with privacy protection
        hourly_data = aggregator.aggregate_hourly(filtered_data)
        
        return jsonify({
            'metric_type': metric_type,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'data': hourly_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/data', methods=['POST'])
def receive_data():
    """Receive sensor data from the simulator."""
    try:
        data = request.get_json()
        if not isinstance(data, list):
            data = [data]
            
        sensor_data.extend(data)
        return jsonify({'message': 'Data received successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 