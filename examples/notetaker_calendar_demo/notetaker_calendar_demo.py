import os
from datetime import datetime, timedelta
from typing import Optional

from nylas import Client
from nylas.models.notetakers import Notetaker
from nylas.models.events import (
    UpdateEventRequest,
    CreateEventRequest,
    EventNotetakerRequest,
    EventNotetakerSettings,
    CreateTimespan,
    CreateEventQueryParams,
    UpdateEventQueryParams,
    CreateAutocreate,
    CreateEventNotetaker
)

# Initialize the Nylas client
nylas = Client(
    api_key=os.getenv("NYLAS_API_KEY"),
    api_uri=os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")
)

def create_event_with_notetaker():
    """Demonstrates how to create a calendar event with a Notetaker bot."""
    print("\n=== Creating Event with Notetaker ===")
    
    # Create the event
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)


    # Create the request body with proper types
    request_body = CreateEventRequest(
        title="Project Planning Meeting",
        description="Initial project planning and resource allocation",
        when=CreateTimespan(
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp())
        ),
        metadata={
            "project_id": "PROJ-123",
            "priority": "high"
        },
        conferencing=CreateAutocreate(
            provider="Google Meet",
            autocreate={}
        ),
        notetaker=CreateEventNotetaker(
            name="Nylas Notetaker",
            meeting_settings=EventNotetakerSettings(
                video_recording=True,
                audio_recording=True,
                transcription=True
            )
        )
    )
    
    # Create the query parameters
    query_params = CreateEventQueryParams(
        calendar_id=os.getenv("NYLAS_CALENDAR_ID")
    )
    
    event = nylas.events.create(
        identifier=os.getenv("NYLAS_GRANT_ID"),
        request_body=request_body,
        query_params=query_params
    )

    return event


def get_event_notetaker(event_id: str) -> Optional[Notetaker]:
    """Demonstrates how to retrieve the Notetaker associated with an event."""
    print("\n=== Retrieving Event Notetaker ===")
    
    # First get the event to get the Notetaker ID
    try:
        event = nylas.events.find(
            identifier=os.getenv("NYLAS_GRANT_ID"),
            event_id=event_id,
            query_params={"calendar_id": os.getenv("NYLAS_CALENDAR_ID")}
        )
    except Exception as e:
        print(f"Error getting event: {e}")
        return None
    
    if not event.data.notetaker or not event.data.notetaker.id:
        print(f"No Notetaker found for event {event_id}")
        return None
    
    notetaker = nylas.notetakers.find(notetaker_id=event.data.notetaker.id, identifier=os.getenv("NYLAS_GRANT_ID"))
    print(f"Found Notetaker for event {event_id}:")
    print(f"- ID: {notetaker.data.id}")
    print(f"- State: {notetaker.data.state}")
    print(f"- Meeting Provider: {notetaker.data.meeting_provider}")
    print(f"- Meeting Settings:")
    print(f"  - Video Recording: {notetaker.data.meeting_settings.video_recording}")
    print(f"  - Audio Recording: {notetaker.data.meeting_settings.audio_recording}")
    print(f"  - Transcription: {notetaker.data.meeting_settings.transcription}")
    
    return notetaker

def update_event_and_notetaker(event_id: str, notetaker_id: str):
    """Demonstrates how to update both an event and its Notetaker."""
    print("\n=== Updating Event and Notetaker ===")
    
    # Create the notetaker meeting settings
    notetaker_settings = EventNotetakerSettings(
        video_recording=False,
        audio_recording=True,
        transcription=False
    )
    
    # Create the notetaker request
    notetaker = EventNotetakerRequest(
        id=notetaker_id,
        name="Updated Nylas Notetaker",
        meeting_settings=notetaker_settings
    )
    
    # Create the update request with proper types
    request_body = UpdateEventRequest(
        title="Updated Project Planning Meeting",
        description="Revised project planning with new timeline",
        metadata={
            "project_id": "PROJ-123",
            "priority": "urgent"
        },
        notetaker=notetaker
    )
    
    # Create the query parameters
    query_params = UpdateEventQueryParams(
        calendar_id=os.getenv("NYLAS_CALENDAR_ID")
    )

    updated_event = nylas.events.update(
        identifier=os.getenv("NYLAS_GRANT_ID"),
        event_id=event_id,
        request_body=request_body,
        query_params=query_params
    )
    
    return updated_event

def main():
    """Main function to run all demo examples."""
    try:
        # Create an event with a Notetaker
        event = create_event_with_notetaker()
        if not event:
            print("Failed to create event")
            return
        
        print(f"Created event with ID: {event.data.id}")
        print(f"Event Notetaker ID: {event.data.notetaker.id}")
        
        # Get the Notetaker for the event
        notetaker = get_event_notetaker(event.data.id)
        if not notetaker:
            print(f"Failed to get Notetaker for event {event.data.id}")
            return
        
        # Update both the event and its Notetaker
        updated_event = update_event_and_notetaker(event.data.id, notetaker.data.id)
        if not updated_event:
            print(f"Failed to update event {event.data.id}")
            return
        
        print(f"Updated event with ID: {updated_event.data.id}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 