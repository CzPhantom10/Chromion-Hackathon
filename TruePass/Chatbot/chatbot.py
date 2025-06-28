#!/usr/bin/env python3
"""
TruePass AI Chatbot
A comprehensive AI assistant for TruePass NFT Marketplace & Blockchain Ticket Validation Platform
Built with g4f library for intelligent conversation handling
"""

import g4f
import json
import re
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class TruePassChatbot:
    """
    Main chatbot class for TruePass platform
    Handles user queries about NFT marketplace, blockchain tickets, and INR payments
    """
    
    def __init__(self, debug: bool = True):
        """Initialize the TruePass chatbot with configuration and knowledge base"""
        
        # Configure g4f
        g4f.debug.logging = debug
        g4f.check_version = False
        
        # Initialize conversation tracking
        self.conversation_history: List[Dict[str, str]] = []
        self.session_start = datetime.now()
        self.user_context = {
            "current_page": None,
            "user_type": "new",  # new, returning, technical
            "last_topic": None
        }
        
        # TruePass comprehensive knowledge base
        self.knowledge_base = {
            "platform_info": {
                "name": "TruePass",
                "tagline": "NFT Marketplace & Blockchain Ticket Validation with INR Payments",
                "description": "A decentralized marketplace for NFTs with integrated blockchain-based ticket validation system",
                "key_benefits": [
                    "Buy NFTs and tickets with Indian Rupees",
                    "Secure blockchain validation using TOTP",
                    "Non-transferable tickets to prevent resale",
                    "Gasless minting with ECDSA signatures",
                    "Offline validation capability"
                ]
            },
            
            "features": {
                "nft_marketplace": {
                    "description": "Complete NFT trading platform with INR support",
                    "capabilities": [
                        "Browse and search NFT collections",
                        "Buy, sell, and trade NFTs with Indian Rupee payments",
                        "Connect Ethereum wallets (MetaMask, WalletConnect)",
                        "View detailed transaction history",
                        "Manage user profiles and collections",
                        "Automatic INR to ETH conversion"
                    ],
                    "supported_wallets": ["MetaMask", "WalletConnect", "Coinbase Wallet"],
                    "blockchains": ["Ethereum", "Polygon (planned)"]
                },
                
                "blockchain_tickets": {
                    "description": "TOTP-based secure ticket validation system",
                    "security_features": [
                        "Time-based One-Time Passwords (TOTP)",
                        "30-second code rotation",
                        "QR code generation for authenticator apps",
                        "Blockchain-based validation recording",
                        "Offline validation support",
                        "Non-transferable NFT tickets"
                    ],
                    "supported_apps": ["Google Authenticator", "Authy", "Microsoft Authenticator"],
                    "validation_process": "Generate → Authenticate → Validate → Record"
                },
                
                "inr_payments": {
                    "description": "Seamless Indian payment integration",
                    "supported_methods": [
                        "UPI (PhonePe, Google Pay, Paytm)",
                        "Credit/Debit Cards",
                        "Net Banking",
                        "Paytm Wallet"
                    ],
                    "payment_flow": "INR Payment → Transak Conversion → ETH → NFT Minting",
                    "security": "PCI DSS compliant, encrypted transactions"
                }
            },
            
            "user_guides": {
                "first_time_setup": [
                    "Install MetaMask browser extension",
                    "Create or import Ethereum wallet",
                    "Visit TruePass website",
                    "Click 'Connect Wallet' button",
                    "Approve wallet connection",
                    "Complete profile setup"
                ],
                
                "buying_tickets_inr": [
                    "Browse available tickets (prices in ₹)",
                    "Ensure wallet is connected",
                    "Select desired ticket and click 'Buy Now'",
                    "Choose payment method (UPI/Card/Net Banking)",
                    "Complete payment in Indian Rupees",
                    "Wait for automatic NFT minting",
                    "Check wallet for your NFT ticket"
                ],
                
                "ticket_generation": [
                    "Navigate to 'Blockchain Tickets' page",
                    "Click 'Generate Tickets' tab",
                    "Enter ticket details (ID, event name, expiry)",
                    "Click 'Generate QR Code'",
                    "Scan QR code with authenticator app",
                    "Save the secret key securely",
                    "Fill blockchain details (recipient, seat, date)",
                    "Click 'Mint Ticket NFT' to create on blockchain"
                ],
                
                "ticket_validation": [
                    "Go to 'Blockchain Tickets' → 'Validate Tickets'",
                    "Select ticket from dropdown or enter Token ID",
                    "Ask ticket holder for current 6-digit TOTP code",
                    "Enter the code in validation field",
                    "Click 'Validate Code' button",
                    "See validation result (Valid/Invalid)",
                    "Optionally click 'Validate on Blockchain' to record"
                ]
            },
            
            "troubleshooting": {
                "wallet_issues": {
                    "connection_failed": [
                        "Ensure MetaMask is installed and unlocked",
                        "Refresh the page and try again",
                        "Check if MetaMask is on correct network (Ethereum)",
                        "Clear browser cache and cookies",
                        "Disable other wallet extensions temporarily",
                        "Try using incognito/private browsing mode"
                    ],
                    "transaction_failed": [
                        "Check if you have sufficient ETH for gas fees",
                        "Ensure network is not congested",
                        "Try increasing gas price in MetaMask",
                        "Wait and retry after a few minutes",
                        "Check Ethereum network status"
                    ]
                },
                
                "payment_issues": {
                    "inr_payment_failed": [
                        "Verify payment method has sufficient balance",
                        "Check internet connection stability",
                        "Ensure payment app/bank is not under maintenance",
                        "Try alternative payment method",
                        "Clear browser cache and retry",
                        "Contact bank if payment is declined"
                    ],
                    "conversion_issues": [
                        "Wait for Transak processing (can take 5-10 minutes)",
                        "Check if conversion limits are exceeded",
                        "Verify KYC status if required",
                        "Contact Transak support for conversion issues"
                    ]
                },
                
                "ticket_problems": {
                    "totp_invalid": [
                        "Ensure device time is synchronized",
                        "Check if ticket hasn't expired",
                        "Generate fresh code from authenticator",
                        "Verify correct secret was scanned",
                        "Try manual entry of secret key"
                    ],
                    "validation_failed": [
                        "Confirm correct Token ID is entered",
                        "Check blockchain connection",
                        "Verify ticket ownership",
                        "Ensure ticket hasn't been used already"
                    ]
                }
            },
            
            "technical_requirements": {
                "browser_support": ["Chrome 90+", "Firefox 88+", "Safari 14+", "Edge 90+"],
                "mobile_support": ["iOS 14+", "Android 8+"],
                "required_extensions": ["MetaMask", "WalletConnect compatible wallet"],
                "network_requirements": "Stable internet connection for blockchain interactions"
            }
        }
        
        # AI system prompt for TruePass context
        self.system_prompt = """You are the official AI assistant for TruePass, an innovative NFT marketplace and blockchain ticket validation platform. You are knowledgeable, helpful, and friendly.

PLATFORM OVERVIEW:
TruePass combines NFT marketplace functionality with blockchain-based ticket validation using TOTP (Time-based One-Time Passwords). Users can buy NFTs and tickets using Indian Rupees through UPI, Paytm, credit cards, etc.

YOUR EXPERTISE:
- NFT Marketplace: Help users buy, sell, trade NFTs with INR payments
- Blockchain Tickets: Guide through TOTP-based ticket generation and validation  
- Payment Processing: Assist with INR payments, wallet connections, conversions
- Technical Support: Troubleshoot wallet, payment, and validation issues
- User Onboarding: Help new users get started with crypto and blockchain

COMMUNICATION STYLE:
- Be warm, patient, and encouraging
- Use simple language for complex blockchain concepts
- Provide step-by-step instructions with clear numbering
- Include relevant emojis to make responses engaging
- Ask clarifying questions when user needs are unclear
- Always prioritize user security and best practices

RESPONSE FORMAT:
- Start with a brief, direct answer
- Provide detailed steps when needed
- Include relevant tips or warnings
- Suggest next steps or related help
- Use Indian context (₹, UPI, etc.) when relevant

Remember: You're helping users navigate both traditional payments and cutting-edge blockchain technology. Make it accessible and exciting!"""

    def analyze_user_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input to determine intent and extract relevant information
        Returns intent category, confidence level, and extracted entities
        """
        user_input_lower = user_input.lower()
        
        # Intent patterns with keywords and confidence scoring
        intent_patterns = {
            "ticket_purchase": {
                "keywords": ["buy ticket", "purchase ticket", "ticket price", "book ticket", "inr", "rupee", "pay"],
                "confidence_boost": ["upi", "paytm", "credit card", "payment"],
                "entities": ["price", "payment_method", "ticket_type"]
            },
            "ticket_generation": {
                "keywords": ["generate ticket", "create ticket", "mint ticket", "new ticket", "totp", "qr code"],
                "confidence_boost": ["authenticator", "google authenticator", "secret key"],
                "entities": ["event_name", "expiry_time", "ticket_id"]
            },
            "ticket_validation": {
                "keywords": ["validate ticket", "verify ticket", "check ticket", "authentication", "totp code"],
                "confidence_boost": ["6 digit", "authenticator code", "validation failed"],
                "entities": ["token_id", "totp_code", "validation_status"]
            },
            "wallet_connection": {
                "keywords": ["wallet", "metamask", "connect wallet", "wallet connection", "ethereum"],
                "confidence_boost": ["can't connect", "connection failed", "wallet error"],
                "entities": ["wallet_type", "error_message", "network"]
            },
            "nft_marketplace": {
                "keywords": ["nft", "marketplace", "collection", "buy nft", "sell nft", "trade"],
                "confidence_boost": ["opensea", "digital art", "collectible"],
                "entities": ["nft_type", "collection_name", "price_range"]
            },
            "payment_issues": {
                "keywords": ["payment failed", "transaction error", "payment not working", "can't pay"],
                "confidence_boost": ["upi failed", "card declined", "payment timeout"],
                "entities": ["payment_method", "error_code", "amount"]
            },
            "technical_support": {
                "keywords": ["error", "not working", "problem", "issue", "help", "stuck"],
                "confidence_boost": ["browser", "mobile", "slow", "crashed"],
                "entities": ["error_type", "device_type", "browser"]
            },
            "general_info": {
                "keywords": ["what is", "how does", "explain", "about", "overview", "features"],
                "confidence_boost": ["truepass", "blockchain", "crypto"],
                "entities": ["topic", "feature_name"]
            }
        }
        
        # Calculate intent scores
        intent_scores = {}
        detected_entities = {}
        
        for intent, pattern in intent_patterns.items():
            score = 0
            
            # Base keyword matching
            keyword_matches = sum(1 for keyword in pattern["keywords"] if keyword in user_input_lower)
            score += keyword_matches * 2
            
            # Confidence boost keywords
            boost_matches = sum(1 for boost in pattern["confidence_boost"] if boost in user_input_lower)
            score += boost_matches * 3
            
            # Length normalization
            score = score / max(len(user_input_lower.split()), 1)
            
            intent_scores[intent] = score
        
        # Determine primary intent
        primary_intent = max(intent_scores, key=intent_scores.get) if intent_scores else "general_info"
        confidence = intent_scores.get(primary_intent, 0)
        
        # Extract entities based on intent
        if primary_intent in intent_patterns:
            # Simple entity extraction (can be enhanced with NLP)
            entities = self._extract_entities(user_input, intent_patterns[primary_intent]["entities"])
            detected_entities = entities
        
        return {
            "intent": primary_intent,
            "confidence": confidence,
            "entities": detected_entities,
            "all_scores": intent_scores
        }
    
    def _extract_entities(self, text: str, entity_types: List[str]) -> Dict[str, str]:
        """Extract specific entities from user input"""
        entities = {}
        text_lower = text.lower()
        
        # Price/amount extraction
        if "price" in entity_types:
            price_match = re.search(r'₹?(\d+(?:,\d+)*)', text)
            if price_match:
                entities["price"] = price_match.group(1)
        
        # Payment method extraction
        if "payment_method" in entity_types:
            payment_methods = ["upi", "paytm", "credit card", "debit card", "net banking"]
            for method in payment_methods:
                if method in text_lower:
                    entities["payment_method"] = method
                    break
        
        # Token ID extraction
        if "token_id" in entity_types:
            token_match = re.search(r'token\s*(?:id)?\s*:?\s*(\w+)', text_lower)
            if token_match:
                entities["token_id"] = token_match.group(1)
        
        # TOTP code extraction
        if "totp_code" in entity_types:
            totp_match = re.search(r'\b(\d{6})\b', text)
            if totp_match:
                entities["totp_code"] = totp_match.group(1)
        
        return entities
    
    def get_contextual_response(self, user_input: str, current_page: str = None) -> str:
        """
        Generate AI response with TruePass-specific context and knowledge
        """
        try:
            # Update user context
            if current_page:
                self.user_context["current_page"] = current_page
            
            # Analyze user intent
            intent_analysis = self.analyze_user_intent(user_input)
            intent = intent_analysis["intent"]
            entities = intent_analysis["entities"]
            
            # Build context message with relevant TruePass information
            context_parts = []
            
            # Add page context
            if current_page:
                context_parts.append(f"User is currently on the {current_page} page of TruePass.")
            
            # Add intent-specific context
            context_parts.append(f"User intent detected: {intent}")
            
            if intent == "ticket_purchase":
                context_parts.append("TICKET PURCHASE CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["user_guides"]["buying_tickets_inr"], indent=2))
                context_parts.append(json.dumps(self.knowledge_base["features"]["inr_payments"], indent=2))
            
            elif intent == "ticket_generation":
                context_parts.append("TICKET GENERATION CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["user_guides"]["ticket_generation"], indent=2))
                context_parts.append(json.dumps(self.knowledge_base["features"]["blockchain_tickets"], indent=2))
            
            elif intent == "ticket_validation":
                context_parts.append("TICKET VALIDATION CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["user_guides"]["ticket_validation"], indent=2))
            
            elif intent == "wallet_connection":
                context_parts.append("WALLET CONNECTION CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["user_guides"]["first_time_setup"], indent=2))
                context_parts.append(json.dumps(self.knowledge_base["troubleshooting"]["wallet_issues"], indent=2))
            
            elif intent == "nft_marketplace":
                context_parts.append("NFT MARKETPLACE CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["features"]["nft_marketplace"], indent=2))
            
            elif intent == "payment_issues":
                context_parts.append("PAYMENT TROUBLESHOOTING CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["troubleshooting"]["payment_issues"], indent=2))
            
            elif intent == "technical_support":
                context_parts.append("TECHNICAL SUPPORT CONTEXT:")
                context_parts.append(json.dumps(self.knowledge_base["troubleshooting"], indent=2))
                context_parts.append(json.dumps(self.knowledge_base["technical_requirements"], indent=2))
            
            # Add extracted entities
            if entities:
                context_parts.append(f"Extracted entities: {json.dumps(entities, indent=2)}")
            
            # Combine context
            full_context = "\n".join(context_parts)
            
            # Prepare messages for AI
            messages = [
                {"role": "system", "content": f"{self.system_prompt}\n\nCURRENT CONTEXT:\n{full_context}"},
                *self.conversation_history[-8:],  # Include recent conversation context
                {"role": "user", "content": user_input}
            ]
            
            # Generate AI response
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=False,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Store conversation
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Update user context
            self.user_context["last_topic"] = intent
            
            return response
            
        except Exception as e:
            error_response = f"""I apologize, but I'm experiencing some technical difficulties right now. 🔧

