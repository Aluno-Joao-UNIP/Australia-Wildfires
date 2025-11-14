import streamlit as st # -> Criação fácil de aplicações web

from view.src.Base import BasePage

class HomePage(BasePage):
    # =================================================================================================================================================
    # Inicialização
    # =================================================================================================================================================
    def __init__(self):
        # Aplica configurações de página
        super().__init__(page_title = "Início", layout = "wide")

    # =================================================================================================================================================
    # Execução
    # =================================================================================================================================================
    def run(self):
        self.apply_config()
        
        st.title("🔥 Introdução a Predição de Queimadas na Austrália")
        st.divider()

        st.subheader("Modelo de Machine Learning baseado em dados do FIRMS (NASA) para estimar risco e intensidade de incêndios naturais")
        st.markdown("""
            ### 🛰️ O que é o FIRMS (NASA)?

            O **FIRMS (Fire Information for Resource Management System)** é um sistema da NASA que disponibiliza dados quase em tempo real 
            sobre focos de incêndio ao redor do mundo. Através de satélites equipados com sensores térmicos avançados, o FIRMS detecta pontos 
            de calor na superfície terrestre e registra queimadas ativas com alta precisão. Esses dados podem ser visualizados em mapas 
            interativos ou baixados via APIs, permitindo que pesquisadores, órgãos ambientais e equipes de resposta a emergências monitorem incêndios, 
            avaliem riscos e tomem decisões estratégicas com rapidez.
            
            Todos os anos, a Austrália enfrenta a chamada **temporada de queimadas**, um período marcado por:
            - Altas temperaturas,
            - Baixa umidade,
            - Ventos constantes,
            - Baixo índice de precipitação.

            Essas condições tornam grande parte do território extremamente vulnerável a incêndios naturais.

            ---
            
            ### 🚨 Uma realidade preocupante

            As queimadas de **2019–2020** foram um marco histórico devido ao seu impacto sem precedentes. Nesse período:

            - **29 milhões de hectares** foram queimados,
            - **3.094 casas** foram destruídas,
            - quase **3 bilhões de animais** morreram ou ficaram desabrigados.

            Além dos danos ambientais e sociais, os incêndios liberam grandes quantidades de dióxido de carbono (CO₂). Somente entre **dezembro de 2019 e janeiro de 2020**, foram emitidas aproximadamente **400 megatoneladas de CO₂**, um valor próximo à **média anual de emissões de todo o país**.

            Essas queimadas não são eventos isolados — elas são parte de uma dinâmica natural que existe há milhões de anos. No entanto, estudos mostram que **as mudanças climáticas intensificam a frequência, a força e os impactos dos incêndios**, criando um ciclo cada vez mais difícil de controlar.

            ---

            ### 🌱 Nosso propósito

            Este projeto tem como objetivo desenvolver uma aplicação capaz de **analisar dados históricos de incêndios e prever novas ocorrências**.  
            A plataforma utiliza a linguagem **Python**, técnicas de manipulação de dados e modelos de predição para transformar milhares de registros em informações visuais acessíveis.

            A aplicação:

            - Coleta e processa dados reais de queimadas de anos anteriores,
            - Gera **dashboards interativos** com gráficos e métricas relevantes,
            - Aplica modelos capazes de **estimar o risco de queimadas futuras**.

            ---

            ### 🧠 Por que prever incêndios?

            A predição de queimadas permite que medidas sejam tomadas **antes** que o desastre aconteça.  
            Entre os principais benefícios estão:

            ✅ Apoio a ações de evacuação antecipada;  
            ✅ Direcionamento de equipes de combate ao fogo;  
            ✅ Planejamento de uso de recursos e infraestrutura;  
            ✅ Redução de perdas ambientais, econômicas e humanas.

            Quando o risco é detectado, governos e instituições podem agir com mais rapidez e precisão.

            ---

            ### 🛰️ Como funciona a aplicação?

            O sistema combina:

            - Dados históricos de incêndios,
            - Informações climáticas e ambientais,
            - Processamento com Python e visualizações em dashboards.

            Por meio dessas análises, o usuário pode observar *tendências de risco*, identificar períodos críticos e explorar indicadores como brilho térmico, localização de focos e intensidade.

            O objetivo é que a ferramenta seja **intuitiva, acessível e visualmente clara**, permitindo que qualquer pessoa — pesquisadores, órgãos públicos e até cidadãos comuns — possa compreender os riscos e agir de forma informada.

            ---

            ### 🌎 Um recurso para o presente e o futuro

            Além de agregar valor científico, o projeto também busca **promover conscientização** sobre o impacto das mudanças climáticas, reforçando a necessidade de ações preventivas e sustentáveis para o futuro do planeta.

            > **Prevenir é sempre melhor do que reagir.  
            Nossa missão é transformar dados em informação — e informação em proteção.**
            """
        )

