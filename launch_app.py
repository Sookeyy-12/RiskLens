#!/usr/bin/env python3
"""
Launch script for the RiskLens Streamlit application.
"""

import os
import sys
import subprocess

def main():
    """Launch the Streamlit app."""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app", "main.py")
    
    # Check if the main.py file exists
    if not os.path.exists(app_path):
        print(f"Error: Could not find {app_path}")
        sys.exit(1)
    
    # Check if we're in a poetry environment
    try:
        result = subprocess.run(["poetry", "--version"], capture_output=True, text=True)
        use_poetry = result.returncode == 0
    except FileNotFoundError:
        use_poetry = False
    
    # Launch Streamlit
    try:
        print("🔥 Starting RiskLens Volatility Analysis Dashboard...")
        print(f"📁 App location: {app_path}")
        print("🌐 Opening in your default browser...")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        if use_poetry:
            print("🎯 Using poetry virtual environment")
            subprocess.run([
                "streamlit", "run", app_path,
                "--theme.base", "dark",
                "--theme.primaryColor", "#ff6b6b",
                "--theme.backgroundColor", "#0e1117",
                "--theme.secondaryBackgroundColor", "#262730",
                "--theme.textColor", "#fafafa"
            ])
        else:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", app_path,
                "--theme.base", "dark",
                "--theme.primaryColor", "#ff6b6b",
                "--theme.backgroundColor", "#0e1117",
                "--theme.secondaryBackgroundColor", "#262730",
                "--theme.textColor", "#fafafa"
            ])
        
    except KeyboardInterrupt:
        print("\n\n👋 RiskLens application stopped.")
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
