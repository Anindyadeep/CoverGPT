import streamlit as st 
from src.routes import Routes

def app():
    st_routes = Routes()
    pages = {
        'Getting started': st_routes.upload_assets
    }

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(pages.keys()))
    pages[page]()


if __name__ == '__main__':
    app()

