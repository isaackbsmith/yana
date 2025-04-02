from pydantic import BaseModel


class MedicationRouteSchema(BaseModel):
    id: int
    name: str
    friendly_name: str
    description: str


class DosageFormSchema(BaseModel):
    id: int
    name: str
    friendly_name: str
    description: str

class BaseMedicationSchema(BaseModel):
    id: str
    generic_name: str
    brand_name: str
    description: str
    strength: str
    dosage: int

class NewMedicationSchema(BaseMedicationSchema):
    dosage_form_id: int
    medication_route_id: int

class MedicationSchema(BaseMedicationSchema):
    dosage_form: str
    medication_route: str
