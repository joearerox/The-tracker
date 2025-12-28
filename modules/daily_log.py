import streamlit as st
from modules import data_manager, ui

def render_log_tab(selected_date):
    # Load data for the selected date
    day_data = data_manager.get_day_data(selected_date)
    
    if selected_date != st.date_input("Today", disabled=True):
        st.warning(f"✏️ You are editing the log for: {selected_date}")

    st.header("Attribute Points")
    
    # --- 1. SLEEP ---
    default_sleep = float(day_data['Sleep_Hours']) if day_data is not None else 7.5
    default_mood = day_data['Wake_Mood'] if day_data is not None else "Normal"
    
    col1, col2 = st.columns(2)
    sleep_hrs = col1.slider("Hours slept?", 0.0, 12.0, default_sleep, 0.5)
    wake_mood = col2.select_slider("Wake Mood?", ["Groggy", "Tired", "Normal", "Energized"], value=default_mood)
    
    sleep_pts = 0
    if 7 <= sleep_hrs <= 9: sleep_pts += 30
    elif sleep_hrs < 6: sleep_pts -= 10
    if wake_mood == "Energized": sleep_pts += 20
    elif wake_mood == "Groggy": sleep_pts -= 10

    # --- 2. NUTRITION (Restored) ---
    st.subheader("🥦 Fuel & Nutrition")
    # Check if saved data has these fields, otherwise default to 0
    def_food = int(day_data['Food_Bonus']) if day_data is not None else 0
    
    # We use bitwise logic or simple checks to restore state, 
    # but for simplicity, we just ask the user to re-check if editing past data
    # (Storing checkboxes individually in CSV is complex, so we store the Total Points for Food)
    
    col_n1, col_n2, col_n3 = st.columns(3)
    fruit = col_n1.checkbox("🍎 Fruit (+10)")
    veg = col_n2.checkbox("🥕 Veg (+10)")
    protein = col_n3.checkbox("🥤 Protein (+5)")
    nutri_pts = (10 if fruit else 0) + (10 if veg else 0) + (5 if protein else 0)

    # --- 3. CUSTOM HABITS & CHORES ---
    st.subheader("✅ Habits & Chores")
    custom_df = data_manager.load_custom_activities()
    completed_customs = []
    custom_pts = 0
    
    for index, row in custom_df.iterrows():
        act_name = row['Activity']
        act_pts = row['Points']
        
        # Check if previously checked
        is_checked = False
        if day_data is not None and isinstance(day_data['Custom_Activities'], str):
            if act_name in day_data['Custom_Activities']:
                is_checked = True
                
        if st.checkbox(f"{act_name} (+{act_pts})", value=is_checked):
            custom_pts += act_pts
            completed_customs.append(act_name)

    # --- 4. CORE STATS & SIDE QUESTS ---
    st.subheader("💪 Movement")
    default_steps = int(day_data['Steps']) if day_data is not None else 0
    steps = st.number_input("Steps today:", step=100, value=default_steps)
    step_pts = int(steps / 100)
    
    # Workout
    default_workout = bool(day_data['Workout_Done']) if day_data is not None else False
    if st.session_state.get('workout_state') == 'done':
        default_workout = True 
    did_workout = st.checkbox("Base Workout (+50 pts)", value=default_workout)
    workout_pts = 50 if did_workout else 0
    
    # Side Quests (Restored)
    st.write("**Side Quests:**")
    sq_col1, sq_col2, sq_col3 = st.columns(3)
    sq_swim = sq_col1.checkbox("Swim Prep (+20)")
    sq_cali = sq_col2.checkbox("Calisthenics (+20)")
    sq_abs = sq_col3.checkbox("Abs (+20)")
    
    extra_pts = 0
    if sq_swim: extra_pts += 20
    if sq_cali: extra_pts += 20
    if sq_abs: extra_pts += 20

    # --- 5. PRODUCTIVITY & BONUSES (Restored) ---
    st.subheader("🧠 Life & Study")
    default_study = int(day_data['Study_Mins']) if day_data is not None else 0
    study_mins = st.slider("Study/Work Minutes:", 0, 240, default_study, 15)
    study_pts = study_mins 
    
    st.write("**Daily Bonuses:**")
    b_drive = st.checkbox("🚗 Driving Lesson (+20)")
    b_moto = st.checkbox("🏍️ Motorbike Lesson (+20)")
    b_errand = st.checkbox("🛒 Errand/Medical (+15)")
    b_exam = st.checkbox("🎓 Exam Success (+50)")
    
    bonus_pts = 0
    if b_drive: bonus_pts += 20
    if b_moto: bonus_pts += 20
    if b_errand: bonus_pts += 15
    if b_exam: bonus_pts += 50

    # --- TOTAL CALCULATION ---
    total_score = sleep_pts + step_pts + workout_pts + custom_pts + nutri_pts + extra_pts + study_pts + bonus_pts
    
    st.divider()
    st.metric("🏆 Current Score", total_score)
    
    if st.button("💾 SAVE PROGRESS", type="primary"):
        data = {
            "Points": total_score,
            "Steps": steps,
            "Sleep_Hours": sleep_hrs,
            "Wake_Mood": wake_mood,
            "Workout_Done": did_workout,
            "Custom_Activities": str(completed_customs),
            "Food_Bonus": nutri_pts, 
            "Study_Mins": study_mins, 
            "Custom_Notes": "" # Placeholder for future diary
        }
        data_manager.save_day(selected_date, data)
        ui.show_rainbow_border()
        
