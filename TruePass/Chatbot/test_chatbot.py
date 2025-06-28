#!/usr/bin/env python3
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import TruePassChatbot, TruePassWebChatbot


class TestTruePassChatbot(unittest.TestCase):
    """Test cases for TruePass chatbot functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = TruePassChatbot(debug=False)
        self.web_chatbot = TruePassWebChatbot()
    
    def test_chatbot_initialization(self):
        """Test chatbot initializes correctly"""
        self.assertIsNotNone(self.chatbot.knowledge_base)
        self.assertIsNotNone(self.chatbot.system_prompt)
        self.assertEqual(len(self.chatbot.conversation_history), 0)
    
    def test_intent_analysis(self):
        """Test intent analysis functionality"""
        # Test ticket purchase intent
        result = self.chatbot.analyze_user_intent("How do I buy tickets with UPI?")
        self.assertEqual(result["intent"], "ticket_purchase")
        self.assertGreater(result["confidence"], 0)
        
        # Test wallet connection intent
        result = self.chatbot.analyze_user_intent("Help me connect my MetaMask wallet")
        self.assertEqual(result["intent"], "wallet_connection")
        
        # Test TOTP/validation intent
        result = self.chatbot.analyze_user_intent("How does TOTP validation work?")
        self.assertEqual(result["intent"], "ticket_validation")
    
    def test_entity_extraction(self):
        """Test entity extraction from user input"""
        # Test price extraction
        entities = self.chatbot._extract_entities("I want to buy a ticket for ₹500", ["price"])
        self.assertEqual(entities.get("price"), "500")
        
        # Test payment method extraction
        entities = self.chatbot._extract_entities("Can I pay with UPI?", ["payment_method"])
        self.assertEqual(entities.get("payment_method"), "upi")
        
        # Test TOTP code extraction
        entities = self.chatbot._extract_entities("My code is 123456", ["totp_code"])
        self.assertEqual(entities.get("totp_code"), "123456")
    
    def test_quick_responses(self):
        """Test quick response functionality"""
        # Test welcome response
        response = self.chatbot.get_quick_response("welcome")
        self.assertIn("Welcome to TruePass", response)
        
        # Test ticket buying response
        response = self.chatbot.get_quick_response("ticket_buying")
        self.assertIn("Buying Tickets with INR", response)
        
        # Test wallet setup response
        response = self.chatbot.get_quick_response("wallet_setup")
        self.assertIn("MetaMask Wallet Setup", response)
    
    def test_conversation_tracking(self):
        """Test conversation history tracking"""
        initial_count = len(self.chatbot.conversation_history)
        
        # Mock g4f response to avoid actual API calls
        with patch('g4f.ChatCompletion.create') as mock_create:
            mock_create.return_value = "Mocked AI response"
            
            response = self.chatbot.get_contextual_response("Test question")
            
            # Check that conversation history was updated
            self.assertEqual(len(self.chatbot.conversation_history), initial_count + 2)
            self.assertEqual(self.chatbot.conversation_history[-2]["role"], "user")
            self.assertEqual(self.chatbot.conversation_history[-1]["role"], "assistant")
    
    def test_web_chatbot_features(self):
        """Test web chatbot specific features"""
        # Test suggested questions
        suggestions = self.web_chatbot.get_suggested_questions()
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        
        # Test chat context
        context = self.web_chatbot.get_chat_context()
        self.assertIn("session_id", context)
        self.assertIn("platform_name", context)
        self.assertEqual(context["platform_name"], "TruePass")
        
        # Test feedback system
        feedback = self.web_chatbot.add_user_feedback("msg_123", 5, "Great response!")
        self.assertEqual(feedback["rating"], 5)
        self.assertEqual(feedback["comment"], "Great response!")
    
    def test_session_data_export(self):
        """Test session data export functionality"""
        export_data = self.web_chatbot.export_session_data()
        
        required_keys = ["session_info", "conversation_data", "feedback_data", "analytics"]
        for key in required_keys:
            self.assertIn(key, export_data)
        
        self.assertEqual(export_data["session_info"]["platform"], "TruePass")


def run_manual_tests():
    """Run manual tests to demonstrate chatbot functionality"""
    print("🧪 TruePass Chatbot - Manual Testing")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = TruePassChatbot(debug=False)
    
    # Test queries
    test_queries = [
        ("Welcome greeting", "Hello! I'm new to TruePass"),
        ("Ticket purchase", "How do I buy tickets with UPI?"),
        ("Wallet connection", "I need help connecting MetaMask"),
        ("TOTP explanation", "What is TOTP validation?"),
        ("Payment methods", "What payment methods do you support?"),
        ("Technical issue", "My payment failed, help!"),
        ("General info", "Tell me about TruePass features")
    ]
    
    print("\n🎯 Testing Query Processing:")
    for test_name, query in test_queries:
        print(f"\n📝 Test: {test_name}")
        print(f"❓ Query: {query}")
        
        # Test intent analysis
        intent_result = chatbot.analyze_user_intent(query)
        print(f"🎯 Intent: {intent_result['intent']} (confidence: {intent_result['confidence']:.2f})")
        
        # Test quick response (if applicable)
        if any(keyword in query.lower() for keyword in ["hello", "hi", "new"]):
            response = chatbot.get_quick_response("welcome")
            print(f"⚡ Quick Response: {response[:100]}...")
        
        print("-" * 50)
    
    print("\n✅ Manual tests completed successfully!")


def run_integration_test():
    """Run integration test with actual chatbot conversation"""
    print("\n🔗 Integration Test - Real Conversation Flow")
    print("=" * 50)
    
    chatbot = TruePassWebChatbot()
    
    # Simulate a complete user journey
    conversation_flow = [
        "Hi, I'm new to blockchain. Can you help me?",
        "How do I buy tickets with Indian payment methods?",
        "I have MetaMask installed, what's next?",
        "What happens after I pay with UPI?",
        "How secure is the TOTP validation?",
        "Thanks for your help!"
    ]
    
    for i, message in enumerate(conversation_flow, 1):
        print(f"\n👤 User Message {i}: {message}")
        
        # Process with chatbot (mock the AI response to avoid API calls)
        with patch('g4f.ChatCompletion.create') as mock_create:
            mock_create.return_value = f"This is a helpful response to: {message}"
            
            response = chatbot.chat(message)
            print(f"🤖 Bot Response: {response[:150]}...")
    
    # Show session summary
    print("\n📊 Session Summary:")
    summary = chatbot.get_conversation_summary()
    print(f"⏱️  Duration: {summary['session_duration']}")
    print(f"💬 Messages: {summary['messages_exchanged']}")
    print(f"🎯 Session ID: {chatbot.session_id}")
    
    print("\n✅ Integration test completed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test TruePass AI Chatbot")
    parser.add_argument("--mode", choices=["unit", "manual", "integration", "all"], 
                       default="all", help="Test mode to run")
    
    args = parser.parse_args()
    
    if args.mode in ["unit", "all"]:
        print("🔬 Running Unit Tests...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    if args.mode in ["manual", "all"]:
        run_manual_tests()
    
    if args.mode in ["integration", "all"]:
        run_integration_test()
    
    print("\n🎉 All tests completed!")
