
#| **Objective:** assess racial-ethnic mix in adolescent suicides and contrast with overall suicides.
#|
#| Other research questions: evolution of the racial-ethnic distribution of adolescent suicides over time (+ relative to the proportion of the population in that age group)
#|
#| In parallel: evolution of the racial-ethnic distribution of overall suicides and adult suicides (20+) over time (+ relative to the proportion of the US population -- overall or 20+)
#|
#| For now, we can focus on the national level.
#|
#| However, we could also assess whether differences among racial-ethnic subgroups are more pronounced in certain HHS regions and/or states.
#|
#| Along these lines, health journalists at CNN, US News, and NBC were most interested in the racial-ethnic mix in the 5 states with a stat. sig. increase in the absolute number of suicides + proportion outcome as well as California (stat. sig. increase in the proportion outcome only).

#| **Data extraction :**
#|
#| [CDC Wonder](https://wonder.cdc.gov/mcd.html), Provisional Mortality Statistics, 2018 through Last Month Request & Current Final Multiple Cause of Death Data
#| 
#| Groupby: Residence HHS Regions, Gender, Year, Single Race 6, Hispanic Origin
#|
#| Cause of death: Intentional self-harm
#|
#| 7 files:
#| *  All years "Overall"  (age-adjusted)
#| *  10-19 years "10-19"
#| *  20-64 years "20-64"
#| *  25-64 years "25-64"  (age-adjusted)
#| *  20+ years "20plus"
#| *  25+ years "25plus"  (age-adjusted)
#| *  65+ years "65plus"  (age-adjusted)
#|
#| Years after 2010

# Run this code to keep plotly figures when exporting the notebook in HTML
import plotly
plotly.offline.init_notebook_mode()

#-------------------------------

from wonder_utils import SuicideData

sd = SuicideData()  # or? reject_list=["More than one race", "Not Stated"]

#-------------------------------

def plot_func(color, by, age_cat, age_cat_name,
              slice, rows, legend_text, by_list,
              plot_age_adjusted, additional_filename_text,
              other_data_slice={}, additional_subplot_title=""):
    data_slice = {"age_strat": slice}
    for key, value in list(other_data_slice.items()):
        data_slice[key] = value
    plot_params = {"x": "year",
                   "color": color,
                   "by": by,
                   "scatter": False,
                   "rows": rows,
                   "data_slice": data_slice,
                   "second_y": {"secondary_y": True,
                                "y": "pop_share",
                                "line_param": {"dash": "dot"}}}
    if not(by_list is None):
        plot_params["by_list"] = by_list
    kwargs = {"secondary_range": [0, 100],
              "secondary_ticksuffix": "%",
              "hide_title": True,
              "second_y_title_text": "% of the population in this age group",
              "legend_text": legend_text,
              "additional_subplot_title": additional_subplot_title}

    plot_params["y"] = "deaths"
    kwargs["y_title_text"] = f"Absolute count of suicides among {age_cat_name} ({age_cat})"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    plot_params["y"] = "suicide_proportion"
    kwargs["y_title_text"] = f"Proportion 1: among {age_cat_name} ({age_cat}), proportion of suicides by {color}"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    kwargs["primary_ticksuffix"] = "%"
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    plot_params["y"] = "suicide_proportion_2"
    kwargs["y_title_text"] = f"Proportion 2: by {color}, proportion of suicides occurring among {age_cat_name} ({age_cat})"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    kwargs.pop("primary_ticksuffix")
    plot_params.pop("primary_ticksuffix")

    plot_params["y"] = "suicide_per_100k"
    kwargs["y_title_text"] = f"Crude suicide rate among {age_cat_name} ({age_cat})"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    if plot_age_adjusted:

        plot_params["y"] = "age_adjusted_rate"
        kwargs["y_title_text"] = f"Age-adjusted suicide rate among {age_cat_name} ({age_cat})"
        kwargs["plot_filename"] = f"working-age_{plot_params['color']}_{plot_params['y']}" + additional_filename_text
        plot_params.update(kwargs)

        sd.plot(**plot_params
            )

#| # Analysis at the national level

#| ## Subpopulation: adolescents (10-19) - 16 graphs

#| ### By Gender

