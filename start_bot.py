#!/usr/bin/env python3
"""
Startup script for the talbot bot
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if required environment variables are set
required_vars = ['TELEGRAM_BOT_TOKEN', 'OMDB_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\nPlease edit the .env file with your actual API keys.")
    print("See README.md for instructions on how to get these keys.")
    sys.exit(1)

print("✅ All required environment variables are set!")
print("🚀 Starting the bot...")

# Change to src directory and run the bot
try:
    os.chdir('src')
    subprocess.run([sys.executable, 'bot.py'], check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Bot exited with error code: {e.returncode}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n🛑 Bot stopped by user")
except Exception as e:
    print(f"❌ Error starting bot: {e}")
    sys.exit(1)
