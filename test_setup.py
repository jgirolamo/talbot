#!/usr/bin/env python3
"""
Test script to verify the talbot bot setup
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print("Environment variables loaded:")
print(f"TELEGRAM_BOT_TOKEN: {'✓ Set' if os.getenv('TELEGRAM_BOT_TOKEN') else '✗ Not set'}")
print(f"OMDB_API_KEY: {'✓ Set' if os.getenv('OMDB_API_KEY') else '✗ Not set'}")
print(f"ANTHROPIC_API_KEY: {'✓ Set' if os.getenv('ANTHROPIC_API_KEY') else '✗ Not set'}")

print("\nNote: You need to edit the .env file with your actual API keys before running the bot.")
