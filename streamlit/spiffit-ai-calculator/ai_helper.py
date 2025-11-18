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
            # Explicitly specify auth_type to override automatic OAuth M2M
            self.workspace = WorkspaceClient(host=host, token=token, auth_type='pat')
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
            logger.info(f"📦 Response type: {type(conversation)}")
            logger.info(f"📦 Response has messages: {hasattr(conversation, 'messages')}")
            logger.info(f"📦 Response has attachments: {hasattr(conversation, 'attachments')}")
            logger.info(f"📦 Response has content: {hasattr(conversation, 'content')}")
            logger.info(f"📦 Response has text: {hasattr(conversation, 'text')}")
            
            if not conversation:
                return "Failed to start Genie conversation (no response)"
            
            # CRITICAL: Check if this is a GenieMessage (no messages array)
            # In this case, the response IS the message, and data is in attachments!
            if not hasattr(conversation, 'messages'):
                logger.info("📨 Response is a GenieMessage (no messages array)")
                logger.info("📨 Looking for data in attachments...")
                
                # For GenieMessage, attachments contain the actual query results
                if hasattr(conversation, 'attachments') and conversation.attachments:
                    logger.info(f"📎 Found {len(conversation.attachments)} attachments")
                    return self._format_genie_attachments(conversation.attachments)
                
                # Fallback to content (but this is likely the question echoed back)
                elif hasattr(conversation, 'content') and conversation.content:
                    content = str(conversation.content)
                    logger.warning(f"⚠️ No attachments found, using content (might be question echo)")
                    logger.info(f"📄 Content: {content[:100]}...")
                    
                    if content.strip() == question.strip():
                        return f"⚠️ Genie returned the question without data. This might mean:\n- No data in the Genie space tables\n- SQL warehouse is stopped\n- Query returned no results"
                    
                    return content
                
                elif hasattr(conversation, 'text') and conversation.text:
                    return str(conversation.text)
                
                else:
                    logger.error("❌ GenieMessage has no attachments, content, or text!")
                    return f"Genie returned a response but it's empty. Response attributes: {[a for a in dir(conversation) if not a.startswith('_')]}"
            
            # Original logic for Conversation objects with messages array
            elif hasattr(conversation, 'messages') and conversation.messages:
                logger.info(f"📨 Found {len(conversation.messages)} messages")
                
                # CRITICAL: Filter out user messages, only get assistant (Genie) messages
                assistant_messages = [msg for msg in conversation.messages if hasattr(msg, 'role') and msg.role == 'ASSISTANT']
                user_messages = [msg for msg in conversation.messages if hasattr(msg, 'role') and msg.role == 'USER']
                
                logger.info(f"📨 User messages: {len(user_messages)}, Assistant messages: {len(assistant_messages)}")
                
                # Get the last ASSISTANT message (Genie's actual response)
                if assistant_messages:
                    last_message = assistant_messages[-1]
                    logger.info(f"📨 Using last assistant message")
                else:
                    # Fallback: use last message regardless
                    last_message = conversation.messages[-1]
                    logger.info(f"📨 No assistant messages found, using last message (might be user message!)")
                
                logger.info(f"📨 Message role: {getattr(last_message, 'role', 'UNKNOWN')}")
                logger.info(f"📨 Message has content: {hasattr(last_message, 'content')}")
                logger.info(f"📨 Message has text: {hasattr(last_message, 'text')}")
                logger.info(f"📨 Message has attachments: {hasattr(last_message, 'attachments')}")
                
                # Try to extract response
                if hasattr(last_message, 'content') and last_message.content:
                    content = str(last_message.content)
                    logger.info(f"✅ Extracted content ({len(content)} chars): {content[:100]}...")
                    
                    # Double-check it's not just the question echoed back
                    if content.strip() == question.strip():
                        logger.warning("⚠️ Content is the same as the question! Looking for attachments...")
                        if hasattr(last_message, 'attachments') and last_message.attachments:
                            return self._format_genie_attachments(last_message.attachments)
                        else:
                            return f"Genie returned the question without an answer. The space may have no data or the query failed."
                    
                    return content
                    
                elif hasattr(last_message, 'text') and last_message.text:
                    text = str(last_message.text)
                    logger.info(f"✅ Extracted text ({len(text)} chars): {text[:100]}...")
                    return text
                    
                elif hasattr(last_message, 'attachments') and last_message.attachments:
                    logger.info(f"📎 Processing {len(last_message.attachments)} attachments")
                    return self._format_genie_attachments(last_message.attachments)
                    
                else:
                    logger.warning("⚠️ Message has no extractable content, text, or attachments")
                    return f"Message format unexpected: {str(last_message)[:200]}"
            
            elif hasattr(conversation, 'content') and conversation.content:
                logger.info(f"✅ Extracted conversation content")
                return conversation.content
            
            elif hasattr(conversation, 'text') and conversation.text:
                logger.info(f"✅ Extracted conversation text")
                return conversation.text
            
            elif hasattr(conversation, 'attachments') and conversation.attachments:
                # Genie may return query results as attachments
                logger.info(f"📎 Processing conversation attachments")
                return self._format_genie_attachments(conversation.attachments)
            
            else:
                # Debug: show what we got
                logger.error("❌ Could not find response in conversation object")
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
            logger.info(f"📎 Formatting {len(attachments)} attachments")
            results = []
            
            for i, attachment in enumerate(attachments):
                logger.info(f"📎 Attachment {i+1} type: {type(attachment)}")
                logger.info(f"📎 Attachment {i+1} attributes: {dir(attachment)}")
                
                # Try different ways to extract data
                if hasattr(attachment, 'query'):
                    query_obj = attachment.query
                    logger.info(f"📊 Found query object: {type(query_obj)}")
                    
                    if hasattr(query_obj, 'query'):
                        results.append(f"**SQL Query:**\n```sql\n{query_obj.query}\n```")
                        logger.info(f"✅ Extracted SQL query")
                    
                    if hasattr(query_obj, 'result'):
                        result_data = query_obj.result
                        logger.info(f"📊 Query result type: {type(result_data)}")
                        
                        # Try to format result nicely
                        if isinstance(result_data, (list, tuple)) and len(result_data) > 0:
                            results.append(f"**Query Results:** {len(result_data)} rows")
                            # Show first few rows
                            results.append(f"```\n{str(result_data[:5])}\n```")
                        else:
                            results.append(f"**Result:**\n```\n{result_data}\n```")
                        logger.info(f"✅ Extracted query results")
                
                # Check for text content
                if hasattr(attachment, 'text') and attachment.text:
                    results.append(f"**Text:** {attachment.text}")
                    logger.info(f"✅ Extracted attachment text")
                
                # Check for content
                if hasattr(attachment, 'content') and attachment.content:
                    results.append(f"**Content:** {attachment.content}")
                    logger.info(f"✅ Extracted attachment content")
            
            if results:
                formatted = "\n\n".join(results)
                logger.info(f"✅ Successfully formatted attachments ({len(formatted)} chars)")
                return formatted
            else:
                logger.warning(f"⚠️ No data extracted from attachments, returning raw")
                return f"Genie returned attachments but couldn't parse them:\n```\n{str(attachments)[:500]}\n```"
                
        except Exception as e:
            logger.error(f"❌ Error formatting attachments: {str(e)}")
            return f"Genie returned data but couldn't format it: {str(e)}\n\nRaw: {str(attachments)[:300]}"
    
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

