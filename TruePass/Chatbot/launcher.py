#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {platform.python_version()}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'g4f', 'flask', 'requests', 'dateutil'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n🔧 Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def show_menu():
    """Display startup menu"""
    print("🚀 TruePass AI Chatbot Launcher")
    print("=" * 40)
    print("1. 💬 Interactive Chat")
    print("2. 📋 Demo Mode")
    print("3. 🌐 Web API Server")
    print("4. 🧪 Run Tests")
    print("5. 📦 Install Dependencies")
    print("6. ❓ Help & Documentation")
    print("7. 🚪 Exit")
    print("=" * 40)

def run_interactive():
    """Run interactive chat mode"""
    print("🎯 Starting Interactive Chat...")
    from chatbot import interactive_chat
    interactive_chat()

def run_demo():
    """Run demo mode"""
    print("📺 Starting Demo Mode...")
    from chatbot import run_chatbot_demo
    run_chatbot_demo()

def run_web_server():
    """Run web API server"""
    print("🌐 Starting Web API Server...")
    from chatbot import create_web_api_wrapper
    
    app = create_web_api_wrapper()
    if app:
        print("🚀 Server starting on http://localhost:5000")
        print("📖 API Documentation available in README.md")
        print("🛑 Press Ctrl+C to stop the server")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to start web server. Check dependencies.")

def run_tests():
    """Run test suite"""
    print("🧪 Running Tests...")
    try:
        subprocess.check_call([sys.executable, "test_chatbot.py"])
    except subprocess.CalledProcessError:
        print("❌ Tests failed!")
    except FileNotFoundError:
        print("❌ Test file not found!")

def show_help():
    """Show help information"""
    print("📚 TruePass AI Chatbot Help")
    print("=" * 40)
    print("🎯 Purpose:")
    print("   AI assistant for TruePass platform")
    print("   Helps with NFTs, tickets, and payments")
    print("")
    print("🔧 Requirements:")
    print("   • Python 3.8+")
    print("   • Internet connection")
    print("   • Dependencies from requirements.txt")
    print("")
    print("📖 Documentation:")
    print("   • README.md - Complete documentation")
    print("   • test_chatbot.py - Test examples")
    print("   • chatbot.py - Main implementation")
    print("")
    print("🌐 Web Integration:")
    print("   Start web server and use API endpoints")
    print("   POST /api/chat for conversations")
    print("   GET /api/suggestions for question ideas")
    print("")
    print("❓ Need more help?")
    print("   Check README.md for detailed instructions")

def main():
    """Main launcher function"""
    # Check Python version
    if not check_python_version():
        return
    
    print("🎉 Welcome to TruePass AI Chatbot!")
    print("   Your intelligent assistant for NFTs and blockchain tickets")
    print("")
    
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Select an option (1-7): ").strip()
            
            if choice == '1':
                if check_dependencies():
                    run_interactive()
                else:
                    print("⚠️  Please install dependencies first (option 5)")
                    
            elif choice == '2':
                if check_dependencies():
                    run_demo()
                else:
                    print("⚠️  Please install dependencies first (option 5)")
                    
            elif choice == '3':
                if check_dependencies():
                    run_web_server()
                else:
                    print("⚠️  Please install dependencies first (option 5)")
                    
            elif choice == '4':
                run_tests()
                
            elif choice == '5':
                install_dependencies()
                
            elif choice == '6':
                show_help()
                
            elif choice == '7':
                print("👋 Thanks for using TruePass AI Chatbot!")
                print("   Happy trading and secure ticket validation! 🎫")
                break
                
            else:
                print("❌ Invalid option. Please choose 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("   Please try again or check your installation.")

if __name__ == "__main__":
    main()
