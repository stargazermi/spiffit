# 🎨 Genie Visualization Options for Spiffit Demo

## The Challenge
When you query a Genie space via API, you get **data + SQL**, but **NOT the charts** that appear in the Databricks Genie UI. To display visualizations in the Streamlit app, you need to recreate them.

---

## Option 1: Embed Genie Space Directly (Easiest - Exact Match!)

### ✅ Pros
- **Exact same UI** as Databricks Genie
- All charts, tables, and formatting preserved
- No code needed to recreate visualizations
- Real-time updates if data changes

### ❌ Cons
- Users see Databricks UI (not your custom branding)
- Authentication required (must pass token)
- Less control over layout
- Not mobile-friendly

### Implementation
```python
import streamlit as st
import streamlit.components.v1 as components

# Embed Genie space in iframe
genie_space_id = "01f0c403c3cf184e9b7f1f6c9ee45905"
workspace_host = "https://dbc-4a93b454-f17b.cloud.databricks.com"

# Option A: Direct embed (requires auth)
genie_url = f"{workspace_host}/genie/rooms/{genie_space_id}"
components.iframe(genie_url, height=800, scrolling=True)

# Option B: Embed with pre-filled query
query = "Show me top performers"
genie_url_with_query = f"{workspace_host}/genie/rooms/{genie_space_id}?query={query}"
components.iframe(genie_url_with_query, height=800)
```

**Auth Challenge**: User needs to be logged into Databricks in their browser.

---

## Option 2: Streamlit Native Charts (Best for Demo!)

### ✅ Pros
- **Full control** over styling and branding
- Clean, simple visualizations
- Mobile-friendly
- No external dependencies
- Matches your app's theme

### ❌ Cons
- Must parse Genie response data
- Manual chart creation
- Different look from Databricks UI

### Implementation
```python
import streamlit as st
import pandas as pd
import json

def display_genie_results_with_charts(genie_response):
    """
    Parse Genie response and create Streamlit charts
    """
    # Extract data from Genie response
    data = extract_data_from_genie(genie_response)
    
    if not data:
        st.warning("No data to visualize")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Auto-detect chart type based on data
    if len(df.columns) == 2:
        # Two columns: likely category + value
        col1, col2 = df.columns
        
        # Bar chart
        st.subheader(f"{col2} by {col1}")
        st.bar_chart(df.set_index(col1)[col2])
        
        # Also show as table
        with st.expander("📊 View Data Table"):
            st.dataframe(df, use_container_width=True)
    
    elif len(df.columns) >= 3:
        # Multiple columns: show as table + optional line chart
        st.dataframe(df, use_container_width=True)
        
        # If there's a date/time column, offer line chart
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols:
            st.line_chart(df.set_index(date_cols[0]))
    
    return df

def extract_data_from_genie(response):
    """
    Extract tabular data from Genie response
    """
    # Genie returns data in TextAttachment with markdown tables
    # Or as structured query results
    
    # Method 1: Parse from text if it's a markdown table
    if hasattr(response, 'text'):
        text = response.text
        # Parse markdown table...
        
    # Method 2: If Genie returns structured data
    if hasattr(response, 'result') and hasattr(response.result, 'data'):
        return response.result.data
    
    return None
```

---

## Option 3: Plotly Interactive Charts (Most Professional!)

### ✅ Pros
- **Interactive**: Hover, zoom, pan, export
- **Beautiful**: Publication-quality charts
- Many chart types: bar, line, scatter, pie, etc.
- Can recreate Genie's exact style
- Professional look

### ❌ Cons
- Additional dependency (`plotly`)
- More code to configure
- Larger page load

### Implementation
```python
import plotly.express as px
import plotly.graph_objects as go

def create_plotly_bar_chart(df, x_col, y_col, title):
    """
    Create professional bar chart matching Genie style
    """
    fig = px.bar(
        df, 
        x=x_col, 
        y=y_col,
        title=title,
        color=y_col,
        color_continuous_scale='Blues',
        labels={y_col: y_col.replace('_', ' ').title()},
        text=y_col  # Show values on bars
    )
    
    fig.update_layout(
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        showlegend=False,
        height=500
    )
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)

def create_plotly_line_chart(df, x_col, y_cols, title):
    """
    Multi-line chart for trends
    """
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=df[x_col], 
            y=df[y_col],
            mode='lines+markers',
            name=y_col.replace('_', ' ').title()
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title='Value',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Usage example
result = genie.query("Show top performers")
df = parse_genie_to_dataframe(result)

create_plotly_bar_chart(
    df, 
    x_col='employee_name', 
    y_col='total_mrr',
    title='Top Sales Performers - September 2024'
)
```

---

## Option 4: SQL Warehouse Direct Query (Skip Genie API!)

### ✅ Pros
- **Direct data access** - no Genie API needed
- Full control over SQL
- Can optimize queries
- Faster for known queries

### ❌ Cons
- Lose natural language capability
- Must write SQL manually
- Not using Genie's intelligence

