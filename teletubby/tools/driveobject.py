import io
from teletubby.general import helpers
from googleapiclient.http import MediaIoBaseUpload


class DriveObject:
    """
    DriveObject represents any file (photo, text document, video, JSON file etc.)
    or folder that can be found on Google Drive. Its attributes are, e.g. file's
    id or date of creation
    """
    mime_type = None

    def __init__(self, body, owner):
        self.drive_id = None
        self.body = body
        self.owner = owner
        self.name = self.build_name()

    def build_name(self):
        return '{}_{}'.format(self.owner.username, helpers.get_timestamp())

    def set_drive_id(self, drive_id):
        self.drive_id = drive_id

    def get_upload_media(self):
        io_body = io.BytesIO(self.body)
        media = MediaIoBaseUpload(
            fd=io_body,
            mimetype=self.mime_type,
            chunksize=self.get_size()
        )
        return media

    def get_size(self):
        return len(self.body)


class DrivePicture(DriveObject):
    mime_type = 'image/jpeg'

    def __init__(self, body, owner):
        super().__init__(body, owner)


class DriveFolder(DriveObject):
    mime_type = 'application/vnd.google-apps.folder'
