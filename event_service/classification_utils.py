from typing import List
from .models import EventOptional, ListEventOptional

def classify_llm(model, text: str) -> list[EventOptional]:
    prompt = (
        """
        You are an expert in event identification and data extraction.

        Carefully analyze the following text and extract structured information for each event mentioned. For every event you identify, provide the following details:

        1. Event Name – The official or most likely name of the event.  
        2. Description – A concise summary of what the event is about.  
        3. Event Type – Classify the event (e.g., concert, conference, festival, exhibition, sports event, etc.).  
        4. Start Date – The date when the event begins (use ISO format: YYYY-MM-DD).  
        5. End Date – The date when the event ends (use ISO format: YYYY-MM-DD).
        For both start and end dates, if the exact date is not available, use the best estimate or set it as None.
        6. Location – The specific venue and city, if available (e.g., \"Madison Square Garden, New York\").

        Important Notes:  
        - If multiple events are described, extract and present details for each one separately.  
        - If the text does not describe any specific event, return nothing—do not invent or infer events that are not clearly described.

        Here is the text to analyze:
       """
        + text
    )
    response = model.invoke(
        prompt,
    )
    events = response.events if isinstance(response, ListEventOptional) else []
    return events
