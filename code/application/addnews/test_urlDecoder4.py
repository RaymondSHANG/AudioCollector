import base64
import requests
from urllib.parse import urlparse

def fetch_decoded_batch_execute(article_id: str) -> str:
    s = (
        '[[["Fbv4je","[\\"garturlreq\\",[[\\"en-US\\",\\"US\\",'
        '[\\"FINANCE_TOP_INDICES\\",\\"WEB_TEST_1_0_0\\"],null,null,1,1,\\"US:en\\",'
        'null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],'
        '\"en-US\\",\\"US\\",1,[2,3,4,8],1,0,\\"655000234\\",0,0,null,0],\\"' + article_id + '\"]",null,"generic"]]]'
    )
    url = "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Referrer": "https://news.google.com/"
    }
    response = requests.post(url, headers=headers, data={"f.req": s})
    
    if response.status_code != 200:
        raise ValueError("Failed to fetch decoded URL")
    
    text = response.text
    header = '[\"garturlres\",\"'
    footer = '\",'
    
    if header not in text:
        raise ValueError("Header not found in response")
    
    start = text.split(header, 1)[1]
    if footer not in start:
        raise ValueError("Footer not found in response")
    
    return start.split(footer, 1)[0]

def decode_google_news_url(source_url: str) -> str:
    parsed_url = urlparse(source_url)
    path_segments = parsed_url.path.split("/")
    
    if parsed_url.hostname == "news.google.com" and len(path_segments) > 1 and path_segments[-2] == "articles":
        base64_part = path_segments[-1]
        decoded_bytes = base64.b64decode(base64_part)
        decoded_str = decoded_bytes.decode("latin1")
        
        prefix = bytes([0x08, 0x13, 0x22])
        suffix = bytes([0xd2, 0x01, 0x00])
        
        if decoded_bytes.startswith(prefix):
            decoded_bytes = decoded_bytes[len(prefix):]
        
        if decoded_bytes.endswith(suffix):
            decoded_bytes = decoded_bytes[:-len(suffix)]
        
        length_byte = decoded_bytes[0]
        if length_byte >= 0x80:
            decoded_str = decoded_bytes[2:length_byte + 2].decode("utf-8")
        else:
            decoded_str = decoded_bytes[1:length_byte + 1].decode("utf-8")
        
        if decoded_str.startswith("AU_yqL"):
            return fetch_decoded_batch_execute(base64_part)
        
        return decoded_str
    
    return source_url


# Example usage
if __name__ == "__main__":
    source_url = 'https://news.google.com/rss/articles/CBMitgFBVV95cUxPaUlwZElneFFmOFJDbjJOUFpOUEZPT3JJNFI5N09QcXpta1ZJZnlzZXpGSTdtdkRBdExaMnFyZjUzUkktWllwRGQ3bUExY0NmZlZwR2Rac01HVlFSbWNKa3RlcXFUTldsUTc1M2VQNU8tbE1xc0FWSG5QbXoxbDBNYmphOENQa0lMcXFrRXZpX052NkJUcUVwZ3Jab1ZUc1dOQUszaXVXbktkSUZ6NGxhd0J1VjhWQdIBuwFBVV95cUxPc1RKc3lNUVdPRXh1aFVLVWFkWXlfWnZyR09hLTlnLUpRUzItZ3JXSTAxQUtQWGpFSzVWSXpORy1yN1lfc0tIWXVaWFU3cVJXQUZxX3RCUmtxaW1LTVlrRXlvQ3FtVmFzZXZsWnlNMjR4d3kyTXZFdWJsY0FfV0NxQklVZnF1a0tsam44OWwwYUsyUDFLY1F4OWdLQVV6aUZYVUFiTVQ4S0locWgyNVdIMTkyQmdGWVctU25r?oc=5&hl=en-US&gl=US&ceid=US:en'
    decoded_url = decode_google_news_url(source_url)
    print(decoded_url)