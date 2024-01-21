from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field


class PatientSchema(BaseModel):
    first_name: str = Field(..., description="The first name of the patient.")
    last_name: str = Field(..., description="The last name of the patient.")
    date_of_birth: date = Field(..., description="The date of birth of the patient.")
    gender: str = Field(..., description="The gender of the patient.")
    contact_number: str = Field(..., description="The contact number of the patient.")
    email: EmailStr = Field(..., description="The email address of the patient.")
    address: str = Field(..., description="The address of the patient.")
    visit_date: date = Field(..., description="The date of the patient's visit.")
    doctor_name: str = Field(..., description="The name of the doctor.")
    diagnosis: str = Field(..., description="The diagnosis for the patient.")
    prescription: str = Field(..., description="The prescription for the patient.")
    appointment_date: date = Field(..., description="The date of the appointment.")
    purpose: str = Field(..., description="The purpose of the appointment.")
    notes: str = Field(..., description="Additional notes about the patient.")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Ilyes",
                "last_name": "Ben Khalifa",
                "date_of_birth": "2002-06-07",
                "gender": "Male",
                "contact_number": "123-456-7890",
                "email": "ilyesbenkhalifa@example.com",
                "address": "123 Mourouj 3, TUNIS",
                "visit_date": "2024-01-03",
                "doctor_name": "Dr. Smith",
                "diagnosis": "Common Cold",
                "prescription": "Antibiotics",
                "appointment_date": "2024-01-12",
                "purpose": "Follow-up",
                "notes": "Patient responded well to treatment.",
            }
        }


class UpdatePatientModel(BaseModel):
    first_name: Optional[str] = Field(None, description="The updated first name of the patient.")
    last_name: Optional[str] = Field(None, description="The updated last name of the patient.")
    date_of_birth: Optional[date] = Field(None, description="The updated date of birth of the patient.")
    gender: Optional[str] = Field(None, description="The updated gender of the patient.")
    contact_number: Optional[str] = Field(None, description="The updated contact number of the patient.")
    email: Optional[EmailStr] = Field(None, description="The updated email address of the patient.")
    address: Optional[str] = Field(None, description="The updated address of the patient.")
    visit_date: Optional[date] = Field(None, description="The updated date of the patient's visit.")
    doctor_name: Optional[str] = Field(None, description="The updated name of the doctor.")
    diagnosis: Optional[str] = Field(None, description="The updated diagnosis for the patient.")
    prescription: Optional[str] = Field(None, description="The updated prescription for the patient.")
    appointment_date: Optional[date] = Field(None, description="The updated date of the appointment.")
    purpose: Optional[str] = Field(None, description="The updated purpose of the appointment.")
    notes: Optional[str] = Field(None, description="Updated additional notes about the patient.")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Ilyes",
                "last_name": "Ben Khalifa",
                "date_of_birth": "2002-06-07",
                "gender": "Male",
                "contact_number": "123-456-7890",
                "email": "ilyesbenkhalifa@gmail.com",
                "address": "123 Mourouj 3, Ben Arous",
                "visit_date": "2024-01-03",
                "doctor_name": "Dr. Mohamed",
                "diagnosis": "Common Cold",
                "prescription": "Antibiotics",
                "appointment_date": "2024-01-12",
                "purpose": "Follow-up",
                "notes": "Patient responded well to treatment.",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
