import sqlite3
from pathlib import Path
from typing import Any

from yana.data.database import DB


def run_query(db_path, sql, params: list[dict[str, Any]]) -> None:
    with DB(db_path, sqlite3.Row) as db:
        print("Executing query")
        db.cursor.executemany(sql, params)
        db.connection.commit()
        print("Finished executing query")


def seed_medication_routes(db_path: Path):
    sql = """
        INSERT INTO medication_routes (
            name,
            friendly_name,
            description
        )
        VALUES (
            :name,
            :friendly_name,
            :description
        );
        """
    params = [
        {
            "name": "Oral",
            "friendly_name": "By Mouth",
            "description": "Medication is swallowed and absorbed through the digestive system"
        },
        {
            "name": "Intravenous",
            "friendly_name": "IV",
            "description": "Medication is injected directly into a vein, entering the bloodstream immediately"
        },
        {
            "name": "Sublingual",
            "friendly_name": "Under the Tongue",
            "description": "Medication is placed under the tongue to dissolve and be absorbed through the mouth's lining"
        },
        {
            "name": "Buccal",
            "friendly_name": "Between the Gums and Cheek",
            "description": "Medication is placed between the gums and cheek to be absorbed through the mouth's lining"
        },
        {
            "name": "Intramuscular",
            "friendly_name": "Into the Muscle",
            "description": "Medication is injected deep into a muscle for gradual absorption"
        },
        {
            "name": "Subcutaneous",
            "friendly_name": "Under the Skin",
            "description": "Medication is injected into the layer of fat just beneath the skin"
        },
        {
            "name": "Topical",
            "friendly_name": "Applied to Skin",
            "description": "Medication is applied directly to the skin's surface"
        },
        {
            "name": "Inhalation",
            "friendly_name": "Breathed In",
            "description": "Medication is inhaled into the lungs, typically using an inhaler or nebulizer"
        },
        {
            "name": "Rectal",
            "friendly_name": "Inserted in the Rectum",
            "description": "Medication is inserted into the rectum for local or systemic effect"
        },
        {
            "name": "Transdermal",
            "friendly_name": "Through the Skin",
            "description": "Medication is absorbed slowly through the skin, often via a patch"
        }
    ]

    try:
        run_query(db_path, sql, params)
    except Exception as e:
        print(f"An Error Occurred: {e}")


def seed_dosage_forms(db_path: Path):
    sql = """
        INSERT INTO dosage_forms (
            name,
            friendly_name,
            description
        )
        VALUES (
            :name,
            :friendly_name,
            :description
        );
        """
    params = [
        {
            "name": "Tablet",
            "friendly_name": "Tablet",
            "description": "A solid, flat, compressed medication in disc shape"
        },
        {
            "name": "Capsule",
            "friendly_name": "Capsule",
            "description": "A small, cylindrical container of medication enclosed in a dissolvable shell"
        },
        {
            "name": "Liquid",
            "friendly_name": "Syrup",
            "description": "A sweet, thick liquid medication often used for oral administration"
        },
        {
            "name": "Injection",
            "friendly_name": "Injection",
            "description": "A liquid medication administered directly into the body using a needle and syringe"
        },
        {
            "name": "Cream",
            "friendly_name": "Skin Cream",
            "description": "A semi-solid emulsion of oil and water for topical application on the skin"
        },
        {
            "name": "Ointment",
            "friendly_name": "Ointment",
            "description": "A greasy or viscous preparation for topical application, often with a higher oil content than creams"
        },
        {
            "name": "Gel",
            "friendly_name": "Gel",
            "description": "A semi-solid, jelly-like substance for topical application or oral use"
        },
        {
            "name": "Patch",
            "friendly_name": "Skin Patch",
            "description": "An adhesive patch that delivers medication through the skin"
        },
        {
            "name": "Suppository",
            "friendly_name": "Suppository",
            "description": "A solid medication designed to be inserted into the rectum, vagina, or urethra"
        },
        {
            "name": "Inhaler",
            "friendly_name": "Inhaler",
            "description": "A device used to deliver medication directly to the lungs through inhalation"
        },
        {
            "name": "Pill",
            "friendly_name": "Pill",
            "description": "A small, round, solid form of medication, often used interchangeably with tablet"
        }
    ]

    try:
        run_query(db_path, sql, params)
    except Exception as e:
        print(f"An Error Occurred: {e}")



def main() -> None:
    db_path = Path("dev.db").resolve()
    seed_dosage_forms(db_path)
    seed_medication_routes(db_path)


if __name__ == "__main__":
    main()
