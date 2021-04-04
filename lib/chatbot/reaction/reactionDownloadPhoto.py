from lib.chatbot.reaction.reactionBase import ReactionBase
from lib.utils.helpers import get_timestamp


class ReactionDownloadPhoto(ReactionBase):

    def __init__(self, message, me):
        super().__init__(message, me)
        self.upload_successful = False

    def response(self):
        if self.upload_successful:
            text = "Nice pic! I added it to your personal folder"
        else:
            text = "Oh crap, I couldn't download that. Try again with a different photo"

        self._send_message(text)

    def action(self):
        file_id, caption = self.message.get_picture_with_caption()
        bytes_picture = self._download_photo(file_id)

        self._save_photo(bytes_picture, self.user.get_username())

    def _download_photo(self, file_id):
        return self.me.chatbot.download_file(file_id)

    def _save_photo(self, img, to_dir):
        name = '{}_{}.jpeg'.format(to_dir, get_timestamp())

        try:
            self.me.storage.write_image(
                img=img,
                name=name,
                to_dir=to_dir
            )
            self.upload_successful = True
        except:
            print("Could not save image")

