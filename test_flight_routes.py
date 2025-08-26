"""
Integration tests for flight route functionality.
Tests the complete flow from input to output.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from metta_integration import find_optimal_route

def test_basic_functionality():
    """Test basic functionality with various inputs"""
    test_cases = [
        ("JFK", "LHR", "speed"),
        ("LAX", "CDG", "cost"),
        ("SFO", "DXB", "comfort")
    ]
    
    for departure, destination, priority in test_cases:
        print(f"\nTesting: {departure} -> {destination} ({priority})")
        
        result = find_optimal_route(departure, destination, priority)
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Success: Found {len(result.get('routes', []))} routes")
            print(f"Explanation: {result.get('explanation', 'No explanation')}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_basic_functionality()