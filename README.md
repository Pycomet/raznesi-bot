# tgbot-starterkit

This repository is a basic flask script for hosting telegram bots with either Google Cloud or Heroku

### Bot Process Flow

## Bot Register New Users And Log New Order

- The bot is connected to a group chat to relay the order
- The bot takes formatted orders from users
- If the user making the first order, register the user with an address to DB
- Process order to group chat with the accept button
- Once the button is clicked, the order is updated with the person that wishes to sell
- Order details are sent to admin and chat
