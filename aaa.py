import cv2
import numpy as np
import tensorflow as tf

# Chargement du modèle TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path="ei-detecte_files-classifier-tensorflow-lite-float32-model.lite")
interpreter.allocate_tensors()

# Définition des détails d'entrée et de sortie
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Fonction de prétraitement de l'image
def preprocess_image(frame):
    resized_frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    normalized_frame = resized_frame / 255.0  # Normalisation des valeurs de pixel entre 0 et 1
    return normalized_frame.astype('float32')

# Capturer la vidéo de la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prétraiter l'image
    processed_frame = preprocess_image(frame)

    # Passer l'image prétraitée au modèle TensorFlow Lite
    interpreter.set_tensor(input_details[0]['index'], np.expand_dims(processed_frame, axis=0))
    interpreter.invoke()

    # Récupérer les résultats de la prédiction
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_label = "Good" if output_data[0][0] < output_data[0][1] else "Bad"

    # Afficher le résultat de la prédiction sur la fenêtre de la webcam
    cv2.putText(frame, predicted_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()