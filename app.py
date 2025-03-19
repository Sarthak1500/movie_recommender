import pickle
import streamlit as st

# Function to recommend movies (without posters)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # Find the index of the selected movie
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Sort by similarity
    recommended_movie_names = []
    for i in distances[1:6]:  # Top 5 recommendations (skip the first one as it's the same movie)
        recommended_movie_names.append(movies.iloc[i[0]].title)  # Add movie name to the list
    return recommended_movie_names

# Custom CSS to style the app
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Streamlit app
st.header('🎬 Movie Recommender System')

# Load movie data and similarity matrix
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))  # Load movie list
    similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load similarity matrix
except FileNotFoundError:
    st.error("Error: Required files (movie_list.pkl or similarity.pkl) not found. Please ensure they are in the correct directory.")
    st.stop()

# Dropdown to select a movie
movie_list = movies['title'].values  # Get list of all movie titles
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)  # Get recommendations

    # Display recommended movie names
    if recommended_movie_names:  # Check if recommendations are available
        st.write("### Recommended Movies:")
        for i, name in enumerate(recommended_movie_names, 1):
            st.write(f"🎥 **{i}. {name}**")
    else:
        st.warning("No recommendations available.")