from flask import Flask, request, jsonify
from app import app
from src.business.predict.predict_business import PredictBusiness
import base64
import io

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction pour analyser une image et renvoyer la classe predict.
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
      description: Poisson a prédire.
    responses:
      200:
        description: Succès de la prédiction.
        schema:
          type: object
          properties:
            espèce:
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
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier envoyé'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Pas de fichier sélectionné'}), 400
        
        try:
            # Créez une instance de PredictBusiness
            predict_business = PredictBusiness.get_instance()
            
            img_bytes = file.read()
            probabilities_list, class_name, image = predict_business.predict(image_bytes=img_bytes)
            
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            return jsonify({
                'espece': class_name,
                'prediction': probabilities_list,
                'image': img_byte_arr
            })
        except Exception as e:
            print(f"Erreur de prédiction : {e}")
            return jsonify({'error': str(e)}), 500