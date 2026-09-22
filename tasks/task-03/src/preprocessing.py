"""Text preprocessing utilities."""

import re


def preprocess_text(text: str, lowercase: bool = True, remove_punctuation: bool = False) -> str:
    """
    Preprocess text for embedding generation.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        remove_punctuation: Remove punctuation marks
    
    Returns:
        Preprocessed text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Lowercase
    if lowercase:
        text = text.lower()
    
    # Remove punctuation
    if remove_punctuation:
        text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """
    Extract keywords from text (simple word frequency).
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
    
    Returns:
        List of keywords
    """
    words = text.lower().split()
    
    # Simple stopwords
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'that',
                 'this', 'these', 'those', 'it', 'its', 'they', 'them', 'their'}
    
    # Count words
    word_freq = {}
    for word in words:
        if len(word) > 2 and word not in stopwords:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, _ in sorted_words[:top_n]]
