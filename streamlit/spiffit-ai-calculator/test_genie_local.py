"""
Quick test script to verify Genie API works with your CLI credentials
Run locally: 
  set DATABRICKS_PROFILE=dlk-hackathon
  python test_genie_local.py
"""

import os
from databricks.sdk import WorkspaceClient

# Set profile via environment variable
os.environ["DATABRICKS_PROFILE"] = "dlk-hackathon"

# Use your CLI profile
workspace = WorkspaceClient()

# Test with the sales space
space_id = "01f0c403c3cf184e9b7f1f6c9ee45905"
question = "What data do you have?"

print(f"Testing Genie space: {space_id}")
print(f"Question: {question}\n")

try:
    # Try create_message (newer API)
    print("Attempting create_message...")
    message = workspace.genie.create_message(
        space_id=space_id,
        content=question
    )
    print(f"✅ Success with create_message!")
    print(f"Response: {message}")
    
except Exception as e:
    print(f"❌ create_message failed: {str(e)}\n")
    
    try:
        # Try start_conversation
        print("Attempting start_conversation...")
        conversation = workspace.genie.start_conversation(
            space_id=space_id,
            content=question
        )
        print(f"✅ Success with start_conversation!")
        print(f"Response: {conversation}")
        
    except Exception as e2:
        print(f"❌ start_conversation also failed: {str(e2)}")