**What you can try:**
• Refresh the page and ask your question again
• Check your internet connection
• Try asking a more specific question

**Need immediate help?**
• Check our Help Center for common solutions
• Contact TruePass support team
• Join our community Discord for real-time help

Error details: {str(e)}"""
            return error_response
    
    def get_quick_response(self, topic: str) -> str:
        """
        Provide instant responses for common TruePass topics
        """
        quick_responses = {
            "welcome": """🎉 **Welcome to TruePass!**

Your gateway to NFTs and blockchain tickets with Indian Rupee payments!

**🚀 Quick Start:**
• New here? I'll guide you through wallet setup
• Want to buy tickets? Ask about our INR payment options  
• Need to validate tickets? Learn about our TOTP system
• Exploring NFTs? Discover our marketplace features

**💡 Popular Questions:**
• "How do I buy tickets with UPI?"
• "What is blockchain ticket validation?"
• "How do I connect my MetaMask wallet?"

What would you like to explore first? 😊""",

            "ticket_buying": """🎫 **Buying Tickets with INR - Super Easy!**

**Step-by-Step Process:**
1️⃣ **Browse** available tickets (prices shown in ₹)
2️⃣ **Connect** your Ethereum wallet (one-time setup)
3️⃣ **Select** your desired ticket and click 'Buy Now'
4️⃣ **Choose** payment: UPI, Paytm, or Credit Card
5️⃣ **Pay** in Indian Rupees - no crypto needed!
6️⃣ **Receive** your NFT ticket automatically in wallet

