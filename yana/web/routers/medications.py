from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.medication import MedicationModel, NewMedicationModel, DosageFormModel, MedicationRouteModel
from yana.service.medications import create_medication, fetch_dosage_form, fetch_dosage_forms, fetch_medication, fetch_medication_route, fetch_medication_routes, modify_medication, remove_medication
from yana.web.exceptions import InternalServerError
from yana.web.types import Config


router = APIRouter(
    prefix="/medications",
    tags=["medications"]
)


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This endpoint is not allowed")


@router.get("/routes")
async def get_medication_routes(config: Config) -> list[MedicationRouteModel] | list:
    try:
        return await fetch_medication_routes(config)
    except ServiceError:
        raise InternalServerError


@router.get("/routes/{route_id}")
async def get_medication_route(config: Config, route_id: int) -> MedicationRouteModel:
    try:
        medication_route = await fetch_medication_route(config, route_id)
        if not medication_route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication route does not exist")
        return medication_route
    except ServiceError:
        raise InternalServerError


@router.get("/forms")
async def get_dosage_forms(config: Config) -> list[DosageFormModel] | list:
    try:
        return await fetch_dosage_forms(config)
    except ServiceError:
        raise InternalServerError


@router.get("/forms/{form_id}")
async def get_dosage_form(config: Config, form_id: int) -> DosageFormModel:
    try:
        dosage_form = await fetch_dosage_form(config, form_id)
        if not dosage_form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dosage form does not exist")
        return dosage_form
    except ServiceError:
        raise InternalServerError


@router.post("/new")
async def new_medication(config: Config, medication: NewMedicationModel):
    try:
        await create_medication(config, medication)
        return {"message": "Medication created successfully"}
    except ServiceError:
        raise InternalServerError


@router.get("/{medication_id}")
async def get_medication(config: Config, medication_id: str):
    try:
        medication = await fetch_medication(config, medication_id)
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication does not exist")
        return medication
    except ServiceError:
        raise InternalServerError


@router.put("/{medication_id}")
async def update_medication(config: Config, medication_id: str, medication: MedicationModel):
    try:
        p_medication = await fetch_medication(config, medication_id)
        if not p_medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medication with ID {medication_id} does not exist")
        return await modify_medication(config, medication)
    except ServiceError:
        raise InternalServerError


@router.delete("/{medication_id}")
async def delete_medication(config: Config, medication_id: str):
    try:
        await remove_medication(config, medication_id)
        return {"message": "Medication deleted successfully"}
    except ServiceError:
        raise InternalServerError


