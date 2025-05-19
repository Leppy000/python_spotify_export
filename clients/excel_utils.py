import pandas as pd

from utils.logger import logger
from clients import SpotifyClient
from utils.utils import sanitize_sheet_name


class ExcelExporter:
    @staticmethod
    def start_export(sp_client: SpotifyClient, excel_filename: str, playlists):
        """Export into an excel all the playlist tracks under every data-sheet

        Args:
            sp_client (SpotifyClient): client for querying tracks (access made)
            excel_filename (str): excel file name
            playlists (_type_): playlist list
        """
        # Using Pandas ExcelWriter to write multiple sheets
        try:
            with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
                logger.info(f"\nProcessing {len(playlists['items'])} playlists...")
                for i, playlist in enumerate(playlists["items"]):
                    playlist_name = playlist["name"]
                    playlist_id = playlist["id"]
                    logger.debug(
                        f"  ({i+1}/{len(playlists['items'])}) Fetching tracks for playlist: '{playlist_name}'..."
                    )

                    tracks_data = sp_client.fetch_all_playlist_items(playlist_id)

                    if tracks_data:
                        df = pd.DataFrame(tracks_data)
                        sanitized_name = sanitize_sheet_name(playlist_name)
                        if (
                            not sanitized_name
                        ):  # Handle case where name becomes empty after sanitizing
                            sanitized_name = f"Playlist_{i+1}"
                        df.to_excel(writer, sheet_name=sanitized_name, index=False)
                        logger.debug(
                            f"    -> Added sheet '{sanitized_name}' with {len(tracks_data)} songs."
                        )
                    else:
                        logger.debug(
                            f"    -> No tracks found or could not retrieve tracks for '{playlist_name}'. An empty sheet might be created or skipped."
                        )
                        # Create an empty sheet
                        pd.DataFrame([]).to_excel(
                            writer,
                            sheet_name=sanitize_sheet_name(playlist_name),
                            index=False,
                        )
        except Exception as e:
            logger.error(f"An error occurred while writing the Excel file: {e}")
            logger.error(
                "Make sure you have 'openpyxl' installed (pip install openpyxl)."
            )
            logger.error(
                f"If the file '{excel_filename}' was open, please close it and try again."
            )
