from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.medication import (
    MedicationModel,
    DosageFormModel,
    MedicationRouteModel,
    NewMedicationModel,
)
from yana.service.medications import (
    create_medication,
    fetch_all_medications,
    fetch_dosage_form,
    fetch_dosage_forms,
    fetch_medication,
    fetch_medication_route,
    fetch_medication_routes,
    modify_medication,
    remove_medication,
)
from yana.api.exceptions import InternalServerError
from yana.api.types import Config


router = APIRouter(prefix="/medications", tags=["medications"])


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )


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
                detail="Medication route does not exist",
            )
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
                detail="Dosage form does not exist",
            )
        return dosage_form
    except ServiceError:
        raise InternalServerError

@router.get("/all")
async def get_all_medications(config: Config) -> list[MedicationModel] | list:
    try:
        return await fetch_all_medications(config)
    except ServiceError:
        raise InternalServerError

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=MedicationModel)
async def new_medication(config: Config, medication: NewMedicationModel):
    try:
        print("NEW MEDICATION: ", medication)
        return await create_medication(config, medication)
    except ServiceError:
        raise InternalServerError


@router.get("/{medication_id}", status_code=status.HTTP_200_OK, response_model=MedicationModel)
async def get_medication(config: Config, medication_id: str):
    try:
        medication = await fetch_medication(config, medication_id)
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication does not exist",
            )
        return medication
    except ServiceError:
        raise InternalServerError


@router.put("/{medication_id}", status_code=status.HTTP_201_CREATED, response_model=MedicationModel)
async def update_medication(
    config: Config, medication_id: str, medication: NewMedicationModel
):
    try:
        p_medication = await fetch_medication(config, medication_id)
        if not p_medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication does not exist",
            )
        return await modify_medication(config, medication, medication_id)
    except ServiceError:
        raise InternalServerError


@router.delete("/{medication_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_medication(config: Config, medication_id: str):
    try:
        medication = await fetch_medication(config, medication_id)
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medication does not exist",
            )
        await remove_medication(config, medication_id)
        return {"message": "Medication deleted successfully"}
    except ServiceError:
        raise InternalServerError
