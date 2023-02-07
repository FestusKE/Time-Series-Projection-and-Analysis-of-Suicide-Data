import requests
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

current_year = datetime.datetime.now().year
base = 'https://www.americashealthrankings.org/api/v1/downloads/'
start = input('Enter Start year (2011-20xx): ')
end = input('Enter End year (2011-20xx): ')
frames = []
for year in range(int(start), int(end)+1):
    # Data before and after 2015 is on different end points hence adding a check
    if year >= 2015:
        # Getting report Id from page
        res = requests.get(f'https://www.americashealthrankings.org/explore/annual/measure/Suicide/state/ALL?edition-year={year}')
    # Faced issues when scraping page for different years, figured out a way to get report ID
        source_id = res.text.split(f'"Name":"{year} Annual","EditionId":')[1][:4]
        # Checking if edition ID is 2,3 or 4 digits
        if source_id.isdecimal():
            df = pd.read_csv(base + source_id)
        elif source_id[:3].isdecimal():
            df = pd.read_csv(base + source_id[:3])
        else:
            df = pd.read_csv(base + source_id[:2])
    else:
        df = pd.read_csv(base + f'report/1/{year}')
    
    # Filtering only suicide data
    df['Measure Name'] = df['Measure Name'].fillna('Blank')
    df_2 = df[df['Measure Name'].str.contains('Suicide')]
    # Adding to dataframes list
    frames.append(df_2)
    
# Merging all yearly data into a single dataframe    
df = pd.concat(frames)
# selecting necessary columns only
df = df[['Edition', 'Measure Name', 'Value', 'State Name']]


"""Date for each parameter is contained in a single CSV file as separate rows, below we will extract data for each parameter in a separate dataframe and plot it"""
# Extracting aggregated suicide data
df_total = df[df['Measure Name'] == 'Suicide']
# Grouping by year and ploting average suicide rate
total_data = df_total.groupby('Edition')['Value'].mean()
total_data.plot(figsize=(10,6), xlabel= 'Year', title = 'Suicides per 100,000 Population', ylabel = 'Suicides per 100,000 population')
plt.show()

# Extracting suicide data for ages 15-24
df_total = df[df['Measure Name'] == 'Suicide - Ages 15-24']
total_data = df_total.groupby('Edition')['Value'].mean()
total_data.plot(figsize=(10,6), xlabel= 'Year', title = 'Suicides Aged 15-24', ylabel = 'Suicides per 100,000 population')
plt.show()

# Extracting gender based Suicide data
df_gender = df[(df['Measure Name'] == 'Suicide - Female') | (df['Measure Name'] == 'Suicide - Male')]
gender_group = df_gender.groupby(['Edition', 'Measure Name'])['Value'].mean()
#gender_group.plot(kind = 'bar')
gender_group.to_frame().reset_index().pivot(index='Edition', columns='Measure Name', values='Value').plot(kind='bar', xlabel= 'Year', title = 'Gender based suicide rate')
plt.show()

# Extracting racial suicide data
df_race = df[(df['Measure Name'] == 'Suicide - American Indian/Alaska Native') | (df['Measure Name'] == 'Suicide - Asian/Pacific Islander') | (df['Measure Name'] == 'Suicide - Black') | (df['Measure Name'] == 'Suicide - Hispanic')]
race_group = df_race.groupby(['Edition', 'Measure Name'])['Value'].mean()
race_group.to_frame().reset_index().pivot(index='Edition', columns='Measure Name', values='Value').plot(kind='bar', xlabel= 'Year', title = 'Race based suicide rate')
plt.show()

# Extracting Age based suicide data
df_age = df[(df['Measure Name'] == 'Suicide - Ages 15-24') | (df['Measure Name'] == 'Suicide - Ages 25-34') | (df['Measure Name'] == 'Suicide - Ages 35-44') | (df['Measure Name'] == 'Suicide - Ages 45-54') | (df['Measure Name'] == 'Suicide - Ages 55-64') | (df['Measure Name'] == 'Suicide - Ages 65-74') | (df['Measure Name'] == 'Suicide - Ages 75-84') | (df['Measure Name'] == 'Suicide - Ages 85+')]
age_group = df_age.groupby(['Measure Name'])['Value'].mean()
age_group.plot(kind ='bar', figsize=(8,5), xlabel= 'Year', title = 'Suicides by age group', ylabel = 'Suicides per 100,000 population')
plt.show()
