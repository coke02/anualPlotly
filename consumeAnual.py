import json
import requests
import plotly.graph_objects as go

correo = '' #https://climatologia.meteochile.gob.cl/application/usuario/loginUsuario
token = '' #https://climatologia.meteochile.gob.cl/application/usuario/loginUsuario
estacion = '330020' #quinta normal

url = f'https://climatologia.meteochile.gob.cl/application/servicios/getTemperaturaHistorica/{estacion}?usuario={correo}&token={token}'

# Hacer la solicitud GET
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    try:
        # Analizar la respuesta JSON
        data = response.json()
        nombreEstacion = data['datosEstacion']['nombreEstacion']
        historicosanuales = data['datosHistoricos']['anuales']
        
        # Extraer las listas de datos
        categorias = []
        minAbs = []
        maxAbs = []
        
        for anual in historicosanuales:
            # Solo agregar datos si no son None
            if anual["valores"]["maxAbs"] is not None and anual["valores"]["minAbs"] is not None:
                categorias.append(str(anual["ano"]))  # Convertir años a cadenas
                maxAbs.append(anual["valores"]["maxAbs"])  # Añadir la temperatura máxima
                minAbs.append(anual["valores"]["minAbs"])  # Añadir la temperatura mínima

        #print("Anios:", categorias)
        #print("Máximas:", maxAbs)
        #print("Mínimas:", minAbs)
        
    except json.JSONDecodeError:
        print("Error al analizar la respuesta JSON")
else:
    print(f"Error en la solicitud: {response.status_code}")

# Graficar los datos
if categorias and minAbs and maxAbs:  # Solo continuar si hay datos válidos

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=maxAbs,
        theta=categorias,  # Años como categorías de texto
        fill='toself',
        name='Temperatura Máxima'
    ))

    fig.add_trace(go.Scatterpolar(
        r=minAbs,
        theta=categorias,  # Años como categorías de texto
        fill='toself',
        name='Temperatura Mínima'
    ))

    min_temp = min(minAbs)
    anio_min = categorias[minAbs.index(min_temp)]
    #print(f"La temperatura mínima fue de {min_temp}°C en {anio_min}")
    max_temp = max(maxAbs)
    anio_max = categorias[maxAbs.index(max_temp)]
    #print(f"La temperatura mínima fue de {max_temp}°C en {anio_max}")

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[min_temp, max_temp]  # Ajustar rango según tus datos filtrados
            )
        ),
        showlegend=True
    )

    fig.update_layout(
        title=dict(
            text=nombreEstacion,
            font=dict(
                size=30
            ),
            automargin=True,
            yref='paper'
        )
    )
    # agrega los maximos y minimos
    # Agregar anotaciones para los valores mínimo y máximo con el símbolo de grado
    fig.add_annotation(
        x=0.5,
        y=0.1,
        text=f'Mínima: {"{0:.1f}".format(min_temp)}°, en {anio_min}',
        showarrow=False,
        font=dict(size=20),
        xref='paper',
        yref='paper'
    )

    fig.add_annotation(
        x=0.5,
        y=0.9,
        text=f'Máxima: {"{0:.1f}".format(max_temp)}°, en {anio_max}',
        showarrow=False,
        font=dict(size=20),
        xref='paper',
        yref='paper'
    )

    fig.show()
else:
    print("No hay suficientes datos válidos para graficar.")
