from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ API de clasificación de residuos funcionando."

@app.route('/clasificar', methods=['POST'])
def clasificar():
    data = request.get_json()
    imagen_url = data.get('imagen')  # debe ser una URL pública

    if not imagen_url:
        return jsonify({'error': 'No se proporcionó una URL de imagen'}), 400

    # URL del modelo entrenado en Roboflow (incluye tu API key)
    api_url = "https://detect.roboflow.com/clasificador-de-residuos_1/2?api_key=MuxjBxWqxry9azrOCWvj"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Enviamos la imagen a Roboflow
        response = requests.post(api_url, json={'image': imagen_url}, headers=headers)
        result = response.json()

        if 'predictions' in result and result['predictions']:
            clase = result['predictions'][0]['class']
        else:
            clase = "Desconocido"

        return jsonify({'resultado': clase})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
