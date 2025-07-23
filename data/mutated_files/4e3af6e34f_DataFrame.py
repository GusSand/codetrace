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


class HungaBungaBase(BaseModel):
    """
    Te Hunga Bunga model combines all SKLearn models and selects the best one.
    It's not allowed to select a validation set manually.

    Not recommended for large sample sizes as it's quite taxing on your own system.
    """

    name = "hunga-bunga"

    def __init__(__tmp0, data: DataLoader, local_save_folder: str = None) :
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

    def execute_prediction(__tmp0, data: <FILL>, name: str = "test") -> DataFrame:
        """
        Actually executes the predictions.
        """
        predictions = __tmp0._model.predict(data.values)
        return DataFrame(predictions)

    def tune(__tmp0):
        """
        For this model, tuning is the same as training
        """
        return __tmp0.train()


class HungaBungaClassifier(HungaBungaBase):
    """
    Classifier model for Hunga Bunga
    """

    name = "hunga-bunga-classifier"

    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __tmp0._model: HBClassifier = HBClassifier()


class HungaBungaRegressor(HungaBungaBase):
    """
    Regressor model for Hunga Bunga
    """

    name = "hunga-bunga-classifier"

    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __tmp0._model: HBRegressor = HBRegressor()
