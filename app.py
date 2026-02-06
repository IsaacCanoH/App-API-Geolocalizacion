from flask import Flask, render_template, request
import requests
# Importa Flask para crear la app y requests para consumir APIs externas

app = Flask(__name__)
# Crea la aplicación Flask

@app.route('/')
def index():
    # Ruta principal que muestra la página de inicio
    return render_template('index.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    # Esta ruta permite buscar un lugar y mostrar gasolineras cercanas
    if request.method == 'POST':
        # Obtiene el texto ingresado por el usuario
        lugar = request.form['lugar']
        
        # URL de la API Nominatim para buscar coordenadas
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": lugar,        # Lugar a buscar
            "format": "json",  # Respuesta en formato JSON
            "limit": 1         # Solo el primer resultado
        }
        
        # Header requerido por Nominatim
        headers = {
            "User-Agent": "Flask-Educational-App"
        }
        
        # Petición para obtener latitud y longitud del lugar
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data:
            # Extrae coordenadas y nombre del lugar encontrado
            lat = data[0]['lat']
            lon = data[0]['lon']
            nombre = data[0]['display_name']
            
            # URL de la API Overpass para consultar gasolineras
            overpass_url = "https://overpass-api.de/api/interpreter"

            # Consulta para obtener gasolineras cercanas al punto
            query = f"""
            [out:json];
            node
            ["amenity"="fuel"]
            (around:3000,{lat},{lon});
            out;
            """

            # Petición para obtener las gasolineras
            response_gas = requests.post(overpass_url, data=query)
            gasolineras = response_gas.json()["elements"]
            
            # Renderiza el mapa con el lugar y las gasolineras
            return render_template(
                'map.html',
                lat=lat,
                lon=lon,
                nombre=nombre,
                gasolineras=gasolineras
            )
    
    # Si no hay resultados o no se envió el formulario
    return render_template('map.html', error=True)

if __name__ == '__main__':
    # Ejecuta la aplicación en modo desarrollo
    app.run(debug=True)
