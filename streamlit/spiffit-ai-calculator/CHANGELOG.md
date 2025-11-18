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

### v1.4.0 - 2024-11-18
**🔐 PAT Token Authentication for Genie**
- ✅ Added PAT Token authentication support (fixes OAuth M2M limitation)
- ✅ Databricks Secrets integration for secure token storage
- ✅ Updated `ai_helper.py` authentication priority: PAT token → CLI profile → OAuth
- ✅ `setup-genie-secrets.ps1` script for easy secret setup
- ✅ `GENIE_PAT_TOKEN_SETUP.md` comprehensive guide
- ✅ No tokens in Git (secure by default)
- ✅ Fixed Genie test button tab switching issue

**Why This Matters:**
- Databricks Apps use OAuth M2M by default (doesn't work with Genie)
- PAT tokens provide full Genie API access
- Secrets keep tokens secure and out of version control

**Setup Required:**
1. Generate PAT token in Databricks UI
2. Run `.\setup-genie-secrets.ps1` to store securely
3. Ensure Genie spaces are shared with PAT token owner
4. Redeploy app

### v1.3.2 - 2024-11-17
**🔧 Genie API Fix (Simplified)**
- ✅ Corrected Genie API call: `start_conversation(space_id, content)`
- ✅ Single API call creates conversation + sends message
- ✅ Comprehensive response parsing (messages, content, text, attachments)
- ✅ Debug output if response format is unexpected

**Technical Details:**
- Correct API: `start_conversation(space_id=..., content=question)`
- This creates the conversation AND sends the first message
- Response parsing handles multiple formats for SDK version compatibility

### v1.3.1 - 2024-11-17 (DEPRECATED - wrong API flow)
**🔧 Critical Fix: Genie API**
- ❌ Tried two-step flow (was incorrect)
- Issue: `start_conversation()` needs `content` parameter

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

