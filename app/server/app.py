from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from typing import Optional
import requests
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from app.server.routes.patient import router as patient_router

app = FastAPI()

# Define your scopes here
# Example scopes: "read:patients", "write:patients", etc.
scopes = {
    "read:patients": "Read access to patient data",
    "write:patients": "Write access to patient data",
}

# OAuth2PasswordBearer is used for handling OAuth2 tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=scopes)

# Secret key to sign the JWT token
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Dummy user data for demonstration purposes (replace it with your own user database)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "testpassword",
    }
}

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token retrieval endpoint
@app.post("/token", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Retrieve an OAuth2 token for authentication.

    - **form_data**: OAuth2PasswordRequestForm - The form data containing username, password, and scope.

    Returns:
    - **Access Token**: OAuth2 token for authentication.
    """
    user = fake_users_db.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a new JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Function to verify token and retrieve user information
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Dummy token validation (replace it with your own token validation logic)
    user = fake_users_db.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Include patient routes
app.include_router(patient_router, tags=["Patient"], prefix="/patient")

# Example route requiring OAuth2 authentication
@app.get("/private-data", tags=["Private Data"])
async def get_private_data(current_user: dict = Depends(get_current_user)):
    """
    Retrieve private data.

    - **current_user**: dict - The current authenticated user.

    Returns:
    - **Response**: Private data along with user information.
    """
    return {"message": "This is private data", "user": current_user}

def predict(prediction):
    if np.argmax(prediction) == 0:
        return 'Glioma'
    elif np.argmax(prediction) == 1:
        return 'Meningioma'
    elif np.argmax(prediction) == 2:
        return 'No tumor'
    else:
        return 'Pituatary'

IMG_SIZE = 64

def prepare(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale
    img_array = img_array / 255.0  # Normalize pixel values
    resized_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return resized_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# Example endpoint to receive an image file and process it
@app.post("/process_image", tags=["Image Processing"])
async def process_image(file: UploadFile = File(...)):
    """
    Process an image file to predict brain tumor.

    - **file**: UploadFile - The image file to be processed.

    Returns:
    - **JSONResponse**: Predicted label for the image.
    """
    # Save the uploaded file to a temporary location (you can customize this)
    file_path = f"{file.filename}"
    with open(file_path, "wb") as image_file:
        image_file.write(file.file.read())

    # Load the saved model
    loaded_model = load_model("app/Brain_Tumor_model.h5")

    # Prepare the image for prediction
    prepared_image = prepare(file_path)

    # Make prediction
    prediction = loaded_model.predict(prepared_image)

    # Get the predicted label
    label = predict(prediction)
    results = "This image represents  ------>>> " + label

    # Return the result as JSON
    return JSONResponse(content={"label": results}, status_code=200)


class BMIInput(BaseModel):
    weight: str
    height: str

@app.post("/calculate_bmi", tags=["BMI Calculator"])
async def calculate_bmi(
    weight: str = Form(...),
    height: str = Form(...)
):
    """
    Calculate BMI using weight and height.

    - **weight**: str - The weight of the person.
    - **height**: str - The height of the person.

    Returns:
    - **JSONResponse**: BMI calculation result.
    """
    url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/metric"
    headers = {
        "X-RapidAPI-Key": "210680b388msh634fdb2c42ba6afp16a992jsn0c77311b93c4",
        "X-RapidAPI-Host": "body-mass-index-bmi-calculator.p.rapidapi.com"
    }

    querystring = {"weight": weight, "height": height}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        raise HTTPException(status_code=500, detail=f"Error connecting to BMI API: {str(e)}")
