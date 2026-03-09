class DomainError(Exception):
    """Base class for domain errors."""
    pass

#Error 404: Not Found
class NotFoundError(DomainError):
    """Raised when an entity is not found."""
    def __init__(self, entity: str, identifier: object) -> None:
        self.entity = entity
        self.identifier = identifier
        super().__init__(f"{entity} with identifier '{identifier}' not found.")

#Error 409: Conflict
class ConflictError(DomainError):
    """Raised when there is a conflict, such as a duplicate entry."""
    def __init__(self, entity: str, field: str, value: object) -> None:
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__(f"{entity} with {field} '{value}' already exists.")

#Error 422: Validation Error
class ValidationError(DomainError):
    """Raised when input data fails validation."""
    def __init__(self, entity: str, message: str) -> None:
        self.entity = entity
        self.message = message
        super().__init__(f"Validation error on entity '{entity}': {message}")

#Error 409: Integrity Error
class IntegrityError(DomainError):
    """Raised when a data integrity issue occurs, such as a foreign key violation."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"Data integrity error: {message}")