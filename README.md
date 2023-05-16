# NAMMA YATRI AUTOMATE - Ride Booking WhatsApp Bot

Backend for AI based chatbot to book ride for Namma Yatri and save user data, update metrics. 


## Problem statement

The ability to book a Namma Yatri auto could open up more demand. Build innovative tech solutions to let customers book an auto without installing the app - E.g. website, WhatsApp, SMS, Phone etc that will cater to users who are uncomfortable or unwilling to use Apps


## Proposed Solution

We propose an innovative solution to help customers book rides with Namma Yatri using __WhatsApp__. Our proposed WhatsApp booking bot, AutoMate, is a simple, user-friendly solution that will make it easier for customers to book rides with Namma Yatri. 
By leveraging the widespread popularity of WhatsApp, we can reach a wider audience and make the booking process more convenient and accessible. We believe this solution aligns well with Namma Yatri's community-led platform and decentralized operations model and will help to drive more demand for their services


## Why WhatsApp Bot?

A WhatsApp bot is a particularly good solution for booking rides in a city like Bangalore because WhatsApp is widely used in the city, with many people relying on it as their primary mode of communication. This means that a WhatsApp booking bot has the potential to reach a large number of potential customers in the city, making it an effective way to generate more demand for Namma Yatri's services. <br/>

A WhatsApp booking bot is a user-friendly and convenient option that can help to streamline the booking process and make it easier for customers to access Namma Yatri's services. By eliminating the need to install an app, the WhatsApp bot can also cater to users who may be uncomfortable or unwilling to use traditional ride-hailing apps.<br/>

Overall, a WhatsApp bot is a well-suited solution for booking rides in Bangalore, as it is a user-friendly, accessible, and convenient option that can help to generate more demand for Namma Yatri's services in this bustling city.


## What makes Automate special?

1. AutoMate is not your regular condition-based bot, it is a __Conversational AI__ bot so it understands the input given by the user and extracts data on its own. 
2. It uses Google Maps API to autocomplete the input entered by the user and then take the most relavant and matching entry to the user input. It then extracts the latitude and longitude and then uses that to find the distance between Source and Destination. It can further be used to show the expected duration of the entire journey based on traffic patterns. 
3. The Chatbot has been developed using Amazon Lex and the entire computition is handled by Amazon Lambda. The database used to store parameters is Amazon DynamoDB so it never faces downtime and can upscale as per the number of users accessing it

## How to access Automate?

The chatbot is live and can be accessed by texting ```join magic-feel``` to the number ```+1 (415) 523-8886``` on WhatsApp.


## Insights

The Web portal containing the live data entered by any user and corresponding __Data Analytics__ can be accessed via:
```
https://paras-sood.github.io/botMetrics/
```


## Future Scope

1. Currently, the bot picks the most relavand the first matched location but in future, we can give the user a set of relavant entries to choose from.
2. A database that keeps track of all the locations that are not served currently. This can further be used to determine where to expand the services to.
3. The bot can further be programmed to give a web-link for live navigation of the ride and notify users with live updates of the ride before an upcoming ride on WhatsApp itself.
4. A database that keeps values of latitude and longitude of a particular
place ID to reduce the number of calls made to the Google Maps API


## Contributing

Contributions are always welcome. _Make sure to write in detail what changes you are proposing._


## Bonus

One of the most underrated YT channel I found - [Corporate Tech](https://www.youtube.com/channel/UCao0lcoqff8hpG27UipstrQ). Do check it out now. <br/>
Happy Coding...
