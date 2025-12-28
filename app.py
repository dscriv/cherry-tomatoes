import streamlit as st
import rottentomatoes as rt

st.set_page_config(page_title="Cherry Tomatoes", page_icon="🍅")
st.title("🍅 Cherry Tomatoes")

query = st.text_input("Search Movie or Series:", placeholder="e.g. Toy Story")

if query:
    try:
        with st.spinner(f"Searching for '{query}'..."):
            # Use the search function to find actual matches
            search_results = rt.search(query)
            
            # Combine Movies and TV results
            results = search_results.get("movies", []) + search_results.get("tv_shows", [])
            
            if not results:
                st.warning("No matches found. Try a different spelling.")
            else:
                # Show the top result automatically
                top_item = results[0]
                name = top_item.get("name")
                is_tv = "/tv/" in top_item.get("url", "")
                
                if is_tv:
                    data = rt.TVShow(name)
                    st.header(f"{data.title} (Series)")
                else:
                    data = rt.Movie(name)
                    st.header(f"{data.title} ({data.year})")
                
                # Layout scores
                c1, c2 = st.columns(2)
                c1.metric("Tomatometer", f"{data.tomatometer}%")
                if hasattr(data, 'audience_score'):
                    c2.metric("Audience", f"{data.audience_score}%")
                
                st.divider()
                st.write(f"**Synopsis:** {data.synopsis}")
                
                st.subheader("Top Critic Reviews")
                if data.reviews:
                    for r in data.reviews[:8]:
                        st.info(f"\"{r}\"")
                else:
                    st.write("No reviews found for this title.")
                    
    except Exception as e:
        st.error("RT is currently blocking the search. Please wait 60 seconds and try again.")
