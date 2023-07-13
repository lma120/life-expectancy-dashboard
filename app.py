# Import dependencies
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px


# Initialize app
app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Life Expectancy Dashboard"
server = app.server

# Load data
mdf = pd.read_csv('dataset/malaysia_life_expectancy.csv')  # malaysian dataset
wdf = pd.read_csv('dataset/who_life_expectancy.csv')  # world dataset

# MALAYSIAN DATASET DATA CLEANING

# replace "80+" with 80 in the Age column, transform into datatype int
mdf['Age'] = mdf['Age'].apply(
    lambda x: 80 if x == '80+' else int(x))
mdf['Year'] = mdf['Year'].str.replace('p', '').str.replace('e', '').astype(int)

# add a new column 'Total Life Expectancy'
mdf['Total life expectancy'] = mdf['Age'] + mdf['Life expectancy']

# renaming the column and variables for convenience
mdf['Major ethnic group'] = mdf['Major ethnic group'].replace({'Bumiputera': 'Malay', 'Indians': 'Indian'})
mdf = mdf.rename(columns={'Major ethnic group' : "Ethnic"})


# WORLD DATASET DATA CLEANING

# Replacing the Null Values with mean values of the data
wdf['Life expectancy ']=wdf['Life expectancy '].fillna(value=wdf['Life expectancy '].mean())
wdf['Adult Mortality']=wdf['Adult Mortality'].fillna(value=wdf['Adult Mortality'].mean())
wdf[' BMI ']=wdf[' BMI '].fillna(value=wdf[' BMI '].mean())
wdf['Income composition of resources']=wdf['Income composition of resources'].fillna(value=wdf['Income composition of resources'].mean())
wdf['Schooling']=wdf['Schooling'].fillna(value=wdf['Schooling'].mean())

# filter only the top 5 correlated variables with life expectancy
wdf.drop(columns=['infant deaths', 'Total expenditure',
       'Diphtheria ' ,'Alcohol', 'GDP', 'Population',
       ' thinness  1-19 years', ' thinness 5-9 years', 'percentage expenditure','Polio','Hepatitis B', 'Measles ','under-five deaths '], inplace=True)

# rename the columns
wdf = wdf.rename(columns={'Life expectancy ': 'Life expectancy', ' BMI ': 'BMI', ' HIV/AIDS' : 'HIV/AIDS' })

