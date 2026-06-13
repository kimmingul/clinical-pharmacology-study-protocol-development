"""Pytest configuration: make the sample_size package importable.

The calculation scripts live in ``.claude/scripts/sample_size/`` and import
their shared helpers as ``from utils.power_analysis import ...`` (each module
also inserts its own directory onto ``sys.path``).  We add the sample_size
directory here so the tests can ``import crossover_2x2_be`` directly.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SAMPLE_SIZE = os.path.join(os.path.dirname(_HERE), "sample_size")
if _SAMPLE_SIZE not in sys.path:
    sys.path.insert(0, _SAMPLE_SIZE)
