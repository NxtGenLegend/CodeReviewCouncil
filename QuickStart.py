import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return success status"""
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Code Review Council - Quick Start")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7+ required")
        print(f"You have: Python {sys.version}")
        sys.exit(1)
    
    print("✓ Python version OK")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not run_command(f"{sys.executable} -m pip install anthropic"):
        print("Error installing dependencies")
        print("Try running manually: pip install anthropic")
        sys.exit(1)
    
    print("✓ Dependencies installed")
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY") and not os.path.exists(".env"):
        print("\nNo API key found. Running setup...")
        run_command(f"{sys.executable} setup.py")
    
    # Show options
    print("\n" + "=" * 40)
    print("Setup complete! What would you like to do?")
    print("\n1. Run demo (no API key needed)")
    print("2. Review example.py")
    print("3. Review your own file")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\nRunning demo...")
        run_command(f"{sys.executable} DemoMode.py")
    elif choice == "2":
        print("\nReviewing example.py...")
        subprocess.run([sys.executable, "main.py"], input="example.py\ny\n", text=True)
    elif choice == "3":
        print("\nStarting code review...")
        run_command(f"{sys.executable} main.py")
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()