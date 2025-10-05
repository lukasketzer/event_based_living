from typing import List
from .models import EventOptional
# TODO:
def enrich_events(events: List[EventOptional], tavily_client=None) -> List[EventOptional]:
    return events
    return_events = []
    for event in events:
        missing_values = []
        for k, v in event:
            if v is None or v == "":
                missing_values.append(k)
        search_query = f"{event.name} {event.description} {event.venue} {event.event_type} {event.address} {event.city}"
        tavily_results = tavily_client.search(search_query) if tavily_client else ""
        prompt = f"""
        I have the following data:

        {event}

        However, some values are missing: {missing_values}.

        Please use the following text to help fill in the missing values:

        {tavily_results}

        Guidelines:
        - Do **not** fabricate or guess any data.
        - Use only the information available in the provided text to complete the missing values.
        - For any dates, ensure they are:
        - Accurate and fact-based
        - Formatted as YYYY-MM-DD (e.g., 2025-07-24)
        """
        response = model.invoke(prompt)
        return_events.append(response.events)
    return return_events
