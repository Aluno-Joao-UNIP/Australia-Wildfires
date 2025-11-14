from datetime import datetime
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

class ModelTrainig:
    def training(self):
        file = "fire_model.pkl"
        directory = os.getcwd()
        path_file = os.path.join(directory, file)
        
        df = pd.read_parquet("models/PredictionModel/sorted_fires_australia.parquet")
        print(f"Carregados em {len(df):,} registros")

        if df.empty:
            print("Erro - parquet nao encontrado")
            print(f"Procurei em {df}")
            print("Execute o pipeline primeiro!")
            exit()
        print(f"Dados carregados do parquet {len(df):,} registros")

        df = df.sample(frac=0.70, random_state=42)
        print(f"\nPronto: {len(df):,} dados do fogo")
        print(f"\nColunas: {list(df.columns)}")
        print(f"\nPrimeiros 3 dados:")
        print(df.head(3))

        # Dados para as queimadas
        df["year"] = df["acq_date"].dt.year
        df["month"] = df["acq_date"].dt.month
        df["day"] = df["acq_date"].dt.day
        df["day_of_year"] = df["acq_date"].dt.dayofyear
        df["week_of_year"] = df["acq_date"].dt.isocalendar().week
        df["quarter"] = df["acq_date"].dt.quarter

        def get_season(month):
            if month in [12, 1, 2]:
                return 3
            elif month in [9, 10, 11]:
                return 2 
            elif month in [3, 4, 5]:
                return 1
            else: 
                return 0

        df["season"] = df["month"].apply(get_season)
        le_daynight = LabelEncoder()
        df["daynight_encoded"] = le_daynight.fit_transform(df["daynight"])
        le_satellite = LabelEncoder()
        df["satellite_encoded"] = le_satellite.fit_transform(df["satellite"])

        frp_median = df["frp"].median()
        df["fire_intensity"] = (df["frp"] > frp_median).astype(int)

        print(f"\n Categoria temporal: year, month, day, day_of_year, week, quarter, season")
        print(f"Categoria do codigo: daynight, satellite")
        print(f"Intensidade do fogo: FRP > {frp_median:.2f} MW")
        print(f"\nDistribuição da intendisade do fogo:")
        print(df["fire_intensity"].value_counts())
        print(f"  0 (Baixo):  {(df["fire_intensity"]==0).sum():,} fires")
        print(f"  1 (Alto): {(df["fire_intensity"]==1).sum():,} fires")

        # Separação para o Machine Learning
        df_clean = df.dropna(subset=["frp", "brightness", "bright_t31", "confidence"])
        print(f"\nDataset limpa: {len(df_clean):,} arquivos")

        # Selecionando para predição
        features = [
            "latitude", "longitude",
            "brightness", "bright_t31",
            "confidence",
            "scan", "track",
            "month", "day_of_year", "season",
            "quarter", "week_of_year",
            "daynight_encoded",
            "satellite_encoded"
        ]

        X = df_clean[features]
        y_intensity = df_clean["fire_intensity"]
        print(f"\nCaracterísticas selecionadas: {len(features)}")
        print(f"Características: {features}")

        # Separando 80% para treino e 20% para teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_intensity, test_size=0.2, random_state=42, stratify=y_intensity
        )

        print(f"\nSeparando os dados:")
        print(f"Treino: {len(X_train):,} samples ({len(X_train)/len(X)*100:.1f}%)")
        print(f"Teste:  {len(X_test):,} samples ({len(X_test)/len(X)*100:.1f}%)")

        # Treinando o ML (100 arvores, 20 maximo de profundidade)
        rf_intensity = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=20,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )

        start_time = datetime.now()
        rf_intensity.fit(X_train, y_train)
        train_time = (datetime.now() - start_time).total_seconds()
        print(f"Modelo treinado em {train_time:.2f} segundos!") # Levando 5mn sem alteracao da quantidade

        rf_intensity.fit(X_train, y_train)
        
        import pickle

        with open("fire_model.pkl", "wb") as f:
            pickle.dump(rf_intensity, f)
        print("\n Modelo salvo como 'fire_model.pkl'")

        # Predições
        y_pred = rf_intensity.predict(X_test)
        y_pred_proba = rf_intensity.predict_proba(X_test)

        # Calculando a precisão
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Precisão: {accuracy*100:.2f}%")

        # Devolvendo os valores
        print(classification_report(y_test, y_pred,
                                    target_names=["Low Intensity", "High Intensity"],
                                    digits=3))

        # Matriz
        cm = confusion_matrix(y_test, y_pred)
        print("\nMatriz Confunsion:")
        print("                 Baixa Predição  Alta Predição")
        print(f"Baixo atual       {cm[0][0]:>13,}  {cm[0][1]:>14,}")
        print(f"Alto atual      {cm[1][0]:>13,}  {cm[1][1]:>14,}")

        true_negatives = cm[0][0]
        false_positives = cm[0][1]
        false_negatives = cm[1][0]
        true_positives = cm[1][1]

        precision_high = true_positives / (true_positives + false_positives)
        recall_high = true_positives / (true_positives + false_negatives)

        print(f"  Precisão(Alta): {precision_high*100:.2f}%")
        print(f"  Recall (Alta):    {recall_high*100:.2f}%")

        feature_importance = pd.DataFrame({
            "feature": features,
            "importance": rf_intensity.feature_importances_
        }).sort_values("importance", ascending=False)

        print("\nTop caracteristicas + importantes:")
        for idx, row in feature_importance.head(10).iterrows():
            print(f"  {row["feature"]:.<25} {row["importance"]:.4f}")
            
        return df_clean, feature_importance, accuracy, cm
