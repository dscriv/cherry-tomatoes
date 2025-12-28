import streamlit as st
import rottentomatoes as rt

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Toy Story")

if query:
    # Use columns to keep it clean on mobile
    try:
        with st.spinner(f"Finding '{query}'..."):
            # The library automatically searches and picks the top result
            movie = rt.Movie(query)
            
            # Display results
            st.header(f"{movie.title} ({movie.year})")
            
            # Show scores in a nice grid
            col1, col2 = st.columns(2)
            col1.metric("Tomatometer", f"{movie.tomatometer}%")
            col2.metric("Audience", f"{movie.audience_score}%")
            
            st.divider()
            st.write(f"**Synopsis:** {movie.synopsis}")
            
            st.subheader("Top Critic Reviews")
            if movie.reviews:
                for r in movie.reviews[:8]:
                    st.info(f"\"{r}\"")
            else:
                st.write("No critic reviews found for this title.")

    except Exception as e:
        # If Movie search fails, try TVShow
        try:
            show = rt.TVShow(query)
            st.header(f"{show.title} (Season 1)")
            st.metric("Tomatometer", f"{show.tomatometer}%")
            st.write(f"**Synopsis:** {show.synopsis}")
            
            st.subheader("Reviews")
            for r in show.reviews[:5]:
                st.info(f"\"{r}\"")
        except:
            st.error("Could not find an exact match. Try adding the year (e.g., 'Batman 2022').")
