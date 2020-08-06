# MusicGram
A simple python app to sync your telegram profile with your spotify/LastFM account


## Before starting!
 - Make sure you have a telegram API KEY and HASH from [here](https://my.telegram.org)
 - Get your API ID/KEY and API SECRET from the service you want to use [Spotify](https://developer.spotify.com/dashboard/) or [LastFM](https://www.last.fm/api/account/create)
 - Use Spotify over LastFM when possible. LastFM doesn't have a way to tell when a song stops playing so the playing song will be cached for 4-5 minutes. 
 
## How to start!

- Clone the repo using git: `$ git clone https://github.com/nitanmarcel/MusicGram && cd MusicGram`
- Install the pip requirements: `pip3 install -r requirements.txt`
- Open the `musicgram/constants.py` file with your favorite editors and configure the app with the required credentials.
- Finally start your app: `python3 -m musicgram`



## Running on heroku:
  - If you plan on using LastFM you don't have to worry about anything and you can skip this.
  - If you're planing on using Spotify and upload this app on heroku, please make sure you already started the app one locally.
  ### - It doesn't matter if you use an already generated telegram session or not, this step is required for the spotify authorization and without running this at least 1 time locally you won't be able to login with spotify.
  
  
 
 ## Donate:
  - [PayPal](paypal.me/marcelalexandrunitan)
  - [Revolut](http://pay.revolut.com/profile/marceli6p)
 
 ### License MIT
