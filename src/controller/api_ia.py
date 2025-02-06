from flask import Flask, request, jsonify
from src.business.predict.predict_business import PredictBusiness
import base64
import io

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction pour analyser une image et renvoyer la classe prédite.
    ---
    tags:
    - Prediction
    consumes:
    - multipart/form-data
    parameters:
    - name: file
      in: formData
      type: file
      required: true
      description: Poisson à prédire.
    responses:
      200:
        description: Succès de la prédiction.
        schema:
          type: object
          properties:
            espece:
              type: string
              description: La classe prédite pour l'image.
            prediction:
              type: array
              items:
                type: object
                properties:
                  label:
                    type: string
                  probability:
                    type: number
            image:
              type: string
              description: L'image en base64.
      400:
        description: Erreur dans la requête (fichier manquant ou invalide).
      500:
        description: Erreur interne.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        predict_business = PredictBusiness.get_instance()
        img_bytes = file.read()
        
        # Get prediction
        probabilities_list, class_name, processed_image = predict_business.predict(image_bytes=img_bytes)
        
        # Convert processed image to base64
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        img_str = base64.b64encode(img_byte_arr).decode()
        
        return jsonify({
            'espece': class_name,
            'prediction': probabilities_list,
            'image': img_str
        })
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)