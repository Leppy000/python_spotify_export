import os

from clients import SpotifyClient
from utils.logger import logger
from clients import ExcelExporter

# Output Excel file name
EXCEL_FILENAME = "spotify_playlists.xlsx"


def main():
    """
    Main function to fetch playlists and export to Excel.
    """
    logger.info("Spotify Playlist to Excel Exporter")
    logger.info("---------------------------------")
    sp_client = SpotifyClient()

    logger.info("Attempting to authenticate with Spotify...")
    sp_client.get_authenticated()

    logger.info("Fetching your playlists...")
    playlists = sp_client.fetch_all_playlist()

    if not playlists or not playlists["items"]:
        logger.warning("No playlists found for your account.")
        return

    # Export playlists
    ExcelExporter.start_export(sp_client, EXCEL_FILENAME, playlists)

    logger.info(f"\nSuccessfully exported playlists to '{EXCEL_FILENAME}'")
    logger.info(
        f"You can find the file in the same directory as the script: {os.getcwd()}"
    )
    logger.info("---------------------------------")


if __name__ == "__main__":
    main()
