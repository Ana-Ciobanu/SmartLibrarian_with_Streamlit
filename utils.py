import json

def get_summary_by_title(title, file_path="complete_book_summaries.json"):
    """
    Returns the detailed summary for a given book title from the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
        for entry in summaries:
            if entry['title'].lower() == title.lower():
                return entry['summary']
    except Exception as e:
        print(f"Error loading summary: {e}")
    return None
