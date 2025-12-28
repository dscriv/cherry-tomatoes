import streamlit as st
import rottentomatoes as rt

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Toy Story")

if query:
    try:
        # In version 1.2.0, we try to fetch the movie directly
        # Use a spinner to show the phone is working
        with st.spinner(f"Looking up '{query}'..."):
            # Try as a movie first
            movie = rt.Movie(query)
            
            if movie.title:
                st.header(f"{movie.title} ({movie.year})")
                st.subheader(f"Score: {movie.tomatometer}")
                
                st.write(f"**Synopsis:** {movie.synopsis}")
                
                st.write("**Top Critic Reviews:**")
                if movie.reviews:
                    for r in movie.reviews[:8]:
                        st.info(f"\"{r}\"")
                else:
                    st.write("No reviews found.")
            else:
                st.warning("No exact match found. Try a more specific title.")

    except Exception as e:
        # If Movie fails, try TV Show
        try:
            show = rt.TVShow(query)
            st.header(f"{show.title} (Season 1)")
            st.subheader(f"Score: {show.tomatometer}")
            st.write(f"**Synopsis:** {show.synopsis}")
            
            st.write("**Top Critic Reviews:**")
            for r in show.reviews[:8]:
                st.info(f"\"{r}\"")
        except:
            st.error("Could not find a match for that title on Rotten Tomatoes.")
