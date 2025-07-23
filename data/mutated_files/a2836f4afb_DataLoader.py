from typing import TypeAlias
__typ2 : TypeAlias = "HungaBungaClassifier"
__typ1 : TypeAlias = "DataFrame"
__typ0 : TypeAlias = "HungaBungaRegressor"
# General python imports
from typing import Union, Optional, Dict, Any

# General data science imports
from hunga_bunga import (
    HungaBungaClassifier as HBClassifier,
    HungaBungaRegressor as HBRegressor,
)
import numpy as np
import pandas as pd
from pandas import DataFrame

# Local imports
from data_processing.data_loader import DataLoader

from .base import BaseModel


class __typ3(BaseModel):
    """
    Te Hunga Bunga model combines all SKLearn models and selects the best one.
    It's not allowed to select a validation set manually.

    Not recommended for large sample sizes as it's quite taxing on your own system.
    """

    name = "hunga-bunga"

    def __init__(__tmp0, data: <FILL>, local_save_folder: str = None) :
        """
        Loads the data.

        Arguments:
            data: The dataloader to use
        """
        super().__init__(data)
        if local_save_folder is not None:
            __tmp0.local_save_folder = local_save_folder
        else:
            __tmp0.local_save_folder = f"data/temp/{__tmp0.name}"

        __tmp0._model: Union[HBClassifier, HBRegressor] = NotImplemented

    def train(__tmp0) -> None:
        """
        Trains the model, with the data provided
        """
        all_data = pd.concat([__tmp0.data.train_data, __tmp0.data.validation_data])
        X = all_data.loc[:, __tmp0.data.feature_columns].values
        Y = all_data.loc[:, __tmp0.data.output_column].values
        all_data = None
        __tmp0._model.fit(X, Y)

    def __tmp1(__tmp0, data, name: str = "test") -> __typ1:
        """
        Actually executes the predictions.
        """
        predictions = __tmp0._model.predict(data.values)
        return __typ1(predictions)

    def __tmp2(__tmp0):
        """
        For this model, tuning is the same as training
        """
        return __tmp0.train()


class __typ2(__typ3):
    """
    Classifier model for Hunga Bunga
    """

    name = "hunga-bunga-classifier"

    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __tmp0._model: HBClassifier = HBClassifier()


class __typ0(__typ3):
    """
    Regressor model for Hunga Bunga
    """

    name = "hunga-bunga-classifier"

    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __tmp0._model: HBRegressor = HBRegressor()
