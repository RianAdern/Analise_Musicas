import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

def Tab_Data_Visualization():
    col1, col2d, col3d, col4 = st.columns([1, 8, 8, 1])
    
    if 'df' not in st.session_state:
        with col2d:
            st.warning("Por favor, faça upload de um arquivo na aba Data Analysis primeiro!")
    else:
        df = st.session_state['df'].copy()  # Criamos uma cópia inicial (não usada diretamente)
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
                chart_type = st.selectbox(
                    "Escolha o tipo de gráfico:",
                    ["Boxplot", "Heatmap", "Histograma", "Scatter Plot", "Count Plot"]
                )
                numeric_cols = ['User_ID', 'User_Text', 'Sentiment_Label', 'Recommended_Song_ID', 
                               'Song_Name', 'Artist', 'Genre', 'Tempo (BPM)', 'Mood', 'Energy', 'Danceability']

        with col3d:
            if df_viz is not None:
                st.subheader("Visualização")
                fig = None  # Variável para armazenar a figura atual

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

                # Botão único para salvar o gráfico selecionado
                if fig is not None:
                    default_name = f"{chart_type.lower().replace(' ', '_')}"
                    if chart_type == "Boxplot" or chart_type == "Histograma" or chart_type == "Count Plot":
                        default_name += f"_{col_to_plot}"
                    elif chart_type == "Scatter Plot":
                        default_name += f"_{x_col}_vs_{y_col}"
                    output_name = st.text_input("Nome do arquivo (sem extensão)", default_name)
                    if st.button("Salvar Gráfico Selecionado"):
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format="png", dpi=300, bbox_inches='tight')
                        buffer.seek(0)
                        st.download_button(
                            label="Download PNG",
                            data=buffer,
                            file_name=f"{output_name}.png",
                            mime="image/png"
                        )
                        st.success(f"Gráfico salvo como '{output_name}.png'!")