import streamlit as st
import time
from modules import data_manager

BASE_WORKOUT = [
    ("Goblet Squats", 30), ("Dumbbell Rows", 30), ("Push-ups", 30),
    ("Overhead Press", 30), ("Reverse Lunges", 30), ("Plank", 30)
]

def render_workout_tab(dev_mode):
    last_date = data_manager.get_last_workout_date()
    
    st.info(f"📅 **Last Completed:** {last_date}")
    
    st.write("### ⚔️ The Base Routine (12 Mins)")
    
    # State management for the workout
    if 'workout_state' not in st.session_state:
        st.session_state['workout_state'] = "ready" # ready, active, done

    if st.session_state['workout_state'] == "done":
        st.success("✅ You have completed the workout for this session!")
        if st.button("Reset / Do it Again"):
            st.session_state['workout_state'] = "ready"
            st.rerun()

    elif st.session_state['workout_state'] == "ready":
        if st.button("▶️ START WORKOUT", type="primary"):
            st.session_state['workout_state'] = "active"
            st.rerun()

    elif st.session_state['workout_state'] == "active":
        placeholder = st.empty()
        st.warning("⚠️ Workout in progress... Do not close tab.")
        
        # Double loop for 2 sets
        for set_num in range(1, 3):
            for name, duration in BASE_WORKOUT:
                actual_duration = 1 if dev_mode else duration
                
                # Countdown
                for i in range(actual_duration, 0, -1):
                    placeholder.metric(label=f"SET {set_num}: {name}", value=f"{i} s")
                    time.sleep(1 if not dev_mode else 0.05)
                
                # Rest
                placeholder.metric(label="Rest / Transition", value="...")
                time.sleep(1 if not dev_mode else 0.05)

        placeholder.empty()
        st.session_state['workout_state'] = "done"
        st.rerun()
      
