#!/usr/bin/env python3
"""
Test Genie API Access with PAT Token
Simple script to verify PAT token authentication works with Genie spaces
"""

import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient

# Load environment variables from .env file
load_dotenv()

def test_genie_connection():
    """Test Genie space access with PAT token"""
    
    print("🔐 Testing Genie API Access with PAT Token")
    print("=" * 50)
    print()
    
    # Get credentials from environment
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    genie_space_id = os.getenv("GENIE_SPACE_ID")
    
    # Validate required variables
    if not host:
        print("❌ DATABRICKS_HOST not set in .env file")
        return False
    
    if not token:
        print("❌ DATABRICKS_TOKEN not set in .env file")
        return False
    
    if not genie_space_id:
        print("❌ GENIE_SPACE_ID not set in .env file")
        return False
    
    print(f"✅ Host: {host}")
    print(f"✅ Token: {token[:10]}...{token[-4:]} (masked)")
    print(f"✅ Genie Space ID: {genie_space_id}")
    print()
    
    # Initialize Databricks client with PAT token
    print("🔌 Connecting to Databricks...")
    try:
        workspace = WorkspaceClient(host=host, token=token)
        print("✅ Databricks client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    print()
    
    # Test 1: Verify current user
    print("👤 Test 1: Verifying current user...")
    try:
        user = workspace.current_user.me()
        print(f"✅ Authenticated as: {user.user_name}")
        print(f"   Display Name: {user.display_name}")
    except Exception as e:
        print(f"❌ Failed to get current user: {e}")
        return False
    
    print()
    
    # Test 2: Get Genie space details
    print(f"📦 Test 2: Accessing Genie space...")
    try:
        space = workspace.genie.get_space(space_id=genie_space_id)
        print(f"✅ Found Genie space: {space.title}")
        print(f"   Description: {space.description}")
        print(f"   Warehouse ID: {space.warehouse_id}")
    except Exception as e:
        print(f"❌ Failed to access Genie space: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Verify you have 'Can Run' or 'Can Manage' permission on the Genie space")
        print("   2. Ensure the SQL warehouse is running")
        print("   3. Check that the Genie space ID is correct")
        return False
    
    print()
    
    # Test 3: Start a conversation with Genie
    print("💬 Test 3: Starting Genie conversation...")
    try:
        print("   ⏳ Initiating conversation (async operation)...")
        wait_obj = workspace.genie.start_conversation(
            space_id=genie_space_id,
            content="Show me the top performers"
        )
        
        print(f"   ⏳ Waiting for Genie response...")
        conversation = wait_obj.result()
        
        print("✅ Genie conversation completed!")
        print(f"   Conversation ID: {conversation.conversation_id if hasattr(conversation, 'conversation_id') else 'N/A'}")
        
        # Debug: Show response structure
        print(f"   Response type: {type(conversation).__name__}")
        
        # Try to parse response in multiple ways
        response_text = None
        
        if hasattr(conversation, 'messages') and conversation.messages:
            print(f"   📨 Found {len(conversation.messages)} message(s)")
            last_message = conversation.messages[-1]
            if hasattr(last_message, 'content'):
                response_text = last_message.content
            elif hasattr(last_message, 'text'):
                response_text = last_message.text
        elif hasattr(conversation, 'content'):
            response_text = conversation.content
        elif hasattr(conversation, 'text'):
            response_text = conversation.text
        
        # Check for attachments (query results)
        if hasattr(conversation, 'attachments') and conversation.attachments:
            print(f"   📎 Found {len(conversation.attachments)} attachment(s) (query results)")
        
        if response_text:
            print(f"📄 Response preview: {response_text[:200]}...")
        else:
            print(f"✅ Received response from Genie (conversation created)")
            
    except Exception as e:
        print(f"❌ Failed to query Genie: {e}")
        import traceback
        print(f"\n🔍 Full error:\n{traceback.format_exc()}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check SQL warehouse is running")
        print("   2. Verify Genie space has data/tables configured")
        print("   3. Check Genie space permissions")
        return False
    
    print()
    print("=" * 50)
    print("🎉 All tests passed! PAT token authentication works!")
    print()
    print("✅ Next step: Deploy app with this PAT token in Databricks Secrets")
    return True


if __name__ == "__main__":
    success = test_genie_connection()
    exit(0 if success else 1)

