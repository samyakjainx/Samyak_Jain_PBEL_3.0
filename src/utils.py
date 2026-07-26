"""
utils.py
---------
Miscellaneous helper functions shared across the app: input
validation, CSV export, and small formatting utilities.
"""

import io
import pandas as pd


def validate_uploaded_files(files: list, allowed_extensions=(".pdf", ".docx")) -> tuple:
    """
    Filters an uploaded file list into valid and invalid groups
    based on file extension.

    Args:
        files: list of Streamlit UploadedFile objects.
        allowed_extensions: tuple of accepted extensions.

    Returns:
        (valid_files, invalid_filenames) tuple.
    """
    valid_files = []
    invalid_filenames = []

    for f in files:
        if f.name.lower().endswith(allowed_extensions):
            valid_files.append(f)
        else:
            invalid_filenames.append(f.name)

    return valid_files, invalid_filenames


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Converts a pandas DataFrame into CSV bytes suitable for
    st.download_button.

    Args:
        df: DataFrame to export.

    Returns:
        UTF-8 encoded CSV bytes.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def clean_candidate_name(filename: str) -> str:
    """
    Strips file extension and replaces underscores/hyphens with
    spaces to produce a friendlier display name for a candidate.

    Args:
        filename: original uploaded file name.

    Returns:
        Cleaned display name, title-cased.
    """
    name = filename.rsplit(".", 1)[0]
    name = name.replace("_", " ").replace("-", " ")
    return name.strip().title()


def truncate_text(text: str, max_chars: int = 400) -> str:
    """
    Truncates text for preview display, adding an ellipsis if cut.

    Args:
        text: full text.
        max_chars: maximum characters to keep.

    Returns:
        Truncated text string.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def format_skill_list(skills: list, empty_placeholder: str = "None") -> str:
    """
    Formats a list of skills into a readable comma-separated string,
    with a placeholder for empty lists.

    Args:
        skills: list of skill strings.
        empty_placeholder: text to show if the list is empty.

    Returns:
        Formatted string.
    """
    if not skills:
        return empty_placeholder
    return ", ".join(s.title() for s in skills)
