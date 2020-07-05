# TelegramBot-IPU
This is the extension to my IPU results website. This app fetches data from the website's own REST API and then processes the jsonified output of the API to be sent to the telegram bot via the Telegram's own webhook. Currently, its deployed to Heroku as worker dyno which almost works 24/7.

## How does it work?
When a message is sent by a user to the Telegram bot, a post request is made to the corresponding webhook. I am using telegram webhook as I didn't wanted to complicate things with my present [ipu results website](https://ipuresultskg.herokuapp.com/) making it to listen to telegram request. So, when a request is made, it can be fetched via Telegram APIs and I have integrated that APIs to a custom Telgram Bot class file. I made my own Telegram Bot class to handle all the post and API calls.

## How result data is fetched?
Whenever my bot receives a post request for a enrollment number, firstly it is validated in the application and then the API call is made to my website. I created a REST API in my website to handle these get requests. The data received by the API is then processed to be sent to the user.
