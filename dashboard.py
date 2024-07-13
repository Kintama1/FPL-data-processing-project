import streamlit as st

# Initialize state variables in session_state
if 'first' not in st.session_state:
    st.session_state.first = True

# Sidebar
st.sidebar.title('Settings')

# Form for League ID with submit button
with st.sidebar.form(key='League ID Form'):
    league_id = st.text_input('League ID')
    submit_button = st.form_submit_button(label='Submit')
if submit_button:
    st.session_state.first = False
# Main content
if st.session_state.first:
    st.title('Welcome to My Streamlit App')
else:
    st.session_state.first = False
    st.write('League ID:', league_id)
    global_info = st.sidebar.checkbox('Global Information', value=True)
    if global_info:
        st.write('Global Information')
        st.write('This is the global information')
    else:
        st.write('No global information')
    # Inputs for selecting two players from the league
        selected_player1 = st.sidebar.selectbox('Select Player 1:', options=['Player A', 'Player B', 'Player C'],placeholder="Choose player 1")  # Replace with actual player selection logic
        selected_player2 = st.sidebar.selectbox('Select Player 2:', options=['Player D', 'Player E', 'Player F'],placeholder="choose player 2")  # Replace with actual player selection logic
        
        st.write('Selected Player 1:', selected_player1)
        st.write('Selected Player 2:', selected_player2)

    # Slider for Gameweek Range
    gameweek_range = st.sidebar.slider('Gameweek Range', 1, 38, (1, 38))

    # Display Gameweek Range in sidebar
    st.write('Selected Gameweek Range:', gameweek_range)
