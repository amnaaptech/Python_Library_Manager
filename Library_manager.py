import json
import os
import streamlit as st
import time

# File for storing data
DATA_FILE = 'library.txt'

# Load library from file
def load_library():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(DATA_FILE, 'w') as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# ✅ Set Default Page in Session State
if "menu" not in st.session_state:
    st.session_state.menu = "📖 Add Book"

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["📖 Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics", "🚪 Exit"], index=["📖 Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics", "🚪 Exit"].index(st.session_state.menu))

# ✅ Add a Book
if menu == "📖 Add Book":
    st.session_state.menu = "📖 Add Book"  # Update session state
    st.header("➕ Add a New Book")
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    year = st.number_input("Enter the publication year:")
    genre = st.text_input("Enter the genre:")
    read = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read
        }
        library.append(new_book)
        save_library(library)
        st.success(f"✅ '{title}' added successfully!")

#  Exit Page
elif menu == "🚪 Exit":
    st.header("👋 Exit")
    st.write("You are about to exit the menu. Click the button below to return to the Add Book page.")

    if st.button("Go to Add Book 📖"):
        st.toast("✅ Goodbye! See you next time...")  # Toast message (won't disappear on rerun)
        time.sleep(1)  # Wait for 1 second
        st.session_state.menu = "📖 Add Book"  # Change menu state
        st.rerun()  # Rerun app


#  Remove a Book
elif menu == "❌ Remove Book":
    st.session_state.menu = "❌ Remove Book"
    st.header("🗑 Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove:", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"✅ '{book_to_remove}' removed successfully!")
    else:
        st.warning("No books available to remove!")

# 🔍 Search for a Book
elif menu == "🔍 Search Book":
    st.session_state.menu = "🔍 Search Book"
    st.header("🔎 Search for a Book")
    search_by = st.radio("Search by:", ["Title", "Author"])
    search_term = st.text_input(f"Enter the {search_by.lower()}:").lower()

    if st.button("Search"):
        results = [book for book in library if search_term in book[search_by.lower()].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} - ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📌 Unread'}")
        else:
            st.warning("⚠ No matching books found.")

# 📚 Display All Books
elif menu == "📚 Display Books":
    st.session_state.menu = "📚 Display Books"
    st.header("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖**{book['title']}** by {book['author']} - ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📌 Unread'}")
    else:
        st.warning("Your library is empty!")

# 📊 Display Statistics
elif menu == "📊 Statistics":
    st.session_state.menu = "📊 Statistics"
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"📚 **Total books:** {total_books}")
    st.write(f"📖 **Books Read:** {read_books}")
    st.write(f"📊 **Percentage Read:** {percentage_read:.2f}%")
