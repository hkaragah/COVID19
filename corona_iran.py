import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation, rc, style, ticker

# list available python magics
# %lsmagic
# -----------------------------------------------------
#style.available
#style.use('fivethirtyeight')
style.use('seaborn-dark')
# -----------------------------------------------------
wide_file = './Data/iran/covid_iran_long.csv'
long_file = './Data/iran/covid_iran_wide.csv'
mapping_file = './Data/iran/iran_region_mapping.csv'
file_name = wide_file

iran_df = pd.read_csv(file_name, sep=',')
# -----------------------------------------------------
def get_cases_by_province(dataframe, province):
    province_filter = dataframe['province'] == province
    cases_by_date = {'date': [], 'cases': []}

    for date in dataframe['date'].unique():
        cases_by_date['date'].append(date)
        date_filter = dataframe['date'] == date
        cases_by_date['cases'].append(dataframe[date_filter & province_filter]['cases'].sum())

    cases_by_date_df = pd.DataFrame.from_dict(cases_by_date)
    cases_by_date_df['cum_cases'] = cases_by_date_df['cases'].cumsum()
    return cases_by_date_df
# -----------------------------------------------------
def get_cases_by_date(data, date):
    """
    Returns a data frame showing data obtained on a specific date
    :param data: Dictionary of DataFrames
    :param date: String
    :return: DataFrame
    """

    province_list = data.keys()
    cases_by_date = {'province': [], 'cases': [], 'cum_cases': []}

    for province in province_list:
        date_filter = data[province]['date'] == date
        cases_by_date['province'].append(province)
        cases_by_date['cases'].append(data[province][date_filter]['cases'].sum())
        cases_by_date['cum_cases'].append(data[province][date_filter]['cum_cases'].sum())

    cases_by_date_df = pd.DataFrame.from_dict(cases_by_date)
    return cases_by_date_df
# -----------------------------------------------------
provinces = iran_df['province'].unique()
dates = iran_df['date'].unique()

all_provinces = {}
for province in provinces:
    all_provinces[province] = get_cases_by_province(iran_df, province)


all_dates = {}
for date in dates:
    all_dates[date] = get_cases_by_date(all_provinces, date)
# -----------------------------------------------------
# colors = dict(zip(iran_df['region'].unique(),['#2E8B57', '#577777', '#00CD66', '#00EE00', '#CAFF70']))
# groups = iran_df.set_index('province')['region'].to_dict()
# -----------------------------------------------------
def aniamte(date):

    df = all_dates[date]
    df.sort_values(by='cum_cases', ascending=True, inplace=True)
    ax.clear()
    ax.barh(df['province'], df['cum_cases'], color='#2E8B57')
    # ax.barh(df['province'], df['cum_cases'], color=[colors[groups[x]] for x in df['province']])

    for i, (cum_cases, province) in enumerate(zip(df['cum_cases'], df['province'])):
        if cum_cases > 0:
            ax.text(cum_cases, i, province + '.' + str(cum_cases), color='#777777', size=8, weight=400, ha='left', va='center')
            # ax.text(cum_cases, i+.25, province, color='#777777', size=7, weight=600, ha='left', va='center')
            # ax.text(cum_cases, i-.25, f'{cum_cases:,.0f}', color='#777777', size=7, ha='left', va='center')

    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=8)
    ax.set_yticks([])
    max = all_dates[date]['cum_cases'].max()
    ax.set_xlim((0,max_x))
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    non_zero = all_dates[date].astype(bool).sum(axis=0)['cum_cases']
    customized_text = str(non_zero) + 'province(s) involved'
    ax.text(0.5, 0.5, customized_text , transform=ax.transAxes, size=8, ha='center', color='#777777')
    ax.text(0.5, 1.07, 'Total Confirmed Cases of COVID-19 in Iran',
            transform=ax.transAxes, size=8, ha='center', color='#777777')
    ax.text(0.5, 1.04, date, transform=ax.transAxes, color='#777777', size=8, ha='center', weight=600,
            bbox=dict(facecolor='#eaeaf1', alpha=1.0, edgecolor='white'))
    # ax.text(0, 1.06, 'Accumulated Confimed Cases of COVID-19', transform=ax.transAxes, size=12, color='#777777')
    ax.text(1, .005, 'Data visualization: Hossein Karagah @GitHub\nData source: Rami Krispin @GitHub',
            size=5, rotation=90, transform=ax.transAxes, ha='left', color='#577777')
    plt.tight_layout()
# -----------------------------------------------------
fig, ax = plt.subplots(figsize=(5,8))
animator = animation.FuncAnimation(fig, aniamte, frames=dates, interval=5000 )
max_x = round(all_dates[dates[-1]]['cum_cases'].max(), -3) + 1
# animator.save('iran_covid19.gif', fps=.5, dpi=720)
writer =  animation.FFMpegWriter(fps=.5, bitrate=10000)
animator.save("iran_covid19.mp4", writer=writer, dpi=720)

