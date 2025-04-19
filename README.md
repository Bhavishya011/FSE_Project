# Privacy-Preserving IoT Smart City Demo

A demonstration of privacy-preserving data collection and analytics for IoT sensors in a smart city environment.

## Features

- Simulated IoT sensor data generation with pseudonymized sensor IDs
- Differential privacy protection using Laplace mechanism
- Real-time data aggregation and visualization
- Simple web dashboard for monitoring privacy-protected metrics

## Project Structure

```
.
├── requirements/           # Project dependencies
├── src/
│   ├── data_collection/   # IoT sensor simulator
│   ├── privacy_engine/    # Differential privacy implementation
│   ├── analytics/         # Data aggregation and analysis
│   └── web_app/          # Web dashboard
├── tests/                # Unit tests
└── deployment/           # Docker configuration
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements/requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest tests/
   ```

3. Start the services using Docker:
   ```bash
   cd deployment
   docker-compose up --build
   ```

4. Access the web dashboard at http://localhost:5000

## Components

### Data Simulator
- Generates synthetic IoT sensor data
- Pseudonymizes sensor IDs
- Emits data at regular intervals

### Privacy Engine
- Implements differential privacy using Laplace mechanism
- Configurable privacy budget (epsilon)
- Noise calibration based on data range

### Analytics
- Hourly aggregation of sensor data
- Privacy-protected statistics
- Basic data analysis functions

### Web Dashboard
- Real-time visualization of privacy-protected metrics
- Time-range selection for historical data
- Simple bar chart and table display

## Privacy Considerations

- Sensor IDs are pseudonymized using SHA-256 hashing
- Differential privacy is applied to all aggregated metrics
- Privacy budget (epsilon) can be adjusted based on requirements
- Noise calibration adapts to data range for optimal utility

## License

MIT License 