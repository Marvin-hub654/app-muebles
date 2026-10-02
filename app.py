import streamlit as st  # Importa la librería Streamlit para crear la app web
from pdf_presupuesto import generar_pdf_presupuesto
import inspect


# Configura la página: título en la pestaña y diseño centrado
st.set_page_config(page_title="Presupuesto Muebles", layout="wide",page_icon="🪚")
#LINEA SEPARADORA DE COLOR VERDE
st.markdown('<hr style="border:1px solid green">', unsafe_allow_html=True)
st.title("Cálculo de presupuesto - Muebles")  # Muestra el título principal de la app
#LINEA SEPARADORA DE COLOR VERDE
st.markdown('<hr style="border:1px solid green">', unsafe_allow_html=True)

#======================================================================================
#LISTA PIEZAS DEL MUEBLE
#crear una lista vacía llamada piezas y conservarla en la memoria temporal de Streamlit.
if "piezas" not in st.session_state:#comprueba si todavía no existe la variable
    st.session_state.piezas = []#crea una lista vacía si no existe.

total_pies = 0 # guarda el total de pies de madera calculada
total_metros = 0#guarda el total de metros cuadrados de madera calculada para pintar
total_madera_extra_feet = 0
#======================================================================================
#LISTA ACCESORIOS
if "accesorios" not in st.session_state:#comprueba si todavía no existe la variable
    st.session_state.accesorios = []#crea una lista vacía si no existe.

costo_parcial_accesorio = 0 #guarda el calculo de la cantidad de accesorios por su valor unitario
total_general_accesorios = 0 #guarda el total general de accesorios/herrajes
#======================================================================================
#Datos iniciales del proyecto
with st.container(border=True):
    col1,col2= st.columns(2)
    with col1:
        nombre_proyecto = st.text_input(label="Nombre del Proyecto",max_chars=50)
        nombre_proyecto = nombre_proyecto.title()#convierte la primer letra del nombre ingresado en mayuscula
    with col2:
        nombre_cliente = st.text_input(label="Nombre del Cliente",max_chars=50)
        nombre_cliente = nombre_cliente.title()

#=====================================================================================
#Medidas de la madera
#ST.FORM crea un cuadro 
with st.form("Formulario", clear_on_submit=True):
    nombre_pieza = st.text_input(label="Nombre de la pieza *",max_chars=30,)
    nombre_pieza = nombre_pieza.title()
    col1,col2,col3 = st.columns(3)
    with col1:
        largo_cm = st.number_input(label="Largo (cm) *",min_value=0.01,step=0.25)
    with col2:
        ancho_cm = st.number_input(label="Ancho (cm) *",min_value=0.01,step=0.25)
    with col3:
        espesor_pulg = st.number_input(label="Espesor (Pulgadas) *", min_value=0.01,step=0.25)
    agregar = st.form_submit_button("Agregar Pieza")
#==============================================================================
#Boton AGREGAR PIEZA
if agregar:
    if nombre_pieza and largo_cm > 0 and ancho_cm > 0 and espesor_pulg > 0:
        largo_pies = largo_cm/30.48 #convierte cms a pies
        ancho_pulg = ancho_cm/2.54 #concierte cms a pulgadas

        pies = (largo_pies*ancho_pulg*espesor_pulg)/12#calcula el total de pies de la pieza
        metros_cuadrados = (largo_cm*ancho_cm)/10000

        #Guarda la pieza como diccionario en la lista de la sesion (st.session_state.piezas = [])
        st.session_state.piezas.append({
            "pieza":nombre_pieza,
            "Largo (cm)":largo_cm,
            "Ancho (cm)":ancho_cm,
            "Espesor (pulg)":espesor_pulg,
            "Total Parcial(ft)" : pies,
            "Metros^2" : metros_cuadrados
        })

        st.success(f"Pieza: {nombre_pieza}, agregada correctamente")
    else:
        st.warning("Completa todos los valores obligatorios marcados con (*)")

#=======================================================================================
#si ya hay piezas guardadas se muestra el resumen
if "cambios_piezas" not in st.session_state:
    st.session_state.cambios_piezas = False

    #Funcion detectar cambios
def activar_guardado():
    st.session_state.cambios_piezas = True
        
st.subheader(body="Resumen")

if st.session_state.piezas:
    datos_editados = st.data_editor(st.session_state.piezas,
                     use_container_width=True,on_change=activar_guardado)#muestra la lista de piezas en una tabla

