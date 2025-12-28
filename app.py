import streamlit as st
import pandas as pd
import datetime
import os
import time

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="Life RPG", page_icon="⚔️", layout="centered")

# --- SIDEBAR: DEVELOPER MODE ---
with st.sidebar:
    st.header("⚙️ Settings")
    dev_mode = st.toggle("🛠️ Developer / Test Mode")
    
    if dev_mode:
        st.warning("⚠️ DEVELOPER MODE ACTIVE")
        st.info("Data will be saved to 'test_data.csv'. Your real history is safe.")
        DATA_FILE = "test_data.csv" 
    else:
        DATA_FILE = "life_rpg_data.csv"

# --- DATA FUNCTIONS ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        columns = ["Date", "Points", "Steps", "Sleep_Hours", "Wake_Mood", 
                   "Workout_Done", "Food_Bonus", "Study_Mins", "Custom_Notes"]
        return pd.DataFrame(columns=columns)

def save_day(date, points, steps, sleep, wake_mood, workout, food, study, notes):
    df = load_data()
    date_str = date.strftime("%Y-%m-%d")
    
    if date_str in df['Date'].values:
        df = df[df['Date'] != date_str]
    
    new_entry = {
        "Date": date_str, "Points": points, "Steps": steps, "Sleep_Hours": sleep,
        "Wake_Mood": wake_mood, "Workout_Done": workout, "Food_Bonus": food,
        "Study_Mins": study, "Custom_Notes": notes
    }
    
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    
    if dev_mode:
        st.toast(f"🧪 Test Data Saved to {DATA_FILE}!")
    else:
        st.success(f"✅ Progress Saved to Permanent Record!")

# --- WORKOUT DATA ---
BASE_WORKOUT = [
    ("Goblet Squats", 30), ("Dumbbell Rows", 30), ("Push-ups", 30),
    ("Overhead Press", 30), ("Reverse Lunges", 30), ("Plank", 30)
]

# --- APP INTERFACE ---
if dev_mode:
    st.markdown("## 🧪 SANDBOX ENVIRONMENT")

st.title("⚔️ My Life RPG")

today = datetime.date.today()
if dev_mode:
    today = st.date_input("🗓️ Test Date Simulator", datetime.date.today())

st.caption(f"Date: {today.strftime('%A, %d %B %Y')}")

if 'points' not in st.session_state: st.session_state['points'] = 0

tab1, tab2, tab3 = st.tabs(["🏋️ Workout Mode", "📝 Daily Log", "📅 History"])

# --- TAB 1: WORKOUT ---
with tab1:
    st.header("Daily Mission: Activation")
    st.write("12 Minutes. No furniture moving. Just 4kg weights.")
    
    if st.button("▶️ START WORKOUT TIMER"):
        st.session_state['workout_active'] = True
    
    if st.session_state.get('workout_active'):
        workout_placeholder = st.empty()
        for set_num in range(1, 3):
            for name, duration in BASE_WORKOUT:
                actual_duration = 1 if dev_mode else duration
                for i in range(actual_duration, 0, -1):
                    workout_placeholder.metric(label=f"SET {set_num}: {name}", value=f"{i} s")
                    time.sleep(1 if not dev_mode else 0.05)
                workout_placeholder.metric(label="Quick Rest", value="...")
                time.sleep(1 if not dev_mode else 0.05)
        st.balloons()
        st.success("MISSION COMPLETE! +50 POINTS")

# --- TAB 2: LOGGING ---
with tab2:
    st.header("Attribute Points")
    
    # A. SLEEP
    col1, col2 = st.columns(2)
    sleep_hrs = col1.slider("Hours slept?", 0.0, 12.0, 7.5, 0.5)
    wake_mood = col2.select_slider("Wake Mood?", ["Groggy", "Tired", "Normal", "Energized"])
    
    sleep_pts = 0
    if 7 <= sleep_hrs <= 9: sleep_pts += 30
    elif sleep_hrs < 6: sleep_pts -= 10
    if wake_mood == "Energized": sleep_pts += 20
    elif wake_mood == "Groggy": sleep_pts -= 10

    # B. PHYSICAL
    steps = st.number_input("Steps today:", step=100, value=0)
    step_pts = int(steps / 100)
    
    did_workout = st.checkbox("✅ Base Workout (+50 pts)")
    workout_pts = 50 if did_workout else 0
    
    extras = st.multiselect("Side Quests:", 
                            ["Swim Prep (+20)", "Calisthenics (+20)", "Abs (+20)", "Stretching (+10)"])
    extra_pts = 0
    if "Swim Prep (+20)" in extras: extra_pts += 20
    if "Calisthenics (+20)" in extras: extra_pts += 20
    if "Abs (+20)" in extras: extra_pts += 20
    if "Stretching (+10)" in extras: extra_pts += 10

    # C. NUTRITION (Restored!)
    st.subheader("🥦 Fuel")
    col_n1, col_n2, col_n3 = st.columns(3)
    fruit = col_n1.checkbox("🍎 Fruit (+10)")
    veg = col_n2.checkbox("🥕 Veg (+10)")
    protein = col_n3.checkbox("🥤 Protein (+5)")
    nutri_pts = (10 if fruit else 0) + (10 if veg else 0) + (5 if protein else 0)

    # D. PRODUCTIVITY
    st.subheader("🧠 Life & Study")
    study_mins = st.slider("Study/Work Minutes:", 0, 240, 0, 15)
    study_pts = study_mins 
    
    bonuses = st.multiselect("Bonuses:", 
                             ["Driving Lesson (+20)", "Motorbike Lesson (+20)", 
                              "Medical/Errand (+15)", "Exam Success (+50)", "Morning Study (+15)"])
    bonus_pts = 0
    if "Driving Lesson (+20)" in bonuses: bonus_pts += 20
    if "Motorbike Lesson (+20)" in bonuses: bonus_pts += 20
    if "Medical/Errand (+15)" in bonuses: bonus_pts += 15
    if "Exam Success (+50)" in bonuses: bonus_pts += 50
    if "Morning Study (+15)" in bonuses: bonus_pts += 15

    # TOTAL & SAVE
    total_score = sleep_pts + step_pts + workout_pts + extra_pts + study_pts + bonus_pts + nutri_pts
    st.markdown(f"### 🏆 Current Score: **{total_score}**")
    
    if st.button("💾 SAVE DAY TO HISTORY"):
        save_day(today, total_score, steps, sleep_hrs, wake_mood, did_workout, nutri_pts, study_mins, str(bonuses))

# --- TAB 3: HISTORY ---
with tab3:
    st.header("Your Legend")
    df = load_data()
    if not df.empty:
        df = df.sort_values(by="Date", ascending=False)
        st.dataframe(df)
        st.line_chart(df.set_index("Date")["Points"])
    else:
        st.info("No data yet.")
        
