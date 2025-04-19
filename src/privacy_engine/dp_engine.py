import numpy as np
from typing import List, Union
import logging
import os
from logging.handlers import RotatingFileHandler

class DPEngine:
    def __init__(self, epsilon: float = 1.0):
        """
        Initialize the differential privacy engine.
        
        Args:
            epsilon: Privacy budget (smaller values = more privacy)
        """
        self.epsilon = epsilon
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging for privacy operations."""
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Create a separate logger for privacy operations
        self.logger = logging.getLogger('privacy')
        self.logger.setLevel(logging.INFO)
        
        # Add file handler if not already added
        if not self.logger.handlers:
            file_handler = RotatingFileHandler(
                'logs/privacy.log',
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s'
            ))
            self.logger.addHandler(file_handler)
    
    def _laplace_noise(self, scale: float) -> float:
        """Generate Laplace noise with given scale."""
        return np.random.laplace(0, scale)
    
    def apply_dp(self, value: float) -> float:
        """
        Apply differential privacy to a single value using Laplace mechanism.
        
        Args:
            value: The original value to protect
            
        Returns:
            The differentially private value
        """
        # For Laplace mechanism, scale = sensitivity / epsilon
        # Assuming sensitivity of 1 for traffic counts
        scale = 1.0 / self.epsilon
        noise = self._laplace_noise(scale)
        protected_value = value + noise
        
        # Log the privacy operation
        self.logger.info(
            f"Applied DP - Original: {value:.2f}, "
            f"Epsilon: {self.epsilon:.2f}, "
            f"Noise: {noise:.2f}, "
            f"Protected: {protected_value:.2f}"
        )
        
        return protected_value
    
    def apply_dp_batch(self, values: List[float]) -> List[float]:
        """
        Apply differential privacy to a list of values.
        
        Args:
            values: List of original values to protect
            
        Returns:
            List of differentially private values
        """
        return [self.apply_dp(v) for v in values]
    
    def calibrate_noise(self, data_range: Union[float, tuple]) -> float:
        """
        Calibrate noise based on data range.
        
        Args:
            data_range: Either a single value (max - min) or tuple (min, max)
            
        Returns:
            Recommended epsilon value
        """
        if isinstance(data_range, tuple):
            sensitivity = data_range[1] - data_range[0]
        else:
            sensitivity = data_range
            
        # Simple heuristic: epsilon = 1/sensitivity
        # This ensures noise scale is proportional to data range
        return 1.0 / sensitivity 