#Boton Guardar
    if st.button(label="Guardar Cambios",disabled=not st.session_state.cambios_piezas):
        for pieza in datos_editados:
            largo_pies = pieza["Largo (cm)"]/30.48
            ancho_pulg = pieza["Ancho (cm)"]/2.54
            espesor_pulg = pieza["Espesor (pulg)"]

            pies = (largo_pies*ancho_pulg*espesor_pulg)/12
            metros_cuadrados = (pieza["Largo (cm)"]*pieza["Ancho (cm)"])/10000

            pieza["Total Parcial(ft)"] = round(pies,2)
            pieza["Metros^2"] = round(metros_cuadrados,2)

        st.session_state.piezas = datos_editados
        st.session_state.cambios_piezas = False
        st.success("Cambios Guardados")
        st.rerun()

    total_pies = sum(pieza["Total Parcial(ft)"] for pieza in st.session_state.piezas)
    total_metros = sum(pieza["Metros^2"] for pieza in st.session_state.piezas)


#=================================================================================
#dividiendo en 4 columnas para:
    col1,col2,col3,col4= st.columns(4)
    with col1:
        st.write(f"Pies Acumulados:")# pies acumulados parcial
        st.info(f"## {total_pies:.2f}")
    with col2:#porcentajes de pies extras por imprevistos
        feet_madera_extra = st.number_input(label="% Madera extra por imprevistos",min_value=0.0,max_value=100.0,value=0.0,step=1.0,format="%.0f")
    with col3:#cantidad de pies extras obtenidos del porcentaje anterior ingresado por el usuario
        total_madera_extra_feet = (total_pies * feet_madera_extra)/100
        st.write(f"Madera Extra:")
        st.info(f"## {total_madera_extra_feet:.2f} ")
    with col4:#gran total de pies de madera
        total_final_madera = total_pies + total_madera_extra_feet
        st.write(f"Total final pies:")
        st.success(f"## {total_final_madera:.2f}")

    if st.button(label="Limpiar Lista"):
        st.session_state.piezas = []
        st.rerun() #recarga la app para limpiar la pantalla

#===============================================================================
col1,col2 = st.columns(2)

with col1:
    precio_pie = st.number_input(label="Precio del feet",min_value=0.5,step=0.5)
with col2:
    costo_total_madera = precio_pie * (total_pies+total_madera_extra_feet)
    st.warning(f"### Costo total en madera:     Q{costo_total_madera:.2f}")

#===============================================================================
#calculo de metros cuadrados
#col1,col2,col3
st.write("Metros cuadrados acumulados")
st.info(f"## {total_metros:.2f}")

#LINEA SEPARADORA DE COLOR AMARILLO
st.markdown('<hr style="border:1px solid yellow">', unsafe_allow_html=True)


#===============================================================================
#CÁLCULO DE TINTES
with st.container(border=True):
    st.subheader(body="Cálculo de Tinte")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        precio_tinte = st.number_input(label="Precio tinte/litro(Q)",min_value=0.1,step=0.10)
    with col2:
        rendimiento_litro_tinte = st.number_input(label="Rendimiento m2/Litro",min_value=0.1,step=0.10)
    with col3:
        litros_usados_tinte = (total_metros/rendimiento_litro_tinte)*.75# se calcula que un 78% de tinte se usa ya que los muebles no se pintan por todas sus caras
        st.write(f"Litros Usados:")
        st.write(f"{litros_usados_tinte:.2f}")
    with col4:
        Costo_tintes = precio_tinte*litros_usados_tinte
        st.write("### Costo Tintes")
        st.warning(f"####           Q{Costo_tintes:.2f}")

#LINEA SEPARADORA DE COLOR AMARILLO
st.markdown('<hr style="border:1px solid yellow">', unsafe_allow_html=True)


