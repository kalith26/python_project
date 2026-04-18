import cv2
from deepface import DeepFace

# Initialize camera
cap = cv2.VideoCapture(0)

# Load Haar Cascade for fast face detection before analysis
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces to isolate the region for DeepFace (improves speed)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        try:
            # Extract face for analysis
            face_roi = frame[y:y+h, x:x+w]
            
            # Analyze emotion using DeepFace
            # enforce_detection=False prevents the program from crashing if a face isn't clear
            results = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            
            # Get the dominant emotion
            emotion = results[0]['dominant_emotion']
            
            # Custom mapping for your specific requests
            display_text = emotion
            if emotion == "sad":
                display_text = "Sad/Crying" # Crying is typically classified as 'sad'
            elif emotion == "neutral":
                display_text = "Neutral/Thinking" # Thinking often looks 'neutral'

            # Draw rectangle and labels
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, display_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
        except Exception as e:
            print(f"Error analyzing face: {e}")

    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
