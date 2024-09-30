# each part of the web scraper inherits from a singleton mixin class that provides a function to set the download path
# the mixin class provides an object variable that keeps track of the current download location, that can be accessed by
# any of the child classes


# a flaw in the implementation of this class is if the self.download_path variable is accessed before the set_download_path is ran


class DownloadHandler:
    # Enforce single instance
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DownloadHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.download_path = None

    def set_download_path(self, driver, download_path):
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": download_path},
        }
        driver.execute("send_command", params)
        self.download_path = download_path