**🎯 Key Benefits:**
• No need to buy crypto first
• All major Indian payment methods supported
• Instant ticket delivery to your wallet
• Secure blockchain ownership

**Need help with any step?** Just ask! 🙋‍♂️""",

            "wallet_setup": """🔗 **MetaMask Wallet Setup - Made Simple!**

**Installation & Setup:**
1️⃣ **Download** MetaMask browser extension
2️⃣ **Create** new wallet or import existing one
3️⃣ **Secure** your seed phrase (keep it safe!)
4️⃣ **Visit** TruePass and click 'Connect Wallet'
5️⃣ **Approve** connection in MetaMask popup
6️⃣ **Ready!** You can now buy NFTs and tickets

**🛡️ Security Tips:**
• Never share your seed phrase with anyone
• Use strong passwords
• Enable 2FA when possible
• Bookmark official TruePass URL

**🆘 Having connection issues?** I can help troubleshoot! 

**📱 Mobile Users:** MetaMask mobile app works great too!""",

            "totp_explanation": """⚡ **TOTP Ticket Validation - Advanced Security!**

**What is TOTP?**
Time-based One-Time Password - generates unique 6-digit codes every 30 seconds

**🔒 How It Works:**
1️⃣ **Generate** ticket with unique QR code
2️⃣ **Scan** QR with Google Authenticator app
3️⃣ **Mint** NFT ticket on blockchain
4️⃣ **Validate** using current 6-digit code from app
5️⃣ **Verify** authenticity instantly

