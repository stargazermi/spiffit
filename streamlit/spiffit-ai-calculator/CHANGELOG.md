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

