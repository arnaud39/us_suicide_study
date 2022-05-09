from typing import Dict, List, Any
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import os

from .blueprint import DataPloter


class SuicideData(DataPloter):
    """Available features to plot: race, year, population, hhs, deaths, deaths_perc, etchnicity, ethno_race, age_strat.


    The data pipeline works as following:"""

    def __init(
        self,
        data_folder: str = "Data",
        indexer_columns: List[str] = [
            "hhs",
            "State",
            "year",
            "race",
            "ethnicity",
            "age_strat",
            "ethno_race",
        ],
        drop_cols: List[str] = [
            "Year Code",
            "State Code",
            "HHS Region",
            "Race Code",
            "Crude Rate",
            "Hispanic Origin Code",
        ],
        reject_list: List[str] = [
            "American Indian or Alaska Native",
            "More than one race",
            "Native Hawaiian or Other Pacific Islander",
            "Not Stated",
        ],
    ) -> None:

        print(reject_list)
        super(SuicideData, self).__init__(
            data_folder=data_folder,
            indexer_columns=indexer_columns,
            drop_cols=drop_cols,
            reject_list=reject_list,
        )

    def file_to_dataframe(
        self,
        data_folder: str,
        file: str,
        rename_mapper: Dict[str, str] = {
            "Single Race 6": "race",
            "Race": "race",
            "Residence HHS Region Code": "hhs",
            "HHS Region Code": "hhs",
            "Population": "population",
            "Year": "year",
            "Deaths": "deaths",
            "Hispanic Origin": "ethnicity",
        },
    ) -> pd.DataFrame:
        """CDC Wonder txt file into dataframe
        Args:
            data_folder (str): where the data files are stored
            file (str): file that we want to process
            rename_mapper (_type_, optional): dictionnary to rename the columns.
                Defaults to {"Single Race 6": "race", "Race": "race",
                             "Residence HHS Region Code": "hhs",
                             "HHS Region Code": "hhs", "Population": "population",
                             "Year": "year", "Deaths": "deaths",
                             "Hispanic Origin": "ethnicity", }.

        Returns:
            pd.DataFrame: converted file into a pandas dataframe
        """
        process_line = lambda line: line.strip().replace('"', "").split("\t")

        lines = []
        with open(f"{data_folder}/{file}", "r") as f:
            for line in iter(lambda: f.readline().rstrip(), '"---"'):
                lines.append(process_line(line))
        # column is on the header, remove corner named notes
        return pd.DataFrame(lines[1:], columns=lines[0][1:]).rename(
            columns=rename_mapper
        )

    def processor(
        self,
        x: pd.DataFrame,
        force_numeric: List[str] = ["population", "Crude Rate"],
    ) -> pd.DataFrame:
        """Process dataframes: convert columns dtype, compute new features.
        Args:
            x (pd.DataFrame): dataframe that we want to process
            force_numeric (List[str], optional): force these columns into numerical columns.
                Defaults to ["population", "Crude Rate"].

        Returns:
            pd.DataFrame: processed dataframe

        """

        # Automatically convert numeric columns to float/int type
        if self.numeric_columns.empty:
            self.numeric_columns = x.apply(
                lambda s: pd.to_numeric(s.replace(np.nan, 0), errors="coerce")
                .notnull()
                .all()
            )

            # compare with the force numeric and prevent numeric columns
            self.convert_cols = [
                col
                for col, bool_ in self.numeric_columns.items()
                if (bool_ or col in force_numeric)  # and col != "year"
                # keep year as str to prevent unexpected ticks on plots
            ]

        x.columns = self.numeric_columns.index

        x.year = x.year.str.extract("(\d+)")
        x = x.replace(
            {
                "Not Hispanic or Latino": "Non-Hispanic",
                "Hispanic or Latino": "Hispanic",
                "Not Applicable": np.nan,
                "Unreliable": np.nan,
                "Asian or Pacific Islander": "API",
                "Asian": "API",
                "Black or African American": "Black",
            }
        )

        x[self.convert_cols] = x[self.convert_cols].apply(
            pd.to_numeric, errors="coerce"
        )

        x = x.loc[
            ~pd.concat(
                [x.eq(forbidden).any(axis=1) for forbidden in self.reject_list], axis=1
            ).any(axis=1)
        ]

        return x.assign(ethno_race=lambda x: x.race + " " + x.ethnicity)

    def load_data(
        self, drop_cols: List[str] = [], identifier: str = "Data"
    ) -> Dict[str, pd.DataFrame]:
        """
        Automatically load all files containing identifier.
        This method is specific to the suicie_rate project and should be
        rewritten for other projects.

        Args:
            drop_cols (List[str], optional): Select what columns should be dropped.
                Defaults to [].
            identifier (str, optional): used to identify which files should be process.
                Defaults to "Data".

        Returns:
            Dict[str, pd.DataFrame]: dictionnary containing specific name of files and its
                associated dataframe.
        """
        available_files = os.listdir("data")
        raw_data = [file for file in available_files if identifier in file]

        data = {
            (entry.split()[-1].split(".")[0], entry.split()[-2]): entry
            for entry in raw_data
        }

        age_strats = set(
            key[0] for key in data.keys()
        )  # {'10-19', '20plus', 'Overall'}

        dataframes = {
            age_strat: pd.concat(
                map(
                    self.processor,
                    [
                        self.file_to_dataframe(self.data_folder, file).assign(
                            age_strat=age_strat
                        )
                        for key_tuple, file in data.items()
                        if key_tuple[0] == age_strat
                    ],
                ),
                axis=0,
            ).drop(columns=drop_cols)
            for age_strat in age_strats
        }
        return dataframes
