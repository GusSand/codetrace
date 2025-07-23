from typing import TypeAlias
__typ2 : TypeAlias = "str"
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


class __typ1:
    """
    Executor class to deal with Numerai uploads and downloads

    Main important methods are format_predictions, download_latest_data and upload_predictions
    """

    def __tmp2(
        __tmp1, public_id: Optional[__typ2] = None, secret_key: Optional[__typ2] = None
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

        __tmp1.napi: numerapi.NumerAPI = numerapi.NumerAPI(
            public_id=public_id, secret_key=secret_key
        )

    def format_predictions(
        __tmp1, predictions: <FILL>, local_folder, name: __typ2 = "predictions"
    ) -> __typ2:
        """
        Formats the predictions and saves them to a local file.

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
            name: The name of the local file

        Returns:
            local_file_location: The location of the file locally.
        """
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)
        local_file_location = f"{local_folder}/{name}.csv"
        LOGGER.info(f"Saving predictions to {local_file_location}")
        predictions.to_csv(
            local_file_location, index=True, header=True, index_label="id"
        )
        return local_file_location

    def __tmp3(__tmp1, local_folder: __typ2, name: __typ2 = None) :
        """
        Downloads the latest data for the tournament        

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
        """
        local_file_folder = __tmp1.napi.download_current_dataset(
            dest_path=local_folder, dest_filename=name, unzip=True
        )
        local_file_folder = local_file_folder.replace(".zip", "")
        return local_file_folder

    def upload_predictions(
        __tmp1,
        predictions: DataFrame,
        local_folder: __typ2 = "data/temp",
        name: __typ2 = "predictions",
    ) -> bool:
        """
        Formats and uploads the predictions.

        Arguments:
            predictions: The dataframe with the predictions, with index and all output columns
            local_folder: The folder to save thepredictions to
            name: The name of the local file

        Returns:
            success: Whether the upload was successful
        """
        local_file = __tmp1.format_predictions(predictions, local_folder, name)
        return __tmp1.upload_predictions_csv(local_file)

    def upload_predictions_csv(__tmp1, file_location) -> bool:
        """
        Uploads the predictions to Numerai

        Arguments:
            file_location: the location of the file in the system

        Returns:
            success: Whether the upload was successful
        """
        LOGGER.info("Uploading predictions to Numerai")
        submission_id = __tmp1.napi.upload_predictions(file_location)
        LOGGER.info("Done with the upload to Numerai")
        return True

    def stake(__tmp1, amount: __typ0, __tmp0: __typ0) :
        """
        Stakes with the current predictions
        """
        __tmp1.napi.stake(__tmp0, amount)
