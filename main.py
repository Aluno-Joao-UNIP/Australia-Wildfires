import streamlit as st

from view.Home import HomePage
from view.pages.Predictions import PredictionsPage
from view.pages.Dashboards import DashboardsPage
from models.Datas import Datas

def main():
    dataset = Datas()
    df = dataset.importDatasetsOnFirms()

    pages = {
        "Inicio": HomePage(),
        "Predicoes": PredictionsPage(),
        "Relatorios": DashboardsPage(df)
    }

    params = st.query_params
    page_from_url = params.get("page", None)

    if "current_page" not in st.session_state:
        st.session_state.current_page = page_from_url or "Inicio"

    st.sidebar.title("📂 Navegação")

    page_selected = st.sidebar.radio(
        "Ir para:",
        list(pages.keys()),
        index=list(pages.keys()).index(st.session_state.current_page),
        key="current_page"
    )

    st.query_params.update({"page": st.session_state.current_page})

    pages[st.session_state.current_page].run()

if __name__ == "__main__":
    main()
