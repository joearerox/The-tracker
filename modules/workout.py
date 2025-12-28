import streamlit as st
import time
from modules import data_manager, ui

# --- EXERCISE DATABASE (Images & Tips) ---
# I've added placeholder image links. In a real app, you can replace these URLs.
EXERCISE_DB = {
    "Goblet Squats": {
        "img": "https://media.tenor.com/2Xy5u8s_VlAAAAAC/goblet-squat.gif",
        "targets": "Quads, Glutes, Core",
        "tips": "• Elbows inside knees.\n• Chest up.\n• Heels down."
    },
    "Dumbbell Rows": {
        "img": "https://media.tenor.com/L7iL-mC9OQIAAAAC/dumbbell-row.gif",
        "targets": "Back (Lats), Biceps",
        "tips": "• Flat back (tabletop).\n• Pull to hip pocket.\n• Squeeze shoulder blades."
    },
    "Push-ups": {
        "img": "https://media.tenor.com/gI-8qCUEko8AAAAC/pushup.gif",
        "targets": "Chest, Triceps, Core",
        "tips": "• Straight body line.\n• Elbows 45 degrees.\n• Chin to floor."
    },
    "Overhead Press": {
        "img": "https://media.tenor.com/fK5d_4K1v4gAAAAC/dumbbell-overhead-press.gif",
        "targets": "Shoulders, Triceps",
        "tips": "• Core tight (don't arch).\n• Press straight up.\n• Controlled lower."
    },
    "Reverse Lunges": {
        "img": "https://media.tenor.com/B1nK4tW_IeUAAAAC/reverse-lunge.gif",
        "targets": "Legs, Balance",
        "tips": "• Step back far.\n• Back knee almost touches floor.\n• Torso upright."
    },
    "Plank": {
        "img": "https://media.tenor.com/t34k0KqfM7UAAAAC/plank-abs.gif",
        "targets": "Deep Core",
        "tips": "• Squeeze glutes.\n• Push floor away.\n• Don't sag hips."
    }
}

# --- WORKOUT STRUCTURES ---
BASE_ROUTINE = [
    {"name": "Goblet Squats", "time": 30},
    {"name": "Dumbbell Rows", "time": 30},
    {"name": "Push-ups", "time": 30},
    {"name": "Overhead Press", "time": 30},
    {"name": "Reverse Lunges", "time": 30},
    {"name": "Plank", "time": 30}
]

SIDE_QUESTS = {
    "Swimmer": [
        {"name": "Stair Sprints", "time": 60},
        {"name": "Superman Extensions", "time": 45},
        {"name": "Dumbbell Pullovers", "time": 45}
    ],
    "Abs": [
        {"name": "Leg Raises", "time": 45},
        {"name": "Russian Twists", "time": 45},
        {"name": "Mountain Climbers", "time": 45}
    ]
}

