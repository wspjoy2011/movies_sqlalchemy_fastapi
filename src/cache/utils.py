from decimal import Decimal
from typing import Union
from uuid import UUID


def json_serializer(obj: Union[UUID, Decimal]) -> Union[str, float]:
    """
    Custom JSON serializer for unsupported types such as UUID and Decimal.

    Args:
        obj (Union[UUID, Decimal]): The object to serialize. Supports UUID and Decimal types.

    Returns:
        Union[str, float]: A JSON-serializable representation of the object:
            - str for UUID,
            - float for Decimal.

    Raises:
        TypeError: If the object type is not supported for serialization.
    """
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
