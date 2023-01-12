import uuid

import websocket

from nylas.client import APIClient
from nylas.client.restful_models import Webhook
from config import DEFAULT_REGION


def open_webhook_tunnel(api, config):
    """
    Open a webhook tunnel and register it with the Nylas API
    1. Creates a UUID
    2. Opens a websocket connection to Nylas' webhook forwarding service,
       with the UUID as a header
    3. Creates a new webhook pointed at the forwarding service with the UUID as the path

    When an event is received by the forwarding service, it will push directly to this websocket
    connection

    Args:
        api (APIClient): The configured Nylas API client
        config (dict[str, any]): Configuration for the webhook tunnel, including callback functions, region,
            and events to subscribe to
    """

    ws_domain = "wss://tunnel.nylas.com"
    callback_domain = "cb.nylas.com"
    # This UUID will map our websocket to a webhook in the forwarding server
    tunnel_id = str(uuid.uuid4())

    region = config.get('region', DEFAULT_REGION)
    triggers = config.get('triggers', [e.value for e in Webhook.Trigger])
    on_message = config.get('on_message', None)
    on_open = config.get('on_open', None)
    on_error = config.get('on_error', None)
    on_close = config.get('on_close', None)
    on_ping = config.get('on_ping', None)
    on_pong = config.get('on_pong', None)
    on_cont_message = config.get('on_cont_message', None)
    on_data = config.get('on_data', None)

    ws = websocket.WebSocketApp(
        ws_domain,
        header={
            'Client-Id': api.client_id,
            'Client-Secret': api.client_secret,
            'Tunnel-Id': tunnel_id,
            'Region': region.value,
        },
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_ping=on_ping,
        on_pong=on_pong,
        on_cont_message=on_cont_message,
        on_data=on_data,
    )
    _build_webhook_tunnel(api, callback_domain, tunnel_id, triggers)
    ws.run_forever()


def _build_webhook_tunnel(api, callback_domain, tunnel_path, triggers):
    webhook = api.webhooks.create()
    webhook.callback_url = "https://{}/{}".format(callback_domain, tunnel_path)
    webhook.triggers = triggers
    webhook.state = Webhook.State.ACTIVE.value
    webhook.save()
    return webhook

