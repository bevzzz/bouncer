if __name__ == "__main__":

    import time
    from teletubby.actors.manager import Manager
    from teletubby.apis.telegramapi import TelegramAPI
    from teletubby.apis.driveapi import GoogleDrive
    import teletubby.tools.globals as glob

    bot_token = glob.config['telegram']['token']
    drive_credentials = glob.config['drive']

    telegram = TelegramAPI(bot_token)
    drive = GoogleDrive.from_config_file(drive_credentials)
    Konstantin = Manager(telegram, drive)
    while True:
        Konstantin.talk()
        time.sleep(3)

