import streamlit as st
from faker import Faker
import pandas as pd

st.set_page_config(page_title="Faker Data", layout="wide")

st.title(":orange[FAKER DATA GENERATOR]")
st.divider()

with st.sidebar:
    st.subheader("Configura tu Faker Data")
    localization = st.selectbox("Idioma", options=["en_US", "es_ES", "fr_FR", "ar_AR", "it_IT", "ja_JP", "pt_BR", "zh_CN"], index=1)
    num_fields = st.number_input("Cantidad de campos", min_value=1,max_value=7,step=1)
    num_rows = st.number_input("Cantidad de filas", min_value=1,max_value=1000,step=1)

    fake = Faker(localization)

    faker_options = {
        "Name": fake.name,
        "Email": fake.email,
        "Address": fake.address,
        "Phone Number": fake.phone_number,
        "Job": fake.job,
        "Company": fake.company,
        "Birth": fake.date_of_birth
    }

    fields_selection = []

    st.write("Selecciona los campos:")

    for i in range(num_fields):
        field = st.selectbox(f"Campo {i + 1}",list(faker_options.keys()),key=f"id_{i}" )
        fields_selection.append(field)

if st.button("Generar Datos"):
    data={field: [faker_options[field]() for _ in range(num_rows)] for field in fields_selection} #se generan datos por num_rows guardados y se repite por cada campo seleccionado 
    
    data['id']=list(range(1,num_rows + 1))
    df = pd.DataFrame(data)
    column_order=['id'] + [col for col in df.columns if col != 'id']#se asegura que id sea la primera columna
    df=df[column_order] #reordena las columnas para que id sea la primera

    st.write("Datos Generados:")
    st.dataframe(df, use_container_width=True, hide_index=True)

    col1,col2 ,_= st.columns([1,1,8]) #se crean 3 columnas pero la tercera es mas grande para que los botones queden a la izquierda

    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV", data= csv, file_name="archivo.csv",mime="text/csv",type="primary"
        )
    with col2:
        json = df.to_json(orient="records",indent=4,force_ascii=False) #indent = espaciado para que sea mas legible, ascii false para que soporte caracteres especiales(ñ, acentos, etc)
        st.download_button(label="Descargar json",data=json,file_name="archivo.json",mime="aplication/json",type="primary")


