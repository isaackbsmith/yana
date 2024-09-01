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


class MedicationSchema(BaseModel):
    id: str
    generic_name: str
    brand_name: str
    description: str
    strength: str
    dosage: int
    dosage_form_id: int
    medication_route_id: int

