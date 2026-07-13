import sqlite3
import pandas as pd

class CloudMetricsAnalytics:
    def __init__(self, db_path='cloudmetrics.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    # Query 1: Top 10 states by case count
    def get_top_states_by_cases(self, limit=10):
        conn = self.get_connection()
        query = '''
            SELECT state, total_cases, total_deaths, total_recovered
            FROM state_summary
            WHERE state != 'Unknown' AND state != 'Cases being assigned to states'
            ORDER BY total_cases DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        return df
    
    # Query 2: Mortality rate by state
    def get_mortality_rate_by_state(self):
        conn = self.get_connection()
        query = '''
            SELECT 
                state,
                total_cases,
                total_deaths,
                ROUND((CAST(total_deaths AS FLOAT) / CAST(total_cases AS FLOAT)) * 100, 2) as mortality_rate
            FROM state_summary
            WHERE state != 'Unknown' 
            AND state != 'Cases being assigned to states'
            AND total_cases > 0
            ORDER BY mortality_rate DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    # Query 3: Recovery rate by state
    def get_recovery_rate_by_state(self):
        conn = self.get_connection()
        query = '''
            SELECT 
                state,
                total_cases,
                total_recovered,
                ROUND((CAST(total_recovered AS FLOAT) / CAST(total_cases AS FLOAT)) * 100, 2) as recovery_rate
            FROM state_summary
            WHERE state != 'Unknown' 
            AND state != 'Cases being assigned to states'
            AND total_cases > 0
            ORDER BY recovery_rate DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    # Query 4: National summary statistics
    def get_national_summary(self):
        conn = self.get_connection()
        query = '''
            SELECT 
                'India' as country,
                SUM(total_cases) as total_cases,
                SUM(total_deaths) as total_deaths,
                SUM(total_recovered) as total_recovered,
                COUNT(DISTINCT state) as affected_states,
                ROUND((CAST(SUM(total_deaths) AS FLOAT) / CAST(SUM(total_cases) AS FLOAT)) * 100, 2) as overall_mortality_rate
            FROM state_summary
            WHERE state != 'Unknown' AND state != 'Cases being assigned to states'
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.iloc[0] if len(df) > 0 else None
    
    # Query 5: High-risk states
    def get_high_risk_states(self):
        conn = self.get_connection()
        query = '''
            SELECT 
                state,
                total_cases,
                total_deaths,
                ROUND((CAST(total_deaths AS FLOAT) / CAST(total_cases AS FLOAT)) * 100, 2) as mortality_rate,
                CASE 
                    WHEN total_cases > 100000 AND (CAST(total_deaths AS FLOAT) / CAST(total_cases AS FLOAT)) > 0.02 THEN 'Critical'
                    WHEN total_cases > 50000 AND (CAST(total_deaths AS FLOAT) / CAST(total_cases AS FLOAT)) > 0.015 THEN 'High'
                    ELSE 'Moderate'
                END as risk_level
            FROM state_summary
            WHERE state != 'Unknown' AND state != 'Cases being assigned to states' AND total_cases > 0
            ORDER BY total_cases DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    # Query 6: Compare states
    def compare_states(self, state_list):
        conn = self.get_connection()
        placeholders = ','.join(['?' for _ in state_list])
        query = f'''
            SELECT 
                state,
                total_cases,
                total_deaths,
                total_recovered,
                ROUND((CAST(total_deaths AS FLOAT) / CAST(total_cases AS FLOAT)) * 100, 2) as mortality_rate,
                ROUND((CAST(total_recovered AS FLOAT) / CAST(total_cases AS FLOAT)) * 100, 2) as recovery_rate
            FROM state_summary
            WHERE state IN ({placeholders})
            ORDER BY total_cases DESC
        '''
        df = pd.read_sql_query(query, conn, params=state_list)
        conn.close()
        return df