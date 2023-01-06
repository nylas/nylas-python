from flask import Blueprint, request, current_app

from nylas.services.routes import DefaultPaths, Routes
from nylas.client import APIClient


class FlaskBinding(Blueprint):
    def __init__(
        self,
        name,
        import_name,
        api,
        default_scopes,
        exchange_mailbox_token_callback,
        client_uri=None,
        override_paths=None,
    ):
        """
        Build a Flask blueprint with routes for:
        1. '/nylas/generate-auth-url': Building the URL for authenticating users to your application via Hosted Authentication
        2. '/nylas/exchange-mailbox-token': Exchange an authorization code for an access token

        Args:
            name (str):
            import_name (str):
            api (APIClient):
            default_scopes (list[str]):
            exchange_mailbox_token_callback:
            client_uri (str):
            override_paths (dict):
        """
        super(FlaskBinding, self).__init__(name, import_name)
        current_app.config["routes"] = Routes(api)
        current_app.config["default_scopes"] = default_scopes
        current_app.config[
            "exchange_mailbox_token_callback"
        ] = exchange_mailbox_token_callback
        current_app.config["client_uri"] = client_uri
        current_app.config["override_paths"] = override_paths

    _nylas_blueprint = Blueprint("nylas", __name__)

    @_nylas_blueprint.route(DefaultPaths.BUILD_AUTH_URL, methods=["POST"])
    def build_auth_url():
        request_body = request.get_json()
        auth_url = current_app.config.get("routes").build_auth_url(
            current_app.config.get("default_scopes"),
            request_body["email_address"],
            request_body["success_url"],
            client_uri=current_app.config.get("client_uri"),
        )
        return auth_url

    @_nylas_blueprint.route(DefaultPaths.EXCHANGE_CODE_FOR_TOKEN, methods=["POST"])
    def exchange_code_for_token():
        request_body = request.get_json()
        access_token = current_app.config.get("routes").exchange_code_for_token(
            request_body["token"]
        )
        res = access_token

        if current_app.config.get("exchange_mailbox_token_callback") and callable(
            current_app.config.get("exchange_mailbox_token_callback")
        ):
            res = current_app.config.get("exchange_mailbox_token_callback")(access_token)

        return res

    def build(self):
        """
        Returns the Flask blueprint configured with Nylas routes to be used in a Flask application

        Returns:
            Blueprint: The configured Flask blueprint instance
        """
        return self._nylas_blueprint
