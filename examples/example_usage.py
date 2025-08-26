"""
Example usage of SkyRoute flight finding functionality.
Demonstrates how to use the MeTTa integration module programmatically.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from metta_integration import find_optimal_route, validate_input

def demonstrate_usage():
    """Demonstrate various usage scenarios"""
    
    print("SkyRoute Usage Examples")
    print("=" * 50)
    
    # Example 1: Basic usage
    print("\n1. Basic Route Finding:")
    print("-" * 30)
    result = find_optimal_route("JFK", "LHR", "speed")
    print_result(result)
    
    # Example 2: Different priority
    print("\n2. Cost-Optimized Route:")
    print("-" * 30)
    result = find_optimal_route("LAX", "CDG", "cost")
    print_result(result)
    
    # Example 3: Comfort priority
    print("\n3. Comfort-Optimized Route:")
    print("-" * 30)
    result = find_optimal_route("SFO", "DXB", "comfort")
    print_result(result)
    
    # Example 4: Error handling
    print("\n4. Error Handling Examples:")
    print("-" * 30)
    
    # Invalid airport code
    print("Invalid airport code:")
    result = find_optimal_route("NY", "LHR", "speed")
    print_result(result)
    
    # Same airports
    print("\nSame departure and destination:")
    result = find_optimal_route("JFK", "JFK", "speed")
    print_result(result)
    
    # Invalid priority
    print("\nInvalid priority:")
    result = find_optimal_route("JFK", "LHR", "invalid")
    print_result(result)

def print_result(result):
    """Print the result in a formatted way"""
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Success!")
        print(f"   From: {result['departure']} → To: {result['destination']}")
        print(f"   Priority: {result['priority']}")
        print(f"   Routes found: {len(result.get('routes', []))}")
        print(f"   Explanation: {result.get('explanation', 'N/A')}")
        
        if 'routes' in result and result['routes']:
            route = result['routes'][0]
            print(f"   Best route: {route.get('total_duration', 'N/A')} "
                  f"for {route.get('total_cost', 'N/A')}")

def demonstrate_validation():
    """Demonstrate input validation"""
    print("\n\n5. Input Validation Examples:")
    print("-" * 30)
    
    test_cases = [
        ("JFK", "LHR", "speed", "Valid"),
        ("JK", "LHR", "speed", "Invalid airport"),
        ("JFK", "LON", "speed", "Invalid airport"),
        ("JFK", "JFK", "speed", "Same airports"),
        ("JFK", "LHR", "invalid", "Invalid priority")
    ]
    
    for departure, destination, priority, description in test_cases:
        error = validate_input(departure, destination, priority)
        status = "✅ Valid" if error is None else f"❌ Invalid: {error}"
        print(f"{description}: {status}")

if __name__ == "__main__":
    demonstrate_usage()
    demonstrate_validation()