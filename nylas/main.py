from nylas import Client
from nylas.models.credentials import CredentialRequest, UpdateCredentialRequest

client_id = "547b1b75-6623-4dcd-8ea9-baf50cf00952"
client_secret = "JzL6OyQVaXvowk8czuGW45mHhVCoHfnZW"
api_key = "nyk_v0_JlN7OgZUgsmEoCx6tguhTMGcRqE0XpoLZz6Lp3824ivER13baJbXENK9EPYw5eKU"


nylas = Client(
    api_key=api_key,
)

creds_data = {"client_id":"bce5ddf5-038e-4653-9843-ec1d4274549e","client_secret":"ZM48Q~Yng3WqXjM2D3f..zZ4g.LBJWFCmE_b7b3Y"}
#
#
creds_created,_ = nylas.connectors.credentials.create("microsoft",CredentialRequest(name="Test creds",credential_type="adminconsent",credential_data=creds_data))
# #
print(creds_created)
# # #
list_response = nylas.connectors.credentials.list("microsoft");
#
print(list_response)
#
creds,_ = nylas.connectors.credentials.find("microsoft",creds_created.id)
# #
print(creds)

updated_creds,_=nylas.connectors.credentials.update("microsoft",creds_created.id,UpdateCredentialRequest(name="New creds",credential_data=creds_data))
# #
print(updated_creds)

deleted_response = nylas.connectors.credentials.destroy("microsoft",updated_creds.id)
print(deleted_response)