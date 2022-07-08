"""
Between 2018 and 2020, compare crude suicide rate and age adjusted rates for the
different pairs of gender/ethnicity. Study at the nation-level on individuals
older than 20 years old
"""
import requests
import bs4 as bs
import pandas as pd
import numpy as np
from collections import defaultdict


# Core functions to extract CDC Wonder data
def createParameterList(parameterList):
    """Helper function to create a parameter list from a dictionary object"""

    parameterString = ""

    for key in parameterList:
        parameterString += "<parameter>\n"
        parameterString += "<name>" + key + "</name>\n"

        if isinstance(parameterList[key], list):
            for value in parameterList[key]:
                parameterString += "<value>" + value + "</value>\n"
        else:
            parameterString += "<value>" + parameterList[key] + "</value>\n"

        parameterString += "</parameter>\n"

    return parameterString


def create_xml(parameters):
    b_parameters = parameters["b_parameters"]
    m_parameters = parameters["m_parameters"]
    f_parameters = parameters["f_parameters"]
    i_parameters = parameters["i_parameters"]
    o_parameters = parameters["o_parameters"]
    vm_parameters = parameters["vm_parameters"]
    v_parameters = parameters["v_parameters"]
    misc_parameters = parameters["misc_parameters"]
    xml_request = "<request-parameters>\n"
    xml_request += createParameterList(b_parameters)
    xml_request += createParameterList(m_parameters)
    xml_request += createParameterList(f_parameters)
    xml_request += createParameterList(i_parameters)
    xml_request += createParameterList(o_parameters)
    xml_request += createParameterList(vm_parameters)
    xml_request += createParameterList(v_parameters)
    xml_request += createParameterList(misc_parameters)
    xml_request += "</request-parameters>"
    return xml_request


def xml2df(xml_data):
    """ This function grabs the root of the XML document and iterates over
        the 'r' (row) and 'c' (column) tags of the data-table
        Rows with a 'v' attribute contain a numerical value
        Rows with a 'l attribute contain a text label and may contain an
        additional 'r' (rowspan) tag which identifies how many rows the value
        should be added. If present, that label will be added to the following
        rows of the data table.

        Function returns a two-dimensional array or data frame that may be
        used by the pandas library."""

    root = bs.BeautifulSoup(xml_data, features="xml")
    all_records = []
    row_number = 0
    rows = root.find_all("r")

    for row in rows:
        if row_number >= len(all_records):
            all_records.append([])

        for cell in row.find_all("c"):
            if 'v' in cell.attrs:
                try:
                    all_records[row_number].append(float(cell.attrs["v"].replace(',','')))
                except ValueError:
                    all_records[row_number].append(cell.attrs["v"])
            else:
                if 'r' not in cell.attrs:
                    all_records[row_number].append(cell.attrs["l"])
                else:

                    for row_index in range(int(cell.attrs["r"])):
                        if (row_number + row_index) >= len(all_records):
                            all_records.append([])
                            all_records[row_number + row_index].append(cell.attrs["l"])
                        else:
                            all_records[row_number + row_index].append(cell.attrs["l"])

        row_number += 1
    return all_records


def process_query(xml_request, columns):

    url = "https://wonder.cdc.gov/controller/datarequest/D76"
    response = requests.post(url, data={"request_xml": xml_request, "accept_datause_restrictions": "true"})

    if response.status_code == 200:
        data = response.text
    else:
        print(f"something went wrong: {response.text}")
    data_frame = xml2df(data)
    df = pd.DataFrame(data=data_frame, columns=columns)
    return df


# Global parameters for our queries

# by-variables" or those parameters selected in the "Group Results By" and the "And By" drop-down lists
# in the "Request Form." These "by-variables" are the cross-tabulations, stratifications or indexes
# to the query results. Expect the results data table to show a row for each category in the by-variables,
# and a column for each measure. For example, if you wish to compare data by sex, then "group results by" gender,
# to get a row for females and a row for males in the output.
# M_ are measures to return, the default measures plus any optional measures.

b_parameters = {
    "B_1": "D76.V1-level1",
    "B_2": "D76.V7",
    "B_3": "D76.V17",
    "B_4": "*None*",
    "B_5": "*None*"
}

# measures to return, the default measures plus any optional measures

m_parameters = {
    "M_1": "D76.M1",   # Deaths, must be included
    "M_2": "D76.M2",   # Population, must be included
    "M_3": "D76.M3",   # Crude rate, must be included
    # "M_31": "D76.M31",        # Standard error (crude rate)
    # "M_32": "D76.M32"         # 95% confidence interval (crude rate)
    # "M_41": "D76.M41", # Standard error (age-adjusted rate)
    # "M_42": "D76.M42",  # 95% confidence interval (age-adjusted rate)
}

# columns based on b_parameters and m_parameters
columns = ["Year", "Gender", "Ethnicity", "Deaths", "Population", "Crude Rate"]  # "Age-adjusted Rate", "Age-adjusted Rate Standard Error"

