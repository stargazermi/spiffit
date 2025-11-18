# Direct CLI Commands to Test Genie Spaces

## Quick Commands

### 1. Check OLD Genie Space (WORKING)
```powershell
databricks api get /api/2.0/genie/spaces/01f0c4ae99271d64835d414b8d43ddfb --profile dlk-hackathon
```

**Expected Result:** ✅ Success
```json
{
  "space_id": "01f0c4ae99271d64835d414b8d43ddfb",
  "title": "Hackathon- SPIFF Analyzer",
  "warehouse_id": "0962fa4cf0922125"
}
```

---

### 2. Check NEW Genie Space (BROKEN)
```powershell
databricks api get /api/2.0/genie/spaces/0110c4ae99271d64835d414b8d43ddfb --profile dlk-hackathon
```

**Expected Result:** ❌ Permission Denied
```
Error: You need "Can View" permission to perform this action
```

---

### 3. List All Accessible Genie Spaces
```powershell
databricks api get /api/2.0/genie/spaces --profile dlk-hackathon
```

**Expected Result:** 
- OLD space `01f0c4ae...` WILL be in the list
- NEW space `0110c4ae...` will NOT be in the list (proving no permissions)

---

### 4. Check Who You're Authenticated As
```powershell
databricks auth describe --profile dlk-hackathon
```

**Expected Result:**
```
Host: https://dbc-4a93b454-f17b.cloud.databricks.com
User: spg1461@ftr.com
Authenticated with: databricks-cli
```

---

### 5. Start Conversation with OLD Space (Test Query)
```powershell
databricks api post /api/2.0/genie/spaces/01f0c4ae99271d64835d414b8d43ddfb/start-conversation --profile dlk-hackathon --json '{"content": "Show me voice opportunities"}'
```

**Expected Result:** ✅ Returns conversation with query results

---

### 6. Start Conversation with NEW Space (Will Fail)
```powershell
databricks api post /api/2.0/genie/spaces/0110c4ae99271d64835d414b8d43ddfb/start-conversation --profile dlk-hackathon --json '{"content": "Show me voice opportunities"}'
```

**Expected Result:** ❌ Permission Denied

---

## The Problem

**Space ID Comparison:**
- OLD (working): `01f0c4ae99271d64835d414b8d43ddfb` ← Notice: `01f0...`
- NEW (broken):  `0110c4ae99271d64835d414b8d43ddfb` ← Notice: `0110...`

**Key Difference:** The IDs are different! It's not just a permission issue on the same space.

**The NEW space either:**
1. Doesn't exist
2. Has no permissions for user `spg1461@ftr.com`
3. Was created in a different workspace
4. Has incorrect sharing settings

---

## How to Fix

### Option 1: Use the OLD Working Space
The OLD space (`01f0c4ae...`) works perfectly. We've already updated the app to use it.

### Option 2: Fix Permissions on NEW Space (if it exists)
1. Navigate to: https://dbc-4a93b454-f17b.cloud.databricks.com/genie/rooms/0110c4ae99271d64835d414b8d43ddfb
2. If it loads → Click "Share" → Add `spg1461@ftr.com` with "Can Manage"
3. If it doesn't load → Space doesn't exist or is in different workspace

---

## Testing Script

Run the automated test:
```powershell
cd C:\code\hackathon\spiffit\streamlit\spiffit-ai-calculator
pwsh test-genie-issue.ps1
```

This will:
- Test OLD space (should work) ✅
- Test NEW space (should fail) ❌
- List all accessible spaces
- Show which spaces you can see
- Provide diagnosis and fix instructions

