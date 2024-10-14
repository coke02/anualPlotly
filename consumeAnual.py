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

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[min(minAbs), max(maxAbs)]  # Ajustar rango según tus datos filtrados
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

    fig.show()
else:
    print("No hay suficientes datos válidos para graficar.")

