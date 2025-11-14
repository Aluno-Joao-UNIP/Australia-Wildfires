from datetime import date, datetime, timedelta
import folium
import os
import streamlit as st # -> Criação fácil de aplicações web
from streamlit_folium import st_folium
import time

from view.src.Base import BasePage
from view.pages.PredictionsDashboards import PredicitonsDashboards
from models.PredictionModel.ModelTraining import ModelTrainig
from models.PredictionModel.PredictModel import PredictModel

class PredictionsPage(BasePage):
    # =================================================================================================================================================
    # Inicialização
    # =================================================================================================================================================
    def __init__(self):
        # Aplica configurações de página
        super().__init__(page_title = "Predições", layout = "wide", page_icon = "view/img/Logo.png")

    # =================================================================================================================================================
    # Execução
    # =================================================================================================================================================
    def run(self):
        self.apply_config()

        def run_home():
            st.title("🧠 Inicie o treinamento do modelo")
            st.divider()

            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.empty()
            
            with col2:
                st.markdown(
                    '''
                        <div style="text-align: center">
                            <h3>Modelo não encontrado!</h3>
                            <p>Realize o treinamento do modelo para gerá-lo, podendo fazer predições das queimadas em todo território australiano de até um ano do dia atual!</p>
                        </div>
                    ''',
                    unsafe_allow_html = True)

                col1, col2, col3 = st.columns([1.2, 1.3, 1])

                with col2:
                    if st.button("Iniciar Treinamento"):
                        st.session_state.page = "loading"
                        st.rerun()

            with col3:
                st.empty()
            
        def run_loading():
            st.title("⚙️ Treinando o Modelo")
            st.divider()
            

            with st.spinner("O modelo está sendo treinado..."):
                st.markdown("**Tempo estimado: 3 a 5 minutos**")
                progress_bar = st.progress(0)
                status_text = st.empty()

                df_clean, feature_importance, accuracy, cm = model.training()
                st.session_state.model = df_clean, feature_importance, accuracy, cm
                progress_bar.progress(100)
                status_text.text(f"Treinando modelo... {100}% concluído")
                time.sleep(3)

                progress_bar.empty()
                status_text.text("✅ Treinamento concluído!")
                time.sleep(3)

            st.success("Treinamento finalizado com sucesso!")
            st.session_state.page = "predict"
            st.rerun()

        def run_predict():
            st.title("🗺️ Saiba se sua região corre riscos")
            st.markdown("#### 🔽 Selecione as opções abaixo para poder realizar a predição:")
            st.divider()
            
            col1, col2, col3 = st.columns([1, 1.8, 1])
            
            with col1:
                st.empty()
            
            with col2:
                # Data mínima = hoje
                data_minima = datetime.today().date()
                # Data máxima = hoje + 1 ano
                data_maxima = data_minima + timedelta(days = 365)
                
                selected_data = st.date_input(label = "Escolha uma data futura", label_visibility = "hidden", value = data_minima, min_value = data_minima, max_value = data_maxima)
                if selected_data > date.today():
                    day = selected_data.day
                    month = selected_data.month
                    year = selected_data.year
                    months = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
                    for number, name in months.items():
                        if month == number:
                            month_name = name
                    st.success(f"Você selecionou o dia {day} de {month_name} de {year}")
                else:
                    st.info("Escolha uma data futura:")

                initial_map = folium.Map(location = [-28.0, 139.0], zoom_start = 4.4)

                map_data = st_folium(initial_map, width = 700, height = 500)
                selectMap = False
                if map_data and map_data["last_clicked"]:
                    lat = map_data["last_clicked"]["lat"]
                    lon = map_data["last_clicked"]["lng"]

                    st.success(f"📍 Latitude: {lat:.4f}, Longitude: {lon:.4f}")
                    selectMap = True
                else:
                    st.info("Clique no mapa para selecionar um ponto.")

                col1, col2, col3 = st.columns([1.2, 1, 1])

                with col2:
                    confirm = st.button("Iniciar Predição")
                    
                if confirm:
                    if selectMap and selected_data != date.today():
                            prediction = predict.predict_fire(lat, lon, month, day, year)
                            st.session_state.result = prediction
                            st.session_state.page = "dashs"
                                        
                    else:
                        st.error("Preencha todas as informacoes para realizar a predicao.")
                
                with col3:
                    st.empty()

        def run_dashs(): 
            try:
                df_clean, feature_importance, accuracy, cm = st.session_state.model
                prediction = st.session_state.result
                pred_dashs = PredicitonsDashboards(df_clean, feature_importance, accuracy, cm, prediction)
                pred_dashs.predictions_dashboards()
            except Exception as e:
                df_clean, feature_importance, accuracy, cm = st.session_state.model
                prediction = st.session_state.result

        file = "fire_model.pkl"
        directory = os.getcwd()
        path_file = os.path.join(directory, file)

        if "page" not in st.session_state:
            st.session_state.page = "home"
            st.session_state.result = 0
            if os.path.isfile(path_file):
                st.session_state.page = "predict"
                
        model = ModelTrainig()
        predict = PredictModel()

        if st.session_state.page == "home":
            run_home()
        elif st.session_state.page == "loading":
            run_loading()
        elif st.session_state.page == "predict":
            run_predict()
        elif st.session_state.page == "dashs":
            run_dashs()
    