### Implementation
```python
from databricks.sdk import WorkspaceClient

def query_warehouse_directly(sql_query, warehouse_id):
    """
    Query SQL Warehouse directly, bypass Genie
    """
    w = WorkspaceClient()
    
    # Execute SQL
    result = w.statement_execution.execute_statement(
        statement=sql_query,
        warehouse_id=warehouse_id,
        wait_timeout='30s'
    )
    
    # Convert to DataFrame
    columns = [col.name for col in result.manifest.schema.columns]
    data = []
    for row in result.result.data_array:
        data.append(dict(zip(columns, row)))
    
    df = pd.DataFrame(data)
    return df

# Pre-defined queries for demo
DEMO_QUERIES = {
    "voice_activations": """
        SELECT 
            opportunity_owner,
            SUM(mrr) as total_mrr,
            CASE 
                WHEN SUM(mrr) >= 1000 THEN 1000
                WHEN SUM(mrr) >= 250 THEN 300
                ELSE 0
            END as incentive_payout
        FROM spg_demo.sales_performance
        WHERE product_type = 'VOIP'
        GROUP BY opportunity_owner
        ORDER BY total_mrr DESC
    """,
    "top_performers": """
        SELECT employee_name, total_mrr, deals_closed
        FROM spg_demo.spiff_winners
        ORDER BY total_mrr DESC
        LIMIT 10
    """
}

# Use in app
df = query_warehouse_directly(
    DEMO_QUERIES["voice_activations"],
    st.session_state.sql_warehouse_id
)

# Display with Streamlit
st.dataframe(df, use_container_width=True)
st.bar_chart(df.set_index('opportunity_owner')['total_mrr'])
```

---

## Option 5: Lakeview Dashboard Embed (Enterprise Look!)

### ✅ Pros
- **Pre-built dashboards** - no coding
- Professional enterprise look
- Databricks native
- Scheduled refresh
- Can share across org

### ❌ Cons
- Requires dashboard creation in Databricks first
- Less dynamic than code
- Auth requirements

### Implementation
```python
# First: Create dashboard in Databricks Lakeview
# Then: Embed in Streamlit

dashboard_id = "your-dashboard-id"
dashboard_url = f"{workspace_host}/sql/dashboards/{dashboard_id}"

# Embed with token auth
st.components.v1.iframe(
    f"{dashboard_url}?embed=true",
    height=800,
    scrolling=True
)
```

---

## 🎯 RECOMMENDATION FOR SPIFFIT DEMO

### For Your Use Case, I Recommend: **Hybrid Approach**

#### **Demo Tab**: Streamlit Native + Plotly (Option 2 + 3)
- Clean, branded, professional
- Mobile-friendly
- Fast loading
- Full control over presentation

#### **Tech Tab**: Embed Genie Space (Option 1)
- Show "behind the scenes"
- Let users experiment with natural language
- Demonstrates Genie capabilities

---

## 📝 Specific Implementation for Spiffit

### Voice Activations Results
```python
def display_voice_activations_results(df):
    """
    Display Voice Activations incentive results with charts
    """
    st.subheader("💰 Voice Activations Incentive Payouts")
    
    # Key metrics at top
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Payout", f"${df['incentive_payout'].sum():,.0f}")
    col2.metric("Winners", len(df[df['incentive_payout'] > 0]))
    col3.metric("Avg Payout", f"${df['incentive_payout'].mean():,.0f}")
    
    # Interactive bar chart
    fig = px.bar(
        df.sort_values('total_mrr', ascending=False).head(10),
        x='opportunity_owner',
        y='incentive_payout',
        color='total_mrr',
        color_continuous_scale='Blues',
        title='Top 10 Voice Activations Winners',
        labels={'incentive_payout': 'Incentive ($)', 'total_mrr': 'MRR ($)'},
        text='incentive_payout'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    with st.expander("📊 View Full Results"):
        st.dataframe(
            df.style.format({
                'total_mrr': '${:,.2f}',
                'incentive_payout': '${:,.2f}'
            }),
            use_container_width=True
        )
```

### Next Month's Play (Competitor Intel)
```python
def display_competitor_recommendations(recommendations):
    """
    Display multi-agent recommendations with visual comparison
    """
    st.subheader("🎯 Recommended SPIFFs for Next Month")
    
    # Parse recommendations (from multi-agent response)
    # Create comparison chart
    
    fig = go.Figure()
    
    # Our current SPIFFs
    fig.add_trace(go.Bar(
        name='Current SPIFFs',
        x=['Fiber', 'VOIP', 'Security'],
        y=[500, 300, 200],
        marker_color='lightblue'
    ))
    
    # Competitor average
    fig.add_trace(go.Bar(
        name='Competitor Avg',
        x=['Fiber', 'VOIP', 'Security'],
        y=[600, 400, 250],
        marker_color='orange'
    ))
    
    # Recommended
    fig.add_trace(go.Bar(
        name='Recommended',
        x=['Fiber', 'VOIP', 'Security'],
        y=[700, 450, 300],
        marker_color='green'
    ))
    
    fig.update_layout(
        title='SPIFF Comparison: Current vs Competitors vs Recommended',
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## 🚀 Quick Implementation Plan

### Step 1: Add Plotly to requirements
```txt
plotly>=5.17.0
```

### Step 2: Create visualization helper module
```python
# streamlit/spiffit-ai-calculator/viz_helper.py
```

### Step 3: Update Demo tab to use visualizations
- Parse Genie responses
- Create appropriate charts
- Add metrics cards
- Keep Copy/Download functionality

### Step 4: (Optional) Add Genie embed to Tech tab
- Show live Genie interface
- Let users experiment

---

## Next Steps?

Would you like me to:
1. **Implement Option 2+3** (Streamlit + Plotly charts in Demo tab)?
2. **Add Option 1** (Genie iframe embed in Tech tab)?
3. **Create visualization helper** module with pre-built chart functions?
4. **All of the above**?

Let me know and I'll build it out! 🎸

