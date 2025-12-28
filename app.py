import streamlit as st
import rottentomatoes as rt

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Toy Story")

if query:
    try:
        with st.spinner(f"Searching RT for '{query}'..."):
            # We try to get the score directly first - this is the most reliable method
            score = rt.tomatometer(query)
            audience = rt.audience_score(query)
            
            if score:
                # If we found a score, we can pull the rest of the info
                movie = rt.Movie(query)
                st.header(f"{movie.title} ({movie.year})")
                
                col1, col2 = st.columns(2)
                col1.metric("Tomatometer", f"{score}%")
                col2.metric("Audience", f"{audience}%")
                
                st.divider()
                st.write(f"**Synopsis:** {movie.synopsis}")
                
                st.subheader("Top Critic Reviews")
                if movie.reviews:
                    for r in movie.reviews[:8]:
                        st.info(f"\"{r}\"")
                else:
                    st.write("No critic reviews found.")
            else:
                # If movie fails, try searching as a TV Show
                show = rt.TVShow(query)
                st.header(f"{show.title} (Season 1)")
                st.metric("Tomatometer", f"{show.tomatometer}%")
                st.write(f"**Synopsis:** {show.synopsis}")
                
                st.subheader("Reviews")
                for r in show.reviews[:5]:
                    st.info(f"\"{r}\"")
                    
    except Exception as e:
        st.error("Match not found. Try adding the year (e.g. 'Toy Story 1995') or check your spelling.")
