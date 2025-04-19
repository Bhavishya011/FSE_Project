import pytest
import numpy as np
from src.privacy_engine.dp_engine import DPEngine

def test_dp_engine_initialization():
    engine = DPEngine(epsilon=0.5)
    assert engine.epsilon == 0.5

def test_laplace_noise():
    engine = DPEngine(epsilon=1.0)
    noise_values = [engine._laplace_noise(1.0) for _ in range(1000)]
    
    # Check that noise is centered around 0
    assert abs(np.mean(noise_values)) < 0.1
    
    # Check that noise has the expected variance
    variance = np.var(noise_values)
    expected_variance = 2.0  # For scale=1.0
    assert abs(variance - expected_variance) < 0.5

def test_apply_dp():
    engine = DPEngine(epsilon=1.0)
    original_value = 50.0
    
    # Test multiple applications to check noise addition
    protected_values = [engine.apply_dp(original_value) for _ in range(100)]
    
    # Check that values are different from original
    assert not all(v == original_value for v in protected_values)
    
    # Check that values are within reasonable range
    for v in protected_values:
        assert abs(v - original_value) < 10.0  # With epsilon=1.0, noise should be relatively small

def test_calibrate_noise():
    engine = DPEngine()
    
    # Test with range tuple
    epsilon1 = engine.calibrate_noise((0, 100))
    assert epsilon1 == 0.01  # 1/100
    
    # Test with single range value
    epsilon2 = engine.calibrate_noise(50)
    assert epsilon2 == 0.02  # 1/50 