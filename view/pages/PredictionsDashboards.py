from datetime import datetime 
import streamlit as st
import pandas as pd
import pickle as pk
import plotly.express as px
import plotly.graph_objects as go

class PredicitonsDashboards:
    def __init__(self, prediction):
        self.prediction = prediction

    def get_training_data(self):
        try: 
            with open("fire_model.pkl", "rb") as f:
                model_data = pk.load(f)

            print("Dados do modelo carregados!")
            print(f"Tipo: {type(model_data)}")
            
            # Se for dicionário, extrai os dados
            if isinstance(model_data, dict):
                df_clean = model_data.get("df_clean")
                feature_importance = model_data.get("feature_importance")
                accuracy = model_data.get("accuracy")
                cm = model_data.get("confusion_matrix")
            else:
                # Modelo antigo - só tem o modelo mesmo
                print("Aviso: Modelo antigo detectado (sem dados extras)")
                return None, None, None, None

            print("Dados carregados com sucesso")
            print(f"Dataset: {len(df_clean):,} registros")
            print(f"Acurácia: {accuracy*100:.2f}%")
            
            return df_clean, feature_importance, accuracy, cm
        
        except FileNotFoundError:
            print("Erro: fire_model.pkl não encontrado")
            print("Execute o treinamento primeiro: python models/PredictionModel/ModelTraining.py")
            return None, None, None, None
        except KeyError as e:
            print("Pickle antigo detectado")
            print(f"Variável '{e}' não encontrada")
            print("Treine novamente rodando: python models/PredictionModel/ModelTraining.py")
            return None, None, None, None
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None, None, None, None
    
    def predictions_dashboards(self):
        df_clean, feature_importance, accuracy, cm = self.get_training_data()

        # Verifica se conseguiu carregar os dados
        if df_clean is None or feature_importance is None:
            st.error("❌ Erro ao carregar dados do modelo!")
            st.warning("Por favor, treine o modelo novamente executando: `python models/PredictionModel/ModelTraining.py`")
            return

        print(f"Feature importance carregado: {type(feature_importance)}")

        st.title("📈 Resultados da Predição")
        st.divider()
        
        prediction_date = self.prediction["date"]
        prediction_date = datetime.strptime(prediction_date, "%Y-%m-%d")
        day = prediction_date.day
        month = prediction_date.month
        year = prediction_date.year
        months = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
        for number, name in months.items():
            if month == number:
                month_name = name  
        
        st.markdown(f"""
            **Data da Predição:** {day} de {month_name} de {year} - {self.prediction["season"]}\n
            **Coordenadas:** {self.prediction["location"]}\n
            **Risco de Incêndio:** {self.prediction["fire_risk"]}\n
            **Intensidade Prevista:** {self.prediction["predicted_intensity"]}\n
            **Índice de Confiança:** {self.prediction["confidence_score"]}\n
            **Brilho Térmico Estimado:** {self.prediction["brightness"]}K\n
            **Temperatura Estimada:** {self.prediction["brightness"] - 273.15:.2f}°C\n
            **Confiança:** {self.prediction["confidence"]}\n
        """)    

        st.title("📊 Gráficos do Modelo")
        st.divider()

        top_features = feature_importance.head(10)

        fig1 = px.bar(
            top_features,
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            title="Random Forest - Top 10 Características",
            labels={"importance": "Importância", "feature": "Característica"},
            color_continuous_scale="Reds",
        )
        fig1.update_layout(yaxis=dict(autorange="reversed"))

        cm_df = pd.DataFrame(
            cm,
            index=["Baixo", "Alto"],
            columns=["Baixo", "Alto"]
        )

        fig2 = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="YlOrRd",
            title=f"Matriz de Confusão - Acurácia: {accuracy*100:.2f}%"
        )

        monthly_fires = df_clean.groupby("month").size()
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        high_risk_months = monthly_fires[monthly_fires > monthly_fires.median()]
        
        df_month = pd.DataFrame({
            "month": months_list,
            "fires": monthly_fires,
            "risk": ["Alto" if i+1 in high_risk_months.index else "Baixo" for i in range(12)]
        })

        fig3 = px.bar(
            df_month,
            x="month",
            y="fires",
            color="risk",
            color_discrete_map={
                "Alto": "#e63946",
                "Baixo": "#f1fa8c"
            },
            title="Distribuição de Incêndios por mês",
            labels={"month": "Mês", "fires": "Incêndios", "risk": "Risco"}
        )
        fig3.add_hline(y=df_month["fires"].median(), line_dash="dash")

        seasonal_fires = df_clean.groupby("season")["fire_intensity"].agg(["count", "mean"])
        seasonal_names = {0: "Inverno", 1: "Outono", 2: "Primavera", 3: "Verão"}
        
        df_seasons = pd.DataFrame({
            "season": [seasonal_names[i] for i in sorted(seasonal_fires.index)],
            "fires": [seasonal_fires.loc[i, "count"] for i in sorted(seasonal_fires.index)]
        })

        fig4 = px.bar(
            df_seasons,
            x="season",
            y="fires",
            text="fires",
            title="Distribuição do Fogo por Estação",
            labels={"season": "Estação", "fires": "Incêndios"}
        )

        fig4.update_traces(marker_color="#e74c3c")

        df_intensity = pd.DataFrame({
            "season": df_seasons["season"],
            "intensity": [seasonal_fires.loc[i, "mean"] * 100 for i in sorted(seasonal_fires.index)]
        })

        fig5 = px.bar(
            df_intensity,
            x="season",
            y="intensity",
            text=df_intensity["intensity"].map(lambda x: f"{x:.1f}%"),
            title="Intensidade do Fogo por Estação (%)",
            labels={"season": "Estações", "intensity": "Intensidade"}
        )
        fig5.update_yaxes(range=[0, 100])

        fig5.update_traces(marker_color="#e74c3c")

        yearly_data = df_clean.groupby("year").agg({
            "fire_intensity": ["count", "mean"]
        }).reset_index()

        yearly_data.columns = ["year", "total_fires", "high_intensity_pct"]
        yearly_data["high_intensity_pct"] *= 100

        fig6 = go.Figure()

        fig6.add_trace(go.Bar(
            x=yearly_data["year"],
            y=yearly_data["total_fires"],
            name="Total de Incêndios",
            marker_color="#e74c3c"
        ))

        fig6.add_trace(go.Scatter(
            x=yearly_data["year"],
            y=yearly_data["high_intensity_pct"],
            mode="lines+markers",
            name="Alta Intensidade (%)",
            marker=dict(color="#e63946", size=8),
            line=dict(color="#e63946", width=3),
            yaxis="y2" 
        ))

        fig6.update_layout(
            title="Tendências de Incêndios ao longo dos anos",
            xaxis=dict(title="Ano"),
            
            yaxis=dict(
                title="Número de Incêndios",
                showgrid=False
            ),
            
            yaxis2=dict(
                title="Alta Intensidade (%)",
                overlaying="y",
                side="right",
                range=[0, 100], 
                showgrid=False
            ),
        )
        
        tab1, tab2, tab3, = st.tabs(["🧠 Modelo", "🗓️ Análise Mensal", "📆 Análise Anual"])

        with tab1:
            col1, col2 = st.columns([1, 1])

            with col1:  
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("**Ocorrencias por mês:**")
                for month_num, fires in monthly_fires.items():
                    st.write(f"  {months_list[month_num-1]:>3} - {fires:>8,} Incêndios ({fires/len(df_clean)*100:>5.2f}%)")
            
            with col2:
                st.plotly_chart(fig3, use_container_width=True)
            
        with tab3:
            st.plotly_chart(fig6, use_container_width=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Padrões do fogo/queimadas por estação:**")
                for season, data in seasonal_fires.iterrows():
                    st.write(f"   {seasonal_names[season]:>6}: {data['count']:>8,} chamas | " + 
                        f"Intensidade alta: {data['mean']*100:>5.1f}%")
            
            with col2:
                st.plotly_chart(fig4, use_container_width=True)
                
