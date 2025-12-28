import pandas as pd
import os
import streamlit as st
import datetime

DATA_FILE = "life_rpg_data.csv"
CONFIG_FILE = "custom_activities.csv"

def load_history():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    columns = ["Date", "Points", "Steps", "Sleep_Hours", "Wake_Mood", 
               "Workout_Done", "Food_Bonus", "Study_Mins", "Custom_Notes", "Custom_Activities"]
    return pd.DataFrame(columns=columns)

def get_day_data(date_obj):
    """Get data for a specific date, or return empty default."""
    df = load_history()
    date_str = date_obj.strftime("%Y-%m-%d")
    row = df[df['Date'] == date_str]
    if not row.empty:
        return row.iloc[0]
    return None

def save_day(date_obj, data_dict):
    df = load_history()
    date_str = date_obj.strftime("%Y-%m-%d")
    
    # Remove existing row for this date
    if date_str in df['Date'].values:
        df = df[df['Date'] != date_str]
    
    # Add date to the data dictionary
    data_dict["Date"] = date_str
    
    # Save
    df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return True

def load_custom_activities():
    """Loads the user's custom habits (Name, Points)."""
    if os.path.exists(CONFIG_FILE):
        return pd.read_csv(CONFIG_FILE)
    return pd.DataFrame([
        {"Activity": "Wash Dishes", "Points": 10},
        {"Activity": "Walk Dogs", "Points": 20}
    ])

def save_custom_activities(df):
    df.to_csv(CONFIG_FILE, index=False)

def get_last_workout_date():
    """Finds the last date the base workout was completed."""
    df = load_history()
    if "Workout_Done" not in df.columns or df.empty:
        return "Never"
    
    # Filter for True and sort
    workouts = df[df['Workout_Done'] == True].sort_values(by="Date", ascending=False)
    if not workouts.empty:
        return workouts.iloc[0]['Date']
    return "Never"

# ... (Keep existing imports and functions: load_history, save_day, etc.) ...

REPS_FILE = "reps_history.csv"

def get_target_reps(exercise_name):
    """Calculates target reps based on average of last 3 sessions + small improvement."""
    if not os.path.exists(REPS_FILE):
        return "10-12" # Default for beginners
    
    df = pd.read_csv(REPS_FILE)
    # Filter for specific exercise
    ex_df = df[df['Exercise'] == exercise_name]
    
    if ex_df.empty:
        return "10-12"
    
    # Get last 3 entries
    last_3 = ex_df.sort_values("Timestamp", ascending=False).head(3)
    avg_reps = last_3['Reps'].mean()
    
    # target is avg + 1 (rounded)
    target = int(avg_reps + 2)
    return f"{target}"

def save_reps(exercise_name, reps_count):
    """Saves the rep count for a specific exercise."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"Timestamp": timestamp, "Exercise": exercise_name, "Reps": reps_count}
    
    if os.path.exists(REPS_FILE):
        df = pd.read_csv(REPS_FILE)
    else:
        df = pd.DataFrame(columns=["Timestamp", "Exercise", "Reps"])
        
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(REPS_FILE, index=False)

def get_session_reps(date_str):
    """Returns a dictionary of exercises done today."""
    if not os.path.exists(REPS_FILE):
        return {}
    df = pd.read_csv(REPS_FILE)
    # Filter by date (substring of timestamp)
    today_df = df[df['Timestamp'].str.contains(date_str)]
    return dict(zip(today_df.Exercise, today_df.Reps))
    
