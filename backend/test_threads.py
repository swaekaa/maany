"""
Test script for thread management functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_thread_management():
    print("🧪 Testing Thread Management Functionality")
    print("=" * 50)
    
    # Test 1: Create threads for user1
    print("\n1. Creating threads for user1...")
    thread1_data = {
        "user_id": "user1", 
        "title": "Library Questions"
    }
    thread1_response = requests.post(f"{BASE_URL}/api/threads", json=thread1_data)
    print(f"Thread 1 created: {thread1_response.status_code}")
    if thread1_response.status_code == 200:
        thread1 = thread1_response.json()
        print(f"Conversation ID: {thread1['conversation_id']}")
        conv_id_1 = thread1['conversation_id']
    
    thread2_data = {
        "user_id": "user1",
        "title": "Cafeteria Queries" 
    }
    thread2_response = requests.post(f"{BASE_URL}/api/threads", json=thread2_data)
    print(f"Thread 2 created: {thread2_response.status_code}")
    if thread2_response.status_code == 200:
        thread2 = thread2_response.json()
        print(f"Conversation ID: {thread2['conversation_id']}")
        conv_id_2 = thread2['conversation_id']
    
    # Test 2: Create threads for user2
    print("\n2. Creating threads for user2...")
    thread3_data = {
        "user_id": "user2",
        "title": "Admission Queries"
    }
    thread3_response = requests.post(f"{BASE_URL}/api/threads", json=thread3_data)
    print(f"Thread 3 created: {thread3_response.status_code}")
    if thread3_response.status_code == 200:
        thread3 = thread3_response.json()
        print(f"Conversation ID: {thread3['conversation_id']}")
        conv_id_3 = thread3['conversation_id']
    
    # Test 3: Add messages to threads
    print("\n3. Adding messages to threads...")
    
    # Add message to thread 1
    msg1_data = {
        "user_id": "user1",
        "conversation_id": conv_id_1,
        "message": "What are the library hours?",
        "language": "en"
    }
    msg1_response = requests.post(f"{BASE_URL}/api/chat", json=msg1_data)
    print(f"Message 1 added: {msg1_response.status_code}")
    
    # Add message to thread 2  
    msg2_data = {
        "user_id": "user1",
        "conversation_id": conv_id_2,
        "message": "What's today's menu?",
        "language": "en"
    }
    msg2_response = requests.post(f"{BASE_URL}/api/chat", json=msg2_data)
    print(f"Message 2 added: {msg2_response.status_code}")
    
    # Add message to thread 3
    msg3_data = {
        "user_id": "user2", 
        "conversation_id": conv_id_3,
        "message": "What documents are required for admission?",
        "language": "en"
    }
    msg3_response = requests.post(f"{BASE_URL}/api/chat", json=msg3_data)
    print(f"Message 3 added: {msg3_response.status_code}")
    
    # Test 4: Get thread lists for each user
    print("\n4. Getting thread lists...")
    
    user1_threads = requests.get(f"{BASE_URL}/api/threads/user1")
    print(f"User1 threads: {user1_threads.status_code}")
    if user1_threads.status_code == 200:
        threads_data = user1_threads.json()
        print(f"User1 has {threads_data['total_count']} threads")
        for thread in threads_data['threads']:
            print(f"  - {thread['title']}: {thread['message_count']} messages")
    
    user2_threads = requests.get(f"{BASE_URL}/api/threads/user2")
    print(f"User2 threads: {user2_threads.status_code}")
    if user2_threads.status_code == 200:
        threads_data = user2_threads.json()
        print(f"User2 has {threads_data['total_count']} threads")
        for thread in threads_data['threads']:
            print(f"  - {thread['title']}: {thread['message_count']} messages")
    
    # Test 5: Get message history for specific threads
    print("\n5. Getting message history...")
    
    thread1_messages = requests.get(f"{BASE_URL}/api/threads/{conv_id_1}/messages")
    print(f"Thread 1 messages: {thread1_messages.status_code}")
    if thread1_messages.status_code == 200:
        messages_data = thread1_messages.json()
        print(f"Thread 1 has {messages_data['total_messages']} messages")
        for msg in messages_data['messages']:
            print(f"  - {msg['sender']}: {msg.get('user_query', msg.get('response_text', ''))[:50]}...")
    
    # Test 6: Add more messages to same thread (conversation continuity)
    print("\n6. Testing conversation continuity...")
    
    followup_msg = {
        "user_id": "user1",
        "conversation_id": conv_id_1,
        "message": "Can I book a study room?",
        "language": "en"
    }
    followup_response = requests.post(f"{BASE_URL}/api/chat", json=followup_msg)
    print(f"Follow-up message added: {followup_response.status_code}")
    
    # Check updated thread
    updated_threads = requests.get(f"{BASE_URL}/api/threads/user1")
    if updated_threads.status_code == 200:
        threads_data = updated_threads.json()
        for thread in threads_data['threads']:
            if thread['conversation_id'] == conv_id_1:
                print(f"Updated thread message count: {thread['message_count']}")
    
    print("\n✅ Thread Management Testing Complete!")

if __name__ == "__main__":
    test_thread_management()
