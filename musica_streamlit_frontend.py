import streamlit as st

from Pacote_Frontend.stream_tab_1 import *
from Pacote_Frontend.stream_tab_2 import * 
from Pacote_Frontend.stream_tab_3 import * 
from Pacote_Frontend.stream_tab_4 import *
from Pacote_Frontend.stream_tab_5 import *

# Configuração inicial da página
st.set_page_config(page_title="Data Processing App", layout="wide")

# Função principal
def main():
    # Criação das tabs
    tab1, tab2, tab3, tab4, tab5= st.tabs([
        "Data Analysis", 
        "Data Cleaning", 
        "Encoding Data", 
        "Data Visualization",
        "Data Resume"
    ])

    # Tab Data Analysis
    with tab1:
        Tab_Data_Analysis()

    # As outras tabs permanecem vazias por enquanto
    with tab2:
        Tab_Data_Cleaning()
        
    with tab3:
        Tab_Encoding_Data()

    with tab4:
        Tab_Data_Visualization()
    
    with tab5:
        Tab_Data_Resume()


if __name__ == '__main__':
    main()