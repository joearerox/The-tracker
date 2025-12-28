import streamlit as st
import datetime
from modules import workout, daily_log, settings, data_manager, ui

# --- PAGE CONFIG ---
st.set_page_config(page_title="Life RPG", page_icon="⚔️", layout="centered")
ui.apply_styling()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧭 Navigation")
    
    # Date Picker (Defaults to Today)
    # This solves your "Auto reset" problem. Today is always Today.
    selected_date = st.date_input("📅 Date Control", datetime.date.today())
    
    dev_mode = st.toggle("🛠️ Developer Mode")

# --- MAIN TABS ---
# We now include a specific "Settings" tab for your customization
tab1, tab2, tab3, tab4 = st.tabs(["📝 Daily Log", "🏋️ Workout", "📊 History", "⚙️ Settings"])

with tab1:
    daily_log.render_log_tab(selected_date)

with tab2:
    workout.render_workout_tab(dev_mode)

with tab3:
    st.header("📜 Your Legend")
    df = data_manager.load_history()
    if not df.empty:
        st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    else:
        st.info("No history yet. Go log your first day!")

with tab4:
    settings.render_settings_tab()
    
