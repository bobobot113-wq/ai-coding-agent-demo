"""
Sample Python Code for AI Agent Demo
=====================================
This file contains intentional issues for the AI agent to find and analyze.
"""

import os
import sys
from typing import List, Dict

# Global variable - not ideal
result_cache = []

def process_data(data):
    """Process some data."""
    # TODO: Add error handling
    # TODO: Add type hints
    
    for item in data:
        # Using print instead of logging
        print(f"Processing: {item}")
        
        # Bare except - not recommended
        except:
            pass
        
        result_cache.append(item)
    
    return result_cache


class DataProcessor:
    """A data processor class."""
    
    def __init__(self, name):
        self.name = name
        self.data = []
    
    def add(self, item):
        self.data.append(item)
    
    def process(self):
        # Missing return type hint
        processed = []
        for item in self.data:
            if type(item) == str:
                processed.append(item.upper())
            else:
                processed.append(item)
        return processed


def calculate_stats(numbers):
    """Calculate statistics."""
    # No input validation
    total = 0
    for num in numbers:
        total = total + num
    
    avg = total / len(numbers)  # Could fail if empty
    
    return {
        'total': total,
        'average': avg,
        'count': len(numbers)
    }


def read_file_content(filepath):
    """Read and return file content."""
    # Bare except clause
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return None


# Main execution
if __name__ == "__main__":
    sample_data = ["hello", "world", 123, "test"]
    results = process_data(sample_data)
    print("Results:", results)
