from typing import TypeAlias
__typ1 : TypeAlias = "bool"
__typ0 : TypeAlias = "float"
# General python imports
from abc import ABC
import logging
import os
from typing import Optional, Dict, Any

# Data science imports
from pandas import DataFrame

# Other imports
import numerapi


LOGGER = logging.getLogger(__name__)


class Numerai:
    """
    Executor class to deal with Numerai uploads and downloads

    Main important methods are format_predictions, download_latest_data and upload_predictions
    """

    def __tmp1(
        __tmp0, public_id: Optional[str] = None, secret_key: Optional[str] = None
    ):
        """
        Initializes the Numerai class to execute numerai things.
        Can take the public id and secret key, else will load them from the env variables
        """
        if public_id is None:
            LOGGER.info("Loading Numerai credentials from environment.")
            public_id = os.environ.get("NUMERAI_PUBLIC_ID", None)
        if secret_key is None:
            secret_key = os.environ.get("NUMERAI_SECRET_KEY", None)
        assert public_id is not None and secret_key is not None, (
            "You need to either provide the numerai public and and secret key, "
            + "or you need to put them in environment variables."
        )

        __tmp0.napi: numerapi.NumerAPI = numerapi.NumerAPI(
            public_id=public_id, secret_key=secret_key
        )

    def format_predictions(
        __tmp0, __tmp3, __tmp2, name: str = "predictions"
    ) -> str:
        """
        Formats the predictions and saves them to a local file.

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
            name: The name of the local file

        Returns:
            local_file_location: The location of the file locally.
        """
        if not os.path.exists(__tmp2):
            os.makedirs(__tmp2)
        local_file_location = f"{__tmp2}/{name}.csv"
        LOGGER.info(f"Saving predictions to {local_file_location}")
        __tmp3.to_csv(
            local_file_location, index=True, header=True, index_label="id"
        )
        return local_file_location

    def download_latest_data(__tmp0, __tmp2, name: str = None) -> str:
        """
        Downloads the latest data for the tournament        

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
        """
        local_file_folder = __tmp0.napi.download_current_dataset(
            dest_path=__tmp2, dest_filename=name, unzip=True
        )
        local_file_folder = local_file_folder.replace(".zip", "")
        return local_file_folder

    def upload_predictions(
        __tmp0,
        __tmp3: DataFrame,
        __tmp2: str = "data/temp",
        name: str = "predictions",
    ) -> __typ1:
        """
        Formats and uploads the predictions.

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
            name: The name of the local file

        Returns:
            success: Whether the upload was successful
        """
        local_file = __tmp0.format_predictions(__tmp3, __tmp2, name)
        return __tmp0.upload_predictions_csv(local_file)

    def upload_predictions_csv(__tmp0, __tmp4: <FILL>) -> __typ1:
        """
        Uploads the predictions to Numerai

        Arguments:
            file_location: the location of the file in the system

        Returns:
            success: Whether the upload was successful
        """
        LOGGER.info("Uploading predictions to Numerai")
        submission_id = __tmp0.napi.upload_predictions(__tmp4)
        LOGGER.info("Done with the upload to Numerai")
        return True

    def stake(__tmp0, amount: __typ0, confidence) :
        """
        Stakes with the current predictions
        """
        __tmp0.napi.stake(confidence, amount)
