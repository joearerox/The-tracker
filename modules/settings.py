import streamlit as st
import pandas as pd
from modules import data_manager

def render_settings_tab():
    st.header("⚙️ Manage Your Activities")
    
    # Load current custom activities
    df = data_manager.load_custom_activities()
    
    st.subheader("Your Custom Habits")
    st.dataframe(df, use_container_width=True)
    
    # Add New
    with st.form("add_activity"):
        col1, col2 = st.columns([3, 1])
        new_name = col1.text_input("New Activity Name (e.g., Walk Dog)")
        new_pts = col2.number_input("Points", min_value=1, value=10)
        submitted = st.form_submit_button("Add Activity")
        
        if submitted and new_name:
            new_row = {"Activity": new_name, "Points": new_pts}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            data_manager.save_custom_activities(df)
            st.success(f"Added {new_name}!")
            st.rerun()

    # Delete Existing
    st.divider()
    to_delete = st.selectbox("Select activity to remove:", df['Activity'].unique())
    if st.button(f"🗑️ Delete '{to_delete}'"):
        df = df[df['Activity'] != to_delete]
        data_manager.save_custom_activities(df)
        st.success("Deleted!")
        st.rerun()
      
