import streamlit as st
import time
from modules import data_manager

# Added descriptions back (Name, Time, Instructions)
BASE_WORKOUT = [
    ("Goblet Squats", 30, "Hold weight at chest. Sit back deep. Knees out."),
    ("Dumbbell Rows", 30, "Flat back. Pull weights to hip pockets. Squeeze back."),
    ("Push-ups", 30, "Straight line from head to heels. Chest to floor."),
    ("Overhead Press", 30, "Core tight. Press straight up. Don't arch back."),
    ("Reverse Lunges", 30, "Step back far. Lower back knee to ground. Torso upright."),
    ("Plank", 30, "Elbows under shoulders. Squeeze glutes and abs hard.")
]

def render_workout_tab(dev_mode):
    last_date = data_manager.get_last_workout_date()
    st.info(f"📅 **Last Completed:** {last_date}")
    
    st.write("### ⚔️ The Base Routine (12 Mins)")
    
    # State management
    if 'workout_state' not in st.session_state:
        st.session_state['workout_state'] = "ready" 

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
        info_box = st.empty() # Placeholder for Form Check text
        
        st.warning("⚠️ Workout in progress... Do not close tab.")
        
        # Double loop for 2 sets
        for set_num in range(1, 3):
            for name, duration, desc in BASE_WORKOUT:
                actual_duration = 1 if dev_mode else duration
                
                # Show Form Guide
                info_box.info(f"**FORM CHECK:** {desc}")
                
                # Countdown
                for i in range(actual_duration, 0, -1):
                    placeholder.metric(label=f"SET {set_num}: {name}", value=f"{i} s")
                    time.sleep(1 if not dev_mode else 0.05)
                
                # Rest
                info_box.empty() # Clear instructions during rest
                placeholder.metric(label="Rest / Transition", value="...")
                time.sleep(1 if not dev_mode else 0.05)

        placeholder.empty()
        st.session_state['workout_state'] = "done"
        st.rerun()
        
