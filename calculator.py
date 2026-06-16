import streamlit as st
import pandas as pd
from datetime import datetime


# Constantes
BEER_PRICE = 3
WATER_PRICE = 2
COCTEL_PRICE = 4
REFRESCO_PRICE = 3
FILENAME = "ventas_nomadart_vol4.csv"


# 1. INICIALIZAR LA MEMORIA
if "ventas" not in st.session_state:
        st.session_state.ventas = pd.DataFrame({
            "Timestamp": [],
            "Cervezas": [],
            "Botellas de agua": [],
            "Copas": [],
            "Refrescos": []
        })

if "total" not in st.session_state:
        st.session_state.total = 0




    # Título centrado utilizando HTML
st.markdown("<h1 style='text-align: center;'>Registro de Ventas</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("\n\n")
# 2. INPUTS
st.markdown("### **Cervezas** 🍺")
num_beers = st.radio("", list(range(0, 16)), horizontal=True)
st.markdown("### **Botellas de agua** 💧")
num_bottles_water = st.number_input("", min_value=0, value=0, step=1,key="agua")
st.markdown("### **Refrescos** 🥤")
num_refrescos = st.number_input("", min_value=0, value=0, step=1,key="refrescos")
st.markdown("### **Copas 🍸**")
num_coctels = st.number_input("", min_value=0, value=0, step=1,key="copas")

# 3. LÓGICA DE CÁLCULO
st.markdown("### Acciones de Venta")
col1, col2 = st.columns(2)

with col1:
    if st.button("Registrar venta 🧮", use_container_width=True):
        new_row = pd.DataFrame([{
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "Cervezas": num_beers,
                "Botellas de agua": num_bottles_water,
                "Copas": num_coctels,
                "Refrescos": num_refrescos
            }])
        
        st.session_state.ventas = pd.concat([st.session_state.ventas, new_row], ignore_index=True)
        suma = (num_beers * BEER_PRICE) + (num_bottles_water * WATER_PRICE) + (num_refrescos * REFRESCO_PRICE) + (num_coctels * COCTEL_PRICE)
            
        st.session_state.total += suma
        st.success(f"Venta registrada: {suma} €")
with col2:
        if st.button("Anular última venta ↩️", use_container_width=True):
            if not st.session_state.ventas.empty:
                last_row = st.session_state.ventas.iloc[-1]
                resta = (
                    (last_row["Cervezas"] * BEER_PRICE) + 
                    (last_row["Botellas de agua"] * WATER_PRICE) + 
                    (last_row["Refrescos"] * REFRESCO_PRICE) + 
                    (last_row["Copas"] * COCTEL_PRICE)
                )
                st.session_state.total -= resta
                st.session_state.ventas = st.session_state.ventas.iloc[:-1]
                st.warning("Última venta eliminada correctamente.")
                st.rerun()
            else:
                st.info("No hay ventas para anular.")


# 4. CIERRE DE CAJA
with st.sidebar:
        st.image("container.jpg")
        st.markdown("---")

        st.markdown("### Control de Caja")


        confirm = st.checkbox("Habilitar el cierre del contenedor")

        if confirm:
            st.subheader(f"Acumulado Total Histórico: {st.session_state.total} €")
            st.write("Historial de Ventas actual:")
            st.dataframe(st.session_state.ventas)
            
            st.download_button(label="Cerrar contenedor 💾",
                data=st.session_state.ventas.to_csv(index=False).encode('utf-8'),
                mime="text/csv",
                file_name= FILENAME,
                use_container_width=True)