def render_workout_tab(dev_mode):
    # Initialize Session State Variables
    if 'wo_active' not in st.session_state:
        st.session_state['wo_active'] = False # Is a workout running?
        st.session_state['wo_stage'] = 'prep' # prep, ready, active, feedback, rest, summary
        st.session_state['wo_queue'] = []     # List of exercises to do
        st.session_state['wo_index'] = 0      # Current exercise index
        st.session_state['timer_val'] = 0     # Timer countdown
        st.session_state['timer_running'] = False
        st.session_state['reps_log'] = {}     # Store reps for this session

    # --- SCREEN 1: PREP (Select Workout) ---
    if st.session_state['wo_stage'] == 'prep':
        st.header("🏋️ Choose Your Mission")
        
        last_date = data_manager.get_last_workout_date()
        st.caption(f"Last Completed: {last_date}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Base Routine")
            st.write("⏱️ 12 Minutes\n💪 Full Body Activation")
            if st.button("🚀 Start Base Workout", use_container_width=True):
                # Load Base Routine (x2 sets)
                st.session_state['wo_queue'] = BASE_ROUTINE + BASE_ROUTINE
                st.session_state['wo_index'] = 0
                st.session_state['wo_active'] = True
                st.session_state['wo_stage'] = 'ready'
                st.session_state['reps_log'] = {}
                st.rerun()
                
        with col2:
            st.subheader("Side Quests (Extras)")
            quest = st.selectbox("Select Quest:", list(SIDE_QUESTS.keys()))
            if st.button(f"⚔️ Start {quest}", use_container_width=True):
                st.session_state['wo_queue'] = SIDE_QUESTS[quest]
                st.session_state['wo_index'] = 0
                st.session_state['wo_active'] = True
                st.session_state['wo_stage'] = 'ready'
                st.rerun()

    # --- HELPER: GET CURRENT EXERCISE DATA ---
    if st.session_state['wo_active']:
        if st.session_state['wo_index'] >= len(st.session_state['wo_queue']):
            st.session_state['wo_stage'] = 'summary'
        
        if st.session_state['wo_stage'] != 'summary':
            current_ex = st.session_state['wo_queue'][st.session_state['wo_index']]
            name = current_ex['name']
            duration = 1 if dev_mode else current_ex['time'] # Fast timer for dev
            
            # Fetch DB Info
            db_info = EXERCISE_DB.get(name, {"img": "", "targets": "General", "tips": "No tips available."})
            target_reps = data_manager.get_target_reps(name)

    # --- SCREEN 2: GET READY (Instruction) ---
    if st.session_state['wo_stage'] == 'ready':
        st.progress(st.session_state['wo_index'] / len(st.session_state['wo_queue']), text=f"Progress: {st.session_state['wo_index']}/{len(st.session_state['wo_queue'])}")
        
        st.title(f"Up Next: {name}")
        
        col_img, col_info = st.columns([1, 1])
        with col_img:
            if db_info['img']:
                st.image(db_info['img'], use_column_width=True)
            else:
                st.info("[Image Placeholder]")
        
        with col_info:
            st.markdown(f"**Targets:** {db_info['targets']}")
            st.info(f"🎯 **Target Reps:** {target_reps}")
            st.write(f"**Tips:**\n{db_info['tips']}")
        
        st.divider()
        if st.button("⏱️ START TIMER", type="primary", use_container_width=True):
            st.session_state['timer_val'] = duration
            st.session_state['timer_running'] = True
            st.session_state['wo_stage'] = 'active'
            st.rerun()
            
        if st.button("🔙 Back"):
             st.session_state['wo_stage'] = 'prep'
             st.rerun()

    # --- SCREEN 3: ACTIVE (Timer) ---
    elif st.session_state['wo_stage'] == 'active':
        st.title(f"🔥 {name}")
        
        # Big Timer Display
        t_col1, t_col2 = st.columns([2,1])
        with t_col1:
            st.metric(label="Time Remaining", value=f"{st.session_state['timer_val']} s")
        with t_col2:
             if db_info['img']: st.image(db_info['img'], width=100)
        
        st.markdown(f"**Focus:** {db_info['tips']}")

        # Controls
        c1, c2, c3 = st.columns(3)
        if c1.button("⏸️ Pause"):
            st.session_state['timer_running'] = False
            st.rerun()
        if c2.button("▶️ Resume"):
            st.session_state['timer_running'] = True
            st.rerun()
        if c3.button("⏭️ Skip"):
            st.session_state['timer_val'] = 0
            st.rerun()

        # Timer Logic (The "Tick")
        if st.session_state['timer_running'] and st.session_state['timer_val'] > 0:
            time.sleep(1) # Wait 1 second
            st.session_state['timer_val'] -= 1
            st.rerun() # Refresh screen
        
        # Timer Finished
        if st.session_state['timer_val'] <= 0:
            st.session_state['wo_stage'] = 'feedback'
            st.rerun()

    # --- SCREEN 4: FEEDBACK (Reps Input) ---
    elif st.session_state['wo_stage'] == 'feedback':
        st.markdown(f"## ✅ {name} Complete!")
        st.markdown("🔔 *Beep Beep!*")
        
        reps = st.number_input(f"How many reps did you do? (Target: {target_reps})", min_value=0, value=int(target_reps.split('-')[0]) if '-' in target_reps else int(target_reps))
        
        if st.button("Confirm & Rest"):
            # Save Reps
            data_manager.save_reps(name, reps)
            st.session_state['reps_log'][name] = st.session_state['reps_log'].get(name, 0) + reps
            
            # Setup Rest
            st.session_state['timer_val'] = 30 # Default rest
            st.session_state['timer_running'] = True
            st.session_state['wo_stage'] = 'rest'
            st.rerun()

    # --- SCREEN 5: REST (Countdown) ---
    elif st.session_state['wo_stage'] == 'rest':
        st.title("💤 REST")
        
        # Peek at next exercise
        next_idx = st.session_state['wo_index'] + 1
        if next_idx < len(st.session_state['wo_queue']):
            next_ex = st.session_state['wo_queue'][next_idx]['name']
            st.info(f"Up Next: **{next_ex}**")
        else:
            st.success("Up Next: Finish Line! 🏁")

        st.metric("Rest Remaining", f"{st.session_state['timer_val']} s")
        
        col1, col2 = st.columns(2)
        if col1.button("➕ Add 30s"):
            st.session_state['timer_val'] += 30
            st.rerun()
        if col2.button("⏭️ Skip Rest"):
            st.session_state['timer_val'] = 0
            st.rerun()

        # Timer Logic
        if st.session_state['timer_running'] and st.session_state['timer_val'] > 0:
            time.sleep(1)
            st.session_state['timer_val'] -= 1
            st.rerun()
            
        if st.session_state['timer_val'] <= 0:
            st.session_state['wo_index'] += 1 # Move to next
            st.session_state['wo_stage'] = 'ready' # Back to start of loop
            st.rerun()

    # --- SCREEN 6: SUMMARY (Done) ---
    elif st.session_state['wo_stage'] == 'summary':
        ui.show_rainbow_border()
        st.title("🎉 WORKOUT COMPLETE!")
        
        # Calculate Bonuses (Logic: Did you improve?)
        improved = False
        st.write("### 📊 Session Stats")
        for ex, count in st.session_state['reps_log'].items():
            target = int(data_manager.get_target_reps(ex))
            status = "⭐ PB!" if count > target else "✅"
            st.write(f"- **{ex}:** {count} reps {status}")
            if count > target + 2:
                improved = True
        
        if improved:
            st.success("🔥 You crushed your targets! +20 Bonus Points")
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
             if st.button("🏁 Finish & Save"):
                 st.session_state['wo_active'] = False
                 st.session_state['wo_stage'] = 'prep'
                 # In a real app, you might auto-log the workout to daily_log here
                 st.rerun()
        
        with col2:
             # Dropdown for Extras
             extra = st.selectbox("Continue with Extra?", ["None"] + list(SIDE_QUESTS.keys()))
             if st.button("Go to Extra"):
                 if extra != "None":
                     st.session_state['wo_queue'] = SIDE_QUESTS[extra]
                     st.session_state['wo_index'] = 0
                     st.session_state['wo_stage'] = 'ready'
                     st.rerun()
            
