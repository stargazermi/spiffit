"""
AI/LLM Integration for Natural Language Queries
Handles Genie and Foundation Model API interactions
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from databricks.sdk.service.sql import StatementState
import json
import os
import logging
import time

# Configure logging
logger = logging.getLogger(__name__)

class IncentiveAI:
    """
    Handles natural language queries using Databricks LLMs
    """
    
    def __init__(self, genie_space_id: str = None, model_name: str = None, 
                 alt_workspace_host: str = None, alt_workspace_token: str = None):
        """
        Initialize AI helper
        
        Args:
            genie_space_id: Optional Genie space ID
            model_name: Optional Foundation Model name 
                       (e.g., 'databricks-meta-llama-3-1-70b-instruct')
            alt_workspace_host: Optional workspace URL for cross-workspace Genie access
            alt_workspace_token: Optional PAT token for cross-workspace Genie access
        """
        # Initialize Databricks client
        # Priority:
        # 1. Alternate workspace (host + token) for cross-workspace Genie spaces
        # 2. PAT token (DATABRICKS_HOST + DATABRICKS_TOKEN) - for Genie access
        # 3. CLI profile (DATABRICKS_PROFILE) - for local development
        # 4. Automatic OAuth - for Databricks Apps (no Genie support)
        
        # Use alternate workspace if provided, otherwise use main workspace
        host = alt_workspace_host or os.getenv("DATABRICKS_HOST")
        token = alt_workspace_token or os.getenv("DATABRICKS_TOKEN")
        profile = os.getenv("DATABRICKS_PROFILE")
        
        # Initialize Databricks client with appropriate authentication
        if host and token:
            self.workspace = WorkspaceClient(host=host, token=token, auth_type='pat')
            self.auth_method = "PAT Token"
        elif profile:
            self.workspace = WorkspaceClient(profile=profile)
            self.auth_method = f"CLI Profile"
        else:
            self.workspace = WorkspaceClient()
            self.auth_method = "OAuth"
        
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
        try:
            # ⏱️ TIMING: Genie API call
            start_time = time.time()
            logger.info(f"⏱️ [START] Genie API call to space {self.genie_space_id}")
            
            # Start conversation and wait for response
            wait_obj = self.workspace.genie.start_conversation(
                space_id=self.genie_space_id,
                content=question
            )
            conversation = wait_obj.result()
            
            elapsed = time.time() - start_time
            logger.info(f"⏱️ [END] Genie API call completed in {elapsed:.2f}s")
            
            if not conversation:
                return "Failed to start Genie conversation (no response)"
            
            # Check if this is a GenieMessage (no messages array)
            if not hasattr(conversation, 'messages'):
                # For GenieMessage, attachments contain the actual query results
                if hasattr(conversation, 'attachments') and conversation.attachments:
                    return self._format_genie_attachments(conversation.attachments)
                
                # Fallback to content
                elif hasattr(conversation, 'content') and conversation.content:
                    content = str(conversation.content)
                    if content.strip() == question.strip():
                        return f"⚠️ Genie returned the question without data. Check:\n- Data in Genie space tables\n- SQL warehouse is running\n- Query returned results"
                    return content
                
                elif hasattr(conversation, 'text') and conversation.text:
                    return str(conversation.text)
                
                else:
                    logger.error("GenieMessage has no attachments, content, or text")
                    return "Genie returned an empty response"
            
            # Original logic for Conversation objects with messages array
            elif hasattr(conversation, 'messages') and conversation.messages:
                # Filter out user messages, only get assistant (Genie) messages
                assistant_messages = [msg for msg in conversation.messages if hasattr(msg, 'role') and msg.role == 'ASSISTANT']
                
                # Get the last ASSISTANT message (Genie's actual response)
                if assistant_messages:
                    last_message = assistant_messages[-1]
                else:
                    # Fallback: use last message regardless
                    last_message = conversation.messages[-1]
                
                
                # Try to extract response
                if hasattr(last_message, 'content') and last_message.content:
                    content = str(last_message.content)
                    
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
                    return text
                    
                elif hasattr(last_message, 'attachments') and last_message.attachments:
                    return self._format_genie_attachments(last_message.attachments)
                    
                else:
                    logger.warning("⚠️ Message has no extractable content, text, or attachments")
                    return f"Message format unexpected: {str(last_message)[:200]}"
            
            elif hasattr(conversation, 'content') and conversation.content:
                return conversation.content
            
            elif hasattr(conversation, 'text') and conversation.text:
                return conversation.text
            
            elif hasattr(conversation, 'attachments') and conversation.attachments:
                # Genie may return query results as attachments
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
    
    def _format_query_results_as_table(self, result_data, max_rows=10):
        """Format query results as a markdown table (without column names)"""
        return self._format_query_results_as_table_with_headers(result_data, None, max_rows)
    
    def _format_query_results_as_table_with_headers(self, result_data, column_names=None, max_rows=10):
        """Format query results as a markdown table with optional column names"""
        if not result_data or len(result_data) == 0:
            return "**Query Results:** No data found"
        
        # Determine number of columns from first row
        first_row = result_data[0]
        if isinstance(first_row, (list, tuple)):
            num_cols = len(first_row)
        else:
            # Single value
            num_cols = 1
            result_data = [[row] for row in result_data]
        
        # Build markdown table
        lines = [f"**Query Results:** {len(result_data)} rows found\n"]
        
        # Table header
        if column_names and len(column_names) == num_cols:
            # Use provided column names
            header = "| " + " | ".join(column_names) + " |"
            separator = "|" + "|".join(["-------" for _ in range(num_cols)]) + "|"
        elif num_cols == 1:
            header = "| Value |"
            separator = "|-------|"
        else:
            # Generic column names
            headers = [f"Column {i+1}" for i in range(num_cols)]
            header = "| " + " | ".join(headers) + " |"
            separator = "|" + "|".join(["-------" for _ in range(num_cols)]) + "|"
        
        lines.append(header)
        lines.append(separator)
        
        # Table rows
        for row in result_data[:max_rows]:
            if isinstance(row, (list, tuple)):
                row_str = "| " + " | ".join([str(val) for val in row]) + " |"
            else:
                row_str = f"| {str(row)} |"
            lines.append(row_str)
        
        # Show truncation message if needed
        if len(result_data) > max_rows:
            lines.append(f"\n*...and {len(result_data) - max_rows} more rows*")
        
        return "\n".join(lines)
    
    def _format_genie_attachments(self, attachments):
        """Format Genie query results from attachments"""
        try:
            results = []
            
            for i, attachment in enumerate(attachments):
                
                # Try different ways to extract data
                if hasattr(attachment, 'query'):
                    query_obj = attachment.query
                    
                    sql_query = None
                    if hasattr(query_obj, 'query'):
                        sql_query = query_obj.query
                        results.append(f"**SQL Query:**\n```sql\n{sql_query}\n```")
                    
                    # Check if query has results embedded
                    has_valid_result = False
                    if hasattr(query_obj, 'result'):
                        result_data = query_obj.result
                        
                        # Check if result_data has actual data
                        if isinstance(result_data, (list, tuple)) and len(result_data) > 0:
                            has_valid_result = True
                            # Format as markdown table
                            table_output = self._format_query_results_as_table(result_data)
                            results.append(table_output)
                        elif isinstance(result_data, str) and result_data.strip():
                            has_valid_result = True
                            results.append(f"**Result:**\n```\n{result_data}\n```")
                        else:
                            logger.warning(f"⚠️ Result is empty or invalid: {type(result_data)} = {result_data}")
                    else:
                        logger.warning("⚠️ Query object has no 'result' attribute")
                    
                    # If no valid result from Genie, execute SQL ourselves
                    if not has_valid_result and sql_query and hasattr(self, 'workspace'):
                        logger.warning("⚠️ No valid results from Genie - executing SQL query ourselves")
                        executed_results = self._execute_sql_query(sql_query)
                        if executed_results:
                            results.append(executed_results)
                        else:
                            results.append("**Query Results:** ⚠️ No data returned (query may have failed or table is empty)")
                
                # Check for text content
                if hasattr(attachment, 'text') and attachment.text:
                    results.append(f"**Text:** {attachment.text}")
                
                # Check for content
                if hasattr(attachment, 'content') and attachment.content:
                    results.append(f"**Content:** {attachment.content}")
            
            if results:
                formatted = "\n\n".join(results)
                return formatted
            else:
                logger.warning(f"⚠️ No data extracted from attachments, returning raw")
                return f"Genie returned attachments but couldn't parse them:\n```\n{str(attachments)[:500]}\n```"
                
        except Exception as e:
            logger.error(f"❌ Error formatting attachments: {str(e)}")
            return f"Genie returned data but couldn't format it: {str(e)}\n\nRaw: {str(attachments)[:300]}"
    
    def _execute_sql_query(self, sql_query: str) -> str:
        """
        Execute a SQL query against the warehouse and return formatted results
        """
        try:
            # ⏱️ TIMING: SQL query execution
            start_time = time.time()
            warehouse_id = os.getenv("SQL_WAREHOUSE_ID", "0962fa4cf0922125")
            logger.info(f"⏱️ [START] SQL execution on warehouse {warehouse_id}")
            
            # Execute SQL statement
            statement = self.workspace.statement_execution.execute_statement(
                warehouse_id=warehouse_id,
                statement=sql_query,
                wait_timeout="30s"
            )
            
            elapsed = time.time() - start_time
            logger.info(f"⏱️ [END] SQL execution completed in {elapsed:.2f}s")
            
            
            # Get result - it might be a property or method
            try:
                if hasattr(statement, 'result'):
                    if callable(statement.result):
                        result = statement.result()  # It's a method
                    else:
                        result = statement.result  # It's a property
                else:
                    # statement itself might be the result
                    result = statement
            except Exception as e:
                logger.error(f"❌ Error accessing result: {str(e)}")
                # Try to use statement directly
                result = statement
            
            if not result:
                logger.warning("⚠️ No result object returned")
                return None
            
            # Check if we got data back
            if hasattr(result, 'data_array') and result.data_array:
                
                # Extract column headers if available
                column_names = None
                if hasattr(result, 'manifest') and hasattr(result.manifest, 'schema') and result.manifest.schema.columns:
                    column_names = [col.name for col in result.manifest.schema.columns]
                
                # Convert to list of lists for table formatting
                data_rows = []
                for row in result.data_array:
                    if hasattr(row, 'values'):
                        data_rows.append(list(row.values))
                    else:
                        data_rows.append([row])
                
                # Format as markdown table with column names
                return self._format_query_results_as_table_with_headers(data_rows, column_names)
            
            elif hasattr(result, 'chunk_index'):
                # Chunked results - fetch them
                return "**Query Results:** Results available but in chunked format (not yet implemented)"
            
            else:
                logger.warning("⚠️ Result object has no data_array")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error executing SQL query: {str(e)}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            if "warehouse" in str(e).lower() or "stopped" in str(e).lower():
                return f"**Query Execution Error:** SQL warehouse may be stopped. Start it in Databricks UI.\n\nError: {str(e)}"
            elif "permission" in str(e).lower() or "authorized" in str(e).lower():
                return f"**Query Execution Error:** Permission denied. Check warehouse permissions.\n\nError: {str(e)}"
            else:
                return f"**Query Execution Error:** {str(e)}"
    
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

