class ProjectError(Exception):
    pass


class OwnerNotFound(ProjectError):
    def __init__(self, message="Owner not found"):
        super().__init__(message)