**🎯 Why It's Amazing:**
• ✅ Prevents ticket fraud and counterfeiting
• ✅ Works offline (no internet needed for validation)
• ✅ Codes change every 30 seconds
• ✅ Non-transferable tickets stop scalping
• ✅ Blockchain-verified authenticity

**📱 Supported Apps:** Google Authenticator, Authy, Microsoft Authenticator

**Want to create your first TOTP ticket?** I'll guide you through it! 🚀""",

            "payment_methods": """💳 **TruePass Payment Methods - Choose What's Best for You!**

**🇮🇳 Supported Indian Payment Methods:**

**UPI Payments** 📱
• PhonePe, Google Pay, Paytm UPI
• Instant transfers
• Most popular choice

**Credit/Debit Cards** 💳
• Visa, MasterCard, RuPay
• Secure encrypted processing
• International cards accepted

**Net Banking** 🏦
• All major Indian banks
• Direct bank transfers
• Highly secure

**Digital Wallets** 📲
• Paytm Wallet
• Other supported wallets

**🔒 Security Features:**
• PCI DSS compliant processing
• 256-bit SSL encryption
• No card details stored
• Instant refund policy

**💰 Automatic Conversion:**
Your INR payment → Transak conversion → ETH → NFT minting
*All happens behind the scenes!*

**Any payment questions?** I'm here to help! 🤝""",

            "troubleshooting": """🔧 **TruePass Troubleshooting Guide**

**🔗 Wallet Connection Issues:**
• Unlock MetaMask and refresh page
• Clear browser cache and cookies
• Check you're on Ethereum network
• Disable other wallet extensions temporarily

**💳 Payment Problems:**
• Verify sufficient balance in payment method
• Check internet connection stability
• Try alternative payment method
• Wait 5-10 minutes for processing

**🎫 Ticket Validation Issues:**
• Sync device time (very important!)
• Generate fresh code from authenticator
• Check ticket hasn't expired
• Verify correct Token ID

**🌐 General Issues:**
• Use supported browsers (Chrome, Firefox, Safari)
• Update to latest browser version
• Disable ad blockers temporarily
• Try incognito/private mode

**💬 Still Need Help?**
• Contact our support team
• Join TruePass community Discord
• Check our detailed FAQ section

**I can provide specific help too - just describe your issue!** 🆘"""
        }
        
        return quick_responses.get(topic, "I don't have a quick response for that topic. Please ask me a specific question and I'll provide detailed help!")
    
    def chat(self, user_input: str, current_page: str = None) -> str:
        """
        Main chat interface - processes user input and returns appropriate response
        """
        if not user_input.strip():
            return "I'd love to help! Please ask me anything about TruePass - NFTs, tickets, payments, or technical support. 😊"
        
        # Check for quick response triggers
        user_input_lower = user_input.lower().strip()
        
        if any(greeting in user_input_lower for greeting in ["hello", "hi", "hey", "welcome"]):
            return self.get_quick_response("welcome")
        
        if any(keyword in user_input_lower for keyword in ["buy ticket", "purchase ticket", "ticket price"]):
            return self.get_quick_response("ticket_buying")
        
        if any(keyword in user_input_lower for keyword in ["wallet", "metamask", "connect wallet"]):
            return self.get_quick_response("wallet_setup")
        
        if any(keyword in user_input_lower for keyword in ["totp", "validation", "authenticate", "verification"]):
            return self.get_quick_response("totp_explanation")
        
        if any(keyword in user_input_lower for keyword in ["payment", "upi", "paytm", "credit card"]):
            return self.get_quick_response("payment_methods")
        
        if any(keyword in user_input_lower for keyword in ["error", "problem", "not working", "issue", "help"]):
            return self.get_quick_response("troubleshooting")
        
        # For complex queries, use AI-powered response
        return self.get_contextual_response(user_input, current_page)
    
    def start_conversation(self) -> str:
        """
        Initialize conversation with welcome message
        """
        welcome_msg = self.get_quick_response("welcome")
        print(welcome_msg)
        return welcome_msg
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get summary of current conversation session
        """
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "messages_exchanged": len(self.conversation_history),
            "topics_discussed": [msg.get("intent", "unknown") for msg in self.conversation_history if "intent" in msg],
            "user_context": self.user_context,
            "last_interaction": self.conversation_history[-1] if self.conversation_history else None
        }


class TruePassWebChatbot(TruePassChatbot):
    """
    Enhanced chatbot for web integration with additional features
    """
    
    def __init__(self, api_endpoint: str = None, session_id: str = None):
        super().__init__()
        self.api_endpoint = api_endpoint
        self.session_id = session_id or f"truepass_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.user_feedback = []
    
    def get_suggested_questions(self) -> List[str]:
        """
        Return contextual suggested questions for users
        """
        base_suggestions = [
            "How do I buy tickets with UPI?",
            "What is blockchain ticket validation?",
            "How do I connect my MetaMask wallet?",
            "Can I use Paytm to buy NFTs?",
            "How does TOTP authentication work?",
            "What do I need to get started?",
            "Is my payment information secure?",
            "How do I validate someone's ticket?"
        ]
        
        # Add contextual suggestions based on conversation history
        if self.user_context.get("last_topic") == "wallet_connection":
            base_suggestions.extend([
                "I'm having wallet connection issues",
                "MetaMask won't connect to TruePass",
                "Do I need ETH in my wallet to buy tickets?"
            ])
        elif self.user_context.get("last_topic") == "ticket_purchase":
            base_suggestions.extend([
                "My payment failed, what should I do?",
                "How long does ticket delivery take?",
                "Can I get a refund on my ticket?"
            ])
        
        return base_suggestions[:8]  # Return top 8 suggestions
    
    def get_chat_context(self) -> Dict[str, Any]:
        """
        Return comprehensive chat context for web frontend
        """
        return {
            "session_id": self.session_id,
            "platform_name": "TruePass",
            "current_page": self.user_context.get("current_page"),
            "conversation_length": len(self.conversation_history),
            "suggested_questions": self.get_suggested_questions(),
            "user_type": self.user_context.get("user_type", "new"),
            "last_topic": self.user_context.get("last_topic"),
            "available_features": list(self.knowledge_base["features"].keys()),
            "session_summary": self.get_conversation_summary()
        }
    
    def add_user_feedback(self, message_id: str, rating: int, comment: str = None):
        """
        Collect user feedback for improving responses
        """
        feedback = {
            "message_id": message_id,
            "rating": rating,  # 1-5 scale
            "comment": comment,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        self.user_feedback.append(feedback)
        return feedback
    
    def export_session_data(self) -> Dict[str, Any]:
        """
        Export complete session data for analysis or support
        """
        return {
            "session_info": {
                "session_id": self.session_id,
                "start_time": self.session_start.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration": str(datetime.now() - self.session_start),
                "platform": "TruePass"
            },
            "conversation_data": {
                "messages": self.conversation_history,
                "message_count": len(self.conversation_history),
                "user_context": self.user_context
            },
            "feedback_data": {
                "feedback_entries": self.user_feedback,
                "average_rating": sum(f["rating"] for f in self.user_feedback) / len(self.user_feedback) if self.user_feedback else None
            },
            "analytics": self.get_conversation_summary()
        }


# Example usage and demonstration
def run_chatbot_demo():
    """
    Demonstrate the TruePass chatbot functionality
    """
    print("=" * 60)
    print("🚀 TruePass AI Assistant - Interactive Demo")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = TruePassChatbot(debug=False)
    
    # Start conversation
    chatbot.start_conversation()
    
    # Demo conversations
    demo_queries = [
        "Hi, I'm new to TruePass. Can you help me get started?",
        "How do I buy tickets with UPI?",
        "I need help connecting my MetaMask wallet",
        "What is TOTP validation and how does it work?",
        "My payment failed, what should I do?",
        "Can I buy NFTs with Indian Rupees?"
    ]
    
    print("\n🎯 Running Demo Conversations...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"📝 Query {i}: {query}")
        print("🤖 Response:")
        response = chatbot.chat(query)
        print(response)
        print("\n" + "-" * 80 + "\n")
        
        # Simulate brief pause between queries
        time.sleep(1)
    
    # Show conversation summary
    print("📊 Session Summary:")
    summary = chatbot.get_conversation_summary()
    print(json.dumps(summary, indent=2, default=str))


def interactive_chat():
    """
    Run interactive chat session with TruePass chatbot
    """
    print("=" * 60)
    print("💬 TruePass AI Assistant - Interactive Chat")
    print("=" * 60)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'help' for suggested questions")
    print("=" * 60)
    
    # Initialize web chatbot for enhanced features
    chatbot = TruePassWebChatbot()
    
    # Welcome message
    chatbot.start_conversation()
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🙏 Thank you for using TruePass AI Assistant!")
                print("💫 Have a great day and happy trading!")
                
                # Show final session summary
                print("\n📊 Final Session Summary:")
                summary = chatbot.get_conversation_summary()
                print(f"⏱️  Session Duration: {summary['session_duration']}")
                print(f"💬 Messages Exchanged: {summary['messages_exchanged']}")
                print(f"📈 Topics Discussed: {len(set(summary.get('topics_discussed', [])))}")
                break
            
            # Show help/suggestions
            if user_input.lower() in ['help', 'suggestions', 'options']:
                print("\n💡 Suggested Questions:")
                suggestions = chatbot.get_suggested_questions()
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"   {i}. {suggestion}")
                continue
            
            # Empty input handling
            if not user_input:
                print("🤔 I didn't catch that. Please ask me something about TruePass!")
                continue
            
            # Get chatbot response
            print("\n🤖 TruePass Assistant:")
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Thanks for using TruePass AI Assistant!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("🔄 Please try asking your question again.")


def create_web_api_wrapper():
    """
    Create a simple web API wrapper for the chatbot (Flask-based)
    """
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)  # Enable cross-origin requests
        
        # Store active chatbot sessions
        active_sessions = {}
        
        @app.route('/api/chat', methods=['POST'])
        def chat_endpoint():
            """Main chat endpoint for web integration"""
            try:
                data = request.get_json()
                
                # Extract request data
                session_id = data.get('session_id', f"web_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                message = data.get('message', '').strip()
                current_page = data.get('current_page')
                
                # Get or create chatbot session
                if session_id not in active_sessions:
                    active_sessions[session_id] = TruePassWebChatbot(session_id=session_id)
                
                chatbot = active_sessions[session_id]
                
                # Process message
                if not message:
                    response = "Please provide a message to get help with TruePass! 😊"
                else:
                    response = chatbot.chat(message, current_page)
                
                # Prepare response
                return jsonify({
                    'success': True,
                    'response': response,
                    'session_id': session_id,
                    'suggested_questions': chatbot.get_suggested_questions(),
                    'context': chatbot.get_chat_context(),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f"Chat processing failed: {str(e)}",
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @app.route('/api/suggestions', methods=['GET'])
        def suggestions_endpoint():
            """Get suggested questions"""
            session_id = request.args.get('session_id')
            
            if session_id and session_id in active_sessions:
                chatbot = active_sessions[session_id]
                suggestions = chatbot.get_suggested_questions()
            else:
                # Default suggestions for new users
                suggestions = [
                    "How do I buy tickets with UPI?",
                    "What is blockchain ticket validation?",
                    "How do I connect my MetaMask wallet?",
                    "Can I use Paytm to buy NFTs?",
                    "What do I need to get started?"
                ]
            
            return jsonify({
                'success': True,
                'suggestions': suggestions,
                'timestamp': datetime.now().isoformat()
            })
        
        @app.route('/api/feedback', methods=['POST'])
        def feedback_endpoint():
            """Collect user feedback"""
            try:
                data = request.get_json()
                session_id = data.get('session_id')
                message_id = data.get('message_id')
                rating = data.get('rating')
                comment = data.get('comment', '')
                
                if session_id in active_sessions:
                    chatbot = active_sessions[session_id]
                    feedback = chatbot.add_user_feedback(message_id, rating, comment)
                    
                    return jsonify({
                        'success': True,
                        'feedback_id': feedback.get('timestamp'),
                        'message': 'Thank you for your feedback!'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Session not found'
                    }), 404
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f"Feedback processing failed: {str(e)}"
                }), 500
        
        @app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'service': 'TruePass AI Chatbot',
                'version': '1.0.0',
                'active_sessions': len(active_sessions),
                'timestamp': datetime.now().isoformat()
            })
        
        return app
        
    except ImportError:
        print("⚠️  Flask not installed. Install with: pip install flask flask-cors")
        return None


def main():
    """
    Main function to run the TruePass chatbot
    """
    import sys
    
    print("🚀 TruePass AI Chatbot System")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'demo':
            print("📋 Running Demo Mode...")
            run_chatbot_demo()
            
        elif mode == 'interactive':
            print("💬 Starting Interactive Chat...")
            interactive_chat()
            
        elif mode == 'web':
            print("🌐 Starting Web API Server...")
            app = create_web_api_wrapper()
            if app:
                print("🎯 Starting Flask server on http://localhost:5000")
                print("📡 API Endpoints:")
                print("   • POST /api/chat - Main chat endpoint")
                print("   • GET /api/suggestions - Get suggested questions")
                print("   • POST /api/feedback - Submit feedback")
                print("   • GET /api/health - Health check")
                print("\n🔗 Integration Example:")
                print("   curl -X POST http://localhost:5000/api/chat \\")
                print("        -H 'Content-Type: application/json' \\")
                print("        -d '{\"message\": \"How do I buy tickets?\", \"session_id\": \"test123\"}'")
                print("\n" + "=" * 50)
                app.run(debug=True, host='0.0.0.0', port=5000)
            else:
                print("❌ Could not start web server. Missing dependencies.")
                
        else:
            print(f"❌ Unknown mode: {mode}")
            print("✅ Available modes: demo, interactive, web")
    else:
        print("🎯 Available Commands:")
        print("   python chatbot.py demo       - Run demonstration")
        print("   python chatbot.py interactive - Start interactive chat")
        print("   python chatbot.py web        - Start web API server")
        print("\n🔧 Quick Test:")
        interactive_chat()


if __name__ == "__main__":
    main()