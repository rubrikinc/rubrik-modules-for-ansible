"""
A Simple Example.
Add this to the same directory as pyRubrik.py to test.
"""
import pyRubrik as RubrikClient

rbkClient = RubrikClient.create("10.0.1.224", "admin", "rubrik123")

print rbkClient.is_encrypted()