import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# Load Data
data = pd.read_csv(r"Output.csv")
df = pd.DataFrame(data)

st.set_page_config(page_title="Netflix Recommendation System", page_icon="📊")
st.header("Overview")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Trends",
    "🌍 Countries",
    "🎭 Genres",
    "🔖 Ratings",
    "🎬 Recommanded Movies",
    "⌛ Duration & Seasons",
    "🕰️ Historical Content"
    ])

with tab1:
    st.subheader("📈 Trends")

    # Total number of contents
    st.write("##### How many `movies` and `TV shows` are there in the dataset?")
    st.write(df['type'].value_counts())
    st.write(f"Total `content type` in datasets : `{df['type'].value_counts().sum()}`")

    # Content addition trend changed over the years
    st.write("##### How has Netflix’s `content addition trend` changed over the years?")

    trend_change = df.groupby("type")['release_year'].value_counts().sort_index().reset_index()

    fig1 = px.line(trend_change, y='count', x='release_year', markers=True, color='type', color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig1)

    # Most focusing content 'type'
    st.write("##### Are Netflix focusing more on `TV shows` or `movies` in recent years?")

    movies = df[(df['type'] == "Movie") & (df["release_year"] >= 2020)]['type'].value_counts()
    tv_shows = df[(df['type'] == "TV Show") & (df["release_year"] >= 2020)]['type'].value_counts()

    content_merge = pd.concat([movies, tv_shows])
    st.write(content_merge)
    st.write("`Netflix focuses more on 'TV Shows' rather than 'Movies' in recent years`")

    # Titles released each year
    st.write("##### How many titles were `released each year`? ")

    titles_each_year = df['release_year'].value_counts().sort_index().reset_index()
    fig2 = px.line(titles_each_year, x='release_year', y='count', markers=True, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig2)

    # Most diverse content in 'Genre'
    st.write("##### Which years had the most `diverse content` in terms of genres?")
    
    diverse_content = df.groupby('Genre')['release_year'].value_counts().sort_values(ascending=False).head(1)
    st.write(diverse_content)


with tab2:
    st.subheader("🌍 Country")
    st.write("##### Which `country` has the highest number of Netflix titles?")

    # Country with highest number of Netflix titles
    country_with_highest_titles = df['country'].value_counts()
    st.write(country_with_highest_titles.head(1))

    # Top Countries with most Netflix original content
    st.write("##### Which `countries` produce the most Netflix original content?")

    original_content = country_with_highest_titles[country_with_highest_titles.index != "unknown"]
    st.write(original_content.head(5))

    # Content comparison between countries
    st.write("##### What type of `content (Genre)` is most popular in `India/US` compared to other countries?")

        # Filtering countries 
    us = df[df['country'] == 'United States'][['Genre','country']].value_counts().reset_index().head(9)

    india = df[df['country'] == 'India'][['Genre','country']].value_counts().reset_index().head(9)

    other = df[(df['country'] != 'India') & (df['country'] != 'United States') & (df['country'] != 'unknown')][['Genre','country']].value_counts().reset_index().head(9)

    combined = pd.concat([us,india,other], ignore_index= True)
    modified = combined.copy()
    modified['country'] = modified['country'].apply(lambda x: x if x in ['United States','India'] else 'Other')

    fig3 = px.bar(modified, x='Genre', y='count', color='country')
    st.plotly_chart(fig3)

with tab3:
    st.subheader("🎭 Genres")

    # Most frequently Genre
    st.write("##### Which `Genres` appear most frequently?")
    genres = df['Genre'].value_counts().reset_index().head(10)
    fig4 = px.bar(genres, x="Genre", y="count", color='Genre')
    st.plotly_chart(fig4)

    # Movie durations across Genre
    st.write("##### How do movie `durations` vary across `genres`?")
    movies_across_genres = df[df['type'] == "Movie"].groupby("Genre")['Minutes'].agg(["min", "mean", "max", "count"]).sort_values(by="count", ascending=False)
    movies_across_genres['mean'] = movies_across_genres['mean'].round(2)
    st.write(movies_across_genres.head(8))

    # Most common genres among recently added content
    st.write("##### Which `genres` are most common among `recently added content`?")

    most_common_genres = df[df['Uploaded_Year'] == df["Uploaded_Year"].max()]['Genre'].value_counts().head(5).reset_index()

    fig5 = px.pie(most_common_genres, names="Genre", values="count")
    st.plotly_chart(fig5)

