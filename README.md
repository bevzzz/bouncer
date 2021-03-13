# bouncer
Dvoretski Konstantin is looking at you suspiciously...

This is a small IoT project. It intends to connect a camera (working off a RPi Zero) to Nuki and use facial recognition to allow me and my flatmates into our apartment.
The app consists of 3 main parts:

1. Manager - server which can be controlled via a Telegram bot.
1. Facial recognition service - a service which can identify the person in the picture (accessed via an API)
1. Camera module that sends the pictures to the Manager

### Manager

Telegram-bot: @dvoretski_bot  
Available commands: `/start`. `/end/`

Currently all it does is upload pictures of the authorized users to their dedicated directories for Facial recognition service's later use.  
The list of the authorized users is defined manually.

