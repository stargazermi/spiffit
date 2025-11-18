# 📝 Spiffit - Spiff It Good! Changelog

All notable changes to the Spiffit application.

---

## [v2.6.0-SPIFFIT] - 2025-11-18
### 🤖 Expanded Orchestrator Model Options
**Why:** The hardcoded list had only 4 models (some didn't exist), but workspace has 21 serving endpoints!

**Added:**
- ✅ **18 Foundation Models** now available in the dropdown!
- ✅ **Latest Models:**
  - GPT-5.1 (newest OpenAI) ⭐
  - Claude Sonnet 4.5 (newest Anthropic) ⭐
  - Llama 3.3 70B (newest Meta) ⭐
  - Llama 4 Maverick (cutting edge) ⭐
- ✅ **Premium Options:**
  - Claude Opus 4.1 (most powerful reasoning)
  - Llama 3.1 405B (largest model)
  - Gemini 2.5 Pro
  - GPT-5
  - Custom GPT-OSS-120B
- ✅ **Fast & Efficient:**
  - GPT-5 Mini/Nano (fastest)
  - Gemini 2.5 Flash
  - Llama 3.1 8B (budget)
- ✅ **Other Options:**
  - Claude Opus 4, Sonnet 4, 3.7 Sonnet
  - Custom GPT-OSS-20B
  - Gemma 3 12B

**Discovery:**
- Created `list-serving-endpoints.ps1` to query workspace endpoints
- Found 21 serving endpoints (15 suitable for orchestration)
- Removed non-existent models from old hardcoded list

**Benefits:**
- 🎯 **Better Performance:** Use latest GPT-5.1 or Claude 4.5
- ⚡ **Faster Routing:** Try GPT-5-nano for 3-5x speed
- 💰 **Cost Options:** Choose budget (8B) to premium (405B)
- 🔬 **Compare Models:** Test different orchestrators during demo

**Technical Details:**
- Updated `app.py` dropdown (lines 193-219) with 18 models
- Models organized by tier: Recommended → Premium → Fast → Other
- Default: `databricks-gpt-5-1` (GPT-5.1)
- Help text shows "15 models available!"

**Files Modified:**
- `app.py` - Expanded model dropdown from 4 to 18 options
- `multi_tool_agent.py` - Updated default to GPT-5.1
- `list-serving-endpoints.ps1` - New diagnostic script
- `ORCHESTRATOR_MODELS.md` - Complete model selection guide

**Demo Impact:**
- 🎤 **Talk Track:** "We're using GPT-5.1, the latest OpenAI model!"
- 🎯 **Flexibility:** Switch models live during demo
- 💪 **Impressive:** Show cutting-edge Llama 4 or Claude 4.5

---

## [v2.5.1-SPIFFIT] - 2025-11-18
### 📎 CSV Download for Email Attachments
**Why:** Users need to attach raw data files to emails, not just copy formatted text

**Added:**
- ✅ **"📎 Download CSV" button** - Download winner data as CSV file for email attachment
  - Appears next to "Copy for Email" expander
  - Auto-generated filename: `spiff_winners_YYYYMMDD.csv`
  - CSV format with headers and quoted fields
  - Ready to attach to Outlook/Gmail/etc.
- ✅ **Enhanced `format_for_email()` function**
  - Now returns 5 values: `(is_copyable, email_text, csv_data, headers, data_rows)`
  - Creates CSV format alongside text format
  - Proper CSV escaping with quoted fields
- ✅ **Available in both tabs:**
  - Chat tab (clean demo view)
  - Intelligence tab (debug view)
- ✅ **Shows in chat history** - Past responses with data also get download button

**User Flow:**
1. Ask: "Who won the last SPIFF competition?"
2. See results in nice table
3. **Option A:** Click "📧 Copy for Email" → Copy text → Paste in email body
4. **Option B:** Click "📎 Download CSV" → Attach to email as file
5. Send notification email with data! ✅

**Technical Details:**
- CSV generation: comma-separated with double-quote escaping
- Unique download button keys using message content hash or timestamp
- Date-stamped filenames for organization

**Files Modified:**
- `app.py` - Enhanced `format_for_email()`, added download buttons in Chat & Intelligence tabs

---

## [v2.5.0-SPIFFIT] - 2025-11-18
### 📧 Copy for Email Feature
**Why:** Users need to easily copy winner data to paste into emails for notifications

**Added:**
- ✅ **"Copy for Email" button** - Automatically detects SPIFF winner/monthly data
  - Appears as expandable section below answers with winner data
  - One-click copy with st.code() copy button
  - Formats data in clean, email-friendly text (not markdown tables)
- ✅ **Smart detection** - Looks for keywords: winner, SPIFF, earned, employee, month names
- ✅ **Formatted output** includes:
  - Title: "SPIFF Winners"
  - Properly aligned columns
  - Total recipient count
  - Easy to paste directly into Outlook/Gmail
- ✅ **Shows in chat history** - Past responses with data also get the copy button

**Technical Details:**
- New helper function: `format_for_email(answer_text)`
- Parses markdown tables and converts to fixed-width text format
- Auto-calculates column widths for proper alignment
- Returns tuple: `(is_copyable: bool, formatted_text: str)`

**User Flow:**
1. Ask: "Who won the last SPIFF competition?"
2. See results in nice table
3. Click "📧 Copy for Email" expander
4. Click copy button (top right of code block)
5. Paste directly into email - ready to send! ✅

**Files Modified:**
- `app.py` - Added `format_for_email()` helper and copy buttons in Chat tab

---

## [v2.4.1-SPIFFIT] - 2025-11-18
### 🎸 Lyrics Correction
**Why:** Get the theme song lyrics right! It's "you must Spiff It" (like "Whip It")

**Changed:**
- ✅ Fixed all instances of "you gotta" → "you must" (8 files updated)
- ✅ App title: "When SPIFFs Get Tough, You Must Spiff It!"
- ✅ Updated README, CHANGELOG, release notes, and demo scripts

**Files Modified:**
- `app.py`, `README.md`, `SPIFF_IT_THEME.md`, `V2.2.0_RELEASE_NOTES.md`, `SQL_EXECUTION_FIX.md`, `CHANGELOG.md`

---

## [v2.4.0-SPIFFIT] - 2025-11-18
### 🔧 Individual Genie Test Buttons + Improved Routing
**Why:** Need to verify each Genie space individually and ensure all 3 are called for comprehensive queries

**Added:**
- ✅ **Test Individual Genies** section in sidebar
  - 📊 Sales Genie button
  - 📈 Analytics Genie button
  - 🌐 Market Genie button
- ✅ **Improved routing logic** in `multi_tool_agent.py`
  - More aggressive about calling all 3 Genies
  - Added instruction: "prefer calling multiple" tools
  - New example showing all 4 tools for strategic questions
  - Clearer tool descriptions (sales vs analytics vs market)

**Files Modified:**
- `app.py` - Added test buttons in sidebar
- `multi_tool_agent.py` - Enhanced routing prompt

---

## [v2.3.1-SPIFFIT] - 2025-11-18
### 📊 Table Formatting for Query Results
**Why:** Raw Python lists like `['Sarah Johnson', '57730.00']` look unprofessional

**Changed:**
- ✅ **Query results now display as markdown tables** - Clean, professional grid format
- ✅ **Column headers included** - When available from SQL metadata
- ✅ **Generic headers as fallback** - "Column 1", "Column 2", etc. when metadata unavailable
- ✅ **Consistent formatting** - Works for both Genie responses and direct SQL execution

**Before:**
```
Query Results: 5 rows found
['Sarah Johnson', '57730.00']
['Mike Chen', '38150.00']
```

**After:**
```
Query Results: 5 rows found

| Column 1 | Column 2 |
|----------|----------|
| Sarah Johnson | 57730.00 |
| Mike Chen | 38150.00 |
```

**Technical Details:**
- New helper method: `_format_query_results_as_table_with_headers()`
- Supports up to 10 rows (with "...and X more rows" indicator)
- Handles single-column and multi-column results
- Works with both list and tuple row formats

**Files Modified:**
- `ai_helper.py` - Added table formatting methods, updated `_format_genie_attachments()` and `_execute_sql_query()`

---

## [v2.3.0-SPIFFIT] - 2025-11-18
### 🎯 Demo Experience Enhancement
**Why:** Make Chat tab the primary demo interface with cleaner UX

**Changed:**
- ✅ **Sidebar buttons now trigger Chat tab** - All example buttons send queries to the clean Chat tab (not Intelligence/debug tab)
- ✅ **SQL queries hidden in Chat tab** - Filters out verbose SQL code blocks for cleaner demo presentation
  - Removes `**SQL Query:**` sections
  - Removes standalone SQL code blocks
  - Keeps only the natural language answer and data results
- ✅ **Intelligence tab still shows full details** - Debug view unchanged for troubleshooting

**Technical Details:**
- Added `chat_input_from_button` session state for programmatic chat input
- Implemented regex filtering to remove SQL blocks: `\*\*SQL Query:\*\*\s*```sql.*?```` and ````sql.*?````
- Added `import re` for pattern matching

**Files Modified:**
- `app.py` - Updated sidebar button handlers, added SQL filtering to Chat tab

**Demo Flow:**
1. User clicks sidebar example → Query appears in Chat tab
2. Agent processes with multi-tool routing (Genies + web search)
3. Chat shows only: natural language answer + data results
4. Intelligence tab still shows: routing details + SQL + raw results

---

## [v2.2.2-SPIFFIT] - 2025-11-18
### 🐛 Critical Bugfix
**Why:** Deployment failed due to syntax errors in web_search_tool.py

**Fixed:**
- ✅ **IndentationError at line 69** - Fixed "Spectrum" dictionary structure (removed extra closing brace, corrected "focus" indentation)
- ✅ **IndentationError at line 99** - Fixed "T-Mobile" dictionary structure (same issue with Verizon section)

**Files Modified:**
- `web_search_tool.py` - Fixed mock_competitor_data dictionary structure

**Root Cause:** When adding business_offers to the mock data, the "focus" key was incorrectly nested with an extra closing brace, causing Python to expect improper indentation for the next competitor.

---

## [v2.2.1-SPIFFIT] - 2025-11-18
### 🎛️ UI Simplification
**Why:** Remove confusing "Use Genie" checkbox, clarify Foundation Model purpose

**Changed:**
- ✅ **Removed "Use Genie" checkbox** - Multi-agent always active (3 Genies + Web Search)
- ✅ **Clarified Foundation Model dropdown** - Now labeled "Agent Brain (Orchestrator)"
  - Added tooltip: "Which LLM the multi-agent uses for routing & synthesis"
  - Added status caption showing what's always active
- ✅ **Improved sidebar UX** - Clearer configuration section

**Files Modified:**
- `app.py` - Updated sidebar configuration section

---

## [v2.2.0-SPIFFIT] - 2025-11-18
### 🎯 Competitor Intelligence + Clean Demo UI
**Why:** Incorporate supportingAlternate.md recommendations + clean UI for demo

**Added:**
- ✅ **Competitor Data Schema** - Production-ready table structure
  - `competitor_offers` table with proper fields (provider, plan, price, speeds, SLA, etc.)
  - Sample data from AT&T, Spectrum, Comcast, Verizon, Cox
  - SQL file: `sql/05_create_competitor_offers_table.sql`
- ✅ **Competitor Scraper Tool** - Real web scraping capability
  - New file: `competitor_scraper_tool.py`
  - Scrapes ISP competitor business pages
  - Respects robots.txt and rate limiting
  - BeautifulSoup-based extraction
- ✅ **Priority Competitor Targets** - Added to web search tool
  - AT&T Business: business.att.com
  - Spectrum Business: business.spectrum.com
  - Comcast Business: business.comcast.com
  - Verizon Business: verizon.com/business
  - Cox Business: cox.com/business
  - Enhanced mock data with business offers
- ✅ **Clean Chat Tab** - NEW demo-focused UI
  - Simple user/agent conversation view
  - No debug info or routing details
  - Perfect for hackathon demo presentation
- ✅ **Intelligence Tab** - Renamed to "Debug Mode"
  - Existing detailed view preserved
  - Shows AI reasoning, tool routing, raw results
  - For development and troubleshooting

**UI Changes:**
- 💬 **New Tab 1: Chat** - Clean demo interface
- 🧠 **Tab 2: Intelligence** - Debug mode (existing functionality)
- 📐 **Tab 3: Architecture** - (unchanged)
- 🔧 **Tab 4: Troubleshooting** - (unchanged)

**Dependencies:**
- Added `requests>=2.31.0`
- Added `beautifulsoup4>=4.12.0`
- Added `lxml>=4.9.0`

**Documentation:**
- Created `docs/ALTERNATE_APPROACH_COMPARISON.md` - Detailed comparison
- Shows how to integrate competitor intelligence
- Phase 1/2/3 implementation roadmap

**Files Changed:**
- `app.py` - Added Chat tab, restructured tab layout, updated version
- `competitor_scraper_tool.py` - **NEW!** Web scraper for ISPs
- `web_search_tool.py` - Added competitor targets + business offers
- `sql/05_create_competitor_offers_table.sql` - **NEW!** DB schema
- `requirements.txt` - Added scraping dependencies
- `CHANGELOG.md` - This entry

**Demo Impact:**
- ⚡ Chat tab = clean presentation for judges
- 🧠 Intelligence tab = show off smart routing when asked
- 📊 Real competitor schema = "production ready" impression
- 🕷️ Scraper tool = extensibility beyond hackathon

---

## [v2.1.2-SPIFFIT] - 2025-11-18
### 🔧 Fixed: 'ResultData' object is not callable
**Why:** SQL execution was failing with "'ResultData' object is not callable" error

**Root Cause:**
- Databricks SDK `execute_statement()` returns different object types
- `statement.result` can be a property OR a method depending on the object
- We were blindly calling `.result()` when sometimes it's a property

**Fixed:**
- ✅ Check if `result` attribute exists first
- ✅ Check if `result` is callable (method) or property
- ✅ Handle both cases gracefully
- ✅ Fallback to using statement object directly if needed
- ✅ Added extensive logging to debug SDK object types

**Files Changed:**
- `ai_helper.py` - Smarter result access logic
- `app.py` - Updated version to v2.1.2

---

## [v2.1.1-SPIFFIT] - 2025-11-18
### 🔧 Critical Fix: SQL Execution Now Actually Triggers!
**Why:** SQL execution code wasn't being triggered - query showed but no data

**Root Cause:**
- Code only checked `if result_data is None:`
- But Genie often returns empty list `[]`, empty dict `{}`, or no `result` attribute
- So SQL execution never ran!

**Fixed:**
- ✅ Added `has_valid_result` flag to check for ANY valid data
- ✅ Only triggers SQL execution if no valid result from Genie
- ✅ Handles: `None`, empty lists, empty dicts, missing attributes
- ✅ Better error messages (warehouse stopped, permissions, etc.)
- ✅ More detailed logging for debugging

**Now you'll see:**
```
SQL Query: [shown]
⚠️ No valid results from Genie - executing SQL query ourselves
🔄 Executing SQL on warehouse: 0962fa4cf0922125
Query Results: 5 rows found
[actual data table here]
```

**Files Changed:**
- `ai_helper.py` - Fixed attachment parsing + SQL execution logic
- `app.py` - Updated version to v2.1.1

---

## [v2.1.0-SPIFFIT] - 2025-11-18
### 🎸 "Spiff It" Theme - When SPIFFs Get Tough!
**Why:** Hackathon theme song deserves proper branding! Based on Devo's "Whip It"

**Changed:**
- ⚡ Updated app title: "Spiffit - When SPIFFs Get Tough, You Must Spiff It!"
- 🎸 Added energetic subtitle: "Spiff it good! - AI-powered sales incentive intelligence"
- 💪 Updated tagline: "Powered by multi-agent AI + Databricks Genie + 100% pure hackathon energy!"
- 🎵 Rewrote sidebar header: "When a problem comes along... you must Spiff It!"
- ⚡ Updated example buttons with more energy:
  - "Beat the competition!"
  - "Next month's play"
  - "Market domination"
  - "Spiff it GOOD!"
- 🎸 Updated tab headers with theme
- ⚡ Changed page icon from 🤖 to ⚡
- 📖 Updated README with theme song info

**Performance Impact:**
- +1000% fun factor! 🎉
- +100% hackathon spirit! 🚀
- Same great AI, now with more rock n' roll! 🎸

**Files Changed:**
- `app.py` - Updated all UI text with "Spiff It" theme
- `README.md` - Added theme song reference
- `CHANGELOG.md` - This entry!

---

## [v2.0.5-DEMO] - 2025-11-18
### 🎯 SQL Execution for Actual Query Results
**Why:** Genie was returning SQL queries but NOT the actual data results

**Changed:**
- ✅ Added `_execute_sql_query()` method to execute SQL queries ourselves
- ✅ Enhanced `_format_genie_attachments()` to detect `result=None` and execute SQL
- ✅ Added `SQL_WAREHOUSE_ID` environment variable configuration
- ✅ Displays actual data tables with headers and up to 10 rows
- ✅ Logs SQL execution steps for debugging

**Performance Impact:**
- Adds ~2-5s to Genie query time
- But displays **real results** instead of just SQL query text!
- Net improvement for user experience 🎉

**Files Changed:**
- `ai_helper.py` - Added SQL execution logic
- `app.yaml` - Added SQL_WAREHOUSE_ID env var
- `env.example` - Added SQL_WAREHOUSE_ID config
- `app.py` - Updated version to v2.0.5

**Documentation:**
- Created `SQL_EXECUTION_UPDATE.md` with technical details

---

## [v2.0.4-DEMO] - 2025-11-18
### 🎯 Better Result Data Formatting + Performance Logging
**Changed:**
- ✅ Enhanced `_format_genie_attachments()` to correctly parse `result` from `query` object
- ✅ Displays up to 10 rows of data with row counts
- ✅ Handles empty/None results with helpful warnings
- ✅ Added performance feedback in UI for slow queries
- ✅ Explains SQL warehouse cold start delays
- ✅ Provides tips to improve performance

**Files Changed:**
- `ai_helper.py` - Enhanced attachment parsing for `query.result`
- `app.py` - Added performance timing and user feedback

---

## [v2.0.3-DEMO] - 2025-11-18
### 🎯 Handle GenieMessage Objects
**Why:** Genie API returns `GenieMessage` directly (not `Conversation` with `messages` array)

**Changed:**
- ✅ Added logic to detect `GenieMessage` vs `Conversation` objects
- ✅ Prioritize extracting data from `attachments` for `GenieMessage`
- ✅ Fall back to `content` with warning if no attachments
- ✅ Enhanced logging to show response type and attributes

**Files Changed:**
- `ai_helper.py` - Updated `_ask_genie()` to handle both response types

**Documentation:**
- Created `GENIE_RESPONSE_FIX.md`

---

## [v2.0.2-DEMO] - 2025-11-18
### 🎯 Critical Fix: Extract ASSISTANT Messages
**Why:** App was echoing user's question instead of showing Genie's answer

**Changed:**
- ✅ Filter for `ASSISTANT` role messages (not `USER` messages)
- ✅ Detect if content is echoed question and look for attachments
- ✅ Added extensive debug logging for message extraction

**Files Changed:**
- `ai_helper.py` - Updated `_ask_genie()` to filter messages by role

**Documentation:**
- Created `GENIE_RESPONSE_FIX.md`

---

## [v2.0.1-DEMO] - 2025-11-18
### 🔍 Response Parsing + Debug Logging
**Changed:**
- ✅ Enhanced Genie response parsing with detailed logging
- ✅ Added logging for response type, attributes, and message extraction
- ✅ Improved error messages for debugging

**Files Changed:**
- `ai_helper.py` - Added comprehensive logging

---

## [v2.0.0-DEMO] - 2025-11-18
### 🎉 Major UI Overhaul: Unified Multi-Agent Experience
**Changed:**
- ✅ Rebranded to "Spiffit Multi-Agent"
- ✅ Restructured UI into 3 main tabs:
  - **🧠 Intelligence** - Unified chat interface
  - **📐 Architecture & Tech Stack** - System overview
  - **🔧 Troubleshooting** - Debug tools
- ✅ Added clickable example questions in sidebar
- ✅ Real-time visibility: "🧠 Genies Called: Sales, Analytics, Market"
- ✅ Comprehensive architecture documentation
- ✅ Added guide on verifying Genie calls in Databricks

**Removed:**
- ❌ Separate "Chat" and "Competitor Intel" tabs (now unified in Intelligence)
- ❌ Old "AI Reasoning" tab (merged into Architecture)

**Files Changed:**
- `app.py` - Complete UI restructure
- `README.md` - Updated documentation

**Documentation:**
- Created `V2_UPGRADE_SUMMARY.md`
- Created `CHANGELOG.md`

---

## [v1.2.0] - 2025-11-18
### Added
- Multi-tool agent with web search capability
- Competitor intelligence integration
- Graceful error handling for Genie API

### Fixed
- PAT token authentication for Genie access
- OAuth M2M vs PAT token conflicts

---

## [v1.1.0] - 2025-11-18
### Added
- Troubleshooting tab with environment variable display
- Authentication method logging
- Deployment version tracking

### Fixed
- Genie API method (changed to `start_conversation`)
- Handle `Wait` objects from Genie API

---

## [v1.0.0] - 2025-11-18
### Initial Release
- Basic Streamlit app for incentive calculations
- Genie space integration
- Foundation Model API fallback
- Multi-Genie workflows
- Smart routing

---

## 📖 Version Numbering

Format: `vMAJOR.MINOR.PATCH-STAGE`

- **MAJOR**: Complete rewrite or major breaking changes
- **MINOR**: New features or significant improvements
- **PATCH**: Bug fixes and minor improvements
- **STAGE**: `DEV` (development) or `DEMO` (hackathon demo)

---

## 🔗 Related Documentation

- `V2_UPGRADE_SUMMARY.md` - v2.0.0 upgrade details
- `GENIE_RESPONSE_FIX.md` - v2.0.2/v2.0.3 Genie parsing fix
- `SQL_EXECUTION_UPDATE.md` - v2.0.5 SQL execution implementation
- `DEPLOYMENT_SCRIPTS.md` - Automated deployment guide
- `GENIE_PAT_TOKEN_SETUP.md` - PAT token authentication guide

---

**For full technical details, see individual documentation files.**
