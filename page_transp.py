import streamlit as st
import pandas as pd
import os
import base64

def get_file(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label} File</a>'
    return href

def transpose_excel():
    st.title("Transpor Arquivos")
    
    uploaded_file = st.file_uploader("Arraste seu arquivo Excel ou clique para selecionar", type=['xls', 'xlsx'])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write('Prévia do arquivo:')
        st.dataframe(df.head())
        
        transpose_source = st.radio("Você deseja transpor a partir de:", ("Colunas", "Linhas"))
        transpose_destination = st.radio("Você deseja transpor para:", ("Linhas", "Colunas"))

        if transpose_source == "Colunas":
            to_transpose = st.multiselect('Escolha as colunas que deseja transpor', df.columns)
        else:
            to_transpose = st.multiselect('Escolha as linhas que deseja transpor', df.index)

        if st.button('Transpor'):
            if not to_transpose:
                st.warning("Por favor, selecione pelo menos uma linha ou coluna para transpor.")
                return

            # Verificação de colunas duplicadas
            if df.columns.duplicated().any():
                st.error("Erro: Seu arquivo contém colunas com nomes duplicados.")
                return

            if transpose_source == "Colunas" and transpose_destination == "Linhas":
                id_vars_cols = [col for col in df.columns if col not in to_transpose]

                # Verifique se as colunas existem
                if not set(id_vars_cols).issubset(df.columns) or not set(to_transpose).issubset(df.columns):
                    st.error("Erro: Algumas colunas selecionadas não estão presentes no arquivo.")
                    return

                transposed_data = df.melt(id_vars=id_vars_cols,
                                          value_vars=to_transpose,
                                          var_name="TransposedColumns",
                                          value_name="Values")
                st.dataframe(transposed_data.head())

            elif transpose_source == "Linhas" and transpose_destination == "Colunas":
                transposed_data = df.loc[to_transpose, :].transpose()
                st.dataframe(transposed_data.head())

            else:
                st.warning("A transposição escolhida não altera o formato. Por favor, escolha opções diferentes.")
                return

            file_name = "transposed_file.xlsx"
            transposed_data.to_excel(file_name, index=True)

            st.success('Arquivo Transposto com Sucesso!')
            st.markdown(get_file(file_name, file_label=file_name), unsafe_allow_html=True)
            st.markdown("Se precisar novamente no futuro, **volte aqui** que estarei feliz em te ajudar! 😉")

            # Apague o arquivo após disponibilizá-lo para download
            os.remove(file_name)
