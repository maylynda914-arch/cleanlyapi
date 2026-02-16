import re
import emoji

def clean_text(text: str) -> str:
    """Basic cleaning: trim spaces, remove weird spacing, normalize."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def remove_emojis(text: str) -> str:
    """Remove all emojis from text."""
    return emoji.replace_emoji(text, replace="")

def normalize_whitespace(text: str) -> str:
    """Fix spacing issues."""
    return re.sub(r"\s+", " ", text).strip()

def strip_urls(text: str) -> str:
    """Remove URLs from text."""
    url_pattern = r"https?://\S+|www\.\S+"
    return re.sub(url_pattern, "", text).strip()

def batch_clean(text_list: list) -> list:
    """Clean multiple texts at once."""
    return [clean_text(t) for t in text_list]
