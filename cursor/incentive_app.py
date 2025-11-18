"""
AI-Powered Incentive Calculator
Databricks App for Hackathon

Deploy with: databricks apps deploy
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="AI Incentive Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF3B3F 0%, #FF8C00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF3B3F;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://www.databricks.com/sites/default/files/inline-images/db-logo-stacked-white-desktop.svg", width=200)
    st.markdown("---")
    
    st.header("🎯 Navigation")
    page = st.radio(
        "Choose a feature:",
        ["📊 Dashboard", "🤖 Ask AI", "💵 Payout Calculator", "📈 What-If Analysis", "🔍 Find Similar Deals"]
    )
    
    st.markdown("---")
    
    st.header("📁 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload new Excel file",
        type=['xlsx', 'xls'],
        help="Upload your incentive data to analyze"
    )
    
    if uploaded_file:
        st.success("✅ File uploaded!")
    
    st.markdown("---")
    
    st.caption("Powered by Databricks AI")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown('<h1 class="main-header">💰 AI Incentive Calculator</h1>', unsafe_allow_html=True)
st.markdown("**Automate your Excel workflows with AI-powered insights**")
st.markdown("---")

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

if page == "📊 Dashboard":
    st.header("📊 Performance Dashboard")
    
    # Load sample data (replace with actual Delta table queries)
    @st.cache_data
    def load_data():
        # TODO: Replace with actual Databricks SQL query
        # df = spark.sql("SELECT * FROM incentive.ae_performance").toPandas()
        df = pd.DataFrame({
            'AE': ['Sarah Johnson', 'Michael Brown', 'Emily Davis', 'David Park', 'Lisa Garcia'],
            'Region': ['Northeast', 'Northwest', 'South', 'West', 'Central'],
            'MRR_Attainment': [112.5, 98.3, 105.7, 89.2, 121.3],
            'TCV_Attainment': [108.2, 95.1, 110.5, 85.6, 115.8],
            'SPF': [98383.62, 51236.50, 87234.21, 42198.33, 102455.67]
        })
        return df
    
    df = load_data()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spf = df['SPF'].sum()
        st.metric("💵 Total SPF", f"${total_spf:,.2f}")
    
    with col2:
        avg_mrr = df['MRR_Attainment'].mean()
        st.metric("📈 Avg MRR Attainment", f"{avg_mrr:.1f}%")
    
    with col3:
        top_performer = df.loc[df['SPF'].idxmax(), 'AE']
        st.metric("🏆 Top Performer", top_performer)
    
    with col4:
        at_risk = len(df[df['MRR_Attainment'] < 100])
        st.metric("⚠️ At Risk", f"{at_risk} AEs")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("MRR Attainment by AE")
        fig = px.bar(
            df, 
            x='AE', 
            y='MRR_Attainment',
            color='MRR_Attainment',
            color_continuous_scale=['red', 'yellow', 'green'],
            labels={'MRR_Attainment': 'MRR Attainment (%)'}
        )
        fig.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Target")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("SPF by Region")
        region_spf = df.groupby('Region')['SPF'].sum().reset_index()
        fig = px.pie(
            region_spf,
            values='SPF',
            names='Region',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.subheader("📋 Detailed Performance Data")
    st.dataframe(
        df.style.background_gradient(subset=['MRR_Attainment', 'TCV_Attainment'], cmap='RdYlGn', vmin=80, vmax=120),
        use_container_width=True
    )

# ============================================================================
# PAGE: ASK AI
# ============================================================================

elif page == "🤖 Ask AI":
    st.header("🤖 Ask AI Anything")
    st.markdown("Use natural language to query your incentive data")
    
    # Sample questions
    st.subheader("💡 Try these questions:")
    sample_questions = [
        "What's the average SPF for AEs above quota?",
        "Show me the top 3 regions by total SPF",
        "Which AEs are at risk of missing their targets?",
        "Calculate total payout for the Northeast region",
        "Who has the highest TCV attainment?"
    ]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_question = st.selectbox("Sample questions:", [""] + sample_questions)
    
    with col2:
        if st.button("Use this question →"):
            question = selected_question
    
    # Custom question input
    question = st.text_input(
        "Or ask your own question:",
        placeholder="e.g., What's my team's total payout this quarter?",
        value=selected_question if selected_question else ""
    )
    
    if st.button("🔮 Ask AI", type="primary"):
        if question:
            with st.spinner("🧠 AI is thinking..."):
                # TODO: Replace with actual AI query
                # answer = ask_ai(question)
                
                # Simulate AI response
                import time
                time.sleep(2)
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"**Question:** {question}")
                st.markdown("---")
                st.markdown("""
                **AI Answer:**
                
                Based on the current data, here's what I found:
                
                - **Total SPF for AEs above quota:** $288,073.50 (3 AEs)
                - **Average SPF:** $96,024.50
                - **Breakdown:**
                  - Sarah Johnson: $98,383.62 (112.5% attainment)
                  - Emily Davis: $87,234.21 (105.7% attainment)  
                  - Lisa Garcia: $102,455.67 (121.3% attainment)
                
                **Insight:** These three AEs represent 70% of total team SPF and are significantly outperforming targets. Consider them for leadership development programs.
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visualization
                st.subheader("📊 Visual Answer")
                sample_data = pd.DataFrame({
                    'AE': ['Sarah Johnson', 'Emily Davis', 'Lisa Garcia'],
                    'SPF': [98383.62, 87234.21, 102455.67],
                    'Attainment': [112.5, 105.7, 121.3]
                })
                
                fig = px.scatter(
                    sample_data,
                    x='Attainment',
                    y='SPF',
                    size='SPF',
                    color='AE',
                    hover_data=['AE', 'SPF', 'Attainment'],
                    labels={'Attainment': 'MRR Attainment (%)', 'SPF': 'SPF Payout ($)'}
                )
                fig.add_vline(x=100, line_dash="dash", line_color="gray", annotation_text="Target")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please enter a question first!")

