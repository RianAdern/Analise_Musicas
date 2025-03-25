import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def Tab_Data_Resume():
    col1, col2e, col3e, col4 = st.columns([1, 5, 5, 1])
    
    with col2e:
        st.header("Resumo de Dados")
        
        if 'df_transformado' not in st.session_state:
            st.warning("Nenhum dataframe transformado disponível. Use as abas anteriores para processar os dados.")
        else:
            df = st.session_state['df_transformado']
            
            # Resumo Geral
            st.subheader("Resumo Geral")
            st.write(f"Número de linhas: {df.shape[0]}")
            st.write(f"Número de colunas: {df.shape[1]}")
            st.write("Colunas e tipos de dados:")
            st.dataframe(df.dtypes)

            # Comparação Antes e Depois
            if 'df' in st.session_state:
                df_original = st.session_state['df']
                st.subheader("Comparação Antes e Depois")
                st.write(f"Linhas originais: {df_original.shape[0]} | Linhas transformadas: {df.shape[0]}")

            # Estatísticas Finais
            st.subheader("Estatísticas Finais")
            st.dataframe(df[['Tempo (BPM)', 'Energy', 'Danceability']].describe())

    with col3e:
        # Visualização Resumida
        st.subheader("Visualização Resumida")
        if 'df' in st.session_state and 'Genre' in st.session_state['df'].columns:
            df_original = st.session_state['df']  # Usa o dataframe original para valores categóricos
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.countplot(data=df_original, x='Genre', ax=ax)
            ax.set_title("Distribuição de Gêneros")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Coluna 'Genre' não encontrada no dataframe original.")

        # Exportação
        st.subheader("Exportar Resumo")
        if 'df_transformado' in st.session_state:
            output_name = st.text_input("Nome do arquivo (sem extensão)", "data_resume")
            if st.button("Salvar Resumo como CSV"):
                csv = df.describe().to_csv()
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{output_name}.csv",
                    mime="text/csv"
                )
                st.success(f"Resumo salvo como '{output_name}.csv'!")