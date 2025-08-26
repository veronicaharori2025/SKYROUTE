"""
MeTTa Integration Module
=======================
Provides interface between Python Flask application and MeTTa reasoning engine.
Handles MeTTa interpreter initialization, query execution, and result parsing.
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import MeTTa
try:
    from hyperon import MeTTa
    METTA_AVAILABLE = True
except ImportError:
    logger.warning("MeTTa/Hyperon not available. Using mock mode.")
    METTA_AVAILABLE = False

class MeTTaIntegration:
    """
    Handles integration with MeTTa reasoning engine for flight route optimization.
    
    Attributes:
        metta (MeTTa): MeTTa interpreter instance
        metta_file (str): Path to MeTTa knowledge base file
    """
    
    def __init__(self, metta_file_path: str = "flight_routes.metta"):
        """
        Initialize MeTTa integration.
        
        Args:
            metta_file_path: Path to the MeTTa knowledge base file
        """
        self.metta_file = metta_file_path
        self.metta = None
        
        if METTA_AVAILABLE:
            self._initialize_metta()
        else:
            logger.warning("Running in mock mode - MeTTa not available")
    
    def _initialize_metta(self):
        """Initialize the MeTTa interpreter and load knowledge base"""
        try:
            self.metta = MeTTa()
            if os.path.exists(self.metta_file):
                self.metta.import_file(self.metta_file)
                logger.info(f"Loaded MeTTa knowledge base from {self.metta_file}")
            else:
                logger.warning(f"MeTTa file {self.metta_file} not found")
        except Exception as e:
            logger.error(f"Failed to initialize MeTTa: {str(e)}")
            self.metta = None
    
    def find_optimal_route(self, departure: str, destination: str, 
                          priority: str = "speed") -> Dict[str, Any]:
        """
        Find optimal flight route using MeTTa reasoning.
        
        Args:
            departure: Departure airport code (e.g., "JFK")
            destination: Destination airport code (e.g., "LHR")
            priority: Optimization priority ("speed", "cost", or "comfort")
            
        Returns:
            Dictionary containing optimal route information or error message
        """
        if not METTA_AVAILABLE or not self.metta:
            return self._mock_find_optimal_route(departure, destination, priority)
        
        try:
            # Construct MeTTa query
            query = f'(find-optimal-route "{departure}" "{destination}" "{priority}")'
            logger.info(f"Executing MeTTa query: {query}")
            
            # Execute query
            results = self.metta.run(query)
            
            # Parse results
            return self._parse_metta_results(results, departure, destination, priority)
            
        except Exception as e:
            logger.error(f"Error executing MeTTa query: {str(e)}")
            return {'error': f'MeTTa execution error: {str(e)}'}
    
    def _parse_metta_results(self, results: List, departure: str, 
                           destination: str, priority: str) -> Dict[str, Any]:
        """
        Parse MeTTa query results into structured response.
        
        Args:
            results: Raw results from MeTTa query execution
            departure: Original departure airport code
            destination: Original destination airport code
            priority: Optimization priority used
            
        Returns:
            Structured response dictionary
        """
        # Implementation for parsing MeTTa results
        # This is a placeholder - implement based on your MeTTa output format
        if not results:
            return {'error': 'No routes found'}
        
        return {
            'departure': departure,
            'destination': destination,
            'priority': priority,
            'routes': [],  # Populate with actual parsed routes
            'explanation': 'Route found using MeTTa logical reasoning',
            'timestamp': '2024-01-01T12:00:00Z'
        }
    
    def _mock_find_optimal_route(self, departure: str, destination: str,
                               priority: str) -> Dict[str, Any]:
        """
        Provide mock response when MeTTa is not available (for development).
        
        Args:
            departure: Departure airport code
            destination: Destination airport code
            priority: Optimization priority
            
        Returns:
            Mock response for testing
        """
        logger.info("Using mock response (MeTTa not available)")
        
        return {
            'departure': departure,
            'destination': destination,
            'priority': priority,
            'routes': [
                {
                    'total_duration': '8h 30m',
                    'total_cost': '$650',
                    'layovers': 1,
                    'flights': [
                        {'from': departure, 'to': 'AMS', 'duration': '6h', 'cost': '$500'},
                        {'from': 'AMS', 'to': destination, 'duration': '2h 30m', 'cost': '$150'}
                    ]
                }
            ],
            'explanation': 'Mock response - fastest route with reasonable layover',
            'timestamp': '2024-01-01T12:00:00Z'
        }

# Global instance
_metta_integration = MeTTaIntegration()

def find_optimal_route(departure: str, destination: str, 
                      priority: str = "speed") -> Dict[str, Any]:
    """
    Find optimal flight route (public interface).
    
    Args:
        departure: Departure airport code
        destination: Destination airport code
        priority: Optimization priority
        
    Returns:
        Route information or error message
    """
    return _metta_integration.find_optimal_route(departure, destination, priority)

def validate_input(departure: str, destination: str, priority: str) -> Optional[str]:
    """
    Validate user input parameters.
    
    Args:
        departure: Departure airport code to validate
        destination: Destination airport code to validate
        priority: Optimization priority to validate
        
    Returns:
        Error message if validation fails, None if valid
    """
    if not departure or len(departure) != 3:
        return "Departure must be a 3-letter airport code"
    
    if not destination or len(destination) != 3:
        return "Destination must be a 3-letter airport code"
    
    if departure == destination:
        return "Departure and destination cannot be the same"
    
    valid_priorities = ['speed', 'cost', 'comfort']
    if priority not in valid_priorities:
        return f"Priority must be one of: {', '.join(valid_priorities)}"
    
    return None