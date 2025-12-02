class CoreError(Exception):
    """Base class for domain-level exceptions."""


class ProductAlreadyExists(CoreError):
    """Raised when attempting to create a duplicate product."""


class ProductNotFound(CoreError):
    """Raised when a product lookup fails."""


class SaleNotFound(CoreError):
    """Raised when a sale lookup fails."""