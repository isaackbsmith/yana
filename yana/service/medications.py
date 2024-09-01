from typing import cast
import uuid
from yana.data.queries.medications import (
    delete_medication,
    insert_medication,
    select_dosage_form,
    select_dosage_forms,
    select_medication,
    select_medication_route,
    select_medication_routes,
    update_medication
)
from yana.data.schemas.medication import DosageFormSchema, MedicationRouteSchema, MedicationSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.medication import DosageFormModel, MedicationModel, MedicationRouteModel, NewMedicationModel
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger


async def fetch_medication(config: YANAConfig, name: str) -> MedicationModel | None:
    try:
        result = await select_medication(config, name)
        if result and isinstance(result, MedicationSchema):
            medication = MedicationModel(**result.model_dump())
            return medication
        return None
    except QueryError:
        api_logger.error("An error occurred fetching medication")
        raise ServiceError("Medication Service Error")


async def create_medication(config: YANAConfig, medication: NewMedicationModel) -> None:

    id = str(uuid.uuid4())

    new_medication = MedicationSchema(**medication.model_dump(), id=id)

    try:
        await insert_medication(config, new_medication)
    except QueryError:
        api_logger.error("An error occurred creating medication")
        raise ServiceError("Medication Service Error")


async def modify_medication(config: YANAConfig, medication: MedicationModel) -> MedicationModel:

    updated_medication = MedicationSchema(**medication.model_dump())

    try:
        await update_medication(config, updated_medication)
        return cast(MedicationModel, await fetch_medication(config, updated_medication.id))
    except QueryError:
        api_logger.error("An error occurred updating medication")
        raise ServiceError("Medication Service Error")


async def remove_medication(config: YANAConfig, id: str) -> None:
    try:
        await delete_medication(config, id)
    except QueryError:
        api_logger.error("An error occurred deleting medication")
        raise ServiceError("Medication Service Error")


async def fetch_medication_route(config: YANAConfig, route_id: int) -> MedicationRouteModel | None:
    try:
        result = await select_medication_route(config, route_id)
        print(result)
        if result and isinstance(result, MedicationRouteSchema):
            medication_route = MedicationRouteModel(**result.model_dump())
            return medication_route
        return None
    except QueryError:
        api_logger.error("An error occurred fetching medication route")
        raise ServiceError("Medication Service Error")


async def fetch_medication_routes(config: YANAConfig):
    try:
        result = await select_medication_routes(config)
        if result and isinstance(result, list) and len(result) > 0:
            medication_routes = list(map(lambda x: MedicationRouteModel(**x.model_dump()), result))
            return medication_routes
        return []
    except QueryError:
        api_logger.error("An error occurred fetching medication routes")
        raise ServiceError("Medication Service Error")


async def fetch_dosage_form(config: YANAConfig, form_id: int) -> DosageFormModel | None:
    try:
        result = await select_dosage_form(config, form_id)
        if result and isinstance(result, DosageFormSchema):
            dosage_form = DosageFormModel(**result.model_dump())
            return dosage_form
        return None
    except QueryError:
        api_logger.error("An error occurred fetching dosage form")
        raise ServiceError("Medication Service Error")


async def fetch_dosage_forms(config: YANAConfig) -> list[DosageFormModel] | list:
    try:
        result = await select_dosage_forms(config)
        if result and isinstance(result, list) and len(result) > 0:
            dosage_forms = list(map(lambda x: MedicationRouteModel(**x.model_dump()), result))
            return dosage_forms
        return []
    except QueryError:
        api_logger.error("An error occurred fetching dosage forms")
        raise ServiceError("Medication Service Error")
