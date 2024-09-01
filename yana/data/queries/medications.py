from yana.data.database import run_query
from yana.data.schemas.medication import DosageFormSchema, MedicationRouteSchema, MedicationSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.types import YANAConfig


async def select_medication(config: YANAConfig, medication_id: str):
    sql = """
        SELECT
            id,
            generic_name,
            brand_name,
            description,
            strength,
            dosage,
            dosage_form_id,
            medication_route_id
        FROM medications
        WHERE id = :id;
    """
    try:
        return await run_query(config=config,
                                 sql=sql,
                                 params={"id": medication_id},
                                 factory=MedicationSchema,
                                 pragma="one")
    except DatabaseError:
        raise QueryError("Error selecting new medication")


async def insert_medication(config: YANAConfig, user: MedicationSchema):
    sql = """
        INSERT INTO medications (
            id,
            generic_name,
            brand_name,
            description,
            strength,
            dosage,
            dosage_form_id,
            medication_route_id
        ) VALUES (
            :id,
            :generic_name,
            :brand_name,
            :description,
            :strength,
            :dosage,
            :dosage_form_id,
            :medication_route_id
        );
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=user.model_dump(),
            factory=MedicationSchema)
    except DatabaseError:
        raise QueryError("Error inserting new medication")


async def update_medication(config: YANAConfig, user: MedicationSchema):
    sql = """
        UPDATE medications
        SET
            generic_name = :generic_name,
            brand_name = :brand_name,
            description = :description,
            strength = :strength,
            dosage = :dosage,
            dosage_form_id = :dosage_form_id,
            medication_route_id = :medication_route_id
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=user.model_dump(),
            factory=MedicationSchema)
    except DatabaseError:
        raise QueryError("Error updating medication")


async def delete_medication(config: YANAConfig, id: str):
    sql = """
        DELETE FROM medications WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": id},
            factory=MedicationSchema)
    except DatabaseError:
        raise QueryError("Error deleting medication")


async def insert_medication_route(config: YANAConfig, route: MedicationRouteSchema):
    sql = """
        INSERT INTO medication_routes (
            id,
            name,
            friendly_name,
            description
        ) VALUES (
            :id,
            :name,
            :friendly_name,
            :description
        );
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=route.model_dump(),
            factory=MedicationRouteSchema)
    except DatabaseError:
        raise QueryError("Error inserting new medication route")


async def select_medication_route(config: YANAConfig, route_id: int):
    sql = """
        SELECT
            id,
            name,
            friendly_name,
            description
        FROM medication_routes
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": route_id},
            pragma="one",
            factory=MedicationRouteSchema)
    except DatabaseError:
        raise QueryError("Error retrieving medication route")


async def select_medication_routes(config: YANAConfig):
    sql = """
        SELECT
            id,
            name,
            friendly_name,
            description
        FROM medication_routes;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=None,
            pragma="all",
            factory=MedicationRouteSchema)
    except DatabaseError:
        raise QueryError("Error retrieving medication routes")


async def insert_dosage_forms(config: YANAConfig, route: DosageFormSchema):
    sql = """
        INSERT INTO dosage_forms (
            id,
            name,
            friendly_name,
            description
        ) VALUES (
            :id,
            :name,
            :friendly_name,
            :description
        );
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=route.model_dump(),
            factory=DosageFormSchema)
    except DatabaseError:
        raise QueryError("Error inserting new dosage form")


async def select_dosage_form(config: YANAConfig, form_id: int):
    sql = """
        SELECT
            id,
            name,
            friendly_name,
            description
        FROM dosage_forms
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": form_id},
            pragma="one",
            factory=DosageFormSchema)
    except DatabaseError:
        raise QueryError("Error retrieving dosage form")


async def select_dosage_forms(config: YANAConfig):
    sql = """
        SELECT
            id,
            name,
            friendly_name,
            description
        FROM dosage_forms;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=None,
            pragma="all",
            factory=DosageFormSchema)
    except DatabaseError:
        raise QueryError("Error retrieving dosage forms")

