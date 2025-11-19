# 🐛 Chart Display Debugging - v3.9.2-SPIFFIT

**Date**: 2025-11-18  
**Issue**: User reports Plotly chart not displaying incentive payout (should show both MRR and Payout like Genie UI)

## 🔍 Changes Made

### 1. Added Comprehensive Logging
**File**: `streamlit/spiffit-ai-calculator/app.py`
**Lines**: 212-229, 292-299

Added detailed logging to debug why the chart might not be displaying:

```python
logger.info(f"📊 Available columns: {list(df.columns)}")

for col in df.columns:
    col_lower = col.lower().replace('_', '').replace(' ', '')
    if 'mrr' in col_lower and not mrr_col:
        mrr_col = col
        logger.info(f"✅ Found MRR column: {col}")
    if ('incentive' in col_lower or 'payout' in col_lower) and not payout_col:
        payout_col = col
        logger.info(f"✅ Found Payout column: {col}")

if not mrr_col:
    logger.warning(f"❌ No MRR column found in: {list(df.columns)}")
if not payout_col:
    logger.warning(f"❌ No Payout column found in: {list(df.columns)}")
```

### 2. Added Warning Messages
**Lines**: 292-299

Added warnings when chart cannot be created:

```python
elif display_ui:
    # Show warning if chart can't be created
    if not mrr_col and not payout_col:
        logger.warning(f"⚠️ Cannot create chart - missing both MRR and Payout columns")
    elif not mrr_col:
        logger.warning(f"⚠️ Cannot create chart - missing MRR column")
    elif not payout_col:
        logger.warning(f"⚠️ Cannot create chart - missing Payout column")
```

## 📊 Expected Chart Behavior

The chart **should** display:
- **Two bars per person** (grouped bar chart)
- **Blue bars**: Sum_MRR (teal color `rgb(31, 119, 180)`)
- **Orange bars**: Sum_Incentive_Payout (orange color `rgb(255, 127, 14)`)
- **Value labels**: Formatted as `$XX,XXX` on top of each bar
- **X-axis**: Opportunity Owner names (tilted 45° if present)
- **Y-axis**: Amount ($)
- **Legend**: Horizontal at top

## 🔧 Diagnosis Steps

1. **Check Databricks App Logs** for the following patterns:
   ```
   📊 Available columns: ['Opportunity_Owner', 'Sum_MRR', 'Sum_Incentive_Payout']
   ✅ Found MRR column: Sum_MRR
   ✅ Found Payout column: Sum_Incentive_Payout
   🎨 Creating chart with MRR=Sum_MRR, Payout=Sum_Incentive_Payout
   ```

2. **If columns are NOT found**, check for:
   - Different column names from Genie (e.g., `Total_MRR`, `Incentive_Payout`, etc.)
   - Column name variations (spaces, underscores, etc.)
   - The actual Genie response format

3. **If columns ARE found but chart doesn't display**:
   - Check for Plotly import errors
   - Check if `st.plotly_chart()` is being called
   - Verify `display_ui=True` is being used

## 🎯 Current Behavior

**Pivot Summary Call** (line 661):
```python
has_data, df = extract_and_display_genie_data(answer, key_prefix="voice_pivot")
# display_ui defaults to True, so chart SHOULD display
```

**Detailed Data Call** (line 600):
```python
has_detailed_data, detailed_df = extract_and_display_genie_data(
    answer, key_prefix="voice_detail", display_ui=False
)
# display_ui=False, so NO chart (correct - we don't want 379 rows charted)
```

## 📝 Next Steps

1. Deploy v3.9.2
2. Run automated demo or "Beat the Competition" button
3. Check logs in Databricks App for column detection
4. Report findings to debug further if needed

## 🔗 Related Files
- `streamlit/spiffit-ai-calculator/app.py` (lines 132-325, 661)
- `docs/GENIE_STYLE_CHARTS_v3.9.0.md` (original chart implementation)

---

**Status**: 🚧 Debugging in progress  
**Hypothesis**: Genie may be returning column names that don't match our detection logic

