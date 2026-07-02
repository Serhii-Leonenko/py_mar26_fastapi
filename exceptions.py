class ProjectError(Exception):
    pass


class OwnerNotFound(ProjectError):
    def __init__(self, message="Owner not found"):
        super().__init__(message)


class ProjectNotFound(ProjectError):
    def __init__(self, message="Project not found"):
        super().__init__(message)


class TaskError(Exception):
    pass


class AssigneeNotFound(TaskError):
    def __init__(self, assignee_ids: list[int]):
        super().__init__(f"Assignee(s) with id(s) {assignee_ids} not found")


class TaskNotFound(TaskError):
    def __init__(self, message="Task not found"):
        super().__init__(message)


class InvalidTokenTypeError(Exception):
    pass
