from nylas import APIClient

# Initialize and connect to the Nylas client
nylas = APIClient(
    "4o81f71v49hzofuudeae42g1",
    "cg9a5hnduixalhk6unf5t1pjc",
    "AHpJI06L9Cf7hgo4aqoG7AodflclWz"
)

event = nylas.events.get("dp67hg3jih66f0ewu43eb66ee")
print(event)
