import streamlit as st

# 1. Inicializar o estado da sessão
# Verifica se a chave 'contador' existe, se não, cria-a com valor 0.
if 'contador' not in st.session_state:
    st.session_state.contador = 0

# 2. Acessar e atualizar o estado da sessão
# Um botão que incrementa o contador quando clicado.
if st.button('Clicar'):
    st.session_state.contador += 1

# Exibir o valor atual do contador
st.write(f'O botão foi clicado {st.session_state.contador} vezes.')

# 3. Usar callbacks para atualizar o estado
# Exemplo com um campo de texto e o estado de um formulário.
# Define uma função de callback para ser chamada quando o texto muda.
def atualiza_texto():
    st.session_state.texto_digitado = st.session_state.input_texto

texto = st.text_input('Digite algo', key='input_texto', on_change=atualiza_texto)

# Exibir o texto que está sendo digitado (a partir do estado da sessão)
st.write(f'Você digitou: {st.session_state.get("texto_digitado", "")}')
