#!/usr/bin/env python
"""
Test runner script for the CISA Advisor project.
This script discovers and runs all tests in the test directory.
"""

import unittest
import os
import sys
import traceback

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_tests():
    """Discover and run all tests in the test directory"""
    # Get the directory containing this script
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Print the Python path for debugging
    print(f"Python path: {sys.path}")
    print(f"Project root: {project_root}")
    print(f"Test directory: {test_dir}")
    
    try:
        # Discover and run all tests
        loader = unittest.TestLoader()
        suite = loader.discover(test_dir, pattern='test_*.py')
        
        # Run the tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Return 0 if all tests passed, 1 if any failed
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error running tests: {e}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(run_tests()) 