# ISO-Country Reference
ISOs_Country = {
    'ABW': 'Aruba', 'AFG': 'Afghanistan', 'AGO': 'Angola', 'AIA': 'Anguilla', 'ALA': 'Åland Islands', 'ALB': 'Albania',
    'AND': 'Andorra', 'ARE': 'United Arab Emirates', 'ARG': 'Argentina', 'ARM': 'Armenia', 'ASM': 'American Samoa',
    'ATA': 'Antarctica', 'ATF': 'French Southern Territories', 'ATG': 'Antigua and Barbuda', 'AUS': 'Australia',
    'AUT': 'Austria', 'AZE': 'Azerbaijan', 'BDI': 'Burundi', 'BEL': 'Belgium', 'BEN': 'Benin',
    'BES': 'Bonaire, Sint Eustatius and Saba', 'BFA': 'Burkina Faso', 'BGD': 'Bangladesh', 'BGR': 'Bulgaria',
    'BHR': 'Bahrain', 'BHS': 'Bahamas', 'BIH': 'Bosnia and Herzegovina', 'BLM': 'Saint Barthélemy', 'BLR': 'Belarus',
    'BLZ': 'Belize', 'BMU': 'Bermuda', 'BOL': 'Bolivia (Plurinational State of)', 'BRA': 'Brazil', 'BRB': 'Barbados',
    'BRN': 'Brunei Darussalam', 'BTN': 'Bhutan', 'BVT': 'Bouvet Island', 'BWA': 'Botswana',
    'CAF': 'Central African Republic',
    'CAN': 'Canada', 'CCK': 'Cocos (Keeling) Islands', 'CHE': 'Switzerland', 'CHL': 'Chile', 'CHN': 'China',
    'CIV': 'Côte d\'Ivoire', 'CMR': 'Cameroon', 'COD': 'Democratic Republic of the Congo', 'COG': 'Congo',
    'COK': 'Cook Islands', 'COL': 'Colombia', 'COM': 'Comoros', 'CPV': 'Cabo Verde', 'CRI': 'Costa Rica', 'CUB': 'Cuba',
    'CUW': 'Curaçao', 'CXR': 'Christmas Island', 'CYM': 'Cayman Islands', 'CYP': 'Cyprus', 'CZE': 'Czechia',
    'DEU': 'Germany', 'DJI': 'Djibouti', 'DMA': 'Dominica', 'DNK': 'Denmark', 'DOM': 'Dominican Republic',
    'DZA': 'Algeria',
    'ECU': 'Ecuador', 'EGY': 'Egypt', 'ERI': 'Eritrea', 'ESH': 'Western Sahara', 'ESP': 'Spain', 'EST': 'Estonia',
    'ETH': 'Ethiopia', 'FIN': 'Finland', 'FJI': 'Fiji', 'FLK': 'Falkland Islands (Malvinas)', 'FRA': 'France',
    'FRO': 'Faroe Islands', 'FSM': 'Micronesia (Federated States of)', 'GAB': 'Gabon',
    'GBR': 'United Kingdom of Great Britain and Northern Ireland', 'GEO': 'Georgia', 'GGY': 'Guernsey', 'GHA': 'Ghana',
    'GIB': 'Gibraltar', 'GIN': 'Guinea', 'GLP': 'Guadeloupe', 'GMB': 'Gambia', 'GNB': 'Guinea-Bissau',
    'GNQ': 'Equatorial Guinea', 'GRC': 'Greece', 'GRD': 'Grenada', 'GRL': 'Greenland', 'GTM': 'Guatemala',
    'GUF': 'French Guiana', 'GUM': 'Guam', 'GUY': 'Guyana', 'HKG': 'Hong Kong',
    'HMD': 'Heard Island and McDonald Islands',
    'HND': 'Honduras', 'HRV': 'Croatia', 'HTI': 'Haiti', 'HUN': 'Hungary', 'IDN': 'Indonesia', 'IMN': 'Isle of Man',
    'IND': 'India', 'IOT': 'British Indian Ocean Territory', 'IRL': 'Ireland', 'IRN': 'Iran (Islamic Republic of)',
    'IRQ': 'Iraq', 'ISL': 'Iceland', 'ISR': 'Israel', 'ITA': 'Italy', 'JAM': 'Jamaica', 'JEY': 'Jersey',
    'JOR': 'Jordan',
    'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan', 'KHM': 'Cambodia', 'KIR': 'Kiribati',
    'KNA': 'Saint Kitts and Nevis', 'KOR': 'Republic of Korea', 'KWT': 'Kuwait',
    'LAO': 'Lao People\'s Democratic Republic',
    'LBN': 'Lebanon', 'LBR': 'Liberia', 'LBY': 'Libya', 'LCA': 'Saint Lucia', 'LIE': 'Liechtenstein',
    'LKA': 'Sri Lanka',
    'LSO': 'Lesotho', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia', 'MAC': 'Macao',
    'MAF': 'Saint Martin (French part)', 'MAR': 'Morocco', 'MCO': 'Monaco', 'MDA': 'Republic of Moldova',
    'MDG': 'Madagascar', 'MDV': 'Maldives', 'MEX': 'Mexico', 'MHL': 'Marshall Islands', 'MKD': 'North Macedonia',
    'MLI': 'Mali', 'MLT': 'Malta', 'MMR': 'Myanmar', 'MNE': 'Montenegro', 'MNG': 'Mongolia',
    'MNP': 'Northern Mariana Islands',
    'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MSR': 'Montserrat', 'MTQ': 'Martinique', 'MUS': 'Mauritius',
    'MWI': 'Malawi',
    'MYS': 'Malaysia', 'MYT': 'Mayotte', 'NAM': 'Namibia', 'NCL': 'New Caledonia', 'NER': 'Niger',
    'NFK': 'Norfolk Island',
    'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NIU': 'Niue', 'NLD': 'Netherlands', 'NOR': 'Norway', 'NPL': 'Nepal',
    'NRU': 'Nauru',
    'NZL': 'New Zealand', 'OMN': 'Oman', 'PAK': 'Pakistan', 'PAN': 'Panama', 'PCN': 'Pitcairn', 'PER': 'Peru',
    'PHL': 'Philippines',
    'PLW': 'Palau', 'PNG': 'Papua New Guinea', 'POL': 'Poland', 'PRI': 'Puerto Rico',
    'PRK': 'Democratic People\'s Republic of Korea',
    'PRT': 'Portugal', 'PRY': 'Paraguay', 'PSE': 'Palestine, State of', 'PYF': 'French Polynesia', 'QAT': 'Qatar',
    'REU': 'Réunion',
    'ROU': 'Romania', 'RUS': 'Russian Federation', 'RWA': 'Rwanda', 'SAU': 'Saudi Arabia', 'SDN': 'Sudan',
    'SEN': 'Senegal',
    'SGP': 'Singapore', 'SGS': 'South Georgia and the South Sandwich Islands',
    'SHN': 'Saint Helena, Ascension and Tristan da Cunha',
    'SJM': 'Svalbard and Jan Mayen', 'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone', 'SLV': 'El Salvador',
    'SMR': 'San Marino',
    'SOM': 'Somalia', 'SPM': 'Saint Pierre and Miquelon', 'SRB': 'Serbia', 'SSD': 'South Sudan',
    'STP': 'Sao Tome and Principe',
    'SUR': 'Suriname', 'SVK': 'Slovakia', 'SVN': 'Slovenia', 'SWE': 'Sweden', 'SWZ': 'Eswatini',
    'SXM': 'Sint Maarten (Dutch part)',
    'SYC': 'Seychelles', 'SYR': 'Syrian Arab Republic', 'TCA': 'Turks and Caicos Islands', 'TCD': 'Chad', 'TGO': 'Togo',
    'THA': 'Thailand', 'TJK': 'Tajikistan', 'TKL': 'Tokelau', 'TKM': 'Turkmenistan', 'TLS': 'Timor-Leste',
    'TON': 'Tonga',
    'TTO': 'Trinidad and Tobago', 'TUN': 'Tunisia', 'TUR': 'Turkey', 'TUV': 'Tuvalu',
    'TWN': 'Taiwan, Province of China',
    'TZA': 'United Republic of Tanzania', 'UGA': 'Uganda', 'UKR': 'Ukraine',
    'UMI': 'United States Minor Outlying Islands',
    'URY': 'Uruguay', 'USA': 'United States of America', 'UZB': 'Uzbekistan', 'VAT': 'Holy See',
    'VCT': 'Saint Vincent and the Grenadines',
    'VEN': 'Venezuela (Bolivarian Republic of)', 'VGB': 'Virgin Islands (British)', 'VIR': 'Virgin Islands (U.S.)',
    'VNM': 'Viet Nam',
    'VUT': 'Vanuatu', 'WLF': 'Wallis and Futuna', 'WSM': 'Samoa', 'YEM': 'Yemen', 'ZAF': 'South Africa',
    'ZMB': 'Zambia',
    'ZWE': 'Zimbabwe'}

