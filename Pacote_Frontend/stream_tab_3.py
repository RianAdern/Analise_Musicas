import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.preprocessing import MultiLabelBinarizer

def Tab_Encoding_Data():
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