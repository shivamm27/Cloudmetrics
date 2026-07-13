import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from sql_queries import CloudMetricsAnalytics
from ai_insights import CloudMetricsAIAnalyst

# Page configuration
st.set_page_config(
    page_title="CloudMetrics - Health Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analyst' not in st.session_state:
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    if api_key:
        st.session_state.analyst = CloudMetricsAIAnalyst(api_key)
    else:
        st.session_state.analyst = None

# Initialize database
db = CloudMetricsAnalytics('cloudmetrics.db')

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.title("📊 CloudMetrics")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "📈 Analysis", "🤖 AI Insights", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.info("**Data Source:** Real-time health data")

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================
if page == "📊 Dashboard":
    st.header("📊 CloudMetrics Dashboard")
    
    # National Summary
    st.subheader("📍 National Overview")
    national = db.get_national_summary()
    
    if national is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cases", f"{national['total_cases']:,}")
        with col2:
            st.metric("Total Deaths", f"{national['total_deaths']:,}")
        with col3:
            st.metric("Total Recovered", f"{national['total_recovered']:,}")
        with col4:
            st.metric("Mortality Rate", f"{national['overall_mortality_rate']:.2f}%")
    
    st.markdown("---")
    
    # Top 10 States by Cases
    st.subheader("🏥 Top 10 States by Case Count")
    top_states = db.get_top_states_by_cases(10)
    
    if not top_states.empty:
        fig = px.bar(
            top_states,
            x='state',
            y='total_cases',
            title="Cases by State",
            labels={'total_cases': 'Total Cases', 'state': 'State'},
            color='total_cases',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(top_states, use_container_width=True)
    
    st.markdown("---")
    
    # Mortality vs Recovery Rates
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💀 Mortality Rates by State")
        mortality_df = db.get_mortality_rate_by_state()
        
        if not mortality_df.empty:
            fig = px.bar(
                mortality_df.head(10),
                x='state',
                y='mortality_rate',
                title="Top 10 States by Mortality Rate",
                labels={'mortality_rate': 'Mortality Rate (%)', 'state': 'State'},
                color='mortality_rate',
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("✅ Recovery Rates by State")
        recovery_df = db.get_recovery_rate_by_state()
        
        if not recovery_df.empty:
            fig = px.bar(
                recovery_df.head(10),
                x='state',
                y='recovery_rate',
                title="Top 10 States by Recovery Rate",
                labels={'recovery_rate': 'Recovery Rate (%)', 'state': 'State'},
                color='recovery_rate',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: DETAILED ANALYSIS
# ============================================================================
elif page == "📈 Analysis":
    st.header("📈 Detailed State Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Compare States", "Mortality Analysis", "Risk Assessment", "Recovery Trends"]
    )
    
    if analysis_type == "Compare States":
        st.subheader("Compare Multiple States")
        
        all_states_df = db.get_top_states_by_cases(100)
        all_states = all_states_df['state'].unique().tolist()
        
        selected_states = st.multiselect(
            "Select states to compare",
            all_states,
            default=all_states[:5]
        )
        
        if selected_states:
            comparison = db.compare_states(selected_states)
            
            st.dataframe(comparison, use_container_width=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=comparison['state'],
                y=comparison['total_cases'],
                name='Total Cases',
                marker_color='lightblue'
            ))
            
            fig.add_trace(go.Bar(
                x=comparison['state'],
                y=comparison['total_deaths'],
                name='Deaths',
                marker_color='red'
            ))
            
            fig.update_layout(
                barmode='group',
                title="State Comparison: Cases and Deaths",
                xaxis_title="State",
                yaxis_title="Count"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Mortality Analysis":
        st.subheader("Mortality Rate Analysis")
        mortality_df = db.get_mortality_rate_by_state()
        
        fig = px.scatter(
            mortality_df.head(20),
            x='total_cases',
            y='mortality_rate',
            hover_data='state',
            title="Mortality Rate vs Total Cases",
            labels={'total_cases': 'Total Cases', 'mortality_rate': 'Mortality Rate (%)'},
            size='total_cases',
            color='mortality_rate',
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(mortality_df.head(15), use_container_width=True)
    
    elif analysis_type == "Risk Assessment":
        st.subheader("High-Risk State Assessment")
        risk_df = db.get_high_risk_states()
        
        st.dataframe(risk_df.head(15), use_container_width=True)
        
        risk_counts = risk_df['risk_level'].value_counts()
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="State Risk Distribution",
            color_discrete_map={'Critical': 'red', 'High': 'orange', 'Moderate': 'yellow'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Recovery Trends":
        st.subheader("Recovery Rate Trends")
        recovery_df = db.get_recovery_rate_by_state()
        
        fig = px.scatter(
            recovery_df.head(20),
            x='total_cases',
            y='recovery_rate',
            hover_data='state',
            title="Recovery Rate vs Total Cases",
            labels={'total_cases': 'Total Cases', 'recovery_rate': 'Recovery Rate (%)'},
            size='total_cases',
            color='recovery_rate',
            color_continuous_scale='Greens'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(recovery_df.head(15), use_container_width=True)

# ============================================================================
# PAGE 3: AI INSIGHTS
# ============================================================================
elif page == "🤖 AI Insights":
    st.header("🤖 AI-Powered Health Insights")
    
    if st.session_state.analyst is None:
        st.error("⚠️ Claude API key not configured.")
        st.info("Set environment variable: `export ANTHROPIC_API_KEY='your-key'`")
    else:
        insight_type = st.selectbox(
            "Select Insight Type",
            ["National Overview", "State Performance", "Mortality Analysis", "Custom Query"]
        )
        
        analyst = st.session_state.analyst
        
        if insight_type == "National Overview":
            st.subheader("📊 National Health Insights")
            
            national = db.get_national_summary()
            
            if national is not None:
                with st.spinner("🤖 Claude is analyzing..."):
                    insights = analyst.generate_national_insights(national)
                
                st.markdown(f"""
                <div style="background-color:#e8f4f8; padding:20px; border-radius:10px; border-left:5px solid #0066cc;">
                {insights}
                </div>
                """, unsafe_allow_html=True)
        
        elif insight_type == "State Performance":
            st.subheader("🏥 State-wise Performance Analysis")
            
            top_states = db.get_top_states_by_cases(10)
            
            with st.spinner("🤖 Claude is analyzing..."):
                insights = analyst.analyze_state_performance(top_states)
            
            st.markdown(f"""
            <div style="background-color:#e8f4f8; padding:20px; border-radius:10px; border-left:5px solid #0066cc;">
            {insights}
            </div>
            """, unsafe_allow_html=True)
        
        elif insight_type == "Mortality Analysis":
            st.subheader("💀 Mortality Rate Deep Dive")
            
            mortality_df = db.get_mortality_rate_by_state()
            
            with st.spinner("🤖 Claude is analyzing..."):
                insights = analyst.mortality_rate_analysis(mortality_df)
            
            st.markdown(f"""
            <div style="background-color:#e8f4f8; padding:20px; border-radius:10px; border-left:5px solid #0066cc;">
            {insights}
            </div>
            """, unsafe_allow_html=True)
        
        elif insight_type == "Custom Query":
            st.subheader("🔍 Ask Claude About Health Data")
            
            user_question = st.text_area(
                "What would you like to know?",
                height=100
            )
            
            if st.button("🤖 Get Insights", key="custom_query"):
                if user_question:
                    context = f"""
                    National Summary: {db.get_national_summary()}
                    Top States: {db.get_top_states_by_cases(5).to_string()}
                    """
                    
                    with st.spinner("🤖 Claude is thinking..."):
                        insights = analyst.custom_analysis(user_question, context)
                    
                    st.markdown(f"""
                    <div style="background-color:#e8f4f8; padding:20px; border-radius:10px; border-left:5px solid #0066cc;">
                    {insights}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a question!")

# ============================================================================
# PAGE 4: SETTINGS
# ============================================================================
elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    st.info("""
    To enable AI insights:
    1. Get Claude API key from https://console.anthropic.com
    2. Set: `export ANTHROPIC_API_KEY='your-key'`
    3. Restart the app
    """)
    
    st.subheader("Database Info")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Database", "cloudmetrics.db")
    
    with col2:
        national = db.get_national_summary()
        if national is not None:
            st.metric("States", int(national['affected_states']))
    
    st.subheader("About")
    st.markdown("""
    **CloudMetrics - Health Analytics Platform**
    
    Full-stack data analytics with:
    - SQLite database
    - Complex SQL queries
    - Generative AI insights (Claude)
    - Interactive Plotly visualizations
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#666; font-size:0.8rem;">
CloudMetrics | Built with Streamlit & Claude AI | 2026
</div>
""", unsafe_allow_html=True)