# ============================================================================
# PAGE: PAYOUT CALCULATOR
# ============================================================================

elif page == "💵 Payout Calculator":
    st.header("💵 Smart Payout Calculator")
    st.markdown("Calculate incentive payouts with AI-powered insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ae_name = st.selectbox(
            "Select AE:",
            ["Sarah Johnson", "Michael Brown", "Emily Davis", "David Park", "Lisa Garcia"]
        )
        
        mrr_actual = st.number_input("MRR Actual ($)", value=125000, step=1000)
        mrr_budget = st.number_input("MRR Budget ($)", value=100000, step=1000)
        
        tcv_actual = st.number_input("TCV Actual ($)", value=850000, step=10000)
        tcv_budget = st.number_input("TCV Budget ($)", value=750000, step=10000)
    
    with col2:
        ethernet_actual = st.number_input("Ethernet Actual", value=12, step=1)
        ethernet_target = st.number_input("Ethernet Target", value=10, step=1)
        
        lit_actual = st.number_input("Lit Building Actual", value=8, step=1)
        lit_target = st.number_input("Lit Building Target", value=6, step=1)
    
    if st.button("🧮 Calculate Payout", type="primary"):
        # Calculate attainments
        mrr_attainment = (mrr_actual / mrr_budget * 100) if mrr_budget > 0 else 0
        tcv_attainment = (tcv_actual / tcv_budget * 100) if tcv_budget > 0 else 0
        ethernet_attainment = (ethernet_actual / ethernet_target * 100) if ethernet_target > 0 else 0
        lit_attainment = (lit_actual / lit_target * 100) if lit_target > 0 else 0
        
        # Simplified payout calculation
        base_spf = 80000
        weighted_attainment = (
            0.4 * mrr_attainment + 
            0.3 * tcv_attainment + 
            0.2 * ethernet_attainment + 
            0.1 * lit_attainment
        ) / 100
        
        calculated_spf = base_spf * weighted_attainment
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Calculated SPF", f"${calculated_spf:,.2f}")
        
        with col2:
            st.metric("📈 Overall Attainment", f"{weighted_attainment * 100:.1f}%")
        
        with col3:
            delta = calculated_spf - base_spf
            st.metric("📊 vs Base SPF", f"${delta:,.2f}", delta=f"{delta:,.2f}")
        
        # Attainment breakdown
        st.subheader("📈 Attainment Breakdown")
        
        attainment_df = pd.DataFrame({
            'Metric': ['MRR', 'TCV', 'Ethernet', 'Lit Building'],
            'Attainment': [mrr_attainment, tcv_attainment, ethernet_attainment, lit_attainment],
            'Weight': [40, 30, 20, 10]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=attainment_df['Metric'],
            y=attainment_df['Attainment'],
            marker_color=['#FF3B3F' if x < 100 else '#28a745' for x in attainment_df['Attainment']],
            text=[f"{x:.1f}%" for x in attainment_df['Attainment']],
            textposition='outside'
        ))
        
        fig.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Target")
        fig.update_layout(
            title="Attainment by Metric",
            yaxis_title="Attainment (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.subheader("🤖 AI Insights")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        
        if weighted_attainment >= 1.1:
            st.markdown(f"""
            ✅ **Excellent Performance!** {ae_name} is significantly exceeding targets.
            
            **Key Strengths:**
            - MRR performance is {mrr_attainment:.1f}% of target
            - TCV attainment at {tcv_attainment:.1f}%
            
            **Recommendation:** This AE is a top performer. Consider for leadership roles or mentoring opportunities.
            """)
        elif weighted_attainment >= 1.0:
            st.markdown(f"""
            ✅ **On Target!** {ae_name} is meeting or exceeding expectations.
            
            **Keep Momentum:** Current trajectory projects strong Q4 performance.
            """)
        else:
            st.markdown(f"""
            ⚠️ **Below Target** - {ae_name} needs support to reach quota.
            
            **Focus Areas:**
            - {'MRR ' if mrr_attainment < 100 else ''}
            - {'TCV ' if tcv_attainment < 100 else ''}
            - {'Ethernet ' if ethernet_attainment < 100 else ''}
            
            **Action Plan:** Schedule 1-on-1 to review pipeline and provide deal coaching.
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: WHAT-IF ANALYSIS
# ============================================================================

elif page == "📈 What-If Analysis":
    st.header("📈 What-If Scenario Analysis")
    st.markdown("Model different scenarios to see impact on payouts")
    
    st.subheader("Current Performance")
    
    ae_name = st.selectbox(
        "Select AE:",
        ["Sarah Johnson", "Michael Brown", "Emily Davis", "David Park", "Lisa Garcia"]
    )
    
    # Mock current data
    current_data = {
        'MRR Actual': 125000,
        'MRR Budget': 100000,
        'TCV Actual': 850000,
        'TCV Budget': 750000,
        'Current SPF': 98383.62
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current MRR", f"${current_data['MRR Actual']:,}")
    with col2:
        st.metric("Current TCV", f"${current_data['TCV Actual']:,}")
    with col3:
        st.metric("Current SPF", f"${current_data['Current SPF']:,}")
    
    st.markdown("---")
    st.subheader("📊 Add Scenarios")
    
    scenarios = []
    num_scenarios = st.number_input("Number of scenarios to test", min_value=1, max_value=5, value=2)
    
    for i in range(num_scenarios):
        with st.expander(f"Scenario {i+1}", expanded=(i==0)):
            col1, col2 = st.columns(2)
            with col1:
                additional_mrr = st.number_input(
                    f"Additional MRR ($)",
                    key=f"mrr_{i}",
                    value=10000,
                    step=1000
                )
            with col2:
                additional_tcv = st.number_input(
                    f"Additional TCV ($)",
                    key=f"tcv_{i}",
                    value=150000,
                    step=10000
                )
            
            scenario_name = st.text_input(
                "Scenario Name",
                key=f"name_{i}",
                value=f"Close Top {i+1} Deal{'s' if i > 0 else ''}"
            )
            
            scenarios.append({
                'name': scenario_name,
                'additional_mrr': additional_mrr,
                'additional_tcv': additional_tcv
            })
    
    if st.button("🔮 Run Analysis", type="primary"):
        st.markdown("---")
        st.subheader("📊 Scenario Comparison")
        
        # Calculate scenarios
        results = []
        results.append({
            'Scenario': 'Current',
            'MRR': current_data['MRR Actual'],
            'TCV': current_data['TCV Actual'],
            'SPF': current_data['Current SPF']
        })
        
        for scenario in scenarios:
            new_mrr = current_data['MRR Actual'] + scenario['additional_mrr']
            new_tcv = current_data['TCV Actual'] + scenario['additional_tcv']
            
            # Simplified SPF calculation
            mrr_attainment = new_mrr / current_data['MRR Budget']
            tcv_attainment = new_tcv / current_data['TCV Budget']
            new_spf = 80000 * (0.4 * mrr_attainment + 0.3 * tcv_attainment + 0.3)
            
            results.append({
                'Scenario': scenario['name'],
                'MRR': new_mrr,
                'TCV': new_tcv,
                'SPF': new_spf
            })
        
        results_df = pd.DataFrame(results)
        
        # Visualization
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=results_df['Scenario'],
            y=results_df['SPF'],
            marker_color=['#FF3B3F' if i == 0 else '#28a745' for i in range(len(results_df))],
            text=[f"${x:,.0f}" for x in results_df['SPF']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="SPF Payout by Scenario",
            yaxis_title="SPF ($)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.dataframe(
            results_df.style.format({
                'MRR': '${:,.0f}',
                'TCV': '${:,.0f}',
                'SPF': '${:,.2f}'
            }),
            use_container_width=True
        )
        
        # AI Recommendation
        st.subheader("🤖 AI Recommendation")
        best_scenario = results_df.loc[results_df['SPF'].idxmax(), 'Scenario']
        best_spf = results_df.loc[results_df['SPF'].idxmax(), 'SPF']
        uplift = best_spf - current_data['Current SPF']
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **Best Scenario:** {best_scenario}
        
        - **Projected SPF:** ${best_spf:,.2f}
        - **Uplift:** ${uplift:,.2f} (+{(uplift/current_data['Current SPF']*100):.1f}%)
        
        **Action Items:**
        1. Prioritize closing deals in the {best_scenario} pipeline
        2. Focus on high-MRR opportunities for maximum impact
        3. Target deals that improve both MRR and TCV attainment
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: FIND SIMILAR DEALS
# ============================================================================

elif page == "🔍 Find Similar Deals":
    st.header("🔍 Find Similar Opportunities")
    st.markdown("Use AI to find deals similar to your best wins")
    
    st.subheader("Search for Similar Deals")
    
    search_method = st.radio(
        "Search by:",
        ["Opportunity Description", "Winning Deal ID", "Product/Service Type"]
    )
    
    if search_method == "Opportunity Description":
        description = st.text_area(
            "Describe the type of deal you're looking for:",
            placeholder="e.g., Enterprise cloud migration with AI/ML components, multi-year contract"
        )
    elif search_method == "Winning Deal ID":
        deal_id = st.text_input(
            "Enter a successful deal ID:",
            placeholder="e.g., OPP-12345"
        )
    else:
        product_type = st.selectbox(
            "Select product/service:",
            ["Enterprise Ethernet", "Voice Services", "Cloud Solutions", "AI/ML Tools", "Data Analytics"]
        )
    
    if st.button("🔍 Search", type="primary"):
        with st.spinner("🔎 Searching for similar deals..."):
            import time
            time.sleep(2)
            
            st.markdown("---")
            st.subheader("📋 Similar Opportunities Found")
            
            # Mock results
            similar_deals = pd.DataFrame({
                'Opportunity': [
                    'Cloud Analytics Platform - Acme Corp',
                    'AI-Powered CRM Integration - TechCo',
                    'Enterprise Data Lake - MegaCorp'
                ],
                'Similarity': [95, 87, 82],
                'MRR': [45000, 38000, 52000],
                'TCV': [540000, 456000, 624000],
                'Close_Date': ['2024-09-15', '2024-08-22', '2024-07-10'],
                'AE': ['Sarah Johnson', 'Emily Davis', 'Lisa Garcia']
            })
            
            st.dataframe(
                similar_deals.style.background_gradient(subset=['Similarity'], cmap='Greens', vmin=70, vmax=100),
                use_container_width=True
            )
            
            # AI Insights
            st.subheader("🤖 Pattern Analysis")
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("""
            **Common Success Factors:**
            
            1. **Deal Structure:** Multi-year contracts (avg 3 years) with annual true-ups
            2. **Decision Makers:** CTO and CFO involvement critical
            3. **Timeline:** Average sales cycle: 4.5 months
            4. **Price Point:** Sweet spot at $40-50k MRR
            5. **Competitive:** Typically beat competitors on integration capabilities
            
            **Recommended Next Steps:**
            - Review these deals' discovery questions
            - Use similar ROI calculators
            - Leverage technical win stories from these AEs
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Visualization
            st.subheader("📊 Deal Comparison")
            fig = px.scatter(
                similar_deals,
                x='MRR',
                y='TCV',
                size='Similarity',
                color='AE',
                hover_data=['Opportunity'],
                labels={'MRR': 'Monthly Recurring Revenue ($)', 'TCV': 'Total Contract Value ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Built with ❤️ using Databricks AI | Hackathon 2024</p>
    <p>Powered by: Genie • AI Functions • LangChain • Vector Search</p>
</div>
""", unsafe_allow_html=True)

