from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from typing import List, Dict, Any
import json
import sys
import os
import logging
from logging.handlers import RotatingFileHandler

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.analytics.aggregate import DataAggregator
from src.privacy_engine.dp_engine import DPEngine

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'),
            static_url_path='')

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')
    
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Application startup')

# Initialize components
dp_engine = DPEngine(epsilon=1.0)  # Default epsilon
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
    - type: metric type (e.g., 'traffic', 'pollution', 'energy')
    - epsilon: privacy budget (default: 1.0)
    - start: ISO format start timestamp
    - end: ISO format end timestamp
    """
    try:
        # Get and validate parameters
        metric_type = request.args.get('type', 'traffic')
        if metric_type not in ['traffic', 'pollution', 'energy']:
            return jsonify({'error': 'Invalid metric type'}), 400
            
        epsilon = float(request.args.get('epsilon', 1.0))
        if not 0.1 <= epsilon <= 3.0:
            return jsonify({'error': 'Epsilon must be between 0.1 and 3.0'}), 400
            
        start_time = datetime.fromisoformat(request.args.get('start'))
        end_time = datetime.fromisoformat(request.args.get('end'))
        
        # Log request
        app.logger.info(f"Metrics request - Type: {metric_type}, Epsilon: {epsilon}, "
                       f"Start: {start_time}, End: {end_time}")
        
        # Filter data for the requested time range
        filtered_data = [
            record for record in sensor_data
            if start_time <= datetime.fromisoformat(record['timestamp']) <= end_time
        ]
        
        if not filtered_data:
            app.logger.warning(f"No data found for time range {start_time} to {end_time}")
            return jsonify({'error': 'No data available for the specified time range'}), 404
        
        # Get hourly aggregates
        hourly_data = aggregator.aggregate_hourly(filtered_data)
        
        # Apply differential privacy with the specified epsilon
        dp_engine.epsilon = epsilon
        protected_data = []
        
        for record in hourly_data:
            original_value = record['original_value']
            protected_value = dp_engine.apply_dp(original_value)
            
            # Log the privacy application
            app.logger.info(f"Applied DP - Original: {original_value:.2f}, "
                          f"Protected: {protected_value:.2f}, Epsilon: {epsilon}")
            
            protected_data.append({
                'timestamp': record['timestamp'],
                'sensor_id': record['sensor_id'],
                'lat': record['lat'],
                'lon': record['lon'],
                'original_value': original_value,
                'protected_value': protected_value
            })
        
        return jsonify({
            'type': metric_type,
            'epsilon': epsilon,
            'data': protected_data
        })
        
    except ValueError as e:
        app.logger.error(f"Value error in metrics endpoint: {str(e)}")
        return jsonify({'error': 'Invalid parameter format'}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error in metrics endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/data', methods=['POST'])
def receive_data():
    """Receive sensor data from the simulator."""
    try:
        data = request.get_json()
        if not isinstance(data, list):
            data = [data]
            
        sensor_data.extend(data)
        app.logger.info(f"Received {len(data)} new data points")
        return jsonify({'message': 'Data received successfully'})
        
    except Exception as e:
        app.logger.error(f"Error receiving data: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 