import streamlit as st
from rottentomatoes_python import Search, Movie, TVShow

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Succession")

if query:
    try:
        results = Search(query)
        all_results = results.movies + results.tv_shows
        
        if not all_results:
            st.warning("No matches found.")
        else:
            for item in all_results:
                score = f"{item.tomatometer}%" if item.tomatometer else "N/A"
                year = item.year if item.year else "???"
                
                # Create a clickable button for each result
                if st.button(f"[{score}] {item.name} ({year})", use_container_width=True):
                    st.divider()
                    # Determine if it's TV or Movie based on URL
                    if "tv" in item.url:
                        data = TVShow(item.name)
                        st.subheader(f"{item.name} (Season 1)")
                    else:
                        data = Movie(item.name)
                        st.subheader(item.name)
                        
                    st.write(f"**Synopsis:** {data.synopsis}")
                    st.write("**Top Critic Reviews:**")
                    for r in data.reviews[:8]:
                        st.info(f"\"{r.text}\"\n— {r.critic}")
    except Exception as e:
        st.error(f"Search failed. RT might be blocking the request. Try again in a moment.")