YEARS = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

ISO_df = pd.DataFrame.from_dict(ISOs_Country, orient='index', columns=['Country']).reset_index().rename(
    columns={'index': 'ISO'})

merged_wdf = pd.merge(wdf, ISO_df, on='Country', how='left')

BINS = [
    "0-2",
    "2.1-4",
    "4.1-6",
    "6.1-8",
    "8.1-10",
    "10.1-12",
    "12.1-14",
    "14.1-16",
    "16.1-18",
    "18.1-20",
    "20.1-22",
    "22.1-24",
    "24.1-26",
    "26.1-28",
    "28.1-30",
    ">30",
]

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="Life Expectancy Analysis: A Comparison of the World and Malaysia"),
                html.P(
                    id="description",
                    children="Life expectancy is a statistical measure that represents the average number of years that a person can expect to live. It is widely used to indicate of overall population health and well-being, and is often used as a benchmark for comparing the health outcomes of different countries or populations. "),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="world-graph-container",
                            children=[
                                html.P(id="world-chart-selector",
                                       children="Select chart to display World Life Expectancy:"),
                                dcc.Dropdown(
                                    options=["Yearly Life Expectancy", "Total Life Expectancy",
                                             "Life Expectancy Based on Country Status",
                                             "Life Expectancy vs Schooling",
                                             "Correlation Matrix Heatmap",
                                             "HIV/AIDS vs Life Expectancy over the World Map",
                                             "Life Expectancy Choropleth Map"],
                                    value="Yearly Life Expectancy",
                                    id="world-chart-dropdown",
                                ),
                                html.Br(),
                                dcc.Graph(
                                    id="selected-world-data",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                ),
                            ]
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                dcc.Graph(
                                    figure=px.scatter_geo(merged_wdf, locations='ISO',
                                                          projection='orthographic',
                                                          opacity=0.8, color='Country', hover_name='Country',
                                                          hover_data=['Life expectancy', 'HIV/AIDS',
                                                                      'Schooling', 'Status'],
                                                          template='plotly_dark',
                                                          title='<b>Average Life Expectancy by Country on World Map')

                                ),

                            ],
                        ),
                    ]
                ),
                html.Div(
                    id="right-column",
                    children=[
                        html.Div(
                            id="selector-container",
                            children=[
                                html.P(id="predictor-selector",
                                       children="Predict Your Life Expectancy as a Malaysian:"),
                                html.Div(
                                    id="left-right-container",
                                    children=[
                                        html.Div(
                                            id="selector-container-left",
                                            children=[
                                                html.Div(
                                                    id="predictor-container-1",
                                                    children=[
                                                        html.P(id="race-selector", children="Select Race:"),
                                                        dcc.Dropdown(
                                                            options=["Chinese", "Malay", "Indian"],
                                                            value="Chinese",
                                                            id="race-selection",
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    id="predictor-container-2",
                                                    children=[
                                                        html.P(id="gender-selector", children="Select Gender:"),
                                                        dcc.Dropdown(
                                                            options=["Male", "Female"],
                                                            value="Male",
                                                            id="gender-selection",
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    id="predictor-container-3",
                                                    children=[
                                                        html.P(id="age-selector", children="Select Age:"),
                                                        dcc.Dropdown(
                                                            options=[age for age in range(85)],
                                                            value=21,
                                                            id="age-selection",
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            id='selector-container-right',
                                            children=[
                                                html.P(id="age-prediction-title",
                                                       children="Your Predicted Life Expectancy is:"),
                                                html.Div(id='age-prediction'),
                                            ]
                                        )
                                    ]
                                )

                            ]
                        ),

                        html.Div(
                            id="graph-container",
                            children=[
                                html.P(id="chart-selector",
                                       children="Select chart to display Malaysia Life Expectancy:"),
                                dcc.Dropdown(
                                    options=["Life Expectancy Distribution Histogram",
                                             "Average Life Expectancy from 2010 to 2015",
                                             "Life Expectancy Based on Sex",
                                             "Life Expectancy Based on Ethnicity",
                                             "Life Expectancy over Years in Malaysia",
                                             "Average Life Expectancy by Ethnic and Sex in Malaysia"],
                                    value="Life Expectancy Distribution Histogram",
                                    id="chart-dropdown",
                                ),
                                dcc.Graph(
                                    id="selected-data",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                ),
                            ]
                        )

                    ]
                ),
            ],
        ),
    ],
)


# @app.callback(Output("heatmap-title", "children"), [Input("years-slider", "value")])
# def update_map_title(year):
#     return "Heatmap of age adjusted mortality rates \
# 				from poisonings in year {0}".format(
#         year
#     )

@app.callback(
    Output('age-prediction', 'children'),
    [
        Input("race-selection", "value"),
        Input("gender-selection", "value"),
        Input("age-selection", "value"),
    ],
)
def update_output_div(race, gender, age):
    mdf_prediction = mdf[(mdf['Ethnic'] == race) & (mdf['Sex'] == gender) & (mdf['Year'] >= 2019) & (
            mdf['Age'] >= age - 5) & (mdf['Age'] <= age + 5)]
    predicted_age = mdf_prediction['Life expectancy'].mean()

    return str(int(predicted_age))


@app.callback(
    Output("selected-world-data", "figure"),
    [
        Input("world-chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def update_graph(chart_dropdown, years_slider):
    year = int(years_slider)
    data = wdf[wdf["Year"] == year]
    iso_data = merged_wdf[merged_wdf["Year"] == year]

    if chart_dropdown == "Total Life Expectancy":
        fig = px.histogram(wdf, x='Life expectancy', template='plotly_dark', title='Total Life Expectancy')

    elif chart_dropdown == "Yearly Life Expectancy":
        fig = px.histogram(data, x='Life expectancy', template='plotly_dark',
                           title='Average Life Expectancy in {0}'.format(year))
        fig.update_xaxes(range=[35, 90])

    elif chart_dropdown == "Life Expectancy Based on Country Status":
        fig = px.violin(data, x='Status', y='Life expectancy', color='Status', template='plotly_dark', box=True,
                        title='Life expectancy Based on Countries status in {0}'.format(year))

    elif chart_dropdown == "HIV/AIDS vs Life Expectancy over the World Map":
        fig = px.scatter_geo(merged_wdf, locations="ISO",
                             color='Life expectancy',
                             size="HIV/AIDS",
                             hover_name="Country",
                             template='plotly_dark',
                             projection='natural earth',
                             title='HIV/AIDS vs Life Expectancy over the World Map',
                             color_continuous_scale=px.colors.sequential.Plasma)

    elif chart_dropdown == "Correlation Matrix Heatmap":
        fig = px.imshow(wdf.corr(), text_auto=True, template='plotly_dark')

    elif chart_dropdown == "Life Expectancy vs Schooling":
        fig = px.scatter(data,y='Schooling',x='Life expectancy',template='plotly_dark',title='<b> Life expectancy versus Schooling in {0}'.format(year))

    elif chart_dropdown == "Life Expectancy Choropleth Map":
        fig = px.choropleth(iso_data, locations="ISO",
                            color='Life expectancy',
                            hover_name="Country",
                            template='plotly_dark',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title='<b> Choropleth Map of Life Expectancy in {0}'.format(year))
    else:
        print("error: no chart")

    return fig


@app.callback(
    Output("selected-data", "figure"),
    [
        Input("chart-dropdown", "value")
    ],
)
def update_graph(chart_dropdown):

    if chart_dropdown == "Life Expectancy Distribution Histogram":
        wdf_filtered = wdf[(wdf['Year'] >= 2010) & (wdf['Year'] <= 2015)]
        mdf_filtered = mdf[(mdf['Year'] >= 2010) & (mdf['Year'] <= 2015)]

        a = mdf_filtered['Total life expectancy']
        b = wdf_filtered['Life expectancy']

        a_data = {
            'Country': ['Malaysia'] * len(a),
            'Life Expectancy': a
        }

        a_df = pd.DataFrame(a_data)

        b_data = {
            'Country': ['World'] * len(b),
            'Life Expectancy': b
        }

        b_df = pd.DataFrame(b_data)
        df = pd.concat([a_df, b_df], ignore_index=True)
        fig = px.histogram(df, x="Life Expectancy", template='plotly_dark', color="Country",
                           marginal="box",
                           hover_data=df.columns,
                           title='Life Expectancy Distribution')

    elif chart_dropdown == "Average Life Expectancy from 2010 to 2015":
        wdf_filtered = wdf[(wdf['Year'] >= 2010) & (wdf['Year'] <= 2015)]
        mdf_filtered = mdf[(mdf['Year'] >= 2010) & (mdf['Year'] <= 2015)]

        mdfYear = mdf_filtered.groupby('Year').mean()
        wdfYear = wdf_filtered.groupby('Year').mean()

        a = mdfYear['Total life expectancy']
        b = wdfYear['Life expectancy']

        a_data = {
            'Country': ['Malaysia'] * len(a),
            'Life Expectancy': a,
            'Year': a.index

        }

        a_df = pd.DataFrame(a_data)

        b_data = {
            'Country': ['World'] * len(b),
            'Life Expectancy': b,
            'Year': b.index
        }

        b_df = pd.DataFrame(b_data)

        df = pd.concat([a_df, b_df], ignore_index=True)

        fig = px.line(df, x="Year", y="Life Expectancy", template='plotly_dark', color="Country", markers=True,
                      title="Annual Life Expectancy between Malaysia and the World")

    elif chart_dropdown == "Life Expectancy Based on Sex":
        fig = px.violin(mdf, x='Sex', y='Total life expectancy', template='plotly_dark', color='Sex', box=True,
                        title='Life expectancy based on Sex')

    elif chart_dropdown == "Life Expectancy Based on Ethnicity":
        fig = px.violin(mdf, x='Ethnic', y='Total life expectancy', template='plotly_dark',
                        color='Ethnic', box=True, title='Life expectancy based on Ethnic')

    elif chart_dropdown == "Life Expectancy over Years in Malaysia":
        byYear = mdf.groupby('Year').mean()

        fig = px.line(byYear, y='Total life expectancy', template='plotly_dark', markers=True,
                      title='Life Expectancy over Years in Malaysia')

    elif chart_dropdown == "Average Life Expectancy by Ethnic and Sex in Malaysia":
        fig = px.histogram(mdf, y='Total life expectancy', x='Ethnic', color='Sex', barmode='group',
                           histfunc='avg', template='plotly_dark',
                           labels={
                               "avg of Total life expectancy": "Average life expectancy",
                           },
                           title='Average Life Expectancy by Ethnic and Sex in Malaysia')

    else:
        print("error: no chart")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
