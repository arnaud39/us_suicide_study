# Objective: assess racial-ethnic mix in adolescent suicides and contrast with overall suicides
# Other research questions: evolution of the racial-ethnic distribution of adolescent suicides over time (+ relative to the proportion of the population in that age group)
# In parallel: evolution of the racial-ethnic distribution of overall suicides and adult suicides (20+) over time (+ relative to the proportion of the US population -- overall or 20+)

# For now, we can focus on the national level.
# However, we could also assess whether differences among racial-ethnic subgroups are more pronounced in certain HHS regions and/or states.
# Along these lines, health journalists at CNN, US News, and NBC were most interested in the racial-ethnic mix in the 5 states with a stat. sig. increase
# in the absolute number of suicides + proportion outcome as well as California (stat. sig. increase in the proportion outcome only).

# Overall population (across age groups) --> read data
RE_Suicide_National <- read.csv("C:/Users/Utilisateur/.../Race_Ethnicity_Suicide_National.txt",header=TRUE,sep='\t')
RE_Suicide_National <- RE_Suicide_National[,2:ncol(RE_Suicide_National)]
names(RE_Suicide_National)
head(RE_Suicide_National)

# Focusing on the 10-19 age group --> read data
RE_Suicide_National_10_19 <- read.csv("C:/Users/Utilisateur/.../Race_Ethnicity_Suicide_National_10_19.txt",header=TRUE,sep='\t')
RE_Suicide_National_10_19 <- RE_Suicide_National_10_19[,2:ncol(RE_Suicide_National_10_19)]
names(RE_Suicide_National_10_19)
head(RE_Suicide_National_10_19)

# Overall population (across age groups) --> aggregate the data properly
RE_Suicide_National_2020 <- RE_Suicide_National[RE_Suicide_National$Year == 2020 & !is.na(RE_Suicide_National$Year),]
RE_Suicide_National_2020_Race <- RE_Suicide_National_2020 %>% filter(Hispanic.Origin != '') %>% group_by(Race) %>% summarise(n=sum(Deaths))
RE_Suicide_National_2020_Ethnicity <- RE_Suicide_National_2020 %>% filter(Hispanic.Origin != '') %>% group_by(Hispanic.Origin) %>% summarise(n=sum(Deaths))

# Focusing on the 10-19 age group --> aggregate the data properly
RE_Suicide_National_10_19_2020 <- RE_Suicide_National_10_19[RE_Suicide_National_10_19$Year == 2020 & !is.na(RE_Suicide_National_10_19$Year),]
RE_Suicide_National_10_19_2020_Race <- RE_Suicide_National_10_19_2020 %>% filter(Hispanic.Origin != '') %>% group_by(Race) %>% summarise(n=sum(Deaths))
RE_Suicide_National_10_19_2020_Ethnicity <- RE_Suicide_National_10_19_2020 %>% filter(Hispanic.Origin != '') %>% group_by(Hispanic.Origin) %>% summarise(n=sum(Deaths))

### Overall population (across age groups): population size by stratum ###

# Stratification by ethnicity: population sizes
Eth_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Eth_Pop_2020.txt",header=TRUE,sep='\t')
Eth_Pop_2020 <- Eth_Pop_2020[,2:ncol(Eth_Pop_2020)]
names(Eth_Pop_2020)
head(Eth_Pop_2020)

## Preliminary results (to be validated) ##

# Hispanic pop: 4571 (i.e., 9.94% vs in the US pop: 18.61%) --> less exacerbated
# Non-hispanic pop: 41296 (i.e., 89.81% vs in the US pop: 81.39%) --> more exacerbated

# Stratification by race: population sizes
Race_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Race_Pop_2020.txt",header=TRUE,sep='\t')
Race_Pop_2020 <- Race_Pop_2020[,2:ncol(Race_Pop_2020)]
names(Race_Pop_2020)
head(Race_Pop_2020)

## Preliminary results (to be validated) ##

# White: 40155 (i.e., 87.33% vs in the US pop: 77.39%) --> more exacerbated
# BAA: 3541 (i.e., 7.70% vs in the US pop: 14.32%) --> less exacerbated
# AIAN: 714 (i.e., 1.55% vs in the US pop: 1.49%) --> in line?
# API: 1569 (i.e., 3.41% vs in the US pop: 6.80%) --> less exacerbated

# Stratification by (race, ethnicity): population sizes
Race_Eth_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Race_Eth_Pop_2020.txt",header=TRUE,sep='\t')
Race_Eth_Pop_2020 <- Race_Eth_Pop_2020[,2:ncol(Race_Eth_Pop_2020)]
names(Race_Eth_Pop_2020)
head(Race_Eth_Pop_2020)

## Preliminary results (to be validated) ##

