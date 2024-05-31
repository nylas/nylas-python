from nylas.resources.folders import Folders

from nylas.models.folders import Folder


class TestFolder:
    def test_folder_deserialization(self):
        folder_json = {
            "id": "SENT",
            "grant_id": "41009df5-bf11-4c97-aa18-b285b5f2e386",
            "name": "SENT",
            "system_folder": True,
            "object": "folder",
            "unread_count": 0,
            "child_count": 0,
            "parent_id": "ascsf21412",
            "background_color": "#039BE5",
            "text_color": "#039BE5",
            "total_count": 0,
            "attributes": ["\\Sent"],
        }

        folder = Folder.from_dict(folder_json)

        assert folder.id == "SENT"
        assert folder.grant_id == "41009df5-bf11-4c97-aa18-b285b5f2e386"
        assert folder.name == "SENT"
        assert folder.system_folder is True
        assert folder.object == "folder"
        assert folder.unread_count == 0
        assert folder.child_count == 0
        assert folder.parent_id == "ascsf21412"
        assert folder.background_color == "#039BE5"
        assert folder.text_color == "#039BE5"
        assert folder.total_count == 0
        assert folder.attributes == "['\\\\Sent']"

    def test_list_folders(self, http_client_list_response):
        folders = Folders(http_client_list_response)

        folders.list(identifier="abc-123",query_params=None)

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/grants/abc-123/folders", None, None, None, overrides=None
        )

    def test_find_folder(self, http_client_response):
        folders = Folders(http_client_response)

        folders.find(identifier="abc-123", folder_id="folder-123")

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/grants/abc-123/folders/folder-123",
            None,
            None,
            None,
            overrides=None,
        )

    def test_create_folder(self, http_client_response):
        folders = Folders(http_client_response)
        request_body = {
            "name": "My New Folder",
            "parent_id": "parent-folder-id",
            "background_color": "#039BE5",
            "text_color": "#039BE5",
        }

        folders.create(identifier="abc-123", request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST",
            "/v3/grants/abc-123/folders",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_update_folder(self, http_client_response):
        folders = Folders(http_client_response)
        request_body = {
            "name": "My New Folder",
            "parent_id": "parent-folder-id",
            "background_color": "#039BE5",
            "text_color": "#039BE5",
        }

        folders.update(
            identifier="abc-123",
            folder_id="folder-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT",
            "/v3/grants/abc-123/folders/folder-123",
            None,
            None,
            request_body,
            overrides=None,
        )

    def test_destroy_folder(self, http_client_delete_response):
        folders = Folders(http_client_delete_response)

        folders.destroy(
            identifier="abc-123",
            folder_id="folder-123",
        )

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE",
            "/v3/grants/abc-123/folders/folder-123",
            None,
            None,
            None,
            overrides=None,
        )
