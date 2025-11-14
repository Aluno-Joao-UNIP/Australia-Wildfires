import streamlit as st

class BasePage:
    # Construtor que inicia as variáveis de configuração
    def __init__(self, page_title, layout, page_icon = "view/img/Logo.png"):
        self.page_title = page_title
        self.page_icon = page_icon
        self.layout = layout
        self.configs = {
            "initial_sidebar": "collapsed"
        }

        # Aplica a configuração da página
        self.apply_config()

    # Função que aplica as configurações de página
    def apply_config(self):
        st.set_page_config(
            page_title = self.page_title,
            page_icon = self.page_icon,
            layout = self.layout,
            initial_sidebar_state = self.configs["initial_sidebar"]
        )