# Hispanic pop: 4571 (i.e., 9.94% vs in the US pop: 18.61%) --> less exacerbated
# White non-hisp: 35716 (i.e., 77.68% vs in the US pop: 60.85%) --> more exacerbated
RE_Suicide_National_2020[RE_Suicide_National_2020$Race == 'White' & RE_Suicide_National_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# Black non-hisp: 3415 (i.e., 7.43% vs in the US pop: 13.24%) --> less exacerbated
RE_Suicide_National_2020[RE_Suicide_National_2020$Race == 'Black or African American' & RE_Suicide_National_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# API non-hisp: 1502 (i.e., 3.27% vs in the US pop: 6.46%) --> less exacerbated
RE_Suicide_National_2020[RE_Suicide_National_2020$Race == 'Asian or Pacific Islander' & RE_Suicide_National_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# AIAN non-hisp: 663 (i.e., 1.44% vs in the US pop: 0.84%) --> in line?
RE_Suicide_National_2020[RE_Suicide_National_2020$Race == 'American Indian or Alaska Native' & RE_Suicide_National_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']

# In the five states + California with a stat sig increase (overall)
# TODO

# In the five states + California with a stat sig increase (per state)
# TODO

### Focus on the 10-19 age group ###

# Stratification by ethnicity: population sizes
Eth_10_19_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Eth_10_19_Pop_2020.txt",header=TRUE,sep='\t')
Eth_10_19_Pop_2020 <- Eth_10_19_Pop_2020[,2:ncol(Eth_10_19_Pop_2020)]
names(Eth_10_19_Pop_2020)
head(Eth_10_19_Pop_2020)

## Preliminary results (to be validated) ##

# Hispanic pop: 549 (i.e., 19.63% vs in the US pop in that age group: 25.11%) --> less exacerbated
# Non-hispanic pop: 2245 (i.e., 80.26% vs in the US pop in that age group: 74.89%) --> more exacerbated

# Stratification by race: population sizes
Race_10_19_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Race_10_19_Pop_2020.txt",header=TRUE,sep='\t')
Race_10_19_Pop_2020 <- Race_10_19_Pop_2020[,2:ncol(Race_10_19_Pop_2020)]
names(Race_10_19_Pop_2020)
head(Race_10_19_Pop_2020)

## Preliminary results (to be validated) ##

# White: 2163 (i.e., 77.33% vs in the US pop in that age group: 75.07%) --> more exacerbated
# BAA: 386 (i.e., 13.80% vs in the US pop in that age group: 16.59%) --> less exacerbated
# AIAN: 99 (i.e., 3.54% vs in the US pop in that age group: 1.85%) --> more exacerbated
# API: 149 (i.e., 5.33% vs in the US pop in that age group: 6.49%) --> less exacerbated

# Stratification by (race, ethnicity): population sizes
Race_Eth_10_19_Pop_2020 <- read.csv("C:/Users/Utilisateur/.../Race_Eth_10_19_Pop_2020.txt",header=TRUE,sep='\t')
Race_Eth_10_19_Pop_2020 <- Race_Eth_0_19_Pop_2020[,2:ncol(Race_Eth_10_19_Pop_2020)]
names(Race_Eth_10_19_Pop_2020)
head(Race_Eth_10_19_Pop_2020)

## Preliminary results (to be validated) ##

# Hispanic pop: 549 (i.e., 19.63% vs in the US pop: 25.11%) --> less exacerbated
# White non-hisp: 1661 (i.e., 59.39%% vs in the US pop: 52.88%) --> more exacerbated
RE_Suicide_National_10_19_2020[RE_Suicide_National_10_19_2020$Race == 'White' & RE_Suicide_National_10_19_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# Black non-hisp: 356 (i.e., 12.73% vs in the US pop: 15.03%) --> less exacerbated
RE_Suicide_National_10_19_2020[RE_Suicide_National_10_19_2020$Race == 'Black or African American' & RE_Suicide_National_10_19_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# API non-hisp: 138 (i.e., 4.93% vs in the US pop: 6.00%) --> less exacerbated
RE_Suicide_National_10_19_2020[RE_Suicide_National_10_19_2020$Race == 'Asian or Pacific Islander' & RE_Suicide_National_10_19_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']
# AIAN non-hisp: 90 (i.e., 3.22% vs in the US pop: 0.98%) --> more exacerbated
RE_Suicide_National_10_19_2020[RE_Suicide_National_10_19_2020$Race == 'American Indian or Alaska Native' & RE_Suicide_National_10_19_2020$Hispanic.Origin == 'Not Hispanic or Latino','Deaths']

# In the five states + California with a stat. sig. increase (overall)
# TODO

# In the five states + California with a stat. sig. increase (per state)
# TODO
