#!/usr/bin/env python3
"""
PhishGuard Africa - Main Entry Point
"""

import sys
import os

# Add the phishguard package to the path
sys.path.insert(0, os.path.join(os.path.dirname(_file_), 'phishguard'))

from phishguard.cli import main

if _name_ == '_main_':
    main()