plot_func(color="gender", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Gender",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race

plot_func(color="race", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ## Subpopulation: working-age adults (20-64) - 16 graphs

#| ### By Gender

plot_func(color="gender", by="age_strat",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="Gender",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race

plot_func(color="race", by="age_strat",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ## Subpopulation: older adults (65plus) - 16 graphs

#| ### By Gender

plot_func(color="gender", by="age_strat",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="Gender",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race

plot_func(color="race", by="age_strat",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ## Subpopulation: all adults (20plus) - 16 graphs

#| ### By Gender

plot_func(color="gender", by="age_strat",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="Gender",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race

plot_func(color="race", by="age_strat",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ## Subpopulation: everyone, all age groups (Overall) - 16 graphs

#| ### By Gender

plot_func(color="gender", by="age_strat",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="Gender",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race

plot_func(color="race", by="age_strat",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| ### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="")

#| # Analysis by HHS region

#| ## First type of visualizations: one subplot by HHS region

#| ### Subpopulation: adolescents (10-19) - 16 graphs, with 10 HHS-region subplots on each

#| #### By Gender

plot_func(color="gender", by="hhs",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=5,
          legend_text="Gender",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Ethnicity

plot_func(color="ethnicity", by="hhs",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=5,
          legend_text="Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race

plot_func(color="race", by="hhs",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=5,
          legend_text="Race",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="hhs",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=5,
          legend_text="Race-Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| ### Subpopulation: working-age adults (20-64) - 16 graphs, with 10 HHS-region subplots on each

#| #### By Gender

plot_func(color="gender", by="hhs",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=5,
          legend_text="Gender",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Ethnicity

plot_func(color="ethnicity", by="hhs",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=5,
          legend_text="Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race

plot_func(color="race", by="hhs",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=5,
          legend_text="Race",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="hhs",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=5,
          legend_text="Race-Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| ### Subpopulation: older adults (65plus) - 16 graphs, with 10 HHS-region subplots on each

#| #### By Gender

plot_func(color="gender", by="hhs",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=5,
          legend_text="Gender",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Ethnicity

plot_func(color="ethnicity", by="hhs",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=5,
          legend_text="Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race

plot_func(color="race", by="hhs",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=5,
          legend_text="Race",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="hhs",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=5,
          legend_text="Race-Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| ### Subpopulation: all adults (20plus) - 16 graphs, with 10 HHS-region subplots on each

#| #### By Gender

plot_func(color="gender", by="hhs",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=5,
          legend_text="Gender",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Ethnicity

plot_func(color="ethnicity", by="hhs",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=5,
          legend_text="Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race

plot_func(color="race", by="hhs",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=5,
          legend_text="Race",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="hhs",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=5,
          legend_text="Race-Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| ### Subpopulation: everyone, all age groups (Overall) - 16 graphs, with 10 HHS-region subplots on each

#| #### By Gender

plot_func(color="gender", by="hhs",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=5,
          legend_text="Gender",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Ethnicity

plot_func(color="ethnicity", by="hhs",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=5,
          legend_text="Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race

plot_func(color="race", by="hhs",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=5,
          legend_text="Race",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| #### By Race-Ethnicity

plot_func(color="ethno_race_4_cat", by="hhs",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=5,
          legend_text="Race-Ethnicity",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted=False,
          additional_filename_text="_hhs_1")

#| ## Second type of visualizations: all HHS regions on the same plot

#| ### Subpopulation: adolescents (10-19) - 16 graphs

#| #### By Gender

plot_func(color="hhs", by="gender",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Ethnicity

plot_func(color="hhs", by="ethnicity",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race

plot_func(color="hhs", by="race",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race-Ethnicity

plot_func(color="hhs", by="ethno_race_4_cat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| ### Subpopulation: working-age adults (20-64) - 16 graphs

#| #### By Gender

plot_func(color="hhs", by="gender",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Ethnicity

plot_func(color="hhs", by="ethnicity",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race

plot_func(color="hhs", by="race",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race-Ethnicity

plot_func(color="hhs", by="ethno_race_4_cat",
          age_cat="20-64",
          age_cat_name="working-age adults",
          slice="20-64",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| ### Subpopulation: older adults (65plus) - 16 graphs

#| #### By Gender

plot_func(color="hhs", by="gender",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Ethnicity

plot_func(color="hhs", by="ethnicity",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race

plot_func(color="hhs", by="race",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race-Ethnicity

plot_func(color="hhs", by="ethno_race_4_cat",
          age_cat="65plus",
          age_cat_name="older adults",
          slice="65plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| ### Subpopulation: all adults (20plus) - 16 graphs

#| #### By Gender

plot_func(color="hhs", by="gender",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Ethnicity

plot_func(color="hhs", by="ethnicity",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race

plot_func(color="hhs", by="race",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race-Ethnicity

plot_func(color="hhs", by="ethno_race_4_cat",
          age_cat="20plus",
          age_cat_name="all adults",
          slice="20plus",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| ### Subpopulation: everyone, all age groups (Overall) - 16 graphs

#| #### By Gender

plot_func(color="hhs", by="gender",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Ethnicity

plot_func(color="hhs", by="ethnicity",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race

plot_func(color="hhs", by="race",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| #### By Race-Ethnicity

plot_func(color="hhs", by="ethno_race_4_cat",
          age_cat="Overall",
          age_cat_name="everyone, all age groups",
          slice="Overall",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_hhs_2")

#| # Additional graphs

#| Adolescents females, by race

plot_func(color="race", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Race",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_filter_gender_female",
          other_data_slice={"gender": "Female",
                            "race": ["White", "Black"]},
          additional_subplot_title=" - Gender=Female")

#| Adolescents females, by ethnicity

plot_func(color="ethnicity", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_filter_gender_female",
          other_data_slice={"gender": "Female"},
          additional_subplot_title=" - Gender=Female")

#| Adolescents females, by race-ethnicity

plot_func(color="ethno_race_4_cat", by="age_strat",
          age_cat="10-19",
          age_cat_name="adolescents",
          slice="10-19",
          rows=1,
          legend_text="Race-Ethnicity",
          by_list=None,
          plot_age_adjusted=False,
          additional_filename_text="_filter_gender_female",
          other_data_slice={"gender": "Female",
                            "ethno_race_4_cat": ["Hispanic",
                                                 "Non-hispanic Black",
                                                 "Non-hispanic White"]},
          additional_subplot_title=" - Gender=Female")
