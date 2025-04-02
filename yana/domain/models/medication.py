from pydantic import BaseModel


class MedicationRouteModel(BaseModel):
    id: int
    name: str
    friendly_name: str
    description: str


class DosageFormModel(BaseModel):
    id: int
    name: str
    friendly_name: str
    description: str


class BaseMedicationModel(BaseModel):
    generic_name: str
    brand_name: str
    description: str
    strength: str
    dosage: int


class NewMedicationModel(BaseModel):
    generic_name: str
    brand_name: str
    description: str
    strength: str
    dosage: int
    dosage_form_id: int
    medication_route_id: int


class MedicationModel(BaseModel):
    id: str
    generic_name: str
    brand_name: str
    description: str
    strength: str
    dosage: int
    dosage_form: str
    medication_route: str
