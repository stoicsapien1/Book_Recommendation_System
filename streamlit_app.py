import pickle
import streamlit as st
import numpy as np

# Load pickled objects
model = pickle.load(open('model.pkl', 'rb'))
book_names = pickle.load(open('book_names.pkl', 'rb'))
final_rating = pickle.load(open('final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))


def fetch_poster(suggestion):
    poster_urls = []

    for book_id in suggestion:
        book_name = book_pivot.index[book_id]
        url = final_rating.loc[final_rating['title'] == book_name, 'img_url'].iloc[0]
        poster_urls.append(url)

    return poster_urls


def recommend_book(book_name):
    books_list = []
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
    except IndexError:
        st.error("Selected book not found. Please try again.")
        return books_list

    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
    poster_urls = fetch_poster(suggestion[0])  

    for i, book_id in enumerate(suggestion[0]):
        book = book_pivot.index[book_id]
        books_list.append((book, poster_urls[i]))

    return books_list


st.title("Book Recommendation System")
st.markdown("## My GitHub: [stoicsapien1/Book_Recommendation_System](https://github.com/stoicsapien1/Book_Recommendation_System)")
st.image("https://i.kym-cdn.com/entries/icons/original/000/018/225/3734744__f0856511d3e1798a4ebbd24b6556800e.jpg")
selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books_info = recommend_book(selected_books)
    cols = st.columns(5)

    for i, (book, url) in enumerate(recommended_books_info):
        with cols[min(i, len(cols) - 1)]:
            st.text(book)
            st.image(url)
            st.text("")  # Add empty text for vertical spacing

st.write("Made with ❤️ by Belal Ahmed Siddiqui")
