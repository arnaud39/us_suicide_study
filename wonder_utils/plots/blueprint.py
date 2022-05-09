from typing import Dict, List, Any
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import os

import abc
from abc import ABC, abstractmethod

class DataPloter(ABC):
    """BluePrint for ploter class. Need to be supercharged with a data loader."""

    def __init__(
        self,
        data_folder: str,
        indexer_columns: List[str],
        drop_cols: List[str],
        reject_list: List[str],
    ):
        """
        Load the files and create dataframes
        """

        self.indexer_columns = indexer_columns  # could compute it later
        self.numeric_columns = pd.Series(dtype="object")
        self.convert_cols = None
        self.data_folder = data_folder
        # every value detected only after 2018
        self.reject_list = reject_list
        # list of unique values of a column
        self.partitions = dict()

        # will be cached
        self.data = self.load_data(drop_cols=drop_cols)
        self.processed_data = dict()

    @abc.abstractproperty
    def load_data(
        self, drop_cols: List[str] = [], identifier: str = "Data"
    ) -> Dict[str, pd.DataFrame]:
        """
        Load all files into a Dict.
        """
        pass

    def relabel_fig(self, fig):
        color = [
            "#636EFA",
            "#EF553B",
            "#00CC96",
            "#AB63FA",
            "#FFA15A",
            "#19D3F3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52",
        ] * 10
        label_color = dict()

        def f(trace):
            next_color = label_color.get(trace.name, None)
            if not next_color:
                next_color = color.pop(0)
                label_color[trace.name] = next_color
                trace.line.color = next_color

            else:
                trace.line.color = next_color
                return trace.update(showlegend=False)
            return trace.update()

        label_color = dict()
        fig.for_each_trace(f)

    def select_data(
        self,
        data_slice: Dict[str, Any] = dict(),
    ) -> pd.DataFrame:
        """Will merge and select data from the data attribute. User can perform a
        request with dictionnaries and slice.

        Args:
            data_slice (Dict[str, Any], optional): slice to filter the dataframe.
                Defaults to dict().

        Returns:
            pd.DataFrame: merge and filtered dataframe

        Example request: {
            "hhs": slice("HHS1", "HHS4"),
            "age_strat": "20-64",
        }

        Will take hhs1,hhs2,hhs3 and hss4 for 20-64 age stratification.
        """

        loc_request = [slice(None)] * len(self.indexer_columns)
        for k, v in data_slice.items():
            loc_request[self.indexer_columns.index(k)] = v

        return (
            pd.concat(self.data.values())
            .reset_index(drop=True)
            .set_index(self.indexer_columns)
            .sort_index()
            .loc[tuple(loc_request), :]
            .reset_index()
        )

    def selection(self, subpop: str, df: pd.DataFrame) -> pd.DataFrame:
        """Warning: return a pointer to the slice, not a copy!
        Args:
            subpop (str): filter by the index "subpop"
            df (pd.DataFrame): multi-index dataframe

        Returns:
            pd.DataFrame: pointer to the slice of the initial dataframe (not a copy!)
        """
        return df.loc[(slice(None), slice(None), subpop)].sort_index().reset_index()

    def merge(
        self,
        x: str = "year",
        color: str = "age_strat",
        by: str = "race",
        data_slice: Dict[str, Any] = {
            "hhs": slice("HHS1", "HHS4"),
            "age_strat": "20-64",
        },
    ) -> pd.DataFrame:
        """
        Args:
            x (str, optional): filter on x-axis. Defaults to "year".
            color (str, optional): filter for different plots.
                Defaults to "age_strat".
            by (str, optional): filter for multiple subplots. Defaults to "race".
            data_slice (Dict[str, Any], optional): restriction on the initial dataset.
                Defaults to { "hhs": slice("HHS1", "HHS4"), "age_strat": "20-64", }.
                Can also be contain lists. Example: {"age_strat": ["10-19", "20-64", "20plus"]}

        Returns:
            pd.DataFrame: merged dataframe according to the filtering criteria
        """

        # if nothing about age is specified then we take the Overall
        if "age_strat" not in [x, color, by, *data_slice.keys()]:
            data_slice.update({"age_strat": "Overall"})

        data_ = self.select_data(data_slice=data_slice)
        # get the list of values by

        by_list = data_[by].unique()
        by_list = [k for k in by_list if k not in self.reject_list]
        by_list.sort()

        # add suicide_per_100k, groupby multi-index
        data_ = (
            data_.set_index([color, x, by])[["deaths", "population"]]
            .groupby(level=[0, 1, 2])
            .sum()
            .assign(
                suicide_per_100k=lambda x: 100000.0 * x.deaths / x.population,
            )
            .reset_index()
            .set_index([color, x, by])
        )

        # add pop_share
        data_ = (
            data_.assign(
                pop_share=lambda x: 100.0
                * x.population
                / x.groupby(level=[1]).sum().population
            )
            .reset_index()
            .set_index([color, x, by])
        )

        return (
            data_,
            by_list,
        )

    def s_print(
        self,
        s: Any,
    ) -> str:
        """prettier string tranformation if type is slice, else convert the element to a string

        Args:
            s (Any): element in data_slice, used to filter a dataframe

        Returns:
            str: string that will appear to the plot title
        """
        if isinstance(s, slice):
            return f"{s.start} -> {s.stop}"
        return str(s)

    def plot(
        self,
        x: str = "year",
        y: str = "deaths",
        color: str = "age_strat",
        by: str = "race",
        scatter: bool = False,
        rows: int = 2,
        data_slice: Dict[str, Any] = dict(),
        second_y: Dict[str, Any] = dict(),
    ) -> None:
        """
        Args:
            x (str, optional): filter on x-axis. Defaults to "year".
            y (str, optional): value on the y-axis. Defaults to "deaths".
            color (str, optional): filter for different plots.
                Defaults to "age_strat".
            by (str, optional): filter for multiple subplots. Defaults to "race".
            scatter (bool, optional): if True, only plot the dots and not the lines.
                Defaults to False.
            rows (int, optional): number of rows for the subplots. The number of columns is
                is calculated in function of the number of subplots and the number of rows.
                Defaults to 2.
            data_slice (Dict[str, Any], optional): restriction on the initial dataset.
                Defaults to dict().
            second_y (Dict[str, Any], optional): Optional secondary y-axis with
                some parameters that can be provided. See example below.
                Defaults to dict().

                Example: second_y = {"secondary_y": True,
                                     "y": "suicide_per_100k",
                                     "line_param": {"dash": "dot"}}
        """

        processed_data, by_list = self.merge(
            x=x, color=color, by=by, data_slice=data_slice
        )

        # adjust the number of cols for the plot
        cols = len(by_list) // rows + 1 if len(by_list) % rows else len(by_list) // rows

        # add a secondary y-axis to the fig if there is another y-axis
        secondary_y = True if second_y.get("secondary_y") else False
        specs = (
            [[{"secondary_y": True} for _ in range(cols)] for _ in range(rows)]
            if secondary_y
            else None
        )
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=tuple(map(lambda x: str(x), by_list)),
            specs=specs,
        )

        mode = "markers" if scatter else "markers+lines"
        for i, subpop in enumerate(by_list):
            sub_df = self.selection(subpop, processed_data).sort_values(by=[x])

            showlegend = i == 0
            for c in np.unique(sub_df[color]):
                sub_df_c = sub_df[sub_df[color] == c]
                fig.add_trace(
                    (
                        go.Scatter(
                            x=sub_df_c[x],
                            y=sub_df_c[y],
                            name=c,
                            showlegend=showlegend,
                            mode=mode,
                        )
                    ),
                    row=(1 + i // cols),
                    col=(1 + i % cols),
                    secondary_y=False,
                )

            # if there is a second plot, add it
            secondary_y_label = second_y.get("y")
            if second_y:
                for c in np.unique(sub_df[color]):
                    sub_df_c = sub_df[sub_df[color] == c]
                    fig.add_trace(
                        (
                            go.Scatter(
                                x=sub_df_c[x],
                                y=sub_df_c[secondary_y_label],
                                name=c,
                                showlegend=showlegend,
                                mode=mode,
                                line=dict(**second_y.get("line_param", dict())),
                            )
                        ),
                        row=(1 + i // cols),
                        col=(1 + i % cols),
                        secondary_y=secondary_y,
                    )

        self.relabel_fig(fig)

        # text if two y
        y_text = "{}{}".format(y, f" and {secondary_y_label}" if second_y else "")
        # slice text in the plot title (if there is at least a slice)
        slice_list = [f"{it[0]}: {self.s_print(it[1])}" for it in data_slice.items()]
        slice_text = ", ".join(slice_list)
        fig.update_layout(
            title_text="{}Evolution of {} by {}<br>{}".format(
                "Temporal " if x == "year" else "", y_text, by, slice_text
            ),
            xaxis_title=x,
            legend_title=by,
            height=330 * rows,
            width=400 * cols,
            plot_bgcolor="rgb(255,255,255)",
        )
        fig.update_xaxes(
            tickangle=-45,
            showline=True,
            linewidth=0.1,
            linecolor="black",
            gridwidth=0.1,
            gridcolor="grey",
        )
        fig.update_yaxes(
            showline=True,
            linewidth=0.1,
            linecolor="black",
            gridwidth=0.1,
            gridcolor="grey",
            secondary_y=False,
            title_text=y,
        )
        if secondary_y:  # update also the secondary y_axis
            fig.update_yaxes(
                showline=True,
                linewidth=0.1,
                linecolor="black",
                gridwidth=0.1,
                gridcolor="grey",
                secondary_y=True,
                title_text=secondary_y_label,
            )
        # text if two y
        y_text = "{}{}".format(y, f"_and_{secondary_y_label}" if second_y else "")
        # save image
        fig.write_image("outputs/{}_{}_by_{}_color_{}.png".format(y_text, x, by, color))
        # show fig
        fig.show()
