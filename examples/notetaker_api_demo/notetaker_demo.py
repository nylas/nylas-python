import os
import sys
import json
from nylas import Client
from nylas.models.notetakers import NotetakerMeetingSettingsRequest, NotetakerState, InviteNotetakerRequest
from nylas.models.errors import NylasApiError

# Initialize the Nylas client
nylas = Client(
    api_key=os.getenv("NYLAS_API_KEY"),
    api_uri=os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")
)

def invite_notetaker():
    """Demonstrates how to invite a Notetaker to a meeting."""
    print("\n=== Inviting Notetaker to Meeting ===")
    
    try:
        meeting_link = os.getenv("MEETING_LINK")
        if not meeting_link:
            raise ValueError("MEETING_LINK environment variable is not set. Please set it with your meeting URL.")
        
        request_body: InviteNotetakerRequest = {
            "meeting_link": meeting_link,
            "name": "Nylas Notetaker",
            "meeting_settings": {
                "video_recording": True,
                "audio_recording": True,
                "transcription": True
            }
        }
        
        print(f"Request body: {json.dumps(request_body, indent=2)}")
        
        notetaker = nylas.notetakers.invite(request_body=request_body)
        
        print(f"Invited Notetaker with ID: {notetaker.data.id}")
        print(f"Name: {notetaker.data.name}")
        print(f"State: {notetaker.data.state}")
        return notetaker
    except NylasApiError as e:
        print(f"Error inviting notetaker: {str(e)}")
        print(f"Error details: {e.__dict__}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in invite_notetaker: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {e.__dict__}")
        raise

def list_notetakers():
    """Demonstrates how to list all Notetakers."""
    print("\n=== Listing All Notetakers ===")
    
    try:
        notetakers = nylas.notetakers.list()
        
        print(f"Found {len(notetakers.data)} notetakers:")
        for notetaker in notetakers.data:
            print(f"- {notetaker.name} (ID: {notetaker.id}, State: {notetaker.state})")
        
        return notetakers
    except NylasApiError as e:
        print(f"Error listing notetakers: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in list_notetakers: {str(e)}")
        raise

def get_notetaker_media(notetaker_id):
    """Demonstrates how to get media from a Notetaker."""
    print("\n=== Getting Notetaker Media ===")
    
    try:
        media = nylas.notetakers.get_media(notetaker_id)
        
        if media.recording:
            print(f"Recording URL: {media.data.recording.url}")
            print(f"Recording Name: {media.data.recording.name}")
            print(f"Recording Type: {media.data.recording.type}")
            print(f"Recording Size: {media.data.recording.size} bytes")
            print(f"Recording Created At: {media.data.recording.created_at}")
            print(f"Recording Expires At: {media.data.recording.expires_at}")
            print(f"Recording TTL: {media.data.recording.ttl} seconds")
        if media.transcript:
            print(f"Transcript URL: {media.data.transcript.url}")
            print(f"Transcript Name: {media.data.transcript.name}")
            print(f"Transcript Type: {media.data.transcript.type}")
            print(f"Transcript Size: {media.data.transcript.size} bytes")
            print(f"Transcript Created At: {media.data.transcript.created_at}")
            print(f"Transcript Expires At: {media.data.transcript.expires_at}")
            print(f"Transcript TTL: {media.data.transcript.ttl} seconds")
        
        return media
    except NylasApiError as e:
        print(f"Error getting notetaker media: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in get_notetaker_media: {str(e)}")
        raise

def leave_notetaker(notetaker_id):
    """Demonstrates how to leave a Notetaker."""
    print("\n=== Leaving Notetaker ===")
    
    try:
        nylas.notetakers.leave(notetaker_id)
        print(f"Left Notetaker with ID: {notetaker_id}")
    except NylasApiError as e:
        print(f"Error leaving notetaker: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in leave_notetaker: {str(e)}")
        raise

def main():
    """Main function to run all demo examples."""
    try:
        # Check for required environment variables
        api_key = os.getenv("NYLAS_API_KEY")
        if not api_key:
            raise ValueError("NYLAS_API_KEY environment variable is not set")
        print(f"Using API key: {api_key[:5]}...")
        
        # Invite a Notetaker to a meeting
        notetaker = invite_notetaker()
        
        # List all Notetakers
        list_notetakers()
        
        # Get media from the Notetaker (if available)
        if notetaker.data.state == NotetakerState.MEDIA_AVAILABLE:
            get_notetaker_media(notetaker.data.id)
        
        # Leave the Notetaker
        leave_notetaker(notetaker.data.id)
        
    except NylasApiError as e:
        print(f"\nNylas API Error: {str(e)}")
        print(f"Error details: {e.__dict__}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nConfiguration Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {e.__dict__}")
        sys.exit(1)

if __name__ == "__main__":
    main() 