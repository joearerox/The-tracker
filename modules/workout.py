import streamlit as st
import time
from modules import data_manager, ui

# --- EXERCISE DATABASE (Images & Tips) ---
# I have updated these to more reliable sources.
# If a GIF doesn't load, the text instructions are now detailed enough to guide you.
EXERCISE_DB = {
    "Goblet Squats": {
        "img": "https://media.tenor.com/2Xy5u8s_VlAAAAAC/goblet-squat.gif",
        "targets": "Quads, Glutes, Core",
        "tips": "1. Hold weight against chest.\n2. Feet shoulder-width apart.\n3. Sit back deep (elbows inside knees).\n4. Push through heels to stand."
    },
    "Dumbbell Rows": {
        "img": "https://media.tenor.com/L7iL-mC9OQIAAAAC/dumbbell-row.gif",
        "targets": "Back (Lats), Biceps",
        "tips": "1. Hinge forward 45° with a FLAT back.\n2. Pull weights to your hip pockets.\n3. Squeeze shoulder blades together at top.\n4. Lower slowly."
    },
    "Push-ups": {
        "img": "https://media.tenor.com/gI-8qCUEko8AAAAC/pushup.gif",
        "targets": "Chest, Triceps, Core",
        "tips": "1. Straight body line from head to heels.\n2. Lower chest to floor.\n3. Elbows at 45° angle (arrow shape, not T).\n4. Push up explosively."
    },
    "Overhead Press": {
        "img": "https://media.tenor.com/fK5d_4K1v4gAAAAC/dumbbell-overhead-press.gif",
        "targets": "Shoulders, Triceps",
        "tips": "1. Stand tall, squeeze abs/glutes.\n2. Press straight up to the sky.\n3. Lock out arms at top.\n4. Lower with control."
    },
    "Reverse Lunges": {
        "img": "https://media.tenor.com/B1nK4tW_IeUAAAAC/reverse-lunge.gif",
        "targets": "Legs, Balance",
        "tips": "1. Step BACK with one foot.\n2. Lower back knee until it almost touches floor.\n3. Keep front knee over ankle.\n4. Push back to start."
    },
    "Plank": {
        "img": "https://media.tenor.com/t34k0KqfM7UAAAAC/plank-abs.gif",
        "targets": "Deep Core",
        "tips": "1. Forearms on ground.\n2. Squeeze glutes and abs HARD.\n3. Don't let hips sag.\n4. Breathe steadily."
    },
    # --- EXTRA QUESTS ---
    "Stair Sprints": {
        "img": "https://media.tenor.com/-p5y2pZtXAAAAAAC/stairs-running.gif",
        "targets": "Cardio, Legs",
        "tips": "Run up safely, walk down. Use the rail if needed."
    },
    "Superman Extensions": {
        "img": "https://media.tenor.com/V9jGkXQ_hEQAAAAC/superman-exercise.gif",
        "targets": "Lower Back",
        "tips": "Lie on belly. Lift arms and legs simultaneously. Hold 2s."
    },
    "Dumbbell Pullovers": {
        "img": "https://media.tenor.com/5w2F_y4WwAAAAAAC/dumbbell-pullover.gif",
        "targets": "Lats, Chest",
        "tips": "Lie on back. Hold weight with both hands. Lower behind head."
    },
    "Decline Push-ups": {
        "img": "https://media.tenor.com/1G6KzZ8_wAAAAAAC/decline-pushup.gif",
        "targets": "Upper Chest",
        "tips": "Feet on stairs/chair, hands on floor. Keep core tight."
    },
    "Tricep Dips": {
        "img": "https://media.tenor.com/9w2F_y4WwAAAAAAC/bench-dip.gif",
        "targets": "Triceps",
        "tips": "Hands on chair/step. Lower hips down, push up."
    },
    "Plank Shoulder Taps": {
        "img": "https://media.tenor.com/8w2F_y4WwAAAAAAC/plank-shoulder-tap.gif",
        "targets": "Core Stability",
        "tips": "High plank. Tap opposite shoulder. Don't rock hips."
    },
    "Leg Raises": {
        "img": "https://media.tenor.com/3w2F_y4WwAAAAAAC/leg-raise.gif",
        "targets": "Lower Abs",
        "tips": "Lie flat. Lift legs to 90°. Lower slowly without touching floor."
    },
    "Russian Twists": {
        "img": "https://media.tenor.com/4w2F_y4WwAAAAAAC/russian-twist.gif",
        "targets": "Obliques",
        "tips": "Sit in V-shape. Twist weight side to side."
    },
    "Mountain Climbers": {
        "img": "https://media.tenor.com/6w2F_y4WwAAAAAAC/mountain-climber.gif",
        "targets": "Cardio, Core",
        "tips": "Push-up position. Drive knees to chest quickly."
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
    "🏊 Swimmer (Pool Prep)": [
        {"name": "Stair Sprints", "time": 60},
        {"name": "Superman Extensions", "time": 45},
        {"name": "Dumbbell Pullovers", "time": 45}
    ],
    "💪 Calisthenics (Upper Body)": [
        {"name": "Decline Push-ups", "time": 45},
        {"name": "Tricep Dips", "time": 45},
        {"name": "Plank Shoulder Taps", "time": 45}
    ],
    "🔥 Core Crusader (Abs)": [
        {"name": "Leg Raises", "time": 45},
        {"name": "Russian Twists", "time": 45},
        {"name": "Mountain Climbers", "time": 45}
    ]
}

def render_workout_tab(dev_mode):
    # Initialize State
    if 'wo_active' not in st.session_state:
        st.session_state['wo_active'] = False
        st.session_state['wo_stage'] = 'prep' 
        st.session_state['wo_queue'] = []
        st.session_state['wo_index'] = 0
        st.session_state['timer_val'] = 0
        st.session_state['timer_running'] = False
        st.session_state['reps_log'] = {}

    # --- SCREEN 1: PREP ---
    if st.session_state['wo_stage'] == 'prep':
        st.header("🏋️ Choose Your Mission")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("⏱️ **Base Routine (12m)**\n\nFull Body Activation")
            if st.button("🚀 START BASE WORKOUT", use_container_width=True, type="primary"):
                st.session_state['wo_queue'] = BASE_ROUTINE + BASE_ROUTINE # 2 Sets
                st.session_state['wo_index'] = 0
                st.session_state['wo_active'] = True
                st.session_state['wo_stage'] = 'ready'
                st.session_state['reps_log'] = {}
                st.rerun()
                
        with col2:
            st.warning("⚔️ **Side Quests (5m)**\n\nAdd-on Finishers")
            quest_name = st.selectbox("Select Quest:", list(SIDE_QUESTS.keys()))
            if st.button(f"Start {quest_name}", use_container_width=True):
                st.session_state['wo_queue'] = SIDE_QUESTS[quest_name]
                st.session_state['wo_index'] = 0
                st.session_state['wo_active'] = True
                st.session_state['wo_stage'] = 'ready'
                st.rerun()

    # --- HELPER: GET DATA ---
    if st.session_state['wo_active'] and st.session_state['wo_stage'] != 'summary':
        if st.session_state['wo_index'] >= len(st.session_state['wo_queue']):
            st.session_state['wo_stage'] = 'summary'
            st.rerun()
            
        current_ex = st.session_state['wo_queue'][st.session_state['wo_index']]
        name = current_ex['name']
        duration = 1 if dev_mode else current_ex['time']
        
        # Get DB Info safely
        db_info = EXERCISE_DB.get(name, {"img": None, "targets": "General", "tips": "No tips available."})
        target_reps = data_manager.get_target_reps(name)

    # --- SCREEN 2: GET READY ---
    if st.session_state['wo_stage'] == 'ready':
        st.progress(st.session_state['wo_index'] / len(st.session_state['wo_queue']))
        st.caption(f"Up Next: {st.session_state['wo_index'] + 1} / {len(st.session_state['wo_queue'])}")
        
        st.markdown(f"### 👉 Get Ready: **{name}**")
        
        col_img, col_info = st.columns([1, 1])
        with col_img:
            if db_info.get("img"):
                st.image(db_info['img'], use_column_width=True)
            else:
                st.warning("No GIF available")
        
        with col_info:
            st.info(f"🎯 **Target Reps:** {target_reps}")
            st.markdown(f"**Muscles:** {db_info['targets']}")
            st.markdown(f"**How to:**\n{db_info['tips']}")

        st.divider()
        c1, c2 = st.columns([3, 1])
        if c1.button("🔥 START EXERCISE", type="primary", use_container_width=True):
            st.session_state['timer_val'] = duration
            st.session_state['timer_running'] = True
            st.session_state['wo_stage'] = 'active'
            st.rerun()
        if c2.button("❌ Quit"):
            st.session_state['wo_stage'] = 'prep'
            st.rerun()

    # --- SCREEN 3: ACTIVE ---
    elif st.session_state['wo_stage'] == 'active':
        st.markdown(f"### 🔥 **{name}**")
        
        # Timer
        t_col1, t_col2 = st.columns([2,1])
        with t_col1:
            st.metric(label="Time Remaining", value=f"{st.session_state['timer_val']} s")
        with t_col2:
            if db_info.get("img"): st.image(db_info['img'], width=100)
            
        st.markdown(f"**Focus:**\n{db_info['tips']}")

        # Controls
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("⏸️ Pause"):
            st.session_state['timer_running'] = False
            st.rerun()
        if c2.button("▶️ Resume"):
            st.session_state['timer_running'] = True
            st.rerun()
        if c3.button("⏭️ Done"):
            st.session_state['timer_val'] = 0
            st.rerun()
        if c4.button("❌ Quit"):
            st.session_state['wo_stage'] = 'prep'
            st.rerun()

        # Timer Logic
        if st.session_state['timer_running'] and st.session_state['timer_val'] > 0:
            time.sleep(1)
            st.session_state['timer_val'] -= 1
            st.rerun()
        
        if st.session_state['timer_val'] <= 0:
            st.session_state['wo_stage'] = 'feedback'
            st.rerun()

    # --- SCREEN 4: FEEDBACK ---
    elif st.session_state['wo_stage'] == 'feedback':
        st.markdown(f"### ✅ **{name}** Finished!")
        st.success("🔔 Time's Up!")
        
        # Determine default value safely
        default_val = 10
        if isinstance(target_reps, str) and '-' in target_reps:
             default_val = int(target_reps.split('-')[0])
        elif isinstance(target_reps, str) and target_reps.isdigit():
             default_val = int(target_reps)
        
        reps = st.number_input(f"Reps completed (Target: {target_reps})", min_value=0, value=default_val)
        
        if st.button("Confirm & Rest", type="primary"):
            data_manager.save_reps(name, reps)
            st.session_state['reps_log'][name] = st.session_state['reps_log'].get(name, 0) + reps
            
            st.session_state['timer_val'] = 30
            st.session_state['timer_running'] = True
            st.session_state['wo_stage'] = 'rest'
            st.rerun()

    # --- SCREEN 5: REST ---
    elif st.session_state['wo_stage'] == 'rest':
        st.markdown("### 💤 **REST**")
        
        # Up Next Preview
        next_idx = st.session_state['wo_index'] + 1
        if next_idx < len(st.session_state['wo_queue']):
            next_ex = st.session_state['wo_queue'][next_idx]['name']
            st.info(f"Up Next: **{next_ex}**")
        else:
            st.balloons()
            st.success("Up Next: **FINISH LINE!** 🏁")

        st.metric("Rest Timer", f"{st.session_state['timer_val']} s")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("➕ Add 30s"):
            st.session_state['timer_val'] += 30
            st.rerun()
        if c2.button("⏭️ Skip Rest"):
            st.session_state['timer_val'] = 0
            st.rerun()
        if c3.button("❌ Quit"):
            st.session_state['wo_stage'] = 'prep'
            st.rerun()

        if st.session_state['timer_running'] and st.session_state['timer_val'] > 0:
            time.sleep(1)
            st.session_state['timer_val'] -= 1
            st.rerun()
            
        if st.session_state['timer_val'] <= 0:
            st.session_state['wo_index'] += 1
            st.session_state['wo_stage'] = 'ready'
            st.rerun()

    # --- SCREEN 6: SUMMARY ---
    elif st.session_state['wo_stage'] == 'summary':
        ui.show_rainbow_border()
        st.title("🎉 WORKOUT COMPLETE!")
        
        st.write("### 📊 Session Stats")
        for ex, count in st.session_state['reps_log'].items():
            st.write(f"- **{ex}:** {count} reps")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
             if st.button("🏁 Finish & Save Day", type="primary"):
                 st.session_state['wo_active'] = False
                 st.session_state['wo_stage'] = 'prep'
                 st.rerun()
        
        with col2:
             st.markdown("**Want more?**")
             quest = st.selectbox("Pick an Extra:", list(SIDE_QUESTS.keys()), key="summary_select")
             if st.button(f"Start {quest}"):
                 st.session_state['wo_queue'] = SIDE_QUESTS[quest]
                 st.session_state['wo_index'] = 0
                 st.session_state['wo_stage'] = 'ready'
                 st.rerun()
        
