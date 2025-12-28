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
