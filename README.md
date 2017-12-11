# Sonome
Random melody generation from a text or from Twitter users. Developed as an assigment for CSCI 5839 at CU Boulder. It may be unstable, please fill issues if you find any errors :)

## Set up
Requirements: python, virtualenv, [fluidsynth](http://www.fluidsynth.org/)

1. `git clone https://github.com/casassg/sonome && cd sonome`
2. `virtualenv env`
3. Activate virtualenv: `. ./env/bin/activate` or `./env/Scripts/activate` (if you are on Windows)
4. `pip install -r requirements.txt`

### Download new Twitter users
This project allows you to download the latest 3200 tweets of a user. To do so you will need to do the following:
1. Register a new [twitter app](https://apps.twitter.com/)
2. Add the following enviroment variables:

- **ACCESS_TOKEN** = Your application access token
- **ACCESS_TOKEN_SECRET** = Your application access token secret
- **CONSUMER_KEY** = Your consumer key
- **CONSUMER_SECRET** = Your consumer secret

This repository already includes tweets from: @maggierogers, @cnn, @terns and @realDonaldTrump

## Run

1. Activate virtualenv: `. ./env/bin/activate` or `./env/Scripts/activate` (if you are on Windows)
2. `python main.py`

## Commands available

- `text <text_to_analyze>`: Creates song based on text_to_analyze
- `user <twitter_user_to_analyze>`: Gets a random tweet from specified user and creates song. Will download tweets from user timeline if it hasn't been downloaded before. Requires the previously mentioned environment variables to run.
- `quit`: Self explanatory
- `about`: Prints about information


## LICENSE

MIT © Gerard Casas
