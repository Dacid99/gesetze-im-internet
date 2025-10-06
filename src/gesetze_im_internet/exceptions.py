class GesetzeImInternetError(Exception):
    pass


class ValidationError(GesetzeImInternetError):
    pass


class DownloadError(GesetzeImInternetError):
    pass


class BadDataError(GesetzeImInternetError):
    pass


class ImproperTag(GesetzeImInternetError):
    pass