# values highlighted in a "Finder" control for hierarchical lists,
# such as the "Regions/Divisions/States/Counties hierarchical" list.

f_parameters = {
    "F_D76.V1": ["2018", "2019", "2020"], # year/month
    "F_D76.V10": ["*All*"], # Census Regions - dont change
    "F_D76.V2": ["X60-X84"], # ICD-10 Codes
    "F_D76.V27": ["*All*"], # HHS Regions - dont change
    "F_D76.V9": ["*All*"] # State County - dont change
}

# contents of the "Currently selected" information areas next to "Finder" controls in the "Request Form."

i_parameters = {
    "I_D76.V1": "*All* (All Dates)",  # year/month
    "I_D76.V10": "*All* (The United States)", # Census Regions - dont change
    "I_D76.V2": "X60-X84 (Intentional self-harm)", # ICD-10 Codes
    "I_D76.V27": "*All* (The United States)", # HHS Regions - dont change
    "I_D76.V9": "*All* (The United States)" # State County - dont change
}

# variable values to limit in the "where" clause of the query, found in multiple select
# list boxes and advanced finder text entry boxes in the "Request Form."

v_parameters = {
    "V_D76.V1": "",         # Year/Month
    "V_D76.V10": "",        # Census Regions
    "V_D76.V11": "*All*",   # 2006 Urbanization
    "V_D76.V12": "*All*",   # ICD-10 130 Cause List (Infants)
    "V_D76.V17": "*All*",   # Hispanic Origin
    "V_D76.V19": "*All*",   # 2013 Urbanization
    "V_D76.V2": "",         # ICD-10 Codes
    "V_D76.V20": "*All*",   # Autopsy
    "V_D76.V21": "*All*",   # Place of Death
    "V_D76.V22": "*All*",   # Injury Intent
    "V_D76.V23": "*All*",   # Injury Mechanism and All Other Leading Causes
    "V_D76.V24": "*All*",   # Weekday
    "V_D76.V25": "*All*",   # Drug/Alcohol Induced Causes
    "V_D76.V27": "",        # HHS Regions
    "V_D76.V4": "*All*",    # ICD-10 113 Cause List
    "V_D76.V5": "*All*", # Ten-Year Age Groups
    "V_D76.V51": "*All*",   # Five-Year Age Groups
    "V_D76.V52": "*All*",   # Single-Year Ages
    "V_D76.V6": "00",       # Infant Age Groups
    "V_D76.V7": "*All*",    # Gender
    "V_D76.V8": "*All*",    # Race
    "V_D76.V9": ""          # State/County
}

# other parameters, such as radio buttons, checkboxes, and lists that are not data categories

# use state location by default,
# show rates per 100,000, use 2013 urbanization and use ICD-10 Codes (D76.V2) for cause of death category

o_parameters = {
    "O_V10_fmode": "freg",    # Use regular finder and ignore v parameter value
    "O_V1_fmode": "freg",     # Use regular finder and ignore v parameter value
    "O_V27_fmode": "freg",    # Use regular finder and ignore v parameter value
    "O_V2_fmode": "freg",     # Use regular finder and ignore v parameter value
    "O_V9_fmode": "freg",     # Use regular finder and ignore v parameter value
    "O_aar": "aar_none",       # age-adjusted rates
    "O_aar_pop": "0000",      # population selection for age-adjusted rates
    "O_age": "D76.V5",        # select age-group (e.g. ten-year, five-year, single-year, infant groups)
    "O_javascript": "on",     # Set to on by default
    "O_location": "D76.V9",   # select location variable to use (e.g. state/county, census, hhs regions)
    "O_precision": "1",       # decimal places
    "O_rate_per": "100000",   # rates calculated per X persons
    "O_show_totals": "false",  # Show totals for
    "O_timeout": "300",
    "O_title": "Digestive Disease Deaths, by Age Group",    # title for data run
    "O_ucd": "D76.V2",        # select underlying cause of death category
    "O_urban": "D76.V19"      # select urbanization category
}

# values for non-standard age adjusted rates (see mortality online databases).

vm_parameters = {
    "VM_D76.M6_D76.V10": "",        # Location
    "VM_D76.M6_D76.V17": "*All*",   # Hispanic-Origin
    "VM_D76.M6_D76.V1_S": "*All*",  # Year
    "VM_D76.M6_D76.V7": "*All*",    # Gender
    "VM_D76.M6_D76.V8": "*All*"     # Race
}

# Miscellaneous hidden inputs/parameters usually passed by web form. These do not change.
misc_parameters = {
    "action-Send": "Send",
    "finder-stage-D76.V1": "codeset",
    "finder-stage-D76.V1": "codeset",
    "finder-stage-D76.V2": "codeset",
    "finder-stage-D76.V27": "codeset",
    "finder-stage-D76.V9": "codeset",
    "stage": "request"
}

