from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

original_url = "https://news.google.com/rss/articles/CBMiWkFVX3lxTE1KYmQyTGY4Sk12ejVrRUluM2UzVmY3Wmt6YjA1OG9DejRDUFN2NmVkLW1wclJZZF8zYkxwRm5GT3VNc2gySGcxNGRET0Ywa3ZqNm5PVElFQks4d9IBX0FVX3lxTE9rckhtOG9nXzF2dy1pdlg4MG9hbEhsZGRHc195bkwxWDk2WWJzTDFoZ0l6VlNIbWtnTVlWVHJoMUNiSW5lRmZWTE8xVG82MXdfUHZhRkRvN2dSbzRNRzc4?oc=5&hl=en-US&gl=US&ceid=US:en"

driver.get(original_url)
redirected_url = driver.current_url  # Get the final redirected URL

print("Redirected URL:", redirected_url)

driver.quit()
