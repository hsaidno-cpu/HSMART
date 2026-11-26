"""Stable error types for pilot policy and package gates."""


class PilotError(Exception):
    def __init__(self, code: str, status_code: int = 400):
        super().__init__(code)
        self.code = code
        self.status_code = status_code


class AuthenticationError(PilotError):
    def __init__(self, code: str = "invalid_token"):
        super().__init__(code, 401)


class AuthorizationError(PilotError):
    def __init__(self, code: str = "access_denied"):
        super().__init__(code, 403)


class ConflictError(PilotError):
    def __init__(self, code: str = "state_conflict"):
        super().__init__(code, 409)


class PackageVerificationError(PilotError):
    def __init__(self, code: str = "package_verification_failed"):
        super().__init__(code, 422)
