# Spiffit AI Calculator - Changelog

## How to Update Version

When deploying new changes:
1. Update `APP_VERSION` in `app.py` (line 17)
2. Add entry below with changes
3. Commit and push
4. Redeploy in Databricks
5. Check **🔧 Troubleshooting** tab to verify timestamp updated

---

## Version History

### v1.3.1 - 2024-11-17
**🔧 Critical Fix: Genie API**
- ✅ Fixed Genie conversation flow (start_conversation → create_message)
- ✅ Proper two-step API call with conversation_id
- ✅ Added attachment parsing for Genie query results
- ✅ Better error messages with troubleshooting guidance

**Technical Details:**
- Genie API requires: `start_conversation()` first to get `conversation_id`
- Then: `create_message(conversation_id=...)` to send queries
- Result may be in `content`, `text`, or `attachments`

### v1.3.0 - 2024-11-17
**🎉 Major Feature: Competitor Intelligence**
- ✅ Added **Multi-Tool Agent** with smart routing
- ✅ New **Competitor Intelligence** tab
- ✅ **Web Search Tool** for competitor SPIFF research
- ✅ Orchestration with **GPT-5.1** from serving endpoints
- ✅ Automatic routing between Genie spaces and web search
- ✅ Result synthesis across multiple data sources
- ✅ Quick action buttons for common queries
- ✅ Tool usage transparency (shows routing decisions)

**Architecture:**
- Multi-tool agent routes queries to appropriate tools
- Genie spaces → internal data (sales, analytics, market)
- Web search → external competitor data
- Foundation Model → orchestration & synthesis

**Demo Queries:**
- "What SPIFFs is AT&T offering?"
- "Compare our programs with Verizon"
- "Recommend competitive SPIFFs for next month"

### v1.2.0 - 2024-11-17
**Changes:**
- ✅ Fixed Genie API method (`start_conversation` instead of `ask_question`)
- ✅ Added deployment version and timestamp to troubleshooting tab
- ✅ Added comprehensive troubleshooting tab with environment info
- ✅ Added test buttons for Databricks and Genie connections

**Features:**
- Environment variable display
- Connection status indicators
- Configuration viewer
- Quick action test buttons

### v1.1.0 - 2024-11-17
**Changes:**
- ✅ Added troubleshooting tab for debugging
- ✅ Connected to Genie spaces (spg-mocking-bird-sales, analytics, market)
- ✅ Environment variables configured in app.yaml

### v1.0.0 - 2024-11-17
**Initial Release:**
- Basic chat interface
- Query parser for intent extraction
- Foundation Model fallback
- Genie space integration
- Example questions sidebar

