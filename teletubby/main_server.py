if __name__ == '__main__':

    from teletubby.apis.myapi_server import Server
    from teletubby.actors.manager import Manager
    from teletubby.apis.telegramapi import TelegramAPI
    from teletubby.apis.driveapi import GoogleDrive
    import teletubby.tools.globals as glob

    bot_token = glob.config['telegram']['token']
    drive_credentials = glob.config['drive']

    chatbot = TelegramAPI(bot_token)
    drive = GoogleDrive.from_config_file(drive_credentials)
    manager = Manager(chatbot, drive)
    server = Server(manager)

    server.activate()
