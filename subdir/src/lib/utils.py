"""DataTrace Utility Functions.

Common utility functions used throughout DataTrace.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional


def generate_uuid() -> str:
    """Generate a new UUID string.

    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def parse_json_safe(data: str, default: Optional[Any] = None) -> Any:
    """Safely parse JSON string.

    Args:
        data: JSON string to parse
        default: Default value to return on error

    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def get_timestamp() -> datetime:
    """Get current UTC timestamp.

    Returns:
        Current datetime in UTC
    """
    return datetime.now(timezone.utc)


def get_timestamp_iso() -> str:
    """Get current UTC timestamp as ISO string.

    Returns:
        ISO formatted timestamp string
    """
    return datetime.now(timezone.utc).isoformat()


def format_bytes(num_bytes: int) -> str:
    """Format bytes to human-readable string.

    Args:
        num_bytes: Number of bytes

    Returns:
        Human-readable string (e.g., "1.2 GB", "500 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def format_rows(num_rows: int) -> str:
    """Format row count to human-readable string.

    Args:
        num_rows: Number of rows

    Returns:
        Human-readable string (e.g., "1.2M", "500K")
    """
    if num_rows >= 1_000_000:
        return f"{num_rows / 1_000_000:.1f}M"
    elif num_rows >= 1_000:
        return f"{num_rows / 1_000:.1f}K"
    return str(num_rows)


def sanitize_sql_identifier(identifier: str) -> str:
    """Sanitize SQL identifier to prevent injection.

    Args:
        identifier: SQL identifier to sanitize

    Returns:
        Sanitized identifier
    """
    # Remove potentially dangerous characters
    return "".join(c for c in identifier if c.isalnum() or c in "_-").strip()


def batch_list(items: list[Any], batch_size: int = 100) -> list[list[Any]]:
    """Split a list into batches.

    Args:
        items: List to split
        batch_size: Size of each batch

    Returns:
        List of batches
    """
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def get_dict_hash(d: dict[str, Any]) -> str:
    """Get a consistent hash for a dictionary.

    Args:
        d: Dictionary to hash

    Returns:
        MD5 hash string
    """
    import hashlib

    # Sort keys for consistent hashing
    sorted_str = json.dumps(d, sort_keys=True, default=str)
    return hashlib.md5(sorted_str.encode()).hexdigest()
