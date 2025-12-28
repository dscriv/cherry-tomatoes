import streamlit as st
import rottentomatoes as rt

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Toy Story")

if query:
    try:
        # Fetch search results from RT
        with st.spinner("Searching..."):
            results = rt.search(query)
        
        # Combine movies and TV into one list
        all_results = results.get("movies", []) + results.get("tv_shows", [])
        
        if not all_results:
            st.warning("No matches found. Try a different name.")
        else:
            st.subheader("Results")
            for item in all_results:
                # Format the label: [Score%] Name (Year)
                score = f"{item.get('tomatometer', 'N/A')}%"
                label = f"[{score}] {item.get('name')} ({item.get('year', 'N/A')})"
                
                # Each result is a button
                if st.button(label, key=item.get('url'), use_container_width=True):
                    st.divider()
                    with st.spinner("Fetching details..."):
                        # If the URL contains '/tv/', it's a series
                        if "/tv/" in item.get('url', ''):
                            data = rt.TVShow(item.get('name'))
                            st.subheader(f"{data.title} (Season 1)")
                        else:
                            data = rt.Movie(item.get('name'))
                            st.subheader(data.title)
                        
                        st.write(f"**Synopsis:** {data.synopsis}")
                        st.write("**Top Critic Reviews:**")
                        
                        if data.reviews:
                            # The library returns reviews as a list of strings
                            for r in data.reviews[:8]:
                                st.info(f"\"{r}\"")
                        else:
                            st.write("No critic reviews found for this title.")
                            
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
