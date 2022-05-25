"""
Create automatically the python script (script_to_convert.py)
in the correct format.
It will be then converted into a notebook "Analysis" when running the
script run_script_to_notebook.py
"""

categories = [("gender", "Gender"),
              ("ethnicity", "Ethnicity"),
              ("race", "Race"),
              ("ethno_race_4_cat", "Race-Ethnicity")]

# change the False (except for adolescents) to True when
# age adjusted rate are implemented
ages_to_plot = [("10-19", "adolescents", False),
                ("20-64", "working-age adults", False),
                ("65plus", "older adults", False),
                ("20plus", "all adults", False),
                ("Overall", "everyone, all age groups", False)]

script = """
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
              plot_age_adjusted, additional_filename_text):
    plot_params = {"x": "year",
                   "color": color,
                   "by": by,
                   "scatter": False,
                   "rows": rows,
                   "data_slice": {"age_strat": slice},
                   "second_y": {"secondary_y": True,
                                "y": "pop_share",
                                "line_param": {"dash": "dot"}}}
    if not(by_list is None):
        plot_params["by_list"] = by_list
    kwargs = {"secondary_range": [0, 100],
              "secondary_ticksuffix": "%",
              "hide_title": True,
              "second_y_title_text": "% of the population in this age group",
              "legend_text": legend_text}

    plot_params["y"] = "deaths"
    kwargs["y_title_text"] = f"Absolute count of suicides among {age_cat_name} ({age_cat})"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    plot_params["y"] = "suicide_proportion"
    kwargs["y_title_text"] = f"Proportion of suicides occurring among {age_cat_name} ({age_cat})"
    kwargs["plot_filename"] = f"{age_cat_name}_{age_cat}_{color}_{plot_params['y']}" + additional_filename_text
    kwargs["primary_ticksuffix"] = "%"
    plot_params.update(kwargs)

    sd.plot(**plot_params
        )

    plot_params["y"] = "suicide_proportion_2"
    kwargs["y_title_text"] = f"Proportion of suicides occurring among {age_cat_name} ({age_cat})"
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
"""

script += """
#| # Analysis at the national level
"""


def add_to_script(age_cat, age_cat_name, plot_age_adjusted):
    nb_graphs = (len(categories) * 5 if plot_age_adjusted
                 else len(categories) * 4)
    s = ""
    s += f"""
#| ## Subpopulation: {age_cat_name} ({age_cat}) - {nb_graphs} graphs
"""
    for cat, legend in categories:

        s += f"""
#| ### By {legend}

plot_func(color="{cat}", by="age_strat",
          age_cat="{age_cat}",
          age_cat_name="{age_cat_name}",
          slice="{age_cat}",
          rows=1,
          legend_text="{legend}",
          by_list=None,
          plot_age_adjusted={plot_age_adjusted},
          additional_filename_text="")
"""
    return s

for age_cat, age_cat_name, plot_age_adjusted in ages_to_plot:
    script += add_to_script(age_cat, age_cat_name, plot_age_adjusted)

script += """
#| # Analysis by HHS region
"""

script += """
#| ## First type of visualizations: one subplot by HHS region
"""

def add_to_script_hhs_1(age_cat, age_cat_name, plot_age_adjusted):
    nb_graphs = (len(categories) * 5 if plot_age_adjusted
                 else len(categories) * 4)
    s = ""
    s += f"""
#| ### Subpopulation: {age_cat_name} ({age_cat}) - {nb_graphs} graphs, with 10 HHS-region subplots on each
"""
    for cat, legend in categories:

        s += f"""
#| #### By {legend}

plot_func(color="{cat}", by="hhs",
          age_cat="{age_cat}",
          age_cat_name="{age_cat_name}",
          slice="{age_cat}",
          rows=2,
          legend_text="{legend}",
          by_list=["HHS" + str(i) for i in range(1, 11)],
          plot_age_adjusted={plot_age_adjusted},
          additional_filename_text="_hhs_1")
"""
    return s


for age_cat, age_cat_name, plot_age_adjusted in ages_to_plot:
    script += add_to_script_hhs_1(age_cat, age_cat_name, plot_age_adjusted)

script += """
#| ## Second type of visualizations: all HHS regions on the same plot
"""


def add_to_script_hhs_2(age_cat, age_cat_name, plot_age_adjusted):
    nb_graphs = (len(categories) * 5 if plot_age_adjusted
                 else len(categories) * 4)
    s = ""
    s += f"""
#| ### Subpopulation: {age_cat_name} ({age_cat}) - {nb_graphs} graphs
"""
    for cat, legend in categories:

        s += f"""
#| #### By {legend}

plot_func(color="hhs", by="{cat}",
          age_cat="{age_cat}",
          age_cat_name="{age_cat_name}",
          slice="{age_cat}",
          rows=1,
          legend_text="HHS Region",
          by_list=None,
          plot_age_adjusted={plot_age_adjusted},
          additional_filename_text="_hhs_2")
"""
    return s


for age_cat, age_cat_name, plot_age_adjusted in ages_to_plot:
    script += add_to_script_hhs_2(age_cat, age_cat_name, plot_age_adjusted)

with open("script_to_convert.py", "w+") as f:
    f.write(script)
