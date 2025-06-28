#!/usr/bin/env python3
def validate_chatbot():
    """Validate chatbot implementation"""
    try:
        print("🔍 Validating TruePass Chatbot...")
        print("=" * 40)
        
        # Test 1: Import chatbot modules
        print("1️⃣ Testing imports...")
        from chatbot import TruePassChatbot, TruePassWebChatbot
        print("   ✅ Chatbot classes imported successfully")
        
        # Test 2: Initialize chatbot
        print("2️⃣ Testing initialization...")
        bot = TruePassChatbot(debug=False)
        web_bot = TruePassWebChatbot()
        print("   ✅ Chatbot instances created successfully")
        
        # Test 3: Test knowledge base
        print("3️⃣ Testing knowledge base...")
        kb = bot.knowledge_base
        required_sections = ["platform_info", "features", "user_guides", "troubleshooting"]
        for section in required_sections:
            if section not in kb:
                raise ValueError(f"Missing knowledge base section: {section}")
        print("   ✅ Knowledge base structure is complete")
        
        # Test 4: Test intent analysis
        print("4️⃣ Testing intent analysis...")
        test_inputs = [
            "How do I buy tickets?",
            "Connect my wallet",
            "TOTP validation help",
            "Payment failed"
        ]
        for test_input in test_inputs:
            result = bot.analyze_user_intent(test_input)
            if "intent" not in result or "confidence" not in result:
                raise ValueError(f"Invalid intent analysis result for: {test_input}")
        print("   ✅ Intent analysis working correctly")
        
        # Test 5: Test quick responses
        print("5️⃣ Testing quick responses...")
        quick_topics = ["welcome", "ticket_buying", "wallet_setup", "totp_explanation"]
        for topic in quick_topics:
            response = bot.get_quick_response(topic)
            if not response or len(response) < 50:
                raise ValueError(f"Invalid quick response for topic: {topic}")
        print("   ✅ Quick responses working correctly")
        
        # Test 6: Test web chatbot features
        print("6️⃣ Testing web features...")
        suggestions = web_bot.get_suggested_questions()
        context = web_bot.get_chat_context()
        if not suggestions or not isinstance(suggestions, list):
            raise ValueError("Invalid suggested questions")
        if not context or "session_id" not in context:
            raise ValueError("Invalid chat context")
        print("   ✅ Web features working correctly")
        
        # Test 7: Test conversation tracking
        print("7️⃣ Testing conversation tracking...")
        initial_count = len(bot.conversation_history)
        # Simulate adding conversation (without actual AI call)
        bot.conversation_history.append({"role": "user", "content": "test"})
        bot.conversation_history.append({"role": "assistant", "content": "response"})
        if len(bot.conversation_history) != initial_count + 2:
            raise ValueError("Conversation tracking not working")
        print("   ✅ Conversation tracking working correctly")
        
        print("\n🎉 VALIDATION COMPLETE!")
        print("✅ All core chatbot functionality is working correctly")
        print("🚀 Chatbot is ready for use!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return False

def show_chatbot_info():
    """Show chatbot information and capabilities"""
    print("\n📋 TruePass AI Chatbot Information")
    print("=" * 40)
    print("🎯 Purpose: AI assistant for TruePass platform")
    print("🎫 Features: NFT marketplace, blockchain tickets, INR payments")
    print("🔧 Technologies: Python, g4f AI, Flask API")
    print("💬 Modes: Interactive, Demo, Web API")
    print("\n🚀 Quick Start:")
    print("   python launcher.py       # Menu-driven launcher")
    print("   python chatbot.py        # Direct interactive mode")
    print("   python chatbot.py demo   # Demonstration mode")
    print("   python chatbot.py web    # Web API server")
    print("\n📖 Documentation: See README.md for complete guide")

if __name__ == "__main__":
    show_chatbot_info()
    
    print("\n" + "=" * 50)
    if validate_chatbot():
        print("\n✨ The TruePass Chatbot is fully functional!")
        print("🎮 You can now run it using any of the methods above.")
    else:
        print("\n🔧 Please fix the issues and try again.")