parameters = {}
parameters["b_parameters"] = b_parameters
parameters["m_parameters"] = m_parameters
parameters["f_parameters"] = f_parameters
parameters["i_parameters"] = i_parameters
parameters["o_parameters"] = o_parameters
parameters["vm_parameters"] = vm_parameters
parameters["v_parameters"] = v_parameters
parameters["misc_parameters"] = misc_parameters


# Adjust the queries, store in dictionary and save the results as dataframes

# Here, we want one dataframe per 5 year-age groups
five_year_age_groups = [[f"{5*i}-{5*(i+1)-1}"] for i in range(4, 20)]  # [["10-14", "15-19"]] + ...
names = [f"{5*i}-{5*(i+1)-1}" for i in range(4, 20)]  # ["10-19"] +
dic_results = {}

for five_year_age_group, name in zip(five_year_age_groups, names):
    print(name)
    parameters["v_parameters"]["V_D76.V51"] = five_year_age_group  # Five-Year Age Groups
    parameters["v_parameters"]["V_D76.V5"] = "*All*"  # Ten-Year Age Groups
    parameters["o_parameters"]["O_age"] = "D76.V51"
    xml_request = create_xml(parameters)
    df = process_query(xml_request, columns)
    # correct trailing spaces in the year column
    df["Year"] = df["Year"].apply(lambda x: x.replace(" ", ""))
    dic_results[name] = df
    df.to_csv(f"suicide_gender_ethnicity_{name}.csv", index=False)

# Weights to calculate age-adjusted rates

weights = {}  # https://www.cdc.gov/nchs/data/statnt/statnt20.pdf
weights["under 1"] = 0.013818
weights["1"] = 0.013687
weights["2-4"] = 0.041630
weights["5"] = 0.014186
weights["6-8"] = 0.042966
weights["9"] = 0.015380
weights["10-11"] = 0.030069
weights["12-14"] = 0.042963
weights["15-17"] = 0.043035
weights["18-19"] = 0.029133
weights["20-24"] = 0.066478
weights["25-29"] = 0.064530
weights["30-34"] = 0.071044
weights["35-39"] = 0.080762
weights["40-44"] = 0.081851
weights["45-49"] = 0.072118
weights["50-54"] = 0.062716
weights["55-59"] = 0.048454
weights["60-64"] = 0.038793
weights["65-69"] = 0.034264
weights["70-74"] = 0.031773
weights["75-79"] = 0.027000
weights["80-84"] = 0.017842
weights["85+"] = 0.015508

weights["10-19"] = weights["10-11"] + weights["12-14"] + weights["15-17"] + weights["18-19"]

# assumption: weights of 85-89, 90-94 and 95-99 are all equals to a third of the weight 85+
weights["85-89"] = weights["85+"] / 3
weights["90-94"] = weights["85+"] / 3
weights["95-99"] = weights["85+"] / 3

# calculate sum of weights 20+ to normalize the weights
sum_weights_20_plus = sum([weights[f"{5*i}-{5*(i+1)-1}"] for i in range(4, 20)])

# merge all dataframe from all five-year age groups (greater than 20)
keys = list(dic_results.keys())
df_to_concat = []
for i in range(len(keys)):
    add_df = dic_results[keys[i]]
    add_df.replace("Not Applicable", 0, inplace=True)
    add_df["Age Group"] = keys[i]  # add age group as a column
    add_df["Weight"] = weights[keys[i]] / sum_weights_20_plus  # normalize weights
    df_to_concat.append(add_df)
df = pd.concat(df_to_concat)

# Recalculate crude rate
df["Crude Rate"] = 100_000 * df["Deaths"] / df["Population"]
df = df.fillna(0)  # replace nan values
df = df.replace(np.inf, 0)  # replace inf values (no population for the age groups 90+?)
dic_res = defaultdict(list)  # store the results
# compare for each year and gender/ethnicity mix the crude suicide rate and the age-adjusted suicide rate
for year in range(2018, 2021):
    for gender in ["Female", "Male"]:
        for ethnicity in ["Not Hispanic or Latino", "Hispanic or Latino"]:
            df_year = df[df["Year"] == str(year)]
            sub_df = df_year[(df_year["Gender"] == gender) & (df_year["Ethnicity"] == ethnicity)]
            crude_rate = 100_000 * sub_df["Deaths"].sum() / sub_df["Population"].sum()
            age_adjusted_rate = (sub_df["Crude Rate"] * sub_df["Weight"]).sum()

            dic_res["Year"].append(year)
            dic_res["Gender"].append(gender)
            dic_res["Ethnicity"].append(ethnicity)
            dic_res["Crude Rate"].append(crude_rate)
            dic_res["Age-adjusted Rate"].append(age_adjusted_rate)

df_res = pd.DataFrame.from_dict(dic_res)
print(df_res)
max_abs_error = (df_res["Crude Rate"] - df_res["Age-adjusted Rate"]).abs().max()
print(f"Maximum Absolute Error: {max_abs_error}")
mape = ((df_res["Age-adjusted Rate"] - df_res["Crude Rate"]) / df_res["Crude Rate"]).abs().max()
print(f"MAPE: {mape}")
