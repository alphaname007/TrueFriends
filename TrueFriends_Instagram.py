import json
import pandas as pd
import streamlit as st


# Streamlit App Config
st.set_page_config(
    page_title="TrueFriends",
    layout="centered",
)

# Streamlit App Title
st.markdown("<h1 style='text-align: center;'>Instagram Friends Analyzer 🙋‍♂️</h1>", unsafe_allow_html=True)


# Upload JSON file
upload_column1, upload_column2 = st.columns(2)
with upload_column1:
    uploaded_followers_file = st.file_uploader("Upload your followers.json file", type=["json"])
with upload_column2:
    uploaded_following_file = st.file_uploader("Upload your following.json file", type=["json"])


if uploaded_followers_file is not None and uploaded_following_file is not None:
    followers = json.load(uploaded_followers_file)
    following = json.load(uploaded_following_file)['relationships_following']

    # Create DataFrames
    df_followers = pd.DataFrame({'name': [x['string_list_data'][0]['value'] for x in followers]})
    df_following = pd.DataFrame({'name': [x['string_list_data'][0]['value'] for x in following]})
    
    # Combine DataFrames
    df_combined = pd.concat([df_followers, df_following])

    # Remove duplicate friend entries
    df_combined = df_combined.drop_duplicates(keep='first')

    # Sort DataFrame on name
    df_combined = df_combined.sort_values(by='name', ascending=True, na_position='last')
    df_combined = df_combined.reset_index(drop=True)

    # Add follow relationships
    df_combined['follows_me'] = df_combined['name'].isin(df_followers['name'])
    df_combined['i_follow'] = df_combined['name'].isin(df_following['name'])
    
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
    df_output = df_output[['name']]

    # Display results with images
    st.header(f"Filtered Friends List - {len(df_output)}")
    if not df_output.empty:
        st.data_editor(
            df_output,
            hide_index=False,
            use_container_width=True
        )
    else:
        st.warning("No matching friends found.")

else:
    st.warning("Upload the followers.json and following.json files wich can be downloaded from the meta profile overview")