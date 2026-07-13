import sqlite3
import requests

# Create SQLite database connection
conn = sqlite3.connect('cloudmetrics.db')
cursor = conn.cursor()

# Create table for state summary
cursor.execute('''
    CREATE TABLE IF NOT EXISTS state_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT UNIQUE NOT NULL,
        total_cases INTEGER,
        total_deaths INTEGER,
        total_recovered INTEGER
    )
''')

print("Attempting to fetch real data from COVID API...")

try:
    # Try to fetch real data from public COVID-19 India API
    url = "https://raw.githubusercontent.com/covid19india/api/master/data.json"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    statewise = data.get('statewise', [])
    
    # Insert real data into database
    for state_data in statewise:
        state = state_data.get('state', 'Unknown')
        confirmed = int(state_data.get('confirmed', 0))
        deaths = int(state_data.get('deaths', 0))
        recovered = int(state_data.get('recovered', 0))
        
        cursor.execute('''
            INSERT OR REPLACE INTO state_summary 
            (state, total_cases, total_deaths, total_recovered)
            VALUES (?, ?, ?, ?)
        ''', (state, confirmed, deaths, recovered))
    
    conn.commit()
    print(f"✓ Successfully loaded {len(statewise)} states from real API")
    
except Exception as e:
    print(f"Could not fetch real data: {e}")
    print("Creating sample data instead...\n")
    
    # If API fails, create sample data
    sample_states = [
        ('Maharashtra', 80000, 1800, 75000),
        ('Delhi', 90000, 2000, 85000),
        ('Kerala', 100000, 2200, 95000),
        ('Tamil Nadu', 110000, 2400, 105000),
        ('Karnataka', 120000, 2600, 115000),
        ('Rajasthan', 130000, 2800, 125000),
        ('Uttar Pradesh', 140000, 3000, 135000),
        ('Gujarat', 150000, 3200, 145000),
        ('West Bengal', 160000, 3400, 155000),
        ('Telangana', 170000, 3600, 165000)
    ]
    
    for state, cases, deaths, recovered in sample_states:
        cursor.execute('''
            INSERT OR REPLACE INTO state_summary 
            (state, total_cases, total_deaths, total_recovered)
            VALUES (?, ?, ?, ?)
        ''', (state, cases, deaths, recovered))
    
    conn.commit()
    print(f"✓ Created sample data for {len(sample_states)} states")

conn.close()
print("✓ Database created: cloudmetrics.db")