# TelegramBot-IPU
![demo](demo/demo.gif)
Try the bot [here](https://t.me/ipuBOT).
This is the extension to my IPU results website. This script fetches data from the website's own REST API and then processes the jsonified output of the API to be sent to the telegram bot via my own hosted webhook. Currently, its deployed to Heroku as a worker dyno which almost works 24/7.

## How does it work?
When a message is sent by a user to the Telegram bot, a post request is made to the corresponding webhook. I am using self hosted web hook so as to have more control over I/O and listen to telegram request.

## How result data is fetched?
Whenever my bot receives a post request for an enrollment number, firstly it is validated in the application and then the API call is made to my website. I created a REST API in my website to handle these get requests. The data received by the API is then processed to be sent to the user.

## Note:
~~*Currently the telegram bot is on maintenance mode as I have consumed whole free dynos on Heroku this month. I am trying to migrate it to a better deployment service so that it is available 24x7 :-)*~~

The bot is fully functional now and will be available 24x7 :-)
