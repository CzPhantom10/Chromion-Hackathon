# TruePass AI Chatbot

An intelligent AI assistant for the TruePass NFT Marketplace & Blockchain Ticket Validation Platform. This chatbot helps users navigate NFT purchases, blockchain ticket validation, and INR payment processing.

## 🚀 Features

### Core Capabilities
- **🎫 Ticket Management**: Guide users through buying tickets with Indian Rupees
- **🔗 Wallet Integration**: Help with MetaMask and other wallet connections
- **🛡️ TOTP Validation**: Explain and assist with blockchain ticket validation
- **💳 Payment Support**: Support for UPI, Paytm, credit cards, and other Indian payment methods
- **🎨 NFT Marketplace**: Help users navigate the NFT marketplace features
- **🛠️ Technical Support**: Troubleshoot common issues and errors

### Advanced Features
- **Intent Analysis**: Automatically detects user intentions and provides contextual responses
- **Entity Extraction**: Extracts relevant information like prices, token IDs, payment methods
- **Session Management**: Tracks conversation history and user context
- **Multi-mode Operation**: Supports interactive chat, demo mode, and web API
- **Feedback System**: Collects user feedback for continuous improvement

## 📋 Requirements

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- `g4f[all]>=0.2.0` - AI conversation engine
- `flask>=2.3.0` - Web API framework
- `flask-cors>=4.0.0` - Cross-origin resource sharing
- `requests>=2.31.0` - HTTP requests
- `python-dateutil>=2.8.0` - Date/time utilities

## 🎯 Usage

### 1. Interactive Chat Mode
Start an interactive conversation with the chatbot:
```bash
python chatbot.py interactive
```

### 2. Demo Mode
Run a demonstration with sample conversations:
```bash
python chatbot.py demo
```

### 3. Web API Mode
Start a Flask web server for API integration:
```bash
python chatbot.py web
```

### 4. Quick Test
Run without arguments for immediate interactive mode:
```bash
python chatbot.py
```

## 🌐 Web API Integration

### Starting the Server
```bash
python chatbot.py web
```
Server runs on `http://localhost:5000`

### API Endpoints

#### Chat Endpoint
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "How do I buy tickets with UPI?",
  "session_id": "user123",
  "current_page": "marketplace"
}
```

Response:
```json
{
  "success": true,
  "response": "Here's how to buy tickets with UPI...",
  "session_id": "user123",
  "suggested_questions": [...],
  "context": {...},
  "timestamp": "2025-06-15T10:30:00"
}
```

#### Other Endpoints
- `GET /api/suggestions` - Get suggested questions
- `POST /api/feedback` - Submit user feedback
- `GET /api/health` - Health check

### Integration Example
```javascript
// Frontend integration example
async function sendMessage(message) {
  const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      session_id: 'user_' + Date.now(),
      current_page: window.location.pathname
    })
  });
  
  const data = await response.json();
  return data.response;
}
```

## 🧪 Testing

### Run All Tests
```bash
python test_chatbot.py
```

### Specific Test Modes
```bash
# Unit tests only
python test_chatbot.py --mode unit

# Manual demonstration tests
python test_chatbot.py --mode manual

# Integration tests
python test_chatbot.py --mode integration
```

## 💡 Example Conversations

### Getting Started
```
User: Hi, I'm new to TruePass. Can you help me?
Bot: 🎉 Welcome to TruePass! Your gateway to NFTs and blockchain tickets with Indian Rupee payments! 
     I'll guide you through wallet setup, ticket purchasing, and more...
```

### Buying Tickets
```
User: How do I buy tickets with UPI?
Bot: 🎫 Buying Tickets with INR - Super Easy!
     1️⃣ Browse available tickets (prices shown in ₹)
     2️⃣ Connect your Ethereum wallet...
```

### Technical Support
```
User: My payment failed, what should I do?
Bot: 🔧 Let me help you troubleshoot the payment issue:
     • Verify payment method has sufficient balance
     • Check internet connection...
```

## 🎨 Customization

### Adding New Intents
```python
# In analyze_user_intent method
intent_patterns = {
    "your_new_intent": {
        "keywords": ["keyword1", "keyword2"],
        "confidence_boost": ["boost1", "boost2"],
        "entities": ["entity1", "entity2"]
    }
}
```

### Adding Quick Responses
```python
# In get_quick_response method
quick_responses = {
    "your_topic": """Your response content with emojis and formatting"""
}
```

### Updating Knowledge Base
```python
# Modify the knowledge_base dictionary in __init__
self.knowledge_base = {
    "new_section": {
        "description": "Your new section",
        "data": [...]
    }
}
```

## 🛡️ Security Considerations

- **API Rate Limiting**: Implement rate limiting for production use
- **Input Validation**: All user inputs are processed safely
- **Session Management**: Sessions expire automatically
- **Error Handling**: Comprehensive error handling prevents crashes
- **CORS Configuration**: Properly configured for web integration

## 📊 Analytics & Monitoring

### Session Tracking
- Conversation duration and message count
- User intent analysis and topic tracking
- Feedback collection and rating analysis
- Error logging and performance monitoring

### Export Session Data
```python
chatbot = TruePassWebChatbot()
session_data = chatbot.export_session_data()
# Contains complete session information for analysis
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **G4F Connection Issues**
   - Check internet connection
   - Try different G4F providers
   - Enable debug mode for detailed logs

3. **Flask Server Issues**
   - Ensure port 5000 is available
   - Check firewall settings
   - Install flask-cors dependency

4. **AI Response Errors**
   - Verify G4F service availability
   - Check API rate limits
   - Try alternative models

### Debug Mode
```python
chatbot = TruePassChatbot(debug=True)  # Enable detailed logging
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## 📄 License

This project is part of the TruePass platform. See the main project repository for license information.

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Contact the TruePass development team
- Join the community Discord server

---

**Built with ❤️ for the TruePass community**
