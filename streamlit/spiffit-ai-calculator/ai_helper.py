"""
AI/LLM Integration for Natural Language Queries
Handles Genie and Foundation Model API interactions
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

class IncentiveAI:
    """
    Handles natural language queries using Databricks LLMs
    """
    
    def __init__(self, genie_space_id: str = None, model_name: str = None):
        """
        Initialize AI helper
        
        Args:
            genie_space_id: Optional Genie space ID
            model_name: Optional Foundation Model name 
                       (e.g., 'databricks-meta-llama-3-1-70b-instruct')
        """
        # Initialize Databricks client
        # Priority:
        # 1. PAT token (DATABRICKS_HOST + DATABRICKS_TOKEN) - for Genie access
        # 2. CLI profile (DATABRICKS_PROFILE) - for local development
        # 3. Automatic OAuth - for Databricks Apps (no Genie support)
        
        host = os.getenv("DATABRICKS_HOST")
        token = os.getenv("DATABRICKS_TOKEN")
        profile = os.getenv("DATABRICKS_PROFILE")
        
        # Log authentication debug info
        logger.info("=" * 60)
        logger.info("🔐 IncentiveAI Authentication Debug")
        logger.info("=" * 60)
        logger.info(f"📋 Environment Variables:")
        logger.info(f"  DATABRICKS_HOST: {host if host else '❌ NOT SET'}")
        logger.info(f"  DATABRICKS_TOKEN: {'✅ SET (***' + token[-4:] + ')' if token else '❌ NOT SET'}")
        logger.info(f"  DATABRICKS_PROFILE: {profile if profile else '❌ NOT SET'}")
        logger.info(f"  GENIE_SPACE_ID (param): {genie_space_id if genie_space_id else '❌ NOT SET'}")
        logger.info("")
        
        if host and token:
            # PAT token authentication (supports Genie)
            logger.info("✅ Using PAT Token authentication (host + token)")
            logger.info(f"   Host: {host}")
            logger.info(f"   Token: ***{token[-4:]}")
            self.workspace = WorkspaceClient(host=host, token=token)
            self.auth_method = "PAT Token"
        elif profile:
            # Local development with CLI profile
            logger.info(f"✅ Using CLI Profile authentication: {profile}")
            self.workspace = WorkspaceClient(profile=profile)
            self.auth_method = f"CLI Profile ({profile})"
        else:
            # Databricks Apps - automatic OAuth (doesn't support Genie)
            logger.warning("⚠️ Using automatic OAuth M2M authentication")
            logger.warning("   This authentication method does NOT support Genie!")
            self.workspace = WorkspaceClient()
            self.auth_method = "OAuth M2M (default)"
        
        logger.info(f"🔑 Auth Method: {self.auth_method}")
        logger.info("=" * 60)
        
        self.genie_space_id = genie_space_id
        self.model_name = model_name or "databricks-meta-llama-3-1-70b-instruct"
    
    def ask_question(self, question: str, calculator_results: dict = None):
        """
        Process a natural language question
        
        Args:
            question: User's question
            calculator_results: Optional pre-computed results to format
            
        Returns:
            Natural language response
        """
        
        # Option 1: Use Genie if you have a space set up
        if self.genie_space_id:
            return self._ask_genie(question)
        
        # Option 2: Use Foundation Model API directly
        else:
            return self._ask_foundation_model(question, calculator_results)
    
    def _ask_genie(self, question: str):
        """
        Query using Genie space
        
        API flow: start_conversation returns Wait object, call .result() to get conversation
        """
        logger.info("=" * 60)
        logger.info("💬 Calling Genie API")
        logger.info("=" * 60)
        logger.info(f"Space ID: {self.genie_space_id}")
        logger.info(f"Question: {question}")
        logger.info(f"Auth Method: {self.auth_method}")
        
        try:
            logger.info("⏳ Initiating conversation (async)...")
            # Start conversation WITH the question (creates conversation + first message)
            # This returns a Wait object - need to call .result()
            wait_obj = self.workspace.genie.start_conversation(
                space_id=self.genie_space_id,
                content=question  # Initial message
            )
            
            logger.info("⏳ Waiting for Genie response...")
            # Wait for Genie to process the query
            conversation = wait_obj.result()
            logger.info("✅ Received response from Genie")
            
            if not conversation:
                return "Failed to start Genie conversation (no response)"
            
            # Extract the response from conversation
            # The conversation object may have different attributes depending on the response
            if hasattr(conversation, 'messages') and conversation.messages:
                # Get the last message (Genie's response)
                last_message = conversation.messages[-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                elif hasattr(last_message, 'text'):
                    return last_message.text
                else:
                    return f"Message format unexpected: {str(last_message)}"
            
            elif hasattr(conversation, 'content'):
                return conversation.content
            
            elif hasattr(conversation, 'text'):
                return conversation.text
            
            elif hasattr(conversation, 'attachments') and conversation.attachments:
                # Genie may return query results as attachments
                return self._format_genie_attachments(conversation.attachments)
            
            else:
                # Debug: show what we got
                return f"Received response from Genie but couldn't parse. Object type: {type(conversation).__name__}. Attributes: {dir(conversation)}"
                
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            
            logger.error("❌ Genie API call failed!")
            logger.error(f"Error: {str(e)}")
            logger.error(f"Space ID: {self.genie_space_id}")
            logger.error(f"Auth Method: {self.auth_method}")
            logger.error(f"Full traceback:\n{error_detail}")
            
            return f"""Genie API Error:
{str(e)}

**Possible causes:**
1. Databricks App doesn't have permission to access Genie spaces
2. API authentication context differs from CLI
3. Genie space permissions need to be shared with the app

**Debug info:**
Space ID: {self.genie_space_id}
Auth Method: {self.auth_method}
Error details: {error_detail}

**To fix:** 
- Check GENIE_PERMISSIONS_FIX.md for permission setup
- Verify space ID is correct in Troubleshooting tab
- Check app logs for authentication details
"""
    
    def _format_genie_attachments(self, attachments):
        """Format Genie query results from attachments"""
        try:
            results = []
            for attachment in attachments:
                if hasattr(attachment, 'query') and hasattr(attachment.query, 'query'):
                    results.append(f"**Query:** {attachment.query.query}")
                if hasattr(attachment, 'query') and hasattr(attachment.query, 'result'):
                    results.append(f"**Result:** {attachment.query.result}")
            return "\n\n".join(results) if results else str(attachments)
        except Exception as e:
            return f"Genie returned data but couldn't format: {str(attachments)}"
    
    def _ask_foundation_model(self, question: str, calculator_results: dict = None):
        """
        Use Foundation Model API (Gemini/Claude/Llama) directly
        """
        
        # Build context from calculator results if provided
        context = ""
        if calculator_results:
            context = f"\n\nAvailable data: {json.dumps(calculator_results, indent=2)}"
        
        # Create prompt
        prompt = f"""You are an AI assistant helping with sales incentive calculations.

User question: {question}
{context}

Provide a clear, conversational answer. If you need specific employee data, ask for it.
If data is provided, format numbers as currency and explain the calculations.
"""
        
        try:
            # Call Foundation Model
            response = self.workspace.serving_endpoints.query(
                name=self.model_name,
                messages=[
                    ChatMessage(
                        role=ChatMessageRole.USER,
                        content=prompt
                    )
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"LLM error: {str(e)}"

