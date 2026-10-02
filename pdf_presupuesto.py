
from fpdf import FPDF
from pathlib import Path
from datetime import datetime


# ============================================================
# CLASE PARA EL PDF
# ============================================================

class PresupuestoPDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font(self.fuente, "", 8)
        self.set_text_color(110, 110, 110)

        self.cell(
            0, 8,
            f"Página {self.page_no()}",
            align="C"
        )


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================


def generar_pdf_presupuesto(
    nombre_proyecto,
    nombre_cliente,
    piezas,
    accesorios,
    total_pies,
    total_metros,
    costo_total_madera,
    precio_tinte,
    litros_usados_tinte,
    Costo_tintes,
    litros_usados_sellador,
    costo_final_sellador,
    litros_tiner_usar,
    costo_final_tiner_sellador,
    suma_sellador_tiner,
    litros_usados_acabado,
    costo_final_acabado,
    litros_tiner_usar2,
    costo_final_tiner_acabado,
    suma_acabado_tiner,
    total_general_accesorios,
    total_sin_ganancia,
    porcentaje_ganancia,
    cantidad_ganancia,
    total_con_ganancia,
    dias_laborados,
    sueldo_diario,
    total_mano_obra,
    flete,
    total_proyecto,
    precio_pie=0,
    feet_madera_extra=0,
    total_madera_extra_feet=0,
    total_final_madera=None
):

    # --------------------------------------------------------
    # CONFIGURACIÓN GENERAL
    # --------------------------------------------------------

    pdf = PresupuestoPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=20)

    # --------------------------------------------------------
    # CONFIGURACIÓN DE FUENTES
    # --------------------------------------------------------

    ruta_arial = Path("C:/Windows/Fonts/arial.ttf")
    ruta_arial_negrita = Path("C:/Windows/Fonts/arialbd.ttf")

    if ruta_arial.exists() and ruta_arial_negrita.exists():

        pdf.add_font(
            "ArialPersonalizada",
            "",
            str(ruta_arial)
        )

        pdf.add_font(
            "ArialPersonalizada",
            "B",
            str(ruta_arial_negrita)
        )

        fuente_normal = "ArialPersonalizada"

    else:
        fuente_normal = "Helvetica"

    pdf.fuente = fuente_normal

    # Si no se encuentra Arial, evitar caracteres
    # incompatibles con Helvetica.

    def texto(valor):
        valor = str(valor)

        if fuente_normal == "Helvetica":
            return valor.encode(
                "latin-1",
                errors="replace"
            ).decode("latin-1")

        return valor

    # --------------------------------------------------------
    # FUNCIONES AUXILIARES
    # --------------------------------------------------------

    def dinero(valor):
        return f"Q {float(valor):,.2f}"

    def salto(altura=5):
        pdf.ln(altura)

    def comprobar_espacio(altura=15):
        if pdf.get_y() + altura > pdf.page_break_trigger:
            pdf.add_page()

    def titulo_seccion(titulo):

        comprobar_espacio(20)

        pdf.set_fill_color(29, 78, 137)#color de fondo azul elegante
        pdf.set_draw_color(29, 78, 137)#color d texto
        pdf.set_text_color(255, 255, 255)  # CAMBIO: texto blanco sobre fondo azul

        pdf.set_font(fuente_normal, "B", 11)

        pdf.cell(
            0,
            10,
            texto(titulo),
            border=1,
            fill=True,
            new_x="LMARGIN",
            new_y="NEXT"
        )

        pdf.set_text_color(0, 0, 0)

        salto(3)

    def fila_resumen(concepto, importe, negrita=False):

        comprobar_espacio(9)

        estilo = "B" if negrita else ""

        pdf.set_font(fuente_normal, estilo, 10)

        pdf.cell(
            125,
            8,
            texto(concepto)
        )

        pdf.cell(
            55,
            8,
            dinero(importe),
            align="R",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    def fila_dato(concepto, valor):

        comprobar_espacio(8)

        pdf.set_font(fuente_normal, "", 10)

        pdf.cell(
            115,
            8,
            texto(concepto)
        )

        pdf.cell(
            65,
            8,
            texto(valor),
            align="R",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    def encabezado_tabla(columnas, anchos):

        pdf.set_fill_color(29, 78, 137) #fondo azul de los encabezados
        pdf.set_text_color(255, 255, 255)#texto blanco sobre el fondo azul
        pdf.set_font(fuente_normal, "B", 9)

        for columna, ancho in zip(columnas, anchos):

            pdf.cell(
                ancho,
                9,
                texto(columna),
                border=1,
                fill=True,
                align="C"
            )

        pdf.ln()

        pdf.set_text_color(0, 0, 0)

    def fila_tabla(valores, anchos, alineaciones=None):

        comprobar_espacio(9)

        pdf.set_font(fuente_normal, "", 9)

        if alineaciones is None:
            alineaciones = ["L"] * len(valores)

        for valor, ancho, alineacion in zip(
            valores,
            anchos,
            alineaciones
        ):

            pdf.cell(
                ancho,
                8,
                texto(valor),
                border=1,
                align=alineacion
            )

        pdf.ln()

    # --------------------------------------------------------
    # CREAR PÁGINA
    # --------------------------------------------------------

    pdf.add_page()

    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    pdf.set_font(fuente_normal, "B", 19)
    pdf.set_text_color(29, 78, 137)  # CAMBIO: título azul elegante

    pdf.cell(
        0,
        13,
        "PRESUPUESTO DE MUEBLES",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_draw_color(29, 78, 137)#bordes de las tablas en azul
    pdf.set_line_width(0.7)

    pdf.line(
        15,
        pdf.get_y(),
        195,
        pdf.get_y()
    )

    pdf.set_text_color(0, 0, 0)#volver a negro despues de los encabezados

    salto(7)

    # --------------------------------------------------------
    # DATOS DEL PROYECTO
    # --------------------------------------------------------

    pdf.set_font(fuente_normal, "B", 11)
    pdf.cell(35, 8, "Proyecto:")

    pdf.set_font(fuente_normal, "", 11)

    pdf.multi_cell(
        145,
        8,
        texto(nombre_proyecto or "Sin nombre"),
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font(fuente_normal, "B", 11)
    pdf.cell(35, 8, "Cliente:")

    pdf.set_font(fuente_normal, "", 11)

    pdf.multi_cell(
        145,
        8,
        texto(nombre_cliente or "Sin nombre"),
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font(fuente_normal, "B", 11)
    pdf.cell(35, 8, "Fecha:")

    pdf.set_font(fuente_normal, "", 11)

    pdf.cell(
        0,
        8,
        datetime.now().strftime("%d/%m/%Y"),
        new_x="LMARGIN",
        new_y="NEXT"
    )

    salto(8)

    # ========================================================
    # 1. PIEZAS DE MADERA
    # ========================================================

    titulo_seccion("1. DETALLE DE PIEZAS DE MADERA")

    anchos_piezas = [50, 27, 27, 26, 25, 25]

    columnas_piezas = [
        "Pieza",
        "Largo cm",
        "Ancho cm",
        "Espesor",
        "Pies",
        "m²"
    ]

    encabezado_tabla(
        columnas_piezas,
        anchos_piezas
    )

    if piezas:

        for pieza in piezas:

            # Nueva página cuando la tabla no cabe.
            if pdf.get_y() + 9 > pdf.page_break_trigger:
                pdf.add_page()

                encabezado_tabla(
                    columnas_piezas,
                    anchos_piezas
                )

            fila_tabla(
                [
                    str(pieza["pieza"])[:26],
                    f'{pieza["Largo (cm)"]:.2f}',
                    f'{pieza["Ancho (cm)"]:.2f}',
                    f'{pieza["Espesor (pulg)"]:.2f}',
                    f'{pieza["Total Parcial(ft)"]:.2f}',
                    f'{pieza["Metros^2"]:.2f}'
                ],
                anchos_piezas,
                ["L", "R", "R", "R", "R", "R"]
            )

    else:

        pdf.set_font(fuente_normal, "", 10)

        pdf.cell(
            0,
            9,
            "No se registraron piezas.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    salto(5)

    fila_dato(
        "Total pies de madera:",
        f"{total_pies:.2f} ft"
    )

    fila_dato(
        "Total metros cuadrados:",
        f"{total_metros:.2f} m²"
    )

    fila_dato(
        "Madera extra por imprevistos:",
        f"{feet_madera_extra:.0f}%"
    )

    fila_dato(
        "Pies adicionales:",
        f"{total_madera_extra_feet:.2f} ft"
    )

    if total_final_madera is None:
        total_final_madera = (
            total_pies + total_madera_extra_feet
        )

    fila_dato(
        "Total final de madera:",
        f"{total_final_madera:.2f} ft"
    )

    fila_dato(
        "Precio por pie:",
        dinero(precio_pie)
    )

    fila_resumen(
        "Costo total de madera:",
        costo_total_madera,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 2. TINTE
    # ========================================================

    titulo_seccion("2. TINTE")

    fila_dato(
        "Precio por litro:",
        dinero(precio_tinte)
    )

    fila_dato(
        "Litros utilizados:",
        f"{litros_usados_tinte:.2f} L"
    )

    fila_resumen(
        "Costo total de tinte:",
        Costo_tintes,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 3. SELLADOR Y TINER
    # ========================================================

    titulo_seccion("3. SELLADOR Y TINER")

    fila_dato(
        "Litros de sellador:",
        f"{litros_usados_sellador:.2f} L"
    )

    fila_resumen(
        "Costo de sellador:",
        costo_final_sellador
    )

    fila_dato(
        "Litros de tiner:",
        f"{litros_tiner_usar:.2f} L"
    )

    fila_resumen(
        "Costo de tiner:",
        costo_final_tiner_sellador
    )

    fila_resumen(
        "Total sellador + tiner:",
        suma_sellador_tiner,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 4. ACABADO Y TINER
    # ========================================================

    titulo_seccion("4. ACABADO Y TINER")

    fila_dato(
        "Litros de acabado:",
        f"{litros_usados_acabado:.2f} L"
    )

    fila_resumen(
        "Costo de acabado:",
        costo_final_acabado
    )

    fila_dato(
        "Litros de tiner:",
        f"{litros_tiner_usar2:.2f} L"
    )

    fila_resumen(
        "Costo de tiner:",
        costo_final_tiner_acabado
    )

    fila_resumen(
        "Total acabado + tiner:",
        suma_acabado_tiner,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 5. ACCESORIOS Y HERRAJES
    # ========================================================

    titulo_seccion("5. ACCESORIOS Y HERRAJES")

    anchos_accesorios = [65, 40, 30, 45]

    columnas_accesorios = [
        "Accesorio / Herraje",
        "Precio unit.",
        "Cantidad",
        "Total"
    ]

    encabezado_tabla(
        columnas_accesorios,
        anchos_accesorios
    )

    if accesorios:

        for accesorio in accesorios:

            if pdf.get_y() + 9 > pdf.page_break_trigger:
                pdf.add_page()

                encabezado_tabla(
                    columnas_accesorios,
                    anchos_accesorios
                )

            fila_tabla(
                [
                    str(accesorio["Accesorio"])[:33],
                    dinero(accesorio["Precio Unitario"]),
                    str(accesorio["Cantidad"]),
                    dinero(
                        accesorio["Total Parcial Accesorio"]
                    )
                ],
                anchos_accesorios,
                ["L", "R", "C", "R"]
            )

    else:

        pdf.set_font(fuente_normal, "", 10)

        pdf.cell(
            0,
            9,
            "No se registraron accesorios.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    salto(5)

    fila_resumen(
        "Total accesorios y herrajes:",
        total_general_accesorios,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 6. RESUMEN DE COSTOS
    # ========================================================

    titulo_seccion("6. RESUMEN DE COSTOS")

    fila_resumen(
        "Madera:",
        costo_total_madera
    )

    fila_resumen(
        "Tinte:",
        Costo_tintes
    )

    fila_resumen(
        "Sellador y tiner:",
        suma_sellador_tiner
    )

    fila_resumen(
        "Acabado y tiner:",
        suma_acabado_tiner
    )

    fila_resumen(
        "Accesorios y herrajes:",
        total_general_accesorios
    )

    pdf.set_draw_color(120, 120, 120)

    pdf.line(
        15,
        pdf.get_y() + 2,
        195,
        pdf.get_y() + 2
    )

    salto(5)

    fila_resumen(
        "TOTAL SIN GANANCIA:",
        total_sin_ganancia,
        negrita=True
    )

    fila_resumen(
        f"Ganancia ({porcentaje_ganancia:.0f}%):",
        cantidad_ganancia
    )

    fila_resumen(
        "TOTAL CON GANANCIA:",
        total_con_ganancia,
        negrita=True
    )

    salto(7)

    # ========================================================
    # 7. MANO DE OBRA
    # ========================================================

    titulo_seccion("7. MANO DE OBRA")

    fila_dato(
        "Días laborados:",
        str(dias_laborados)
    )

    fila_dato(
        "Sueldo diario:",
        dinero(sueldo_diario)
    )

    fila_resumen(
        "Total mano de obra:",
        total_mano_obra,
        negrita=True
    )

    salto(10)

    # FLETE 
    fila_resumen(
        "Flete:",
        flete,
        negrita=True
)
    salto(10)

    # ========================================================
    # 8. TOTAL FINAL DEL PROYECTO
    # ========================================================

    comprobar_espacio(35)

    pdf.set_fill_color(29, 78, 137)  # CAMBIO: total final azul elegante
    pdf.set_text_color(255, 255, 255)

    pdf.set_font(fuente_normal, "B", 14)

    pdf.cell(
        0,
        17,
        texto(
            f"TOTAL DEL PROYECTO: {dinero(total_proyecto)}"
        ),
        border=1,
        fill=True,
        align="C",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_text_color(0, 0, 0)

    salto(8)

    pdf.set_font(fuente_normal, "", 9)

    pdf.multi_cell(
        0,
        6,
        texto(
            "Presupuesto generado a partir de los datos "
            "registrados en la aplicación."
        ),
        align="C"
    )

    # ========================================================
    # DEVOLVER EL PDF COMO BYTES
    # ========================================================

    return bytes(pdf.output())