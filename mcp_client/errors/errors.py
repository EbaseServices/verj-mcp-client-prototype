from ..utilities.errors_util import ProjectError


class ClientError(ProjectError) :
    """Wraps underlying exceptions to make handling them easier for calling code."""
