# SGD-SEK-Telebot

## Overview
- Using the ***python-telegram-bot library*** along with ***currencyapi***, this bot sends SGD to SEK announcements every 6 hours.
- https://t.me/swedishER_bot

## Features
- Automatically fetches the latest exchange rate between SGD and SEK.
- Sends periodic announcements every 6 hours.
- Allows users to subscribe and unsubscribe from announcements via Telegram commands.

## Prerequisites
- Python 3.x
- Telegram bot token
- AlphaVantage API key
- currencyapi API key

## Versions
- There are 2 other versions of the bot: main_scrape.py and main_vantage_api.py
- Deployed version is using main_currencyapi.py which uses ***currencyapi*** to obtain the necessary data
- main_scrape.py is using ***Beautiful Soup*** library to scrape the data needed
- main_vantageapi.py is using ***AlphaVantage API*** to obtain the necessary data