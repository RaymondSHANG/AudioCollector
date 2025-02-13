import base64
import requests
from urllib.parse import urlparse

def fetch_decoded_batch_execute(article_id):
    """Fetch the actual URL using Google's batchexecute protocol."""
    payload = (
        f'[[["Fbv4je","[\\"garturlreq\\",[[\\"en-US\\",\\"US\\",'
        f'[\\"FINANCE_TOP_INDICES\\",\\"WEB_TEST_1_0_0\\"],null,null,1,1,'
        f'\\"US:en\\",null,180,null,null,null,null,null,0,null,null,'
        f'[1608992183,723341000]],\\"en-US\\",\\"US\\",1,[2,3,4,8],1,0,'
        f'\\"655000234\\",0,0,null,0],\\"{article_id}\\"]",null,"generic"]]]'
    )

    response = requests.post(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
        headers={
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Referrer": "https://news.google.com/"
        },
        data={"f.req": payload}
    )

    text = response.text
    header = '[\\"garturlres\\",\\"'
    footer = '\\",'

    if header in text:
        start = text.split(header, 1)[1]
        if footer in start:
            return start.split(footer, 1)[0]

    raise ValueError("Could not extract the actual article URL")

def decode_google_news_url(source_url):
    """Decode a Google News encoded RSS article URL into the actual news article link."""
    parsed_url = urlparse(source_url)
    path_parts = parsed_url.path.split("/")

    if parsed_url.hostname == "news.google.com" and len(path_parts) > 2 and path_parts[-2] == "articles":
        base64_encoded = path_parts[-1]

        try:
            decoded_bytes = base64.b64decode(base64_encoded)
            decoded_str = decoded_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return source_url  # If decoding fails, return original URL

        prefix = bytes([0x08, 0x13, 0x22])
        suffix = bytes([0xd2, 0x01, 0x00])

        # Remove prefix if present
        if decoded_bytes.startswith(prefix):
            decoded_bytes = decoded_bytes[len(prefix):]

        # Remove suffix if present
        if decoded_bytes.endswith(suffix):
            decoded_bytes = decoded_bytes[:-len(suffix)]

        # Extract the actual URL
        len_byte = decoded_bytes[0]
        if len_byte >= 0x80:
            extracted_url = decoded_bytes[2:len_byte + 2].decode("utf-8", errors="ignore")
        else:
            extracted_url = decoded_bytes[1:len_byte + 1].decode("utf-8", errors="ignore")

        # Handle the newer encoding style
        if extracted_url.startswith("AU_yqL"):
            return fetch_decoded_batch_execute(base64_encoded)

        return extracted_url
    else:
        return source_url

# Example usage:
original_url = "https://news.google.com/rss/articles/CBMitgFBVV95cUxPaUlwZElneFFmOFJDbjJOUFpOUEZPT3JJNFI5N09QcXpta1ZJZnlzZXpGSTdtdkRBdExaMnFyZjUzUkktWllwRGQ3bUExY0NmZlZwR2Rac01HVlFSbWNKa3RlcXFUTldsUTc1M2VQNU8tbE1xc0FWSG5QbXoxbDBNYmphOENQa0lMcXFrRXZpX052NkJUcUVwZ3Jab1ZUc1dOQUszaXVXbktkSUZ6NGxhd0J1VjhWQdIBuwFBVV95cUxPc1RKc3lNUVdPRXh1aFVLVWFkWXlfWnZyR09hLTlnLUpRUzItZ3JXSTAxQUtQWGpFSzVWSXpORy1yN1lfc0tIWXVaWFU3cVJXQUZxX3RCUmtxaW1LTVlrRXlvQ3FtVmFzZXZsWnlNMjR4d3kyTXZFdWJsY0FfV0NxQklVZnF1a0tsam44OWwwYUsyUDFLY1F4OWdLQVV6aUZYVUFiTVQ4S0locWgyNVdIMTkyQmdGWVctU25r?oc=5&hl=en-US&gl=US&ceid=US:en"

decoded_url = decode_google_news_url(original_url)
print("Decoded URL:", decoded_url)