#===================================================================
#CALCULO DEL COSTO DEL SELLADOR Y TINER
#===================================================================
#SELLADOR
with st.container(border=True):
    st.subheader(body="Cálculo de Sellador y Tiner")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        precio_sellador_galon = st.number_input(label="Precio Sellador (gl)",min_value=1,step=1,key="precio_sellador_galon")
    with col2:
        rendimiento_sellador_litro= st.number_input(label="Rendimiento m2/litro",min_value=1,step=1,key="rendimiento_sellador")
    with col3:
        total_metros = float(total_metros)
        rendimiento_sellador_litro = float(rendimiento_sellador_litro)

        #if rendimiento_sellador_litro >0:
        litros_usados_sellador = (total_metros*2)/rendimiento_sellador_litro#se multiplican los metros cuadrados por 2 porque el sellador se aplica por los dos lados de la tabla no importando que vaya en el interior el sellado
        st.write("Litros Usados")
        st.write(f"{litros_usados_sellador:.2f}")
        #else:
        #litros_usados_sellador = 0.0
        #st.warning("ERROR: El rendimiento del sellador debe ser mayor a 0")

    with col4:
        precio_sellador_litro = precio_sellador_galon/4 #cada galon tiene 4 litros, convirtiento precio galon a precio litros
        costo_final_sellador = precio_sellador_litro*litros_usados_sellador
        st.write("Costo Sellador")
        st.write(f"####   Q{costo_final_sellador:.2f}")

#TINER
with st.container(border=True):
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        precio_tiner_galon = st.number_input(label="Precio Tiner(gl)",min_value=1,step=1,key="tiner_sellador")
    with col2:
        st.write("Litros Tiner a Utilizar")
        litros_tiner_usar= litros_usados_sellador *2# se usa el doble de sellador formula 2 de tiner por 1 de sellador
        st.write(f"{litros_tiner_usar:.2f}")
    with col3:
        precio_tiner_litro = precio_tiner_galon/3.785411784 # 3.78.. litros tiene el galon de tiner, convirtiendo precio de galon tiner a precio litro tiner
        costo_final_tiner_sellador= litros_tiner_usar*precio_tiner_litro
        st.write("Costo Tiner")
        st.write(f"#### {costo_final_tiner_sellador:.2f}")
    with col4:
        suma_sellador_mas_tiner = costo_final_sellador+costo_final_tiner_sellador
        st.write("### Costo Sellador+Tiner")
        st.warning(f"#### {suma_sellador_mas_tiner:.2f}")

#LINEA SEPARADORA DE COLOR AMARILLO
st.markdown('<hr style="border:1px solid yellow">', unsafe_allow_html=True)


#========================================================================================
#CALCULO DEL COSTO DEL ACABADO Y TINER
#=======================================================================================
#ACABADO
with st.container(border=True):
    st.subheader(body="Cálculo de Acabado y Tiner")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        precio_acabado_galon = st.number_input(label="Precio Acabado (gl)",min_value=1,step=1,key="precio_acabado_galon")
    with col2:
        rendimiento_acabado_litro= st.number_input(label="Rendimiento m2/litro",min_value=1,step=1,key="rendimiento_acabado")
    with col3:
        litros_usados_acabado = (total_metros)/rendimiento_acabado_litro#generalmente el acabado solo se aplica a las partes visibles del mueble, por eso no me multiplican los metros cuadrados por 2
        st.write("Litros Usados")
        st.write(f"{litros_usados_acabado:.2f}")
    with col4:
        precio_acabado_litro = precio_acabado_galon/4 #cada galon tiene 4 litros, convirtiento precio galon a precio litros
        costo_final_acabado = precio_acabado_litro*litros_usados_acabado
        st.write("Costo Acabado")
        st.write(f"####   Q{costo_final_acabado:.2f}")

#TINER
with st.container(border=True):
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        precio_tiner_galon2 = st.number_input(label="Precio Tiner(gl)",min_value=1,step=1,key="tiner_acabado")
    with col2:
        st.write("Litros Tiner a Utilizar")
        litros_tiner_usar2= litros_usados_acabado# formula 1 a 1 para el acabado
        st.write(f"{litros_tiner_usar2:.2f}")
    with col3:
        precio_tiner_litro2 = precio_tiner_galon2/3.785411784 # 3.78.. litros tiene el galon de tiner, convirtiendo precio de galon tiner a precio litro tiner
        costo_final_tiner_acabado= litros_tiner_usar2*precio_tiner_litro2
        st.write("Costo Tiner")
        st.write(f"#### {costo_final_tiner_acabado:.2f}")
    with col4:
        suma_acabado_mas_tiner = costo_final_acabado+costo_final_tiner_acabado
        st.write("### Costo Acabado+Tiner")
        st.warning(f"#### {suma_acabado_mas_tiner:.2f}")

