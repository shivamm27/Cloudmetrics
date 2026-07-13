from anthropic import Anthropic

class CloudMetricsAIAnalyst:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
    
    def generate_national_insights(self, national_summary):
        """Generate insights from national health summary"""
        
        summary_text = f"""
        National Health Summary:
        - Total Cases: {national_summary['total_cases']:,}
        - Total Deaths: {national_summary['total_deaths']:,}
        - Total Recovered: {national_summary['total_recovered']:,}
        - Affected States: {national_summary['affected_states']}
        - Overall Mortality Rate: {national_summary['overall_mortality_rate']}%
        """
        
        prompt = f"""You are a public health analyst. Analyze this health data and provide:
        1. Key public health insights
        2. Risk assessment
        3. 2-3 actionable recommendations for health authorities
        
        Data:
        {summary_text}
        
        Keep response concise (150 words max), professional, and actionable."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def analyze_state_performance(self, state_df):
        """Analyze state-wise performance and generate insights"""
        
        state_data = state_df.head(10).to_string()
        
        prompt = f"""You are a health epidemiologist. Analyze this state-wise health data and provide:
        1. Which states are performing best/worst and why
        2. Key patterns you observe
        3. Specific recommendations for underperforming states
        
        Top 10 States by Cases:
        {state_data}
        
        Keep response concise (150 words max), specific, and data-driven."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def mortality_rate_analysis(self, mortality_df):
        """Analyze mortality rates and health implications"""
        
        high_mortality = mortality_df.head(5).to_string()
        
        prompt = f"""You are a public health expert. Analyze these mortality rates and explain:
        1. Why some states have higher mortality rates
        2. Healthcare infrastructure implications
        3. Urgent interventions needed
        
        States with Highest Mortality Rates:
        {high_mortality}
        
        Keep response concise (150 words max) and focus on actionable insights."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def custom_analysis(self, analysis_request, data_context):
        """Custom analysis based on user request"""
        
        prompt = f"""You are a health analytics expert. 
        
        User's question: {analysis_request}
        
        Data context: {data_context}
        
        Provide a concise, insightful analysis (150 words max) based on the data provided."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message