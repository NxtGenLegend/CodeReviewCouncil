import os
import sys
import subprocess
import platform

def setup_api_key():
    print("Code Review Council Setup - Claude Haiku 3.5 Edition")
    print("=" * 55)
    print("This project uses Claude Haiku 3.5 for fast, intelligent code reviews")
    print("=" * 55)
    
    print("\nYou'll need an Anthropic API key to use this tool.")
    print("Get one at: https://console.anthropic.com/api-keys")
    print("")
    
    api_key = input("Enter your Anthropic API key: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty")
        return False
    
    print("\nChoose how to save the API key:")
    print("1. Environment variable (recommended)")
    print("2. .env file")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        system = platform.system()
        
        if system == "Windows":
            subprocess.run(["setx", "ANTHROPIC_API_KEY", api_key], check=True)
            print("\nAPI key saved! Restart your terminal for changes to take effect.")
        else:
            shell = os.environ.get("SHELL", "/bin/bash")
            shell_config = os.path.expanduser("~/.bashrc")
            
            if "zsh" in shell:
                shell_config = os.path.expanduser("~/.zshrc")
            
            with open(shell_config, "a") as f:
                f.write(f'\nexport ANTHROPIC_API_KEY="{api_key}"\n')
            
            print(f"\nAPI key saved to {shell_config}")
            print("Run: source " + shell_config + " to load it in current session")
    
    elif choice == "2":
        with open(".env", "w") as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        
        print("\nAPI key saved to .env file")
        print("Note: You'll need to install python-dotenv: pip install python-dotenv")
        print("And add these lines to the top of main.py:")
        print("  from dotenv import load_dotenv")
        print("  load_dotenv()")
    
    else:
        print("Invalid choice")
        return False
    
    return True

def test_setup():
    print("\nTesting setup...")
    
    try:
        import anthropic
        print("✓ Anthropic package installed")
    except ImportError:
        print("✗ Anthropic package not found. Run: pip install anthropic")
        return False
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✓ API key found in environment")
    elif os.path.exists(".env"):
        print("✓ .env file found")
    else:
        print("✗ No API key configuration found")
        return False
    
    print("\nSetup complete! You can now run: python main.py")
    print("\nThis project uses Claude Haiku 3.5 for fast, accurate code reviews")
    print("through 5 specialized agents working together.")
    return True

if __name__ == "__main__":
    if setup_api_key():
        test_setup()