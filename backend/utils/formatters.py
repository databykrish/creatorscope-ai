"""Utility formatters for converting raw values to display format."""


def format_number(num: int) -> str:
    """Format large numbers to human-readable format.

    Args:
        num: Number to format

    Returns:
        Formatted string (e.g., "1.1M", "890K", "2.3B")
    """
    if num is None or num == 0:
        return "0"

    num = int(num)

    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B".rstrip("0").rstrip(".")
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M".rstrip("0").rstrip(".")
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K".rstrip("0").rstrip(".")
    else:
        return str(num)


def calculate_engagement_rate(likes: int, views: int) -> float:
    """Calculate engagement rate as a percentage.

    Args:
        likes: Total engagement (likes, comments, etc.)
        views: Total views

    Returns:
        Engagement rate as a percentage (e.g., 4.8)
    """
    if views == 0:
        return 0.0
    return round((likes / views) * 100, 2)


def calculate_consistency_score(
    upload_history: list[dict[str, int]],
) -> int:
    """Calculate upload consistency score (0-100).

    Args:
        upload_history: List of dicts with 'date' and 'count' keys

    Returns:
        Consistency score (0-100)
    """
    if not upload_history or len(upload_history) < 2:
        return 50  # Default for insufficient data

    # Calculate average days between uploads
    intervals = []
    for i in range(1, len(upload_history)):
        prev_date = upload_history[i - 1].get("date", 0)
        curr_date = upload_history[i].get("date", 0)
        if curr_date > prev_date:
            intervals.append(curr_date - prev_date)

    if not intervals:
        return 50

    avg_interval = sum(intervals) / len(intervals)
    max_interval = max(intervals)

    # Score based on regularity
    if max_interval == 0:
        return 100
    regularity = min(100, int((avg_interval / max_interval) * 100))
    return regularity


def truncate_text(text: str, max_length: int = 150) -> str:
    """Truncate text to max length, adding ellipsis if needed.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
