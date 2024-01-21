import motor.motor_asyncio
from datetime import date
from bson.objectid import ObjectId

# MongoDB connection details
MONGO_DETAILS = "mongodb://localhost:27017"

# Connect to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Select the database
database = client.patientdb

# Select the collection within the database
patient_collection = database.get_collection("patients")


# Helper function to format patient data
def patient_helper(patient) -> dict:
    """
    Format patient data for response.

    - **patient**: MongoDB document - The patient data retrieved from the database.

    Returns:
    - **dict**: Formatted patient data.
    """
    return {
        "id": str(patient["_id"]),
        "first_name": patient["first_name"],
        "last_name": patient["last_name"],
        "date_of_birth": date.fromisoformat(patient["date_of_birth"]),
        "gender": patient["gender"],
        "contact_number": patient["contact_number"],
        "email": patient["email"],
        "address": patient["address"],
        "visit_date": date.fromisoformat(patient["visit_date"]),
        "doctor_name": patient["doctor_name"],
        "diagnosis": patient["diagnosis"],
        "prescription": patient["prescription"],
        "appointment_date": date.fromisoformat(patient["appointment_date"]),
        "purpose": patient["purpose"],
        "notes": patient["notes"],
    }


# Retrieve all patients present in the database
async def retrieve_patients():
    """
    Retrieve all patients from the database.

    Returns:
    - **list**: List of formatted patient data.
    """
    patients = []
    async for patient in patient_collection.find():
        patients.append(patient_helper(patient))
    return patients


# Add a new patient into to the database
async def add_patient(patient_data: dict) -> dict:
    """
    Add a new patient to the database.

    - **patient_data**: dict - Patient data to be added.

    Returns:
    - **dict**: Formatted data of the newly added patient.
    """
    patient = await patient_collection.insert_one(patient_data)
    new_patient = await patient_collection.find_one({"_id": patient.inserted_id})
    return patient_helper(new_patient)


# Retrieve a patient with a matching ID
async def retrieve_patient(id: str) -> dict:
    """
    Retrieve a patient with a matching ID from the database.

    - **id**: str - ID of the patient to be retrieved.

    Returns:
    - **dict**: Formatted data of the retrieved patient.
    """
    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        return patient_helper(patient)


# Update a patient with a matching ID
async def update_patient(id: str, data: dict):
    """
    Update a patient with a matching ID in the database.

    - **id**: str - ID of the patient to be updated.
    - **data**: dict - Updated data for the patient.

    Returns:
    - **False**: If an empty request body is sent.
    - **dict**: Formatted data of the updated patient.
    - **False**: If the patient with the given ID does not exist.
    """
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    # Convert date fields to ISO format if present
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.isoformat()

    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        updated_patient = await patient_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_patient.modified_count:
            # Return the updated patient data
            return await patient_collection.find_one({"_id": ObjectId(id)})

    return False


# Delete a patient from the database
async def delete_patient(id: str):
    """
    Delete a patient with a matching ID from the database.

    - **id**: str - ID of the patient to be deleted.

    Returns:
    - **True**: If the patient with the given ID is successfully deleted.
    - **False**: If the patient with the given ID does not exist.
    """
    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        await patient_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
