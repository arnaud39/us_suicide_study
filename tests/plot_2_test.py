from wonder_utils import SuicideData


def test_implementation() -> None:
    """Check if the data load properly."""

    sd = SuicideData()
 
    plot_params = {
        "save_file": False,
        "show_fig": False,
        "x": "year",
        "color": "gender",
        "by": "age_strat",
        "scatter": False,
        "rows": 1,
        "data_slice": {"age_strat": "25-64"},
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
        "legend_text": "Gender",
    }

    plot_params["y"] = "deaths"
    kwargs[
        "y_title_text"
    ] = "Absolute count of suicides among working-age adults (25-64)"
    kwargs["plot_filename"] = f"working-age_{plot_params['color']}_{plot_params['y']}"
    plot_params.update(kwargs)

    sd.plot(**plot_params)

    plot_params["y"] = "suicide_proportion"
    kwargs[
        "y_title_text"
    ] = "Proportion of suicides occurring among working-age adults (25-64)"
    kwargs["plot_filename"] = f"working-age_{plot_params['color']}_{plot_params['y']}"
    kwargs["primary_ticksuffix"] = "%"
    plot_params.update(kwargs)
    kwargs.pop("primary_ticksuffix")
    plot_params.pop("primary_ticksuffix")

    sd.plot(**plot_params)

    plot_params["y"] = "suicide_per_100k"
    kwargs["y_title_text"] = "Crude suicide rate among working-age adults (25-64)"
    kwargs["plot_filename"] = f"working-age_{plot_params['color']}_{plot_params['y']}"
    plot_params.update(kwargs)

    sd.plot(**plot_params)

    plot_params["y"] = "age_adjusted_rate"
    kwargs[
        "y_title_text"
    ] = "Age-adjusted suicide rate among working-age adults (25-64)"
    kwargs["plot_filename"] = f"working-age_{plot_params['color']}_{plot_params['y']}"
    plot_params.update(kwargs)

    sd.plot(**plot_params)
