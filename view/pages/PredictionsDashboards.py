from datetime import datetime 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#from models.PredictionModel.ModelTraining import ModelTrainig
from models.PredictionModel.PredictModel import PredictModel

class PredicitonsDashboards:
    def __init__(self, df_clean, feature_importance, accuracy, cm, prediction):
        self.df_clean = df_clean
        self.feature_importance = feature_importance
        self.accuracy = accuracy
        self.cm = cm
        self.prediction = prediction
    
    def predictions_dashboards(self):
        st.title("📈 Resultados da Predição")
        st.divider()
        
        prediction_date = self.prediction["date"]
        prediction_date = datetime.strptime(prediction_date, "%d/%m/%Y")
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

        top_features = self.feature_importance.head(10)

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
            self.cm,
            index=["Baixo", "Alto"],
            columns=["Baixo", "Alto"]
        )

        fig2 = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="YlOrRd",
            title=f"Matriz de Confusão - Acurácia: {self.accuracy*100:.2f}%"
        )

        monthly_fires = self.df_clean.groupby("month").size()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        high_risk_months = monthly_fires[monthly_fires > monthly_fires.median()]
        
        df_month = pd.DataFrame({
            "month": months,
            "fires": monthly_fires,
            "risk": ["Alto" if i+1 in high_risk_months.index else "Baixo" for i in range(12)]
        })

        fig3 = px.bar(
            df_month,
            x="month",
            y="fires",
            color="risk",
            color_discrete_map={
                "High": "#e63946",
                "Low": "#f1fa8c"
            },
            title="Distribuição de Incêndios por mês",
            labels={"month": "Mês", "fires": "Incêndios", "risk": "Risco"}
        )
        fig3.add_hline(y=df_month["fires"].median(), line_dash="dash")

        seasonal_fires = self.df_clean.groupby("season")["fire_intensity"].agg(["count", "mean"])
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

        yearly_data = self.df_clean.groupby("year").agg({
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
                st.plotly_chart(fig1, width = "stretch")
                
            with col2:
                st.plotly_chart(fig2, width = "stretch")
        
        with tab2:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("**Ocorrencias por mês:**")
                for month, fires in monthly_fires.items():
                    st.write(f"  {months[month-1]:>3} - {fires:>8,} Incêndios ({fires/len(self.df_clean)*100:>5.2f}%)")
            
            with col2:
                st.plotly_chart(fig3, width = "stretch")
            
        with tab3:
            st.plotly_chart(fig6, width = "stretch")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Padrões do fogo/queimadas por estação:**")
                for season, data in seasonal_fires.iterrows():
                    st.write(f"   {seasonal_names[season]:>6}: {data["count"]:>8,} chamas | " + 
                        f"Intensidade alta: {data["mean"]*100:>5.1f}%")
            
            with col2:
                st.plotly_chart(fig4, width = "stretch")
                
