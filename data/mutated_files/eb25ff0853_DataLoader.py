from typing import TypeAlias
__typ0 : TypeAlias = "DataFrame"
from abc import ABC
import logging
from typing import Dict, Any, Optional

# Data science libraries
from pandas import DataFrame

# Local imports
from data_processing.data_loader import DataLoader

LOGGER = logging.getLogger(__name__)


class BaseModel(ABC):
    """
    The base model to be used in this project.

    This is an abstract class. Please subclass it to implement each method.
    """

    def __tmp3(__tmp0, data: <FILL>) :
        """
        Loads the data.

        Arguments:
            data: The dataloader to use
        """
        __tmp0.data = data

    def __tmp1(__tmp0) -> None:
        """
        Trains the model, with the data provided
        """
        return NotImplemented

    def __tmp2(__tmp0) -> None:
        """
        Load the already trained model to not have to train again.
        """
        return NotImplemented

    def __tmp4(
        __tmp0, data_loader: Optional[DataLoader] = None, all_data: bool = False, **kwargs
    ) -> __typ0:
        """
        Predict based on an already trained model.

        Arguments:
            data_looader: The data to predict. If not provided, it will default to the local data loader.
            all_data: Whehter to predict all the data in the data loader. If false, the test data will be predicted.
        """
        if data_loader is None:
            data_loader = __tmp0.data

        if all_data:
            data = data_loader.data
            name = "predict"
        else:
            data = data_loader.test_data
            name = "test"
        X_test = data.loc[:, data_loader.feature_columns]

        # Here the magic actually happens. Implementation specific
        predictions = __tmp0.execute_prediction(X_test, name, **kwargs)

        predictions = data_loader.format_predictions(predictions, all_data=all_data)
        return predictions

    def execute_prediction(__tmp0, data: __typ0, name: str = "test") -> __typ0:
        """
        Actually executes the predictions. Based on implementation

        Arguments:
            data: The data to predict
            **kwargs: Any other parameters for the correct execution

        Return:
            The predictions in a dataframe
        """
        return NotImplemented

    def tune(__tmp0) :
        """
        Tunes the current models with the provided hyperparameter tuning dict.
        """
        return NotImplemented
