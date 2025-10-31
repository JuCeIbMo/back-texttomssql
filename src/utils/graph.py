from flask import jsonify
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

def generate_comparison_chart(dia1, dia2):
    # Configuración de la figura con más altura para las etiquetas debajo
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')

    # Etiquetas mejoradas
    label1 = f"{dia1['DAY']}/{dia1['MONTH']}/{dia1['YEAR']}"
    label2 = f"{dia2['DAY']}/{dia2['MONTH']}/{dia2['YEAR']}"

    # Métricas a comparar
    metricas = ['Ventas\nTotales', 'Subtotal', 'Impuesto', 'Descuento',
                'Cantidad\nFacturas', 'Ticket\nPromedio', 'Crecimiento\nvs Anterior']

    # Valores para visualización (normalizados)
    valores_dia1 = [
        dia1['VENTA'],
        dia1['SUBTOTAL'],
        dia1['IMPUESTO'],
        dia1['DESCUENTO'],
        dia1['QTY_FAC'] * 100,
        dia1['FAC_PROM'],
        dia1['DIFERENCIA EN %'] * 10
    ]

    valores_dia2 = [
        dia2['VENTA'],
        dia2['SUBTOTAL'],
        dia2['IMPUESTO'],
        dia2['DESCUENTO'],
        dia2['QTY_FAC'] * 100,
        dia2['FAC_PROM'],
        dia2['DIFERENCIA EN %'] * 10
    ]

    # Posiciones con más espacio
    x = np.arange(len(metricas))
    width = 0.38

    # Colores profesionales
    color1 = '#3498db'  # Azul profesional
    color2 = '#e67e22'  # Naranja profesional

    # Crear barras con mejor diseño
    bars1 = ax.bar(x - width/2, valores_dia1, width, label=label1,
                   color=color1, alpha=0.9, edgecolor='#2c3e50', linewidth=2,
                   zorder=3)
    bars2 = ax.bar(x + width/2, valores_dia2, width, label=label2,
                   color=color2, alpha=0.9, edgecolor='#2c3e50', linewidth=2,
                   zorder=3)

    # Título mejorado
    ax.set_title("VENTAS "f"{dia1['DAY']}/{dia1['MONTH']}/{dia1['YEAR']}" " vs. " f"{dia2['DAY']}/{dia2['MONTH']}/{dia2['YEAR']}" ,
                 fontsize=24, fontweight='bold', pad=25, color='#2c3e50')
    ax.set_ylabel('Valores ($) / Unidades', fontsize=14, fontweight='bold', color='#34495e')
    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontsize=12, fontweight='bold', color='#2c3e50')

    # Leyenda mejorada
    legend = ax.legend(fontsize=13, loc='upper left', framealpha=0.95,
                       shadow=True, fancybox=True, edgecolor='#2c3e50')
    legend.get_frame().set_facecolor('#ecf0f1')
    legend.get_frame().set_linewidth(2)

    # Grid mejorado
    ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.2, color='#95a5a6', zorder=0)
    ax.set_axisbelow(True)

    # Añadir líneas separadoras verticales entre secciones
    separadores = [3.5]  # Entre métricas monetarias y no monetarias
    for sep in separadores:
        ax.axvline(x=sep, color='#bdc3c7', linestyle=':', linewidth=2, alpha=0.6, zorder=1)

    # Valores reales para mostrar
    valores_reales_dia1 = [
        dia1['VENTA'], dia1['SUBTOTAL'], dia1['IMPUESTO'], dia1['DESCUENTO'],
        dia1['QTY_FAC'], dia1['FAC_PROM'], dia1['DIFERENCIA EN %']
    ]

    valores_reales_dia2 = [
        dia2['VENTA'], dia2['SUBTOTAL'], dia2['IMPUESTO'], dia2['DESCUENTO'],
        dia2['QTY_FAC'], dia2['FAC_PROM'], dia2['DIFERENCIA EN %']
    ]

    # Valores sobre las barras y variaciones DEBAJO
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        h1 = bar1.get_height()
        h2 = bar2.get_height()

        # Formatear valores según el tipo
        if i in [0, 1, 2, 3, 5]:  # Valores monetarios
            texto1 = f'${valores_reales_dia1[i]:,.0f}'
            texto2 = f'${valores_reales_dia2[i]:,.0f}'
        elif i == 4:  # Cantidad de facturas
            texto1 = f'{int(valores_reales_dia1[i])}'
            texto2 = f'{int(valores_reales_dia2[i])}'
        else:  # Porcentaje
            texto1 = f'{valores_reales_dia1[i]:.1f}%'
            texto2 = f'{valores_reales_dia2[i]:.1f}%'

        # Valores encima de las barras
        ax.text(bar1.get_x() + bar1.get_width()/2, h1 + max(valores_dia1 + valores_dia2) * 0.02, texto1,
                ha='center', va='bottom', fontweight='bold', fontsize=11, color='#2c3e50')

        ax.text(bar2.get_x() + bar2.get_width()/2, h2 + max(valores_dia1 + valores_dia2) * 0.02, texto2,
                ha='center', va='bottom', fontweight='bold', fontsize=11, color='#2c3e50')

        # Calcular y mostrar variación DEBAJO de las barras
        if valores_reales_dia1[i] != 0:
            variacion = ((valores_reales_dia2[i] / valores_reales_dia1[i]) - 1) * 100
            color_var = '#27ae60' if variacion > 0 else '#e74c3c'
            simbolo = '▲' if variacion > 0 else '▼'

            # Posición debajo de las barras (valor y negativo)
            y_pos = -max(valores_dia1 + valores_dia2) * 0.08

            ax.text(x[i], y_pos, f'{simbolo} {variacion:+.1f}%',
                    ha='center', va='top', color=color_var,
                    fontweight='bold', fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                             edgecolor=color_var, linewidth=2, alpha=0.9))

    # Ajustar límites del eje Y para dar espacio a las etiquetas debajo
    y_min = -max(valores_dia1 + valores_dia2) * 0.15
    y_max = max(valores_dia1 + valores_dia2) * 1.25
    ax.set_ylim(y_min, y_max)

    # Resumen mejorado
    variacion_ventas = ((dia2['VENTA']/dia1['VENTA']-1)*100)
    variacion_facturas = ((dia2['QTY_FAC']/dia1['QTY_FAC']-1)*100)
    variacion_ticket = ((dia2['FAC_PROM']/dia1['FAC_PROM']-1)*100)

    simbolo_ventas = '▲' if variacion_ventas > 0 else '▼'
    simbolo_facturas = '▲' if variacion_facturas > 0 else '▼'
    simbolo_ticket = '▲' if variacion_ticket > 0 else '▼'

    textstr = f'''╔═══ RESUMEN EJECUTIVO ═══╗
    ║ {simbolo_ventas} Ventas:    {variacion_ventas:+6.1f}%
    ║ {simbolo_facturas} Facturas:  {variacion_facturas:+6.1f}%
    ║ {simbolo_ticket} Ticket Prom: {variacion_ticket:+6.1f}%
    ╚═════════════════════════╝'''

    props = dict(boxstyle='round,pad=1', facecolor='#ecf0f1', alpha=0.95,
                 edgecolor='#34495e', linewidth=2.5)
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, fontfamily='monospace', fontweight='bold', color='#2c3e50')

    plt.tight_layout(rect=[0, 0.04, 1, 1])

    # Convertir la figura a un objeto BytesIO y luego a base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)  # Cerrar la figura para liberar memoria
    return image_base64