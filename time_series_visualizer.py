import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df = df.set_index(['date'])
#filter out data that lies too many standard deviatons from the mean
df = df[(df['value'].quantile(0.025) <= df['value']) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    #reformat date, as it makes starting date 1970 (epoch)
    df.index = pd.to_datetime(df.index)

    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 5))
    sns.lineplot(data=df, x = df.index, y = 'value',color='red').set(
        title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019', 
        ylabel = "Page Views",
        xlabel = "Date")

    #set form for date
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
    date_form = mdates.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_form)
    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    #group the data by month
    df_bar = df.groupby(pd.Grouper(freq="M"))
    #to each group find the mean
    df_bar = df_bar.mean()

    #reformat date, as it makes starting date 1970 (epoch)
    df_bar.index = pd.to_datetime(df_bar.index)
    #seperate the date into year and month, to use as x axis and hue respectively
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Draw bar plot
    #set month order for hues
    months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
    
    fig, ax = plt.subplots(figsize=(8,6))
    

    sns.barplot(data=df_bar, x ='year', y='value',
                 hue= 'month', hue_order=months,
                 palette=sns.color_palette()).set(
        ylabel = "Average Page Views",
        xlabel = "Years")
   

    #set the x labels to rotate
    plt.xticks(rotation=90)
    #adjust legend position
    plt.legend(loc = "upper left")

    #ax.axes.set_xlim(-0.5,3.6)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(16,6))
    sns.boxplot(data = df_box, x = 'year', y = 'value', ax=ax[0], 
                palette=sns.color_palette(n_colors =4),
                fliersize=2).set(
        ylabel = 'Page Views',
        xlabel = 'Year',
        title = 'Year-wise Box Plot (Trend)'
    )

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    sns.boxplot(data = df_box, x = 'month', y='value',order = months, ax=ax[1],
                palette=sns.color_palette(palette="husl",n_colors=12), width=0.6,
                fliersize=2).set(
        ylabel = 'Page Views',
        xlabel = 'Month',
        title = 'Month-wise Box Plot (Seasonality)'
    )




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