#===============================================================================
#===============================================================================
#CALCULO DE HERRAJES Y MATERIALES AUXILIARES
#LINEA SEPARADORA DE COLOR ROJO
st.markdown('<hr style="border:1px solid red">', unsafe_allow_html=True)

#ST.FORM crea un cuadro 
st.subheader("Cálculo de Accesorios/Herrajes")
with st.form("Formulario_accesorios", clear_on_submit=True):
    nombre_accesorio = st.text_input(label="Nombre del Accesorio/Herraje *",max_chars=50,key="nombre_accesorio")
    nombre_accesorio= nombre_accesorio.title()
    col1,col2 = st.columns(2)
    with col1:
        precio_unit_accesorio = st.number_input(label="Precio Unitario *",min_value=0.25,step=0.25,key="precio_unit_accesorio")
    with col2:
        cantidad_accesorio = st.number_input(label="Cantidad *",min_value=1,step=1,key="cantidad_accesorio")
    #with col3:
        #total_parcial_accesorio = st.number_input(label="Espesor (Pulgadas) *", min_value=0.01,step=0.25)
    agregar_accesorio = st.form_submit_button("Agregar Accesorio/Herraje",key="agregar_accesorio")
#==============================================================================
#BOTON AGREGAR ACCESORIOS
if agregar_accesorio:
    if nombre_accesorio and precio_unit_accesorio > 0 and cantidad_accesorio > 0:

        costo_parcial_accesorio = precio_unit_accesorio * cantidad_accesorio

        #Guarda el accesorio como diccionario en la lista de la sesion (st.session_state.accesorio = [])
        st.session_state.accesorios.append({
            "Accesorio":nombre_accesorio,
            "Precio Unitario":precio_unit_accesorio,
            "Cantidad":cantidad_accesorio,
            "Total Parcial Accesorio" : round(costo_parcial_accesorio,2),
        })

        st.success(f"Accesorio/Herraje: {nombre_accesorio}, agregada correctamente")
    else:
        st.warning("Completa todos los valores obligatorios marcados con (*)")

#=======================================================================================
#si ya hay piezas guardadas se muestra el resumen
if "cambios_accesorios" not in st.session_state:
    st.session_state.cambios_accesorios = False

    #Funcion detectar cambios
def activar_guardado_accesorio():
    st.session_state.cambios_accesorios = True
        
st.subheader(body="Resumen Accesorios/Herrajes")

if st.session_state.accesorios:
    datos_editados_accesorios = st.data_editor(st.session_state.accesorios,
                     use_container_width=True,on_change=activar_guardado_accesorio)#muestra la lista de accesorios/herrajes en una tabla

#BOTON GUARDAR ACCESORIOS=====================================================================
    if st.button(label="Guardar Cambios Accesorios/Herrajes",disabled=not st.session_state.cambios_accesorios,key="guardar_cambios_accesorios"):
        
        for accesorio in datos_editados_accesorios:

            #Recalcular el total parcial
            precio_acc = accesorio["Precio Unitario"]
            cantidad_acc = accesorio["Cantidad"]

            total_acc = precio_acc * cantidad_acc

            accesorio["Total Parcial Accesorio"] = round(total_acc,2)

#GUARDAMOS LOS DATOS MODIFICADOS
        st.session_state.accesorios = datos_editados_accesorios
        st.session_state.cambios_accesorios = False
        st.success("Cambios de Accesorios/Herrajes guardados correctamente")
        st.rerun()

    total_general_accesorios = sum(accesorio["Total Parcial Accesorio"] for accesorio in st.session_state.accesorios)

st.warning(f"## Costo total Accesorios/Herrajes:    Q.{total_general_accesorios:.2f}")

if st.button(label="Limpiar Lista",key="limpiar_lista_accesorios"):
    st.session_state.accesorios = []
    st.rerun() #recarga la app para limpiar la pantalla
#===============================================================================
#===============================================================================
#CALCULO TOTAL DE MADERA, ACCESORIOS Y GANANCIA

#LINEA SEPARADORA DE COLOR AZUL
st.markdown('<hr style="border:1px solid blue">', unsafe_allow_html=True)
st.subheader("Cálculo de ganancia sobre madera, tinte,barnices y accesorios/herrajes")
col1,col2,col3,col4 = st.columns(4)
with col1:
    total_sin_ganancia = costo_total_madera+Costo_tintes+suma_sellador_mas_tiner+suma_acabado_mas_tiner+total_general_accesorios
    st.warning(f"Total sin Ganancia: Q{total_sin_ganancia:.2f}")
