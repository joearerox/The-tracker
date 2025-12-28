import streamlit as st
from modules import data_manager, ui

def render_log_tab(selected_date):
    # Load data for the selected date (if it exists)
    day_data = data_manager.get_day_data(selected_date)
    
    # If editing past, show warning
    if selected_date != st.date_input("Today", disabled=True):
        st.warning(f"✏️ You are editing the log for: {selected_date}")

    st.header("Attribute Points")
    
    # --- 1. SLEEP ---
    # Default values from saved data if available, else defaults
    default_sleep = float(day_data['Sleep_Hours']) if day_data is not None else 7.5
    default_mood = day_data['Wake_Mood'] if day_data is not None else "Normal"
    
    col1, col2 = st.columns(2)
    sleep_hrs = col1.slider("Hours slept?", 0.0, 12.0, default_sleep, 0.5)
    wake_mood = col2.select_slider("Wake Mood?", ["Groggy", "Tired", "Normal", "Energized"], value=default_mood)
    
    # Calc Sleep Points
    sleep_pts = 0
    if 7 <= sleep_hrs <= 9: sleep_pts += 30
    elif sleep_hrs < 6: sleep_pts -= 10
    if wake_mood == "Energized": sleep_pts += 20
    elif wake_mood == "Groggy": sleep_pts -= 10

    # --- 2. DYNAMIC CUSTOM ACTIVITIES ---
    st.subheader("✅ Habits & Chores")
    custom_df = data_manager.load_custom_activities()
    
    # We store completed habits in a list
    completed_customs = []
    custom_pts = 0
    
    # Create a checkbox for each custom activity
    for index, row in custom_df.iterrows():
        act_name = row['Activity']
        act_pts = row['Points']
        
        # Check if it was previously checked in saved data
        is_checked = False
        if day_data is not None and isinstance(day_data['Custom_Activities'], str):
            if act_name in day_data['Custom_Activities']:
                is_checked = True
                
        if st.checkbox(f"{act_name} (+{act_pts})", value=is_checked):
            custom_pts += act_pts
            completed_customs.append(act_name)

    # --- 3. STANDARD TRACKING ---
    st.subheader("💪 Core Stats")
    default_steps = int(day_data['Steps']) if day_data is not None else 0
    steps = st.number_input("Steps today:", step=100, value=default_steps)
    step_pts = int(steps / 100)
    
    # Workout Check
    default_workout = bool(day_data['Workout_Done']) if day_data is not None else False
    if st.session_state.get('workout_state') == 'done':
        default_workout = True # Auto-check if they just finished
        
    did_workout = st.checkbox("Base Workout (+50 pts)", value=default_workout)
    workout_pts = 50 if did_workout else 0

    # --- CALC TOTAL ---
    total_score = sleep_pts + step_pts + workout_pts + custom_pts
    
    st.metric("🏆 Current Score", total_score)
    
    if st.button("💾 SAVE PROGRESS"):
        data = {
            "Points": total_score,
            "Steps": steps,
            "Sleep_Hours": sleep_hrs,
            "Wake_Mood": wake_mood,
            "Workout_Done": did_workout,
            "Custom_Activities": str(completed_customs), # Save list as string
            # You can add Food/Study back here if you want
            "Food_Bonus": 0, "Study_Mins": 0, "Custom_Notes": ""
        }
        data_manager.save_day(selected_date, data)
        ui.show_rainbow_border() # <-- NEW ANIMATION
      