with tab4:
    st.subheader("⭐ Ratings")
    st.write("##### What is the most common `rating` for Netflix content?")

    # Common 'rating' for Netflix content 
    common_rating = df['rating'].value_counts().reset_index().head()
    fig8 = px.pie(common_rating, names="rating", values="count", color="rating", color_discrete_sequence=px.colors.qualitative.Set1, hole=0.5)
    st.plotly_chart(fig8)

    # Difference in rating distribution between 'movies' & 'TV Shows'
    st.write("##### Is there a difference in `rating distribution` between `movies` and `TV shows`")

    rating_of_movies = df[df['type'] == 'Movie']['rating'].value_counts().head(10)
    rating_of_tv_shows = df[df['type'] == 'TV Show']['rating'].value_counts().head(10)
    merge = pd.concat([rating_of_movies, rating_of_tv_shows])
    merged_df = merge.groupby(merge.index).sum().sort_values(ascending=True).reset_index()

    fig6 = px.bar(merged_df, x="count", y="rating",color="rating", color_discrete_sequence=px.colors.qualitative.Bold, text="count")
    st.plotly_chart(fig6)

with tab6:
    st.subheader("⌛ Duration & Seasons")
    st.write("##### What is the average `duration` of movies?")

    average_watch = df[df["type"] == "Movie"]["Minutes"].agg(["mean", "count"])
    st.write(f"- `Average watch duration of Movies : {average_watch["mean"]:.2f} mins`")
    st.write(f"- `Total number of Movies : {average_watch["count"].astype(int)}`<br><br>",unsafe_allow_html=True)

    st.write("##### How many `seasons` do TV shows typically have?")
    seasons_watch = df[df["type"] == "TV Show"]["Seasons"].agg(["min", "mean","max","count"])
    st.write(seasons_watch.round(2))

    st.write(f"- `Average watch duration of TV Shows : {seasons_watch['mean']:.2f} seasons`")
    st.write(f"- `Total number of TV Shows : {seasons_watch['count'].astype(int)}`")

with tab7:
    st.subheader("🕰️ Historical Content")

    st.write("##### Do `older movies (pre-2000)` still make up a large portion of Netflix’s library?")

    movies_before_2000 = df[(df['type'] == "Movie") & (df['release_year'] < 2000)].shape[0]
    movies_after_2000 = df[(df['type'] == "Movie") & (df['release_year'] >= 2000)].shape[0]

    # Create DataFrame for plotting
    movie_data = pd.DataFrame({
        "Category": ["Movies Before 2000", "Movies with 2000 & After"],
        "Count": [movies_before_2000, movies_after_2000]
    })

    custom_colors = ["#0079A1", "#DF3004"]
    fig7 = px.pie(
        movie_data,
        names="Category",
        values="Count",
        color_discrete_sequence=custom_colors,
        hole=0.33
    )
    st.plotly_chart(fig7, use_container_width=True)

with tab5:
    st.subheader("Recommanded Movies")

    country = st.selectbox(options=df[df["country"] != "unknown"]['country'].unique(), label="Select Country")

    movie_genre = st.selectbox(options=df['Genre'].sort_values(ascending=True).unique(), label="Select Movie Genre")

    suggest = df[(df['Genre'] == movie_genre) & (df['country'] == country)].sort_values(ascending=False ,by='release_year').head(6)

    def movie_poster(movie_title):
        movie_list = []
        for movie in movie_title:
            url = f"https://www.omdbapi.com/?t={movie}&apikey=a8abe21d"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                poster = data.get('Poster', None)
                if poster and poster != 'N/A':
                    movie_list.append((movie, poster))
            else:
                st.error(f"Movie '{movie}' not found!")
        return movie_list

    posters = movie_poster(suggest['title'])

    if posters:
        html = "<div style='display: flex; flex-wrap: wrap; justify-content: space-between; margin: 20px; margin-top: 50px; gap: 20px;'>"

        for title, img in posters:
            html += f"""
                <div style="text-align: center;">
                    <img src="{img}" width="180" height="260"
                        style="border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
                    <p style="margin-top: 8px; font-weight: 600; font-size: 14px; color: #E50914;">{title}</p>
                </div>
            """

        html += "</div>"
        st.html(html)

    else:
        st.info("No posters found for this selection.")

