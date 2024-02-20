import requests
# URL to send the request to
url = 'https://hebrew-academy.org.il/?s=%D7%90%D7%91%D7%99%D7%91#gsc.tab=0&gsc.q=%D7%90%D7%91%D7%99%D7%91&gsc.page=1'
response = requests.get(url, verify=False)


# Print the response text
print(response.text)
