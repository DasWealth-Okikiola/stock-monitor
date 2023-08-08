import requests
from twilio.rest import Client

stock_url = "https://www.alphavantage.co/query?"
news_url = "https://newsapi.org/v2/everything?"

vantage_key = "your vantage API key"
news_api_key = "news key"
twilio_auth_token = "your auth token"
twilio_sid = "twilio sid"
twilio_phone_number = "+ your twilio phone"

symbol = "TSLA"
company_name = 'Tesla Inc'

stock_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": vantage_key
}
stock_response = requests.get(url=stock_url, params=stock_api_parameters)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
# Tracking down needed data by passing in first key
# making all items a list, so it gets the first and second day data
data_dict = [v for (k, v) in data.items()]
day_1 = data_dict[0]
day_2 = data_dict[1]
yesterday_close = day_1["4. close"]
two_days_ago_close = day_2["4. close"]
print(yesterday_close, two_days_ago_close)

# Calculate the absolute difference between the two values
difference = float(yesterday_close) - float(two_days_ago_close)
# Calculate the percentage difference
percentage_difference = round((difference / float(yesterday_close)) * 100)

emoji = None
if percentage_difference > 0:
    emoji = "🔺"
else:
    emoji = "🔻"

# Calculate the percentage difference
# Print the result
# print(f"Percentage Difference: {percentage_difference}%")

if abs(percentage_difference) > 1:
    news_api_params = {
        "qInTitle": company_name,
        "apiKey": news_api_key,
    }

    news_response = requests.get(url=news_url, params=news_api_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_articles = news_data[:3]
    #   print(three_articles)
    #   make a list of articles and headlines
    articles_formatted = [
        f"{company_name}: {percentage_difference}%{emoji}\nHeadline: {article['title']}\nBrief: {article['description']}"
        for article in
        three_articles]
    #  print(articles_formatted)
    # send each article separately with twilio
    for article in articles_formatted:
        client = Client(twilio_sid, twilio_auth_token)
        message = client.messages.create(
            from_=twilio_phone_number,
            body=article,
            to='receiver"s phone'
        )
        print(message.status)
