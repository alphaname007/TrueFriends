import json
import pandas as pd
import streamlit as st


# Streamlit App Config
st.set_page_config(
    page_title="TrueFriends",
    layout="centered",
)

# Streamlit App Title
st.markdown("<h1 style='text-align: center;'>Snapchat Friends Analyzer 🙋‍♂️</h1>", unsafe_allow_html=True)


# Upload JSON file
uploaded_file = st.file_uploader("Upload your friends.json file", type=["json"])

if uploaded_file is not None:
    data = json.load(uploaded_file)
    
    # Create DataFrames
    df_added_friends = pd.DataFrame(data['added_friends'])
    df_friends = pd.DataFrame(data['friends'])
    
    # Define relevant columns
    relevant_columns = ['name', 'display', 'user_id', 'type', 'bitmoji_avatar_id']
    df_added_friends = df_added_friends[relevant_columns]
    df_friends = df_friends[relevant_columns]
    
    # Combine DataFrames
    df_combined = pd.concat([df_added_friends, df_friends])

    # Remove duplicate friend entries and prefer rows with image
    df_combined = df_combined.sort_values(by='bitmoji_avatar_id', ascending=False, na_position='last')
    df_combined = df_combined.drop_duplicates(subset='name', keep='first')

    # Sort DataFrame on name
    df_combined = df_combined.sort_values(by='name', ascending=True, na_position='last')
    df_combined = df_combined.reset_index(drop=True)

    # Generate Bitmoji image URLs
    df_combined['avatar_url'] = df_combined['bitmoji_avatar_id'].apply(lambda x: f"https://cf-st.sc-cdn.net/3d/render/10226021-{x}-v1.webp" if pd.notna(x) else "")
    
    # Add follow relationships
    df_combined['follows_me'] = df_combined['name'].isin(df_added_friends['name'])
    df_combined['i_follow'] = df_combined['name'].isin(df_friends['name'])
    
    # Streamlit Switches for Filtering
    st.header("Filter Relations")
    filter_column1, filter_column2 = st.columns(2)
    with filter_column1:
        follows_me = st.toggle("Show people who follow me", value=True)
    with filter_column2:
        i_follow = st.toggle("Show people I follow", value=True)
    
    # Apply filters based on user selection
    df_output = df_combined[(df_combined['follows_me'] == follows_me) & (df_combined['i_follow'] == i_follow)]
    
    # Keep only relevant columns
    df_output = df_output[['avatar_url', 'display', 'name']]

    # Display results with images
    st.header(f"Filtered Friends List - {len(df_output)}")
    if not df_output.empty:
        st.data_editor(
            df_output,
            column_config={
                "avatar_url": st.column_config.ImageColumn("Preview Image")
            },
            hide_index=False,
            use_container_width=True
        )
    else:
        st.warning("No matching friends found.")

else:
    st.warning("Upload the friends.json file wich can be extracted with the browsers developer tools from snapchat web")