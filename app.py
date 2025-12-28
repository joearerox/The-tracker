import streamlit as st
import pandas as pd
import datetime
import os
import time

# --- CONFIGURATION & SETUP ---
DATA_FILE = "life_rpg_data.csv"

# Set page to look like an app
st.set_page_config(page_title="Life RPG", page_icon="⚔️", layout="centered")

# --- DATA FUNCTIONS ---
def load_data():
    """Loads the history of your days."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create empty dataframe with columns if file doesn't exist
        columns = ["Date", "Points", "Steps", "Sleep_Hours", "Wake_Mood", 
                   "Workout_Done", "Food_Bonus", "Study_Mins", "Custom_Notes"]
        return pd.DataFrame(columns=columns)

def save_day(date, points, steps, sleep, wake_mood, workout, food, study, notes):
    """Saves today's stats to the CSV file."""
    df = load_data()
    
    # Convert date to string for storage
    date_str = date.strftime("%Y-%m-%d")
    
    # Check if entry for today already exists, if so, remove it (to overwrite)
    if date_str in df['Date'].values:
        df = df[df['Date'] != date_str]
    
    new_entry = {
        "Date": date_str,
        "Points": points,
        "Steps": steps,
        "Sleep_Hours": sleep,
        "Wake_Mood": wake_mood,
        "Workout_Done": workout,
        "Food_Bonus": food,
        "Study_Mins": study,
        "Custom_Notes": notes
    }
    
    # Add new row and save
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success(f"✅ Progress Saved! Total Points: {points}")

# --- WORKOUT DATA (From previous chat) ---
BASE_WORKOUT = [
    ("Goblet Squats", 30, "Hold weight at chest. Sit back deep."),
    ("Dumbbell Rows", 30, "Flat back. Pull weights to hips."),
    ("Push-ups", 30, "Straight line. Chest to floor."),
    ("Overhead Press", 30, "Press weights to sky. Core tight."),
    ("Reverse Lunges", 30, "Step back, knee down."),
    ("Plank", 30, "Statue mode. Squeeze glutes.")
]

# --- THE APP INTERFACE ---

# 1. HEADER & SCORE
st.title("⚔️ My Life RPG")
today = datetime.date.today()
st.caption(f"Date: {today.strftime('%A, %d %B %Y')}")

# Initialize Session State for Points if not there
if 'points' not in st.session_state:
    st.session_state['points'] = 0

# 2. TABS FOR DIFFERENT MODES
tab1, tab2, tab3 = st.tabs(["🏋️ Workout Mode", "📝 Daily Log", "📅 History & Stats"])

# --- TAB 1: THE WORKOUT COMPANION ---
with tab1:
    st.header("Daily Mission: Activation")
    st.write("12 Minutes. No furniture moving. Just 4kg weights.")
    
    if st.button("▶️ START WORKOUT TIMER"):
        st.session_state['workout_active'] = True
    
    if st.session_state.get('workout_active'):
        workout_placeholder = st.empty()
        
        # Loop through workout twice
        for set_num in range(1, 3): 
            for name, duration, desc in BASE_WORKOUT:
                # WORK PHASE
                for i in range(duration, 0, -1):
                    workout_placeholder.metric(
                        label=f"SET {set_num}: {name} (GO!)", 
                        value=f"{i} s",
                        delta="Work Hard!"
                    )
                    time.sleep(1)
                
                # REST PHASE
                for i in range(30, 0, -1):
                    workout_placeholder.metric(
                        label=f"REST (Breathe)", 
                        value=f"{i} s",
                        delta_color="off",
                        delta="Get ready for next..."
                    )
                    time.sleep(1)
        
        st.balloons()
        st.session_state['workout_complete'] = True
        st.success("MISSION COMPLETE! +50 POINTS")

