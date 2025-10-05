from .repository import EventsDB, SessionLocal
from typing import List, Optional
import logging
import sqlalchemy
from .models import EventOptional
from psycopg import errors
from .embedding_utils import create_documents
import uuid

def DTO_to_EventDB(dto: EventOptional) -> EventsDB:
    return EventsDB(
        name=dto.name,
        description=dto.description,
        event_type=dto.event_type.value,
        start_date=dto.start_date,
        start_time=dto.start_time,
        end_date=dto.end_date,
        end_time=dto.end_time,
        address=dto.address,
        city=dto.city,
        country=dto.country,
        postal_code=dto.postal_code,
        venue=dto.venue,
        url=dto.url,
        price=dto.price,
    )

def save_to_db(events: List[EventOptional], ids: Optional[List[str]] = None):
    logging.info(
        f"Initiating save operation for {len(events)} event(s) to the database."
    )
    with SessionLocal() as session:
        for idx, event in enumerate(events):
            event_db = DTO_to_EventDB(event)
            if ids:
                setattr(
                    event_db, "id", ids[idx]
                )
            session.add(event_db)
        session.commit()
    logging.info(f"Database commit successful for {len(events)} event(s).")

def check_db_consistency():
    """Check if the vector DB and the relational DB have the same number of elements."""
    with SessionLocal() as session:
        rdb_count = session.query(EventsDB).count()
        try:
            result = session.execute(
                sqlalchemy.text("SELECT COUNT(*) FROM langchain_pg_embedding;")
            )
            vdb_count = result.scalar()
        except sqlalchemy.exc.ProgrammingError as e:
            logging.error(f"Error querying vector DB: {e}")
            vdb_count = 0


    logging.info(
        f"Relational DB contains {rdb_count} record(s); Vector DB contains {vdb_count} record(s). Consistency check: {'PASSED' if rdb_count == vdb_count else 'FAILED'}."
    )
    return rdb_count == vdb_count

def save_to_vector_and_relational(events: List[EventOptional], vectorstore, ids: Optional[List[str]] = None):
    if len(events) == 0 or events is None:
        return
    if ids is None:
        ids = [str(uuid.uuid4()) for _ in events]
    assert len(events) == len(ids)
    vectorstore.add_documents(
        documents=create_documents(events),
        ids=ids
    )
    save_to_db(events, ids)