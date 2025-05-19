import requests, base64

from utils import logger
from spotipy import Spotify, SpotifyOAuth
from utils.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from clients.errors import MissingAuth


class SpotifyClient:
    # Scope needed to read user's playlists
    _SCOPE = "playlist-read-private playlist-read-collaborative"
    _SPOTIFY_AUTH_URL: str = "https://accounts.spotify.com/api/token"
    __sp: Spotify = None

    def get_credentials(self, client_id, client_secret):
        """
        Retrieving from Spotify the credentials for authentication:
        https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
        """

        # Create the correct authorization base64 string
        base64_auth = base64.b64encode(bytes(f"{client_id}:{client_secret}", "utf-8"))

        headers = {
            "Authorization": f"Basic {base64_auth}",
            "form": {"grant_type": "client_credentials"},
            "json": True,
        }

        try:
            res = requests.post(self._SPOTIFY_AUTH_URL, headers)
        except Exception as e:
            logger.error(f"Error retrieving credentials from spotify {e}")

        return res

    def get_authenticated(self):
        if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
            logger.error("Server-side credentials not found in Environment")
            raise MissingAuth("Missing server-side credentials")

        if self.__sp:
            logger.info("User already authenticated")

        # User not already authenticated
        logger.info("Starting user authentication")

        try:
            self.__sp = Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=SPOTIPY_CLIENT_ID,
                    client_secret=SPOTIPY_CLIENT_SECRET,
                    redirect_uri=SPOTIPY_REDIRECT_URI,
                    scope=self._SCOPE,
                )
            )
            user = self.__sp.current_user()
            logger.debug(
                f"Successfully authenticated as {user['display_name']} ({user['id']})."
            )
        except Exception as e:
            logger.error(f"Error during Spotify authentication: {e}")
            logger.error(
                "Please ensure your credentials and redirect URI are correct and that you have an internet connection."
            )
            return
        finally:
            logger.info("Ending user authentication")

    def fetch_all_playlist(self):
        try:
            playlists = self.__sp.current_user_playlists(
                limit=50
            )  # Max 50 playlists per request for playlist list
        except Exception as e:
            logger.error(f"Error fetching playlists: {e}")
            return

        return playlists

    def fetch_all_playlist_items(self, playlist_id):
        """
        Fetches all items from a playlist, handling pagination.
        Spotify API returns a maximum of 100 items per request.
        """
        results = []
        offset = 0
        # Max limit per request
        limit = 100
        while True:
            page = self.__sp.playlist_items(
                playlist_id,
                offset=offset,
                limit=limit,
                fields="items(track(name,artists(name))),next",
            )
            if page and page["items"]:
                for item in page["items"]:
                    track_info = item.get("track")
                    # Handles cases where track might be None (e.g., local files not synced)
                    if track_info:
                        track_name = track_info.get("name")
                        artists = track_info.get("artists")
                        # Join multiple artist names, take the first one if available
                        artist_name = (
                            artists[0]["name"] if artists else "Unknown Artist"
                        )
                        results.append(
                            {"Artist": artist_name, "Song Title": track_name}
                        )
                if page["next"]:
                    offset += limit
                else:
                    break  # No more pages
            else:
                break  # No items or error
        return results
