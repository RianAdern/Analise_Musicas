import streamlit as st
import pandas as pd

def Tab_Data_Analysis():
    col1, col2, col3, col4 = st.columns([1, 5, 7, 1])
    
    with col2:  # Segunda coluna - Upload
        st.header("Upload de Arquivo")
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("Arquivo carregado com sucesso!")
                st.session_state['df'] = df
            except Exception as e:
                st.error(f"Erro ao carregar o arquivo: {e}")
                return

    with col3:  # Terceira coluna - Análise Exploratória
        if 'df' in st.session_state:
            df = st.session_state['df']
            st.header("Análise Exploratória")
            
            st.subheader("Informações Básicas")
            st.write(f"Número de linhas: {df.shape[0]}")
            st.write(f"Número de colunas: {df.shape[1]}")
            
            st.subheader("Primeiras 5 linhas")
            st.dataframe(df.head())

            st.subheader("Estatísticas Descritivas")
            st.dataframe(df.describe())
            
            st.subheader("Tipos de Dados e Valores Nulos")
            buffer = pd.DataFrame({
                'Tipo de Dado': df.dtypes,
                'Valores Nulos': df.isnull().sum(),
                '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(buffer)