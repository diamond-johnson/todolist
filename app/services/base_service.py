from typing import Optional
from app.exceptions.base import ValidationError


class BaseService:
    """Base service class with shared validation logic."""

    def _validate_text(self, text: Optional[str], max_words: int, field: str) -> None:
        """Validate text length to prevent overly long inputs."""
        if text is None:
            return
        words = text.split()
        if len(words) > max_words:
            raise ValidationError(f"{field} exceeds {max_words} words")