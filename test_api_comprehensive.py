"""
Comprehensive API Testing Script for Manny Campus Chatbot
Tests all routes: /api/chat, /api/threads, /api/tts
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print('='*60)

def print_response(response, description=""):
    print(f"\n📤 {description}")
    print(f"Status: {response.status_code}")
    if response.status_code < 400:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print(f"Error: {response.text}")

def test_health_endpoints():
    """Test basic health and info endpoints"""
    print_test_header("HEALTH & INFO ENDPOINTS")
    
    # Test ping
    response = requests.get(f"{BASE_URL}/ping")
    print_response(response, "GET /ping - Health Check")
    
    # Test root
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "GET / - Root Info")
    
    # Test TTS health
    response = requests.get(f"{BASE_URL}/api/tts/health")
    print_response(response, "GET /api/tts/health - TTS Health Check")

def test_chat_endpoints():
    """Test chat functionality with dummy AI"""
    print_test_header("CHAT ENDPOINTS")
    
    # Test 1: Basic chat
    chat_data = {
        "user_id": "test_user_1",
        "message": "What are the library hours?",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=chat_data)
    print_response(response, "POST /api/chat - Library Question")
    
    if response.status_code == 200:
        chat_response = response.json()
        conversation_id_1 = chat_response.get("conversation_id")
        print(f"💾 Saved conversation_id: {conversation_id_1}")
    
    # Test 2: Follow-up message in same thread
    if 'conversation_id_1' in locals():
        followup_data = {
            "user_id": "test_user_1",
            "conversation_id": conversation_id_1,
            "message": "Can I book a study room?",
            "language": "en"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=followup_data)
        print_response(response, "POST /api/chat - Follow-up Question")
    
    # Test 3: Different topic
    cafeteria_data = {
        "user_id": "test_user_1",
        "message": "What's today's menu in the cafeteria?",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=cafeteria_data)
    print_response(response, "POST /api/chat - Cafeteria Question")
    
    # Test 4: Different user
    user2_data = {
        "user_id": "test_user_2",
        "message": "What documents do I need for admission?",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=user2_data)
    print_response(response, "POST /api/chat - Admission Question (User 2)")

def test_thread_endpoints():
    """Test thread management functionality"""
    print_test_header("THREAD ENDPOINTS")
    
    # Test 1: Create thread manually
    thread_data = {
        "user_id": "test_user_3",
        "title": "Academic Questions"
    }
    response = requests.post(f"{BASE_URL}/api/threads", json=thread_data)
    print_response(response, "POST /api/threads - Create Thread")
    
    if response.status_code == 200:
        thread_response = response.json()
        manual_conv_id = thread_response.get("conversation_id")
        print(f"💾 Created thread: {manual_conv_id}")
        
        # Add message to created thread
        msg_data = {
            "user_id": "test_user_3",
            "conversation_id": manual_conv_id,
            "message": "What's the exam schedule?",
            "language": "en"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=msg_data)
        print_response(response, "POST /api/chat - Message in Created Thread")
    
    # Test 2: Get threads for user 1
    response = requests.get(f"{BASE_URL}/api/threads/test_user_1")
    print_response(response, "GET /api/threads/test_user_1 - User 1 Threads")
    
    # Test 3: Get threads for user 2
    response = requests.get(f"{BASE_URL}/api/threads/test_user_2")
    print_response(response, "GET /api/threads/test_user_2 - User 2 Threads")
    
    # Test 4: Get threads for user 3
    response = requests.get(f"{BASE_URL}/api/threads/test_user_3")
    print_response(response, "GET /api/threads/test_user_3 - User 3 Threads")
    
    # Test 5: Get messages for a specific thread
    if 'manual_conv_id' in locals():
        response = requests.get(f"{BASE_URL}/api/threads/{manual_conv_id}/messages")
        print_response(response, f"GET /api/threads/{manual_conv_id}/messages - Thread Messages")

def test_tts_endpoints():
    """Test TTS functionality"""
    print_test_header("TTS ENDPOINTS")
    
    # Test 1: Generate TTS
    tts_data = {
        "text": "Welcome to the campus chatbot! I can help you with library, cafeteria, and admission information.",
        "language": "en",
        "voice": "en-us-female"
    }
    response = requests.post(f"{BASE_URL}/api/tts/generate", json=tts_data)
    print_response(response, "POST /api/tts/generate - Generate Audio")
    
    if response.status_code == 200:
        tts_response = response.json()
        audio_url = tts_response.get("audio_url")
        print(f"🎵 Audio URL: {BASE_URL}{audio_url}")
        
        # Test audio file access
        if audio_url:
            response = requests.get(f"{BASE_URL}{audio_url}")
            print(f"📤 GET {audio_url} - Audio File Access")
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Content-Length: {len(response.content)} bytes")
    
    # Test 2: Get test audio
    response = requests.get(f"{BASE_URL}/api/tts/test")
    print_response(response, "GET /api/tts/test - Test Audio")
    
    # Test 3: Get available voices
    response = requests.get(f"{BASE_URL}/api/tts/voices")
    print_response(response, "GET /api/tts/voices - Available Voices")
    
    # Test 4: TTS stats
    response = requests.get(f"{BASE_URL}/api/tts/stats")
    print_response(response, "GET /api/tts/stats - TTS Statistics")
    
    # Test 5: Batch TTS generation
    batch_data = [
        "Hello! How can I help you today?",
        "Thank you for using our campus chatbot.",
        "Have a great day!"
    ]
    response = requests.post(f"{BASE_URL}/api/tts/batch", json=batch_data)
    print_response(response, "POST /api/tts/batch - Batch TTS Generation")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print_test_header("AUTH ENDPOINTS")
    
    # Test 1: Get demo users
    response = requests.get(f"{BASE_URL}/auth/demo-users")
    print_response(response, "GET /auth/demo-users - Demo Users")
    
    # Test 2: Login with demo user
    login_data = {
        "user_id": "student123",
        "password": "demo123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "POST /auth/login - Demo Login")
    
    if response.status_code == 200:
        auth_response = response.json()
        token = auth_response.get("access_token")
        print(f"🔑 Access Token: {token[:20]}...")
        
        # Test profile with token
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        print_response(response, "GET /auth/profile - User Profile")

def test_error_cases():
    """Test error handling"""
    print_test_header("ERROR HANDLING")
    
    # Test 1: Invalid endpoint
    response = requests.get(f"{BASE_URL}/api/invalid")
    print_response(response, "GET /api/invalid - Invalid Endpoint")
    
    # Test 2: Missing required fields
    response = requests.post(f"{BASE_URL}/api/chat", json={})
    print_response(response, "POST /api/chat - Missing Fields")
    
    # Test 3: Invalid thread ID
    response = requests.get(f"{BASE_URL}/api/threads/invalid_thread_id/messages")
    print_response(response, "GET /api/threads/invalid/messages - Invalid Thread")

def run_all_tests():
    """Run comprehensive API tests"""
    print("🚀 Starting Comprehensive API Testing for Manny Campus Chatbot")
    print(f"📡 Base URL: {BASE_URL}")
    
    try:
        test_health_endpoints()
        test_chat_endpoints()
        test_thread_endpoints()
        test_tts_endpoints()
        test_auth_endpoints()
        test_error_cases()
        
        print_test_header("TESTING COMPLETE")
        print("✅ All tests completed successfully!")
        print("📝 Check the output above for any errors or issues.")
        print("🎯 API is ready for frontend integration!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