with col2:
    porcentaje_ganancia = st.number_input(label="Ingresa % Ganancia",min_value=1,step=1,key="porcentaje_ganancia",format="%.0f")
with col3:
    cantidad_ganancia = (total_sin_ganancia*porcentaje_ganancia)/100
    st.info(f"##### Ganancia: Q{cantidad_ganancia:.2f}")
with col4:
    total_con_ganancia = total_sin_ganancia+cantidad_ganancia
    st.warning(f"###### Total con Ganancia: Q{total_con_ganancia:.2f}") 

st.markdown('<hr style="border:1px solid blue">', unsafe_allow_html=True)

#===============================================================================
#===============================================================================
#CALCULO TOTAL DE MANO DE OBRA

st.subheader("Mano de Obra")
col1,col2,col3 = st.columns(3)
with col1:
    dias_laborados = st.number_input(label="Dias Laborados",min_value=1,step=1,key="dias_laborados")
with col2:
    sueldo_diario = st.number_input(label="Sueldo Diario (Q)",min_value=1,step=1,key="sueldo_diario")
with col3:
    total_mano_obra = dias_laborados*sueldo_diario
    st.warning(f"Total Mano de Obra: Q{total_mano_obra:.2f}")
#===============================================================================
#===============================================================================
#FLETE
st.subheader("Flete")
col1,col2 = st.columns(2)
with col1:
    flete = st.number_input(
        label="Costo del Flete (Q)",
        min_value=0.0,
        step=10.0,
        key="flete"
    )
with col2:
    st.warning(f"Total Flete: Q{flete:.2f}")


#===============================================================================
#===============================================================================
#TOTAL FINAL DEL PROYECTO
st.markdown('<hr style="border:1px solid violet">', unsafe_allow_html=True)
total_proyecto = total_con_ganancia+total_mano_obra+flete

st.success(f"# COSTO TOTAL DEL PROYECTO: Q.{total_proyecto:.2f}")

#===============================================================================
#===============================================================================
#BOTON GENERAR PDF
 
# ============================================================
# DESCARGAR PRESUPUESTO EN PDF
# ============================================================

st.markdown("---")
st.subheader("Descargar presupuesto")

pdf_presupuesto = generar_pdf_presupuesto(
    nombre_proyecto=nombre_proyecto,
    nombre_cliente=nombre_cliente,

    piezas=st.session_state.piezas,
    accesorios=st.session_state.accesorios,

    total_pies=total_pies,
    total_metros=total_metros,

    costo_total_madera=costo_total_madera,

    precio_tinte=precio_tinte,
    litros_usados_tinte=litros_usados_tinte,
    Costo_tintes=Costo_tintes,

    litros_usados_sellador=litros_usados_sellador,
    costo_final_sellador=costo_final_sellador,
    litros_tiner_usar=litros_tiner_usar,
    costo_final_tiner_sellador=costo_final_tiner_sellador,
    suma_sellador_tiner=suma_sellador_mas_tiner,

    litros_usados_acabado=litros_usados_acabado,
    costo_final_acabado=costo_final_acabado,
    litros_tiner_usar2=litros_tiner_usar2,
    costo_final_tiner_acabado=costo_final_tiner_acabado,
    suma_acabado_tiner=suma_acabado_mas_tiner,

    total_general_accesorios=total_general_accesorios,

    total_sin_ganancia=total_sin_ganancia,
    porcentaje_ganancia=porcentaje_ganancia,
    cantidad_ganancia=cantidad_ganancia,
    total_con_ganancia=total_con_ganancia,

    dias_laborados=dias_laborados,
    sueldo_diario=sueldo_diario,
    total_mano_obra=total_mano_obra,
    flete=flete,

    total_proyecto=total_proyecto,

    # Datos adicionales de madera
    precio_pie=precio_pie,
    feet_madera_extra=(
        feet_madera_extra
        if st.session_state.piezas else 0
    ),
    total_madera_extra_feet=(
        total_madera_extra_feet
        if st.session_state.piezas else 0
    ),
    total_final_madera=(
        total_final_madera
        if st.session_state.piezas else total_pies
    )
)

st.download_button(
    label="📄 Descargar Presupuesto PDF",
    data=pdf_presupuesto,
    file_name="Presupuesto_Muebles.pdf",
    mime="application/pdf",
    key="descargar_presupuesto_pdf"
)

