import streamlit as st
import pandas as pd
from datetime import datetime


# Constantes
BEER_PRICE = 4
WATER_PRICE = 2
COCTEL_PRICE = 7
REFRESCO_PRICE = 3
GLASS_PRICE = 1
BEER_DISCOUNT = 0.25
COCTEL_DISCOUNT = 0.5
FILENAME = "ventas_nomadart_vol5.csv"
DRINK_LIMIT = 16



def make_breakdown_message(breakdown:dict):
     message = ""
     for item,amount in breakdown.items():
          if amount:
               message += f"{item}: {amount}  \n"
     return message
    
     

def register_item():
    num_beers = st.session_state["num_beers"]
    num_water = st.session_state["num_water"]
    num_refrescos = st.session_state["num_refrescos"]
    num_copas = st.session_state["num_copas"]
    num_vasos = st.session_state["num_vasos"]
    num_vasos_devueltos=st.session_state["num_vasos_devueltos"]

    suma = (num_beers * st.session_state.beer_price) + (num_water * WATER_PRICE) + (num_refrescos * REFRESCO_PRICE) + (num_copas* st.session_state.coctel_price) + num_vasos*GLASS_PRICE - num_vasos_devueltos*GLASS_PRICE 
    breakdown = {"Cervezas": num_beers,
                "Botellas de agua": num_water,
                "Copas": num_copas,
                "Refrescos": num_refrescos,
                "Vasos":num_vasos,
                "Vasos_devueltos":num_vasos_devueltos}
    new_row = pd.DataFrame([{
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                **breakdown,
                "Venta(€)":suma,
            }])
    st.session_state.ventas = pd.concat([st.session_state.ventas, new_row], ignore_index=True)
    st.session_state.total += suma
    st.session_state["mensaje_venta"]=f"Venta registrada: {suma} €"
    st.session_state["desglose"]=make_breakdown_message(breakdown)
    
    # Reiniciar contadores
    st.session_state["num_beers"] = 0
    st.session_state["num_water"] = 0
    st.session_state["num_copas"] = 0
    st.session_state["num_vasos"] = 0
    st.session_state["num_vasos_devueltos"] = 0
    st.session_state["num_refrescos"] = 0




# 1. INICIALIZAR LA MEMORIA
if "beer_price" not in st.session_state:
      st.session_state.beer_price = BEER_PRICE
if "coctel_price" not in st.session_state:
      st.session_state.coctel_price = COCTEL_PRICE

if "ventas" not in st.session_state:
        st.session_state.ventas = pd.DataFrame({
    "Timestamp": [],
    "Cervezas": [],
    "Botellas de agua": [],
    "Copas": [],
    "Refrescos": [],
    "Vasos": [],
    "Vasos_devueltos": [],
    "Venta(€)": []
}).astype({
    "Timestamp": "datetime64[ns]",  # Define el tipo de fecha/tiempo
    "Cervezas": "int",
    "Botellas de agua": "int",
    "Copas": "int",
    "Refrescos": "int",
    "Vasos": "int",
    "Vasos_devueltos": "int",
    "Venta(€)": "float"             # Define el tipo numérico para dinero
})
if "total" not in st.session_state:
        st.session_state.total = 0



#st.markdown("---")

# 2. INPUTS
title_size="####"
st.markdown(
    """
    <style>
    /* Apuntar directamente al contenedor del texto dentro de los botones de las pestañas */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        font-size: 25px !important;  /* Ajusta los píxeles según lo que necesites */
        font-weight: 500;            /* Opcional: define el grosor de la letra */
    </style>
    """,
    unsafe_allow_html=True
)
tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs(["🍺", "🍸", "💧", "🥤", "Vasos devueltos","Vasos"])

with tab1:
    st.radio("Cervezas",list(range(0, DRINK_LIMIT)), horizontal=True,key="num_beers")
with tab2:
     st.radio("Copas", list(range(0, DRINK_LIMIT)), horizontal=True,key="num_copas")
with tab3:
    st.radio("Agua", list(range(0, DRINK_LIMIT)), horizontal=True,key="num_water")
with tab4:
    st.radio("Refrescos", list(range(0, DRINK_LIMIT)), horizontal=True,key="num_refrescos")
with tab5:
    st.radio("Vasos devueltos", list(range(0, DRINK_LIMIT)), horizontal=True,key="num_vasos_devueltos")
with tab6:
    st.radio("Vasos", list(range(0, DRINK_LIMIT)), horizontal=True,key="num_vasos")




# 3. LÓGICA DE CÁLCULO
st.markdown("### Acciones de Venta")
col1, col2 = st.columns(2)

with col1:
    st.button("Registrar venta 🧮", use_container_width=True,on_click=register_item)
    if "mensaje_venta" in st.session_state:
        st.success(st.session_state["mensaje_venta"])
        del st.session_state["mensaje_venta"]
    if "desglose" in st.session_state:
        st.success(st.session_state["desglose"])
        del st.session_state["desglose"]
         
        
        
with col2:
        if st.button("Anular última venta ↩️", use_container_width=True):
            if not st.session_state.ventas.empty:
                last_row = st.session_state.ventas.iloc[-1]
                st.session_state.total -= last_row["Venta(€)"]
                st.session_state.ventas = st.session_state.ventas.iloc[:-1]
                st.warning("Última venta eliminada correctamente.")
                st.rerun()
            else:
                st.info("No hay ventas para anular.")


# 4. CIERRE DE CAJA Y DESCUENTOS
with st.sidebar:
        st.image("container.jpg")
        st.markdown("---")

        st.markdown("### Descuentos")
        if st.checkbox(f"Aplicar {int(BEER_DISCOUNT*100)}% dto a cervezas"):
            st.session_state.beer_price = BEER_PRICE - BEER_PRICE*BEER_DISCOUNT
        else:
            st.session_state.beer_price = BEER_PRICE
        if st.checkbox(f"Aplicar {int(COCTEL_DISCOUNT*100)}% dto a copas"):
            st.session_state.coctel_price = COCTEL_PRICE - COCTEL_PRICE*COCTEL_DISCOUNT
        else:
            st.session_state.coctel_price = COCTEL_PRICE
        

        st.markdown("### Control de Caja")


        confirm = st.checkbox("Abrir contenedor")

        if confirm:
            st.subheader(f"Acumulado Total Histórico: {st.session_state.total} €")
            st.write("Últimas 5 ventas:")
            st.dataframe(st.session_state.ventas.tail())
            
            st.download_button(label="Cerrar contenedor 💾",
                data=st.session_state.ventas.to_csv(index=False).encode('utf-8'),
                mime="text/csv",
                file_name= FILENAME,
                use_container_width=True)
