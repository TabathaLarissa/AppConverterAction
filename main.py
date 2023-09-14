import streamlit as st
from page_conversor import converter
from page_transp import transpose_excel
from streamlit_option_menu import option_menu

def main():
    # Movemos a leitura do CSS para a função principal para evitar que ele seja aplicado na tela de inicialização
    with open("stylet.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # O menu estará dentro do sidebar, então ele será renderizado corretamente
    with st.sidebar:
        st.image("Logoapp.png")
        selected = option_menu('', ['Converter Formato', 'Transpor Arquivo'], 
            icons=['file-earmark-arrow-down-fill', 'arrow-left-right'], menu_icon=" ", default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "#FFC000", "font-size": "22px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "font-family": "Segoe UI, sans-serif"},
                "nav-link-selected": {"background-color": "#333333"},
            }
        )
        
        # Agora as páginas são chamadas após o menu
    if selected == 'Converter Formato':
        converter()
    elif selected == 'Transpor Arquivo':
        transpose_excel()

if __name__ == '__main__':
    main()
