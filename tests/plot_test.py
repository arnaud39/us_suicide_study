from wonder_utils import SuicideData


def test_implementation() -> None:
    """Check if the data load properly."""

    sd = SuicideData()
    sd.data

    plot_params = {
        "save_file": False,
        "show_fig": False,
        "x": "year",
        "color": "ethnicity",
        "by": "age_strat",
        "scatter": False,
        "rows": 1,
        "data_slice": {"age_strat": "10-19"},
        "second_y": {
            "secondary_y": True,
            "y": "pop_share",
            "line_param": {"dash": "dot"},
        },
    }
    kwargs = {
        "secondary_range": [0, 100],
        "secondary_ticksuffix": "%",
        "hide_title": True,
        "second_y_title_text": "% of the population in this age group",
        "legend_text": "Ethnicity",
    }

    plot_params["y"] = "deaths"
    kwargs["y_title_text"] = "Absolute count of suicides among adolescents (10-19)"
    kwargs["plot_filename"] = f"adolescents_{plot_params['color']}_{plot_params['y']}"
    plot_params.update(kwargs)

    sd.plot(**plot_params)

    plot_params["y"] = "suicide_proportion"
    kwargs[
        "y_title_text"
    ] = "Proportion of suicides occurring among adolescents (10-19)"
    kwargs["plot_filename"] = f"adolescents_{plot_params['color']}_{plot_params['y']}"
    kwargs["primary_ticksuffix"] = "%"
    plot_params.update(kwargs)
    kwargs.pop("primary_ticksuffix")
    plot_params.pop("primary_ticksuffix")

    sd.plot(**plot_params)

    plot_params["y"] = "suicide_per_100k"
    kwargs["y_title_text"] = "Crude suicide rate among adolescents (10-19)"
    kwargs["plot_filename"] = f"adolescents_{plot_params['color']}_{plot_params['y']}"
    plot_params.update(kwargs)

    sd.plot(**plot_params)
