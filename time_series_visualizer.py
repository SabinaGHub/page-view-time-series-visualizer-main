import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')
df.index=pd.to_datetime(df.index)
# Clean data
df = df.loc[(df['value']>=df['value'].quantile(0.025)) & (df['value']<=df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, axes=plt.subplots()
    axes.plot(df.index,df['value'], c='red')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019') 


    # Save image and return fig (don't change this part)
    plt.show()
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():

    # Copy and modify data for monthly bar plot
    df_bar=df.copy()    
    df_bar['month']=df_bar.index.strftime("%B")
    df_bar['year']=df_bar.index.year
    df_bar['month_num']=df_bar.index.month #required for later sorting
    df_bar=df_bar.groupby(['year','month']).mean().reset_index()

    #find and add missing values 
    i=min(set(df_bar['year'].to_list()))
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    while i<max(set(df_bar['year'].to_list())):
        for monthinlist in months:
            if (monthinlist not in df_bar.loc[df_bar['year']==i,'month'].to_list()):
                df_bar.loc[len(df_bar)]=[i,monthinlist,0,months.index(monthinlist)+1]         
        i+=1

    df_bar=df_bar.sort_values(by=['year','month_num']).reset_index()
    df_bar=df_bar[['year','month_num','value']]
    df_bar = df_bar.pivot(index='year', columns='month_num', values='value')

    # Draw bar plot
    years=np.arange(len(df_bar.index))
    fig, ax=plt.subplots(layout='constrained')
    width=0.05
    mult=0
    for month in df_bar.columns:
        label=months[int(month)-1]
        ax.bar(years + mult*width, df_bar[month], width=width ,label=label)
        mult+=1

    ax.set_xticks(years + width * (len(df_bar.columns) - 1) / 2)
    ax.set_xticklabels(df_bar.index)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Yearly Value Distribution by Month')
    ax.legend(title='Month')

    
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
    df_box['date']=pd.to_datetime(df_box['date'])
    df_box['month_num']=df_box['date'].dt.month
    df_box=df_box.sort_values(by=['month_num'])

    fig, (ax1,ax2)=plt.subplots(nrows=1,ncols=2)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax1.set(xlabel='Year', ylabel='Page Views')
    ax2.set(xlabel='Month', ylabel='Page Views')
    sns.boxplot(ax=ax1,x= df_box['year'], y=df_box['value'] )
    sns.boxplot(ax=ax2,x= df_box['month'], y=df_box['value'] )


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
