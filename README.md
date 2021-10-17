# TelegramBot-IPU 🤖

![Technocolab-Final-Project](https://socialify.git.ci/kaustubhgupta/TelegramBot-IPU/image?description=1&language=1&owner=1&pattern=Circuit%20Board&theme=Light)

## About 😃
This bot receives the user inputs via webhook, makes backed API, and then processes it to be sent to the user. Currently, it's deployed to Heroku and wrapped in Flask which almost works 24/7. 


When a message is sent by a user to the Telegram bot, a post request is made to the corresponding webhook. I am using a self-hosted webhook so as to have more control over I/O and listen to telegram requests. Whenever my bot receives a post request for an enrollment number, firstly it is validated in the application and then the API call is made to my website. I created a REST API on my website to handle these get requests. The data received by the API is then processed to be sent to the user.

## Bot Link ⚡
Try the bot [here](https://t.me/ipuBOT)

## Preview (As of Oct 17. 2021) 📺
![demo](demo/demo.gif)
