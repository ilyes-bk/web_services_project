from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from app.server.database import (
    add_patient,
    delete_patient,
    retrieve_patient,
    retrieve_patients,
    update_patient,
)
from app.server.models.patient import (
    ErrorResponseModel,
    ResponseModel,
    PatientSchema,
    UpdatePatientModel,
)

router = APIRouter()

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "testpassword",
    }
}

scopes = {
    "read:patients": "Read access to patient data",
    "write:patients": "Write access to patient data",
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=scopes)

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.post("/", response_description="Patient data added into the database")
async def add_patient_data(
    patient: PatientSchema = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Add patient data to the database.

    - **patient**: PatientSchema - The data of the patient to be added.
    - **current_user**: dict - The current authenticated user.

    Returns:
    - **ResponseModel**: Patient data added successfully.
    """
    patient = jsonable_encoder(patient)
    new_patient = await add_patient(patient)
    return ResponseModel(new_patient, "Patient added successfully.")

@router.get("/", response_description="Patients retrieved")
async def get_patients(current_user: dict = Depends(get_current_user)):
    """
    Retrieve a list of patients from the database.

    - **current_user**: dict - The current authenticated user.

    Returns:
    - **ResponseModel**: Patients data retrieved successfully.
    """
    patients = await retrieve_patients()
    if patients:
        return ResponseModel(patients, "Patients data retrieved successfully")
    return ResponseModel(patients, "Empty list returned")

@router.get("/{id}", response_description="Patient data retrieved")
async def get_patient_data(id, current_user: dict = Depends(get_current_user)):
    """
    Retrieve patient data by ID from the database.

    - **id**: str - The ID of the patient.
    - **current_user**: dict - The current authenticated user.

    Returns:
    - **ResponseModel**: Patient data retrieved successfully.
    - **ErrorResponseModel**: An error occurred. (404 - Patient doesn't exist.)
    """
    patient = await retrieve_patient(id)
    if patient:
        return ResponseModel(patient, "Patient data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Patient doesn't exist.")

@router.put("/{id}")
async def update_patient_data(
    id: str, req: UpdatePatientModel = Body(...), current_user: dict = Depends(get_current_user)
):
    """
    Update patient data by ID in the database.

    - **id**: str - The ID of the patient to be updated.
    - **req**: UpdatePatientModel - The updated data for the patient.
    - **current_user**: dict - The current authenticated user.

    Returns:
    - **ResponseModel**: Patient name updated successfully.
    - **ErrorResponseModel**: An error occurred. (404 - There was an error updating the patient data.)
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_patient = await update_patient(id, req)
    if updated_patient:
        return ResponseModel(
            "Patient with ID: {} name update is successful".format(id),
            "Patient name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the patient data.",
    )

@router.delete("/{id}", response_description="Patient data deleted from the database")
async def delete_patient_data(id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete patient data by ID from the database.

    - **id**: str - The ID of the patient to be deleted.
    - **current_user**: dict - The current authenticated user.

    Returns:
    - **ResponseModel**: Patient deleted successfully.
    - **ErrorResponseModel**: An error occurred. (404 - Patient with id {0} doesn't exist.)
    """
    deleted_patient = await delete_patient(id)
    if deleted_patient:
        return ResponseModel(
            "Patient with ID: {} removed".format(id), "Patient deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Patient with id {0} doesn't exist".format(id)
    )
