# TelegramBot-IPU

![TelegramBot-IPU](https://socialify.git.ci/kaustubhgupta/TelegramBot-IPU/image?language=1&theme=Light&stargazers=1&description=1&pulls=1&issues=1&forks=1&owner=1)

![demo](demo/demo.gif)
Try the bot [here](https://t.me/ipuBOT).
This bot receives the user inputs via webhook, makes backed API, and then processes it to be sent to the user. Currently, it's deployed to Heroku and wrapped in Flask which almost works 24/7.

## How does it work?
When a message is sent by a user to the Telegram bot, a post request is made to the corresponding webhook. I am using self hosted web hook so as to have more control over I/O and listen to telegram request.

## How result data is fetched?
Whenever my bot receives a post request for an enrollment number, firstly it is validated in the application and then the API call is made to my website. I created a REST API in my website to handle these get requests. The data received by the API is then processed to be sent to the user.

## Note:
~~*Currently the telegram bot is on maintenance mode as I have consumed whole free dynos on Heroku this month. I am trying to migrate it to a better deployment service so that it is available 24x7 :-)*~~

The bot is fully functional now and will be available 24x7 :-)
