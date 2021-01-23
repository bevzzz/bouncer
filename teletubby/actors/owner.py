import teletubby.tools.globals as glob
from teletubby.apis.driveapi import GoogleDrive


class Owner:
    """
    Represents a person, who talks to TelegramBot and whose pictures might be sent.
    Has information about the Storage (both LocalStorage and DriveStorage) where
    files related to him are written to/read from.
    """
    instances = {}

    def __init__(self, owner_dto):
        self.username = owner_dto.get_username()
        self.owner_id = owner_dto.get_id()
        self.first_name = owner_dto.get_firstname()
        self.last_name = owner_dto.get_lastname()
        self.full_name = owner_dto.get_fullname()
        # self.folder_id = self.get_folder_id()
        self.role = 'GUEST'
        self.offer_auth = True
        self.instances[self.owner_id] = self

    @classmethod
    def get_instance(cls, params):
        owner_dto = OwnerDTO(params)
        owner_id = owner_dto.get_id()
        try:
            owner = cls.instances[owner_id]
        except KeyError:
            owner = cls(owner_dto)
        return owner

    def get_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def ask_to_authorize(self):
        return self.offer_auth

    def set_ask_to_authorize_false(self):
        self.offer_auth = False

    def make_a_friend(self):
        self.role = 'FRIEND'

    def get_folder_id(self):
        google_drive = GoogleDrive.from_config_file(glob.config['drive'])
        if google_drive.exists_folder(self.username):
            folder_id = google_drive.get_folder_by_name(self.username)['id']
        else:
            folder_id = google_drive.create_folder(self.username)
        return folder_id


class OwnerDTO:

    def __init__(self, params):
        self.params = params

    def get_id(self):
        return self.params['id']

    def is_bot(self):
        return self.params['is_bot']

    def get_username(self):
        return self.params.get('username', '')

    def get_firstname(self):
        return self.params.get('first_name', '')

    def get_lastname(self):
        return self.params.get('last_name', '')

    def get_fullname(self):
        firstname = self.get_firstname()
        lastname = self.get_lastname()
        return ' '.join([firstname, lastname])
