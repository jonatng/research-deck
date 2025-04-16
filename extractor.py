from trafilatura import fetch_url, extract

def extract_text_from_url(url: str) -> str:
    downloaded = fetch_url(url)
    if downloaded:
        return extract(downloaded)
    return ""