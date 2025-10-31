# Ventas Comparación App

## Descripción
La aplicación "Ventas Comparación App" es un servicio web que permite comparar las ventas de dos días diferentes. Utiliza Flask como framework web y matplotlib para generar gráficos de comparación de datos de ventas.

## Estructura del Proyecto
```
ventas-comparacion-app
├── src
│   ├── app.py          # Punto de entrada de la aplicación Flask
│   └── utils
│       └── graph.py    # Funciones para generar gráficos
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

## Instalación
Para instalar las dependencias del proyecto, asegúrate de tener `pip` instalado y ejecuta el siguiente comando en la raíz del proyecto:

```
pip install -r requirements.txt
```

## Uso
1. Inicia el servidor Flask ejecutando el siguiente comando:

```
python src/app.py
```

2. Realiza una solicitud POST al endpoint `/comparar` con dos objetos JSON que representen los datos de los días a comparar. La estructura de los objetos debe ser similar a la siguiente:

```json
{
    "YEAR": 2022,
    "MONTH": 1,
    "DAY": 14,
    "QTY_FAC": 3,
    "MONTOBRUTO": 1343.99,
    "DESCUENTO": 0,
    "SUBTOTAL": 1343.99,
    "IMPUESTO": 94.08,
    "VENTA": 1438.07,
    "FAC_PROM": 479.36,
    "DIFERENCIA EN %": 72.31
}
```

3. La respuesta será una imagen en formato base64 que representa el gráfico de comparación de ventas.

## Ejemplo de Solicitud
```bash
curl -X POST http://localhost:5000/comparar -H "Content-Type: application/json" -d '{
    "dia1": {
        "YEAR": 2022,
        "MONTH": 1,
        "DAY": 14,
        "QTY_FAC": 3,
        "MONTOBRUTO": 1343.99,
        "DESCUENTO": 0,
        "SUBTOTAL": 1343.99,
        "IMPUESTO": 94.08,
        "VENTA": 1438.07,
        "FAC_PROM": 479.36,
        "DIFERENCIA EN %": 72.31
    },
    "dia2": {
        "YEAR": 2022,
        "MONTH": 1,
        "DAY": 15,
        "QTY_FAC": 5,
        "MONTOBRUTO": 2100.50,
        "DESCUENTO": 50,
        "SUBTOTAL": 2050.50,
        "IMPUESTO": 143.54,
        "VENTA": 2194.04,
        "FAC_PROM": 438.81,
        "DIFERENCIA EN %": 52.54
    }
}'
```

## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar la aplicación, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT.