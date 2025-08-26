"""
Unit tests for MeTTa integration module.
Tests input validation, error handling, and basic functionality.
"""

import unittest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from metta_integration import validate_input, find_optimal_route

class TestMeTTaIntegration(unittest.TestCase):
    """Test cases for MeTTa integration functionality"""
    
    def test_validate_input_valid(self):
        """Test validation of valid input parameters"""
        error = validate_input("JFK", "LHR", "speed")
        self.assertIsNone(error)
    
    def test_validate_input_invalid_airport(self):
        """Test validation of invalid airport codes"""
        error = validate_input("JK", "LHR", "speed")
        self.assertEqual(error, "Departure must be a 3-letter airport code")
        
        error = validate_input("JFK", "LON", "speed")
        self.assertEqual(error, "Destination must be a 3-letter airport code")
    
    def test_validate_input_same_airports(self):
        """Test validation of same departure and destination"""
        error = validate_input("JFK", "JFK", "speed")
        self.assertEqual(error, "Departure and destination cannot be the same")
    
    def test_validate_input_invalid_priority(self):
        """Test validation of invalid priority"""
        error = validate_input("JFK", "LHR", "invalid")
        self.assertEqual(error, "Priority must be one of: speed, cost, comfort")
    
    def test_find_optimal_route_mock(self):
        """Test finding optimal route (mock mode)"""
        result = find_optimal_route("JFK", "LHR", "speed")
        
        self.assertIn('departure', result)
        self.assertIn('destination', result)
        self.assertIn('priority', result)
        self.assertIn('routes', result)
        
        self.assertEqual(result['departure'], 'JFK')
        self.assertEqual(result['destination'], 'LHR')
        self.assertEqual(result['priority'], 'speed')

if __name__ == '__main__':
    unittest.main()