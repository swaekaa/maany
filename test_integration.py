#!/usr/bin/env python3
"""
Integration Test Script for Frontend-Backend Connection
Tests the complete flow from frontend to backend API
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8080"

class IntegrationTester:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.frontend_url = FRONTEND_URL
        self.test_results: Dict[str, Any] = {}
        
    async def test_backend_health(self) -> bool:
        """Test if backend is responding"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/ping") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Backend Health: {data['message']}")
                        return True
                    else:
                        print(f"❌ Backend Health: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Backend Health: {str(e)}")
            return False
    
    async def test_frontend_health(self) -> bool:
        """Test if frontend is responding"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.frontend_url) as response:
                    if response.status == 200:
                        print(f"✅ Frontend Health: Responding")
                        return True
                    else:
                        print(f"❌ Frontend Health: HTTP {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Frontend Health: {str(e)}")
            return False
    
    async def test_chat_api(self) -> bool:
        """Test chat API functionality"""
        try:
            test_message = {
                "user_id": "integration_test_user",
                "message": "Test message from integration script",
                "language": "en"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.backend_url}/api/chat",
                    json=test_message,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Chat API: Response received")
                        print(f"   Conversation ID: {data.get('conversation_id', 'N/A')}")
                        print(f"   Response Length: {len(data.get('response', ''))}")
                        print(f"   Sources: {len(data.get('sources', []))}")
                        print(f"   TTS URL: {'Yes' if data.get('tts_audio_url') else 'No'}")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Chat API: HTTP {response.status} - {error_text}")
                        return False
        except Exception as e:
            print(f"❌ Chat API: {str(e)}")
            return False
    
    async def test_threads_api(self) -> bool:
        """Test threads API functionality"""
        try:
            # Create a thread
            thread_data = {
                "user_id": "integration_test_user",
                "title": "Integration Test Thread"
            }
            
            async with aiohttp.ClientSession() as session:
                # Create thread
                async with session.post(
                    f"{self.backend_url}/api/threads",
                    json=thread_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        print(f"❌ Threads API: Failed to create thread - HTTP {response.status}")
                        return False
                    
                    thread_result = await response.json()
                    conversation_id = thread_result.get("conversation_id")
                    
                # Get user threads
                async with session.get(f"{self.backend_url}/api/threads/integration_test_user") as response:
                    if response.status == 200:
                        threads = await response.json()
                        print(f"✅ Threads API: Created and retrieved threads")
                        print(f"   Thread Count: {len(threads)}")
                        print(f"   Latest Thread ID: {conversation_id}")
                        return True
                    else:
                        print(f"❌ Threads API: Failed to get threads - HTTP {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Threads API: {str(e)}")
            return False
    
    async def test_tts_api(self) -> bool:
        """Test TTS API functionality"""
        try:
            tts_data = {
                "text": "This is a test of the text-to-speech system.",
                "language": "en",
                "voice": "en-us-female"
            }
            
            async with aiohttp.ClientSession() as session:
                # Test TTS generation
                async with session.post(
                    f"{self.backend_url}/api/tts/generate",
                    json=tts_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        audio_url = data.get("audio_url")
                        
                        # Test audio file access
                        async with session.get(f"{self.backend_url}{audio_url}") as audio_response:
                            if audio_response.status == 200:
                                audio_size = len(await audio_response.read())
                                print(f"✅ TTS API: Audio generated and accessible")
                                print(f"   Audio URL: {audio_url}")
                                print(f"   Audio Size: {audio_size} bytes")
                                print(f"   Duration: {data.get('duration', 'N/A')} seconds")
                                return True
                            else:
                                print(f"❌ TTS API: Audio file not accessible - HTTP {audio_response.status}")
                                return False
                    else:
                        error_text = await response.text()
                        print(f"❌ TTS API: HTTP {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ TTS API: {str(e)}")
            return False
    
    async def test_auth_api(self) -> bool:
        """Test authentication API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get demo users
                async with session.get(f"{self.backend_url}/auth/demo-users") as response:
                    if response.status == 200:
                        data = await response.json()
                        demo_users = data.get("demo_users", [])
                        
                        if demo_users:
                            # Test login with first demo user
                            first_user = demo_users[0]
                            login_data = {
                                "user_id": first_user["user_id"],
                                "password": first_user["password"]
                            }
                            
                            async with session.post(
                                f"{self.backend_url}/auth/login",
                                json=login_data,
                                headers={"Content-Type": "application/json"}
                            ) as login_response:
                                if login_response.status == 200:
                                    login_result = await login_response.json()
                                    token = login_result.get("access_token")
                                    
                                    # Test profile access with token
                                    headers = {"Authorization": f"Bearer {token}"}
                                    async with session.get(
                                        f"{self.backend_url}/auth/profile",
                                        headers=headers
                                    ) as profile_response:
                                        if profile_response.status == 200:
                                            profile = await profile_response.json()
                                            print(f"✅ Auth API: Login and profile access successful")
                                            print(f"   Demo Users: {len(demo_users)}")
                                            print(f"   Test User: {profile.get('full_name', 'N/A')}")
                                            return True
                                        else:
                                            print(f"❌ Auth API: Profile access failed - HTTP {profile_response.status}")
                                            return False
                                else:
                                    print(f"❌ Auth API: Login failed - HTTP {login_response.status}")
                                    return False
                        else:
                            print(f"❌ Auth API: No demo users found")
                            return False
                    else:
                        print(f"❌ Auth API: Failed to get demo users - HTTP {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Auth API: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Frontend-Backend Integration Tests")
        print("=" * 60)
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("Frontend Health", self.test_frontend_health),
            ("Chat API", self.test_chat_api),
            ("Threads API", self.test_threads_api),
            ("TTS API", self.test_tts_api),
            ("Auth API", self.test_auth_api),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testing {test_name}...")
            try:
                result = await test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name}: Unexpected error - {str(e)}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status:<8} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Frontend-Backend integration is working correctly!")
            print("\n📋 Next Steps:")
            print("1. Open http://localhost:8080 in your browser")
            print("2. Click the 'API Test' button in the bottom left")
            print("3. Test the chat widget by clicking the floating chat button")
            print("4. Try asking questions like:")
            print("   - What are the library hours?")
            print("   - What's today's cafeteria menu?")
            print("   - How do I pay my fees?")
        else:
            print(f"❌ {total - passed} tests failed. Check the logs above for details.")
            
        return passed == total

async def main():
    """Main function to run integration tests"""
    tester = IntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
