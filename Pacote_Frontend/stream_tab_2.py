import streamlit as st
import pandas as pd
import numpy as np

def Tab_Data_Cleaning():

    col1, col2b, col3b, col4 = st.columns([1, 5, 5, 1])
    
    if 'df' not in st.session_state:
        with col2b:
            st.warning("Por favor, faça upload de um arquivo na aba Data Analysis primeiro!")
    else:
        df = st.session_state['df'].copy()  # Criamos uma cópia para modificações
        
        with col2b:
            st.header("Limpeza de Dados")
            
            # Verificação de duplicatas
            st.subheader("1. Verificação de Duplicatas")
            duplicatas = df.duplicated().sum()
            st.write(f"Número de linhas duplicadas: {duplicatas}")
            if duplicatas > 0:
                if st.button("Remover Duplicatas"):
                    df = df.drop_duplicates()
                    st.session_state['df'] = df
                    st.success(f"{duplicatas} linhas duplicadas removidas!")
                    st.write(f"Novo número de linhas: {df.shape[0]}")

            # Verificação de valores nulos
            st.subheader("2. Valores Nulos")
            nulos = df.isnull().sum()
            if nulos.sum() > 0:
                st.write("Colunas com valores nulos:")
                st.dataframe(nulos[nulos > 0])
                opcao_nulos = st.selectbox(
                    "Escolha uma ação para valores nulos:",
                    ["Nenhuma", "Remover linhas", "Preencher com média (numéricos)", "Preencher com moda"]
                )
                if st.button("Aplicar ação nos nulos"):
                    if opcao_nulos == "Remover linhas":
                        df = df.dropna()
                        st.success("Linhas com nulos removidas!")
                    elif opcao_nulos == "Preencher com média (numéricos)":
                        numeric_columns = df.select_dtypes(include=[np.number]).columns
                        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
                        st.success("Valores numéricos preenchidos com média!")
                    elif opcao_nulos == "Preencher com moda":
                        df = df.fillna(df.mode().iloc[0])
                        st.success("Valores preenchidos com moda!")
                    st.session_state['df'] = df

        with col3b:
            # Verificação de consistência categórica
            st.subheader("3. Consistência de Dados Categóricos")
            categoricas = df.select_dtypes(include=['object']).columns
            if len(categoricas) > 0:
                coluna_selecionada = st.selectbox("Selecione uma coluna categórica:", categoricas)
                valores_unicos = df[coluna_selecionada].value_counts()
                st.write("Distribuição dos valores:")
                st.dataframe(valores_unicos, width=500)
                
                # Verificação de possíveis inconsistências (ex: variações de maiúsculas/minúsculas)
                valores_normalizados = df[coluna_selecionada].str.lower().value_counts()
                if not valores_unicos.equals(valores_normalizados):
                    st.warning("Possíveis inconsistências detectadas (maiúsculas/minúsculas)!")
                    if st.button("Padronizar para minúsculas"):
                        df[coluna_selecionada] = df[coluna_selecionada].str.lower()
                        st.session_state['df'] = df
                        st.success("Valores padronizados para minúsculas!")

            # Outras verificações adicionais
            st.subheader("4. Outras Verificações")
            numericas = df.select_dtypes(include=[np.number]).columns
            if len(numericas) > 0:
                coluna_num = st.selectbox("Selecione uma coluna numérica:", numericas)
                stats = df[coluna_num].describe()
                st.write("Estatísticas:")
                st.dataframe(stats)
                # Verificação de outliers (método IQR)
                Q1 = df[coluna_num].quantile(0.25)
                Q3 = df[coluna_num].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[coluna_num] < (Q1 - 1.5 * IQR)) | (df[coluna_num] > (Q3 + 1.5 * IQR))).sum()
                if outliers > 0:
                    st.write(f"Número de possíveis outliers: {outliers}")
                    if st.button("Remover outliers desta coluna"):
                        df = df[~((df[coluna_num] < (Q1 - 1.5 * IQR)) | (df[coluna_num] > (Q3 + 1.5 * IQR)))]
                        st.session_state['df'] = df
                        st.success("Outliers removidos!")