import streamlit as st
import pandas as pd
import numpy as np
# Necessário importar essas bibliotecas no início do arquivo
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.preprocessing import MultiLabelBinarizer

import seaborn as sns
import matplotlib.pyplot as plt


# Configuração inicial da página
st.set_page_config(page_title="Data Processing App", layout="wide")

# Função principal
def main():
    # Criação das tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Data Analysis", 
        "Data Cleaning", 
        "Encoding Data", 
        "Data Visualization"
    ])

    # Tab Data Analysis
    with tab1:
        col1, col2, col3, col4 = st.columns([1, 5, 7, 1])
        with col2:  # Segunda coluna
            st.header("Upload de Arquivo")
            # Upload do arquivo CSV
            uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
            
            if uploaded_file is not None:
                # Leitura do arquivo
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("Arquivo carregado com sucesso!")
                    
                    # Armazenar o dataframe na sessão
                    st.session_state['df'] = df

                except Exception as e:
                    st.error(f"Erro ao carregar o arquivo: {e}")
                    return

        with col3:  # Terceira coluna
            if 'df' in st.session_state:
                df = st.session_state['df']
                st.header("Análise Exploratória")
                
                # Mostrar informações básicas
                st.subheader("Informações Básicas")
                st.write(f"Número de linhas: {df.shape[0]}")
                st.write(f"Número de colunas: {df.shape[1]}")
                
                # Mostrar primeiras linhas
                st.subheader("Primeiras 5 linhas")
                st.dataframe(df.head())

                # Estatísticas básicas
                st.subheader("Estatísticas Descritivas")
                st.dataframe(df.describe())
                
                # Informações sobre tipos de dados e valores nulos
                st.subheader("Tipos de Dados e Valores Nulos")
                buffer = pd.DataFrame({
                    'Tipo de Dado': df.dtypes,
                    'Valores Nulos': df.isnull().sum(),
                    '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
                })
                st.dataframe(buffer)

    # As outras tabs permanecem vazias por enquanto
    with tab2:
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
                # Verificação de valores numéricos inconsistentes
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
        
    with tab3:
        col1, col2c, col3c, col4c = st.columns([1, 7, 3, 1])
        if 'df' not in st.session_state:
            with col2c:
                st.warning("Por favor, faça upload de um arquivo na aba Data Analysis primeiro!")
        else:
            with col2c:
                st.header("Encoding de Dados")
                
                # Mostrar colunas disponíveis
                st.write("Colunas disponíveis no dataset:")
                st.write(st.session_state['df'].columns.tolist())

                # Botão único para todas as transformações
                if st.button("Executar Todas as Transformações"):
                    df = st.session_state['df'].copy()  # Pegamos o df atual
                    
                    # Instanciação dos encoders
                    label_encoder = LabelEncoder()
                    ordinal_encoder = OrdinalEncoder()
                    multilabel_encoder = MultiLabelBinarizer()

                    # Definição das colunas
                    nominal_cols = ['User_Text', 'Sentiment_Label', 'Song_Name', 'Artist', 'Genre', 'Mood']
                    ordinal_cols = ['Tempo (BPM)', 'Energy', 'Danceability']
                    multilabel_cols = []

                    try:
                        # 1. Pré-processamento de IDs
                        st.subheader("1. Pré-processamento de IDs")
                        df['User_ID'] = df['User_ID'].str.replace('U', '').astype(int)
                        df['Recommended_Song_ID'] = df['Recommended_Song_ID'].str.replace('S', '').astype(int)
                        st.write("IDs processados com sucesso!")

                        # 2. Nominal Encoding
                        st.subheader("2. Encoding Nominal (LabelEncoder)")
                        for col in nominal_cols:
                            if col in df.columns:
                                df[col] = label_encoder.fit_transform(df[col])
                                st.write(f"ENCODED >>> {col}")

                        # 3. Ordinal Encoding
                        st.subheader("3. Encoding Ordinal (OrdinalEncoder)")
                        for col in ordinal_cols:
                            if col in df.columns:
                                df[col] = ordinal_encoder.fit_transform(df[[col]])
                                st.write(f"ENCODED >>> {col}")

                        # 4. Multilabel Encoding
                        st.subheader("4. Encoding Multilabel (MultiLabelBinarizer)")
                        if len(multilabel_cols) > 0:
                            for col in multilabel_cols:
                                if col in df.columns:
                                    df[col] = multilabel_encoder.fit_transform(df[[col]])
                                    st.write(f"ENCODED >>> {col}")
                        else:
                            st.write("Nenhuma coluna multilabel definida")

                        # Atualizar o session_state com todas as transformações
                        st.session_state['df_transformado'] = df
                        st.success("Todas as transformações concluídas com sucesso!")
                        
                        # Mostrar resultado
                        st.write("Pré-visualização do dataframe transformado:")
                        st.dataframe(df.head())

                    except Exception as e:
                        st.error(f"Erro durante as transformações: {e}")

            with col3c:
                st.subheader("Exportar Dados")
                if 'df_transformado' in st.session_state:
                    output_name = st.text_input("Nome do arquivo (sem extensão)", "encoded_data")
                    if st.button("Salvar como CSV"):
                        try:
                            csv = st.session_state['df_transformado'].to_csv(index=False)
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name=f"{output_name}.csv",
                                mime="text/csv"
                            )
                            st.success(f"Arquivo '{output_name}.csv' pronto para download!")
                        except Exception as e:
                            st.error(f"Erro ao salvar o arquivo: {e}")



    with tab4:
        col1, col2d, col3d, col4 = st.columns([1, 8, 8, 1])
        if 'df' not in st.session_state:
            with col2d:
                st.warning("Por favor, faça upload de um arquivo na aba Data Analysis primeiro!")
        else:
            df = st.session_state['df'].copy()  # Criamos uma cópia para modificações
            with col2d:
                st.header("Data Visualization")
                
                # Input opcional de CSV
                st.subheader("Upload Opcional")
                uploaded_file = st.file_uploader("Carregar outro CSV (opcional)", type=['csv'], key="viz_upload")
                if uploaded_file is not None:
                    try:
                        df_viz = pd.read_csv(uploaded_file)
                        st.success("Arquivo carregado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao carregar o arquivo: {e}")
                else:
                    # Usar df_transformado por padrão, se disponível
                    if 'df_transformado' in st.session_state:
                        df_viz = st.session_state['df_transformado']
                        st.info("Usando o dataframe transformado da aba Encoding Data")
                    elif 'df' in st.session_state:
                        df_viz = st.session_state['df']
                        st.info("Usando o dataframe original (não transformado)")
                    else:
                        st.warning("Nenhum dataframe disponível. Faça upload na aba Data Analysis ou use o upload opcional.")
                        df_viz = None

                # Se houver um dataframe para visualizar
                if df_viz is not None:
                    # Seleção de tipo de gráfico
                    chart_type = st.selectbox(
                        "Escolha o tipo de gráfico:",
                        ["Boxplot", "Heatmap", "Histograma", "Scatter Plot", "Count Plot"]
                    )

                    # Configurações comuns
                    numeric_cols = ['User_ID', 'User_Text', 'Sentiment_Label', 'Recommended_Song_ID', 
                                'Song_Name', 'Artist', 'Genre', 'Tempo (BPM)', 'Mood', 'Energy', 'Danceability']

            with col3d:
                if df_viz is not None:
                    st.subheader("Visualização")

                    # Boxplot
                    if chart_type == "Boxplot":
                        col_to_plot = st.selectbox("Selecione a coluna:", numeric_cols, index=7)  # Default: Tempo (BPM)
                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.boxplot(data=df_viz, y=col_to_plot, ax=ax)
                        ax.set_title(f"Boxplot de {col_to_plot}")
                        st.pyplot(fig)

                    # Heatmap
                    elif chart_type == "Heatmap":
                        st.write("Correlação entre variáveis numéricas")
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(df_viz[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                        ax.set_title("Mapa de Calor - Correlação")
                        st.pyplot(fig)

                    # Histograma
                    elif chart_type == "Histograma":
                        col_to_plot = st.selectbox("Selecione a coluna:", numeric_cols, index=7)  # Default: Tempo (BPM)
                        bins = st.slider("Número de bins:", 5, 50, 20)
                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.histplot(data=df_viz, x=col_to_plot, bins=bins, ax=ax)
                        ax.set_title(f"Histograma de {col_to_plot}")
                        st.pyplot(fig)

                    # Scatter Plot
                    elif chart_type == "Scatter Plot":
                        x_col = st.selectbox("Eixo X:", numeric_cols, index=7)  # Default: Tempo (BPM)
                        y_col = st.selectbox("Eixo Y:", numeric_cols, index=9)  # Default: Energy
                        hue_col = st.selectbox("Coluna para cor (opcional):", ["Nenhum"] + numeric_cols, index=4)  # Default: Song_Name
                        fig, ax = plt.subplots(figsize=(8, 6))
                        if hue_col == "Nenhum":
                            sns.scatterplot(data=df_viz, x=x_col, y=y_col, ax=ax)
                        else:
                            sns.scatterplot(data=df_viz, x=x_col, y=y_col, hue=hue_col, ax=ax)
                        ax.set_title(f"Scatter: {x_col} vs {y_col}")
                        st.pyplot(fig)

                    # Count Plot
                    elif chart_type == "Count Plot":
                        col_to_plot = st.selectbox("Selecione a coluna:", numeric_cols, index=6)  # Default: Genre
                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.countplot(data=df_viz, x=col_to_plot, ax=ax)
                        ax.set_title(f"Contagem de {col_to_plot}")
                        plt.xticks(rotation=45)
                        st.pyplot(fig)


if __name__ == '__main__':
    main()