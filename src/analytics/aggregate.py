import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..privacy_engine.dp_engine import DPEngine

class DataAggregator:
    def __init__(self, epsilon: float = 1.0):
        self.dp_engine = DPEngine(epsilon)
        
    def _parse_timestamp(self, record: Dict[str, Any]) -> datetime:
        """Parse ISO format timestamp from record."""
        return datetime.fromisoformat(record['timestamp'])
    
    def aggregate_hourly(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aggregate records by hour and apply differential privacy.
        
        Args:
            records: List of sensor records
            
        Returns:
            List of aggregated and privacy-protected records
        """
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(records)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by hour and sensor_id
        hourly_agg = df.groupby([
            pd.Grouper(key='timestamp', freq='H'),
            'sensor_id'
        ]).agg({
            'value': 'mean',
            'lat': 'first',
            'lon': 'first'
        }).reset_index()
        
        # Apply differential privacy to the aggregated values
        protected_values = self.dp_engine.apply_dp_batch(hourly_agg['value'].tolist())
        hourly_agg['protected_value'] = protected_values
        
        # Convert back to list of dictionaries
        result = []
        for _, row in hourly_agg.iterrows():
            result.append({
                'timestamp': row['timestamp'].isoformat(),
                'sensor_id': row['sensor_id'],
                'lat': row['lat'],
                'lon': row['lon'],
                'original_value': row['value'],
                'protected_value': row['protected_value']
            })
            
        return result
    
    def get_sensor_stats(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate basic statistics for sensor data.
        
        Args:
            records: List of sensor records
            
        Returns:
            Dictionary containing min, max, and range of values
        """
        values = [r['value'] for r in records]
        return {
            'min': min(values),
            'max': max(values),
            'range': max(values) - min(values)
        } 