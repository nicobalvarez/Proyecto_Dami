import pdfplumber
from flask import Flask, jsonify, request

app = Flask(__name__)

def leer_pdf(ruta_archivo):
    try:
        with pdfplumber.open(ruta_archivo) as pdf:
            texto = ''
            for pagina in pdf.pages:
                texto += pagina.extract_text() + '\n'  # Extraer texto de cada página
            return texto.strip()  # Retornar el texto sin espacios al inicio o final
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return None

@app.route('/leer-pdf', methods=['POST'])
def obtener_texto_pdf():
    # Obtener el archivo desde la solicitud
    archivo = request.files.get('file')
    
    if archivo:
        # Guardar el archivo temporalmente
        ruta_archivo = f'temp_{archivo.filename}'
        archivo.save(ruta_archivo)

        # Leer el contenido del PDF
        texto_pdf = leer_pdf(ruta_archivo)

        # Eliminar el archivo temporal si es necesario
        # import os
        # os.remove(ruta_archivo)

        if texto_pdf is not None:
            return jsonify({"texto": texto_pdf}), 200
        else:
            return jsonify({"error": "No se pudo extraer el texto del PDF."}), 500
    else:
        return jsonify({"error": "No se proporcionó ningún archivo."}), 400

if __name__ == '__main__':
    app.run(debug=True)