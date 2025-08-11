#!/usr/bin/env python3
"""
Test script to demonstrate CRUD operations with post-actions
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_crud_operations():
    """Test CRUD operations and see post-actions in action"""
    
    print("🚀 Testing CRUD Operations with Post-Actions")
    print("=" * 50)
    
    # First, login to get session
    print("\n1️⃣ Logging in...")
    login_response = requests.post(f"{API_BASE}/auth/mock_login/")
    if login_response.status_code == 200:
        print("✅ Login successful")
        cookies = login_response.cookies
    else:
        print("❌ Login failed")
        return
    
    # Test CREATE (POST)
    print("\n2️⃣ Creating Model2 item...")
    create_data = {
        "title": "Test Model2 Created",
        "content": "This is test content for creation. It will trigger script execution and email sending."
    }
    
    create_response = requests.post(
        f"{API_BASE}/model2/",
        json=create_data,
        cookies=cookies
    )
    
    if create_response.status_code == 201:
        created_item = create_response.json()
        print(f"✅ Created Model2 with ID: {created_item['id']}")
        print(f"   Title: {created_item['title']}")
        print(f"   Content: {created_item['content'][:50]}...")
        print("   📧 Email notification sent!")
        print("   🔧 Script executed!")
    else:
        print(f"❌ Create failed: {create_response.status_code}")
        print(f"   Response: {create_response.text}")
        return
    
    item_id = created_item['id']
    
    # Test READ (GET)
    print(f"\n3️⃣ Reading Model2 item {item_id}...")
    read_response = requests.get(f"{API_BASE}/model2/{item_id}/", cookies=cookies)
    
    if read_response.status_code == 200:
        item = read_response.json()
        print(f"✅ Read successful")
        print(f"   Title: {item['title']}")
        print(f"   Content: {item['content'][:50]}...")
        print(f"   Created by: {item['created_by']}")
    else:
        print(f"❌ Read failed: {read_response.status_code}")
    
    # Test UPDATE (PUT)
    print(f"\n4️⃣ Updating Model2 item {item_id}...")
    update_data = {
        "title": "Updated Test Model2",
        "content": "This content has been updated. This will trigger script execution and email notification."
    }
    
    update_response = requests.put(
        f"{API_BASE}/model2/{item_id}/",
        json=update_data,
        cookies=cookies
    )
    
    if update_response.status_code == 200:
        updated_item = update_response.json()
        print(f"✅ Update successful")
        print(f"   New Title: {updated_item['title']}")
        print(f"   New Content: {updated_item['content'][:50]}...")
        print("   📧 Update email notification sent!")
        print("   🔧 Script executed with updated data!")
    else:
        print(f"❌ Update failed: {update_response.status_code}")
        print(f"   Response: {update_response.text}")
    
    # Test DELETE
    print(f"\n5️⃣ Deleting Model2 item {item_id}...")
    delete_response = requests.delete(f"{API_BASE}/model2/{item_id}/", cookies=cookies)
    
    if delete_response.status_code == 204:
        print("✅ Delete successful")
    else:
        print(f"❌ Delete failed: {delete_response.status_code}")
    
    # Test LIST
    print(f"\n6️⃣ Listing all Model2 items...")
    list_response = requests.get(f"{API_BASE}/model2/", cookies=cookies)
    
    if list_response.status_code == 200:
        items = list_response.json()
        print(f"✅ List successful - Found {len(items)} items")
        for item in items:
            print(f"   - ID: {item['id']}, Title: {item['title']}")
    else:
        print(f"❌ List failed: {list_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎯 CRUD Test Complete!")
    print("\n📋 What you should see in your Django console:")
    print("   - Script execution logs after create/update")
    print("   - Email sending logs")
    print("   - Any errors or success messages")

if __name__ == "__main__":
    test_crud_operations()
