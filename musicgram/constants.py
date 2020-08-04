# Edit this according to your needs
# Get api credentials for LastFM at: https://www.last.fm/api/account/create
# Get api credentials for Spotify at https://developer.spotify.com/dashboard/


# Telegram credentials from my.telegram.org
# Telegram api id
API_ID = 0

# Telegram api hash
API_HASH = 'a'

# Your initial last name to which telegram to change when nothing it's playing
INITIAL_LAST_NAME = ''

# Spotify / LastFM credentials

# If the app should use spotify or LastFM. Defaults to SPOTIFY
USE_SPOTIFY = True

# Spotify api id or LastFM api key
API_KEY = 'a'
# Spotify api secret or LastFM api secret
API_SECRET = 'b'

# Change this to your LastFM username if you're using the LastFM
# credentials, else let it unchanged
USERNAME = "musicgram"

# Spotify redirect uri.
# Just if you connect with your spotify account. Don't forget to use the same redirect url you set in your app's settings.
# Most of the time you don't need to change it. If you are about to use
# this with any server make sure you run it locally the first time.

REDIRECT_URI = 'http://localhost:8888/callback'

# How many seconds the client should sleep before querying spotify/lastFM
# For LastFM use 10 or 20 seconds because of a bug that sometimes return false results from the API. // TODO: Fix
# For Spotify 1 works perfectly.
UPDATE_TIME = 1