# --- TAB 2: DAILY LOGGING (The Point System) ---
with tab2:
    st.header("Attribute Points")
    
    # A. SLEEP
    st.subheader("💤 Sleep & Recovery")
    sleep_hrs = st.slider("Hours slept?", 0.0, 12.0, 7.5, 0.5)
    wake_mood = st.select_slider("How did you wake up?", 
                                 options=["Groggy/Pain", "Tired but ok", "Normal", "Energized"])
    
    # Calculate Sleep Points
    sleep_pts = 0
    if 7 <= sleep_hrs <= 9: sleep_pts += 30
    elif sleep_hrs < 6: sleep_pts -= 10
    
    if wake_mood == "Energized": sleep_pts += 20
    elif wake_mood == "Groggy/Pain": sleep_pts -= 10
    
    st.info(f"Sleep XP: {sleep_pts}")

    # B. PHYSICAL
    st.subheader("💪 Physical Stats")
    steps = st.number_input("Steps today:", step=100, value=0)
    step_pts = int(steps / 100) # 1 pt per 100 steps
    
    did_workout = st.checkbox("✅ Did the Base Workout (+50 pts)")
    workout_pts = 50 if did_workout else 0
    
    extras = st.multiselect("Side Quests Completed:", 
                            ["Swimming Prep (+20)", "Calisthenics (+20)", "Core/Abs (+20)", "Stretching (+10)"])
    extra_pts = len(extras) * 20 # Simplified avg

    # C. NUTRITION
    st.subheader("🥦 Fuel")
    col1, col2 = st.columns(2)
    eaten_fruit = col1.checkbox("🍎 Ate Fruit (+10)")
    eaten_veg = col2.checkbox("🥕 Ate Veg (+10)")
    supplements = st.checkbox("🥤 Protein Shake (+5)")
    nutri_pts = (10 if eaten_fruit else 0) + (10 if eaten_veg else 0) + (5 if supplements else 0)

    # D. PRODUCTIVITY / LIFE
    st.subheader("🧠 Productivity & Life")
    study_mins = st.slider("Minutes Studied/Worked:", 0, 240, 0, 15)
    study_pts = study_mins # 1 pt per minute
    
    bonuses = st.multiselect("Daily Bonuses:", 
                             ["Driving Lesson (+20)", "Motorbike Lesson (+20)", 
                              "Medical/Errand (+15)", "Exam Success (+50)", "Morning Study (+15)"])
    
    bonus_pts = 0
    if "Driving Lesson (+20)" in bonuses: bonus_pts += 20
    if "Motorbike Lesson (+20)" in bonuses: bonus_pts += 20
    if "Medical/Errand (+15)" in bonuses: bonus_pts += 15
    if "Exam Success (+50)" in bonuses: bonus_pts += 50
    if "Morning Study (+15)" in bonuses: bonus_pts += 15

    # E. CUSTOM QUESTS
    st.subheader("✨ Custom Quests")
    custom_desc = st.text_input("New Quest Name (e.g., 'Clean Room')")
    custom_val = st.number_input("Point Value", 0, 100, 10)
    if st.button("Add Custom Quest"):
        # In a full app, we'd save this to a list, for now we just add the points manually
        st.session_state['custom_pts'] = st.session_state.get('custom_pts', 0) + custom_val
        st.toast(f"Added {custom_val} points!")
    
    custom_total = st.session_state.get('custom_pts', 0)

    # --- TOTAL SCORE ---
    total_score = sleep_pts + step_pts + workout_pts + extra_pts + nutri_pts + study_pts + bonus_pts + custom_total
    
    st.markdown(f"## 🏆 Total Daily Score: **{total_score}**")
    
    if st.button("💾 SAVE DAY TO HISTORY"):
        save_day(today, total_score, steps, sleep_hrs, wake_mood, did_workout, nutri_pts, study_mins, str(bonuses))

# --- TAB 3: HISTORY ---
with tab3:
    st.header("Your Legend")
    df = load_data()
    
    if not df.empty:
        # Sort by date
        df = df.sort_values(by="Date", ascending=False)
        
        # Metric Cards
        avg_score = df['Points'].mean()
        colA, colB = st.columns(2)
        colA.metric("Days Tracked", len(df))
        colB.metric("Average Score", f"{avg_score:.0f}")
        
        # Chart
        st.subheader("Score History")
        st.line_chart(df.set_index("Date")["Points"])
        
        # Data Table
        st.dataframe(df)
        
        # Correlation Insight (Simple)
        st.subheader("💡 Insights")
        best_day = df.loc[df['Points'].idxmax()]
        st.write(f"**Best Day:** {best_day['Date']} ({best_day['Points']} pts)")
        st.write("Keep hitting those workouts to beat your high score!")
    else:
        st.info("No data yet. Save your first day in the 'Daily Log' tab!")
