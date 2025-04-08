import os
from datetime import datetime, timedelta

from nylas import Client
from nylas.models.notetakers import NotetakerMeetingSettings, MeetingProvider
from nylas.models.events import EventMetadata

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
    
    event = nylas.events.create(
        title="Project Planning Meeting",
        description="Initial project planning and resource allocation",
        start_time=start_time,
        end_time=end_time,
        metadata=EventMetadata(
            project_id="PROJ-123",
            priority="high"
        )
    )
    
    # Create a Notetaker bot for the event
    notetaker = nylas.notetakers.invite(
        meeting_link=event.conferencing.details.meeting_url,
        name="Project Planning Notetaker",
        meeting_settings=NotetakerMeetingSettings(
            video_recording=True,
            audio_recording=True,
            transcription=True
        )
    )
    
    print(f"Created event with ID: {event.id}")
    print(f"Created Notetaker with ID: {notetaker.id}")
    return event, notetaker

def get_event_notetaker(event_id):
    """Demonstrates how to retrieve the Notetaker associated with an event."""
    print("\n=== Retrieving Event Notetaker ===")
    
    # First get the event to get the Notetaker ID
    event = nylas.events.find(event_id)
    if not event.notetaker or not event.notetaker.id:
        print(f"No Notetaker found for event {event_id}")
        return None
    
    notetaker = nylas.notetakers.find(event.notetaker.id)
    print(f"Found Notetaker for event {event_id}:")
    print(f"- ID: {notetaker.id}")
    print(f"- State: {notetaker.state}")
    print(f"- Meeting Provider: {notetaker.meeting_provider}")
    
    return notetaker

def update_event_and_notetaker(event_id, notetaker_id):
    """Demonstrates how to update both an event and its Notetaker."""
    print("\n=== Updating Event and Notetaker ===")
    
    # Update the event
    updated_event = nylas.events.update(
        event_id,
        title="Updated Project Planning Meeting",
        description="Revised project planning with new timeline",
        metadata=EventMetadata(
            project_id="PROJ-123",
            priority="urgent"
        )
    )
    
    # Update the Notetaker
    updated_notetaker = nylas.notetakers.update(
        notetaker_id,
        name="Updated Project Planning Notetaker",
        meeting_settings=NotetakerMeetingSettings(
            video_recording=True,
            audio_recording=True,
            transcription=True
        )
    )
    
    print(f"Updated event with ID: {updated_event.id}")
    print(f"Updated Notetaker with ID: {updated_notetaker.id}")
    return updated_event, updated_notetaker

def main():
    """Main function to run all demo examples."""
    try:
        # Create an event with a Notetaker
        event, notetaker = create_event_with_notetaker()
        
        # Get the Notetaker for the event
        get_event_notetaker(event.id)
        
        # Update both the event and its Notetaker
        updated_event, updated_notetaker = update_event_and_notetaker(event.id, notetaker.id)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 