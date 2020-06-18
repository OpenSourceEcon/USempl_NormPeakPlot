'''
This module downloads the Dow Jones Industrial Average (DJIA) daily closing
price data series from either Stooq.com or from this directory and
organizes it into 15 series, one for each of the last 15 recessions--
from the current 2020 Coronavirus recession to the Great Depression of
1929. It then creates a normalized peak plot of the DJIA for each of the last
15 recessions using the Bokeh plotting library.

This module defines the following function(s):
    get_djia_data()
    djia_npp()
'''
# Import packages
import numpy as np
import pandas as pd
import pandas_datareader as pddr
import datetime as dt
import os
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Title, Legend, HoverTool
# from bokeh.models import Label
from bokeh.palettes import Category20

'''
Define functions
'''


def get_djia_data(frwd_days_max, bkwd_days_max, end_date_str,
                  download_from_internet=True):
    '''
    This function either downloads or reads in the DJIA data series and adds
    variables days_frm_peak and close_dv_pk for each of the last 15 recessions.

    Args:
        frwd_days_max (int): maximum number of days forward from the peak to
            plot
        bckwd_days_max (int): maximum number of days backward from the peak to
            plot
        end_date_str (str): end date of DJIA time series in 'YYYY-mm-dd' format
        download_from_internet (bool): =True if download data from Stooq.com,
            otherwise read date in from local directory

    Other functions and files called by this function:
        djia_close_[yyyy-mm-dd].csv

    Files created by this function:
        djia_close_[yyyy-mm-dd].csv
        djia_close_pk_[yyyy-mm-dd].csv

    Returns:
        djia_close_pk (DataFrame): N x 46 DataFrame of days_frm_peak, Date{i},
            Close{i}, and close_dv_pk{i} for each of the 15 recessions for the
            periods specified by bkwd_days_max and frwd_days_max
        end_date_str2 (str): actual end date of DJIA time series in
            'YYYY-mm-dd' format. Can differ from the end_date input to this
            function if the final data for that day have not come out yet
            (usually 2 hours after markets close, 6:30pm EST), or if the
            end_date is one on which markets are closed (e.g. weekends and
            holidays). In this latter case, the pandas_datareader library
            chooses the most recent date for which we have DJIA data.
        peak_vals (list): list of peak DJIA value at the beginning of each of
            the last 15 recessions
        peak_dates (list): list of string date (YYYY-mm-dd) of peak DJIA value
            at the beginning of each of the last 15 recessions
        rec_label_yr_lst (list): list of string start year and end year of each
            of the last 15 recessions
        rec_label_yrmth_lst (list): list of string start year and month and end
            year and month of each of the last 15 recessions
        rec_beg_yrmth_lst (list): list of string start year and month of each
            of the last 15 recessions
        maxdate_rng_lst (list): list of tuples with start string date and end
            string date within which range we define the peak DJIA value at the
            beginning of each of the last 15 recessions
    '''
    end_date = dt.datetime.strptime(end_date_str, '%Y-%m-%d')

    # Name the current directory and make sure it has a data folder
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    data_fldr = 'data'
    data_dir = os.path.join(cur_path, data_fldr)
    if not os.access(data_dir, os.F_OK):
        os.makedirs(data_dir)

    filename_basic = ('data/djia_close_' + end_date_str + '.csv')
    filename_full = ('data/djia_close_pk_' + end_date_str + '.csv')

    if download_from_internet:
        # Download the DJIA data directly from Stooq.com
        # (requires internet connection)
        start_date = dt.datetime(1896, 5, 27)
        djia_df = pddr.stooq.StooqDailyReader(symbols='^DJI',
                                              start=start_date,
                                              end=end_date).read()
        djia_close = djia_df['Close']
        djia_close = pd.DataFrame(djia_close).sort_index()  # Sort old to new
        djia_close = djia_close.reset_index(level=['Date'])
        end_date_str2 = djia_close['Date'].iloc[-1].strftime('%Y-%m-%d')
        end_date = dt.datetime.strptime(end_date_str2, '%Y-%m-%d')
        filename_basic = ('data/djia_close_' + end_date_str2 + '.csv')
        filename_full = ('data/djia_close_pk_' + end_date_str2 + '.csv')
        djia_close.to_csv(filename_basic, index=False)
    else:
        # Import the data as pandas DataFrame
        end_date_str2 = end_date_str
        data_file_path = os.path.join(cur_path, filename_basic)
        djia_close = pd.read_csv(data_file_path,
                                 names=['Date', 'Close'],
                                 parse_dates=['Date'], skiprows=1,
                                 na_values=['.', 'na', 'NaN'])
        djia_close = djia_close.dropna()

    print('End date of DJIA series is', end_date.strftime('%Y-%m-%d'))

    # Set recession-specific parameters
    rec_label_yr_lst = \
        ['1929-1933',  # (Aug 1929 - Mar 1933) Great Depression
         '1937-1938',  # (May 1937 - Jun 1938)
         '1945',       # (Feb 1945 - Oct 1945)
         '1948-1949',  # (Nov 1948 - Oct 1949)
         '1953-1954',  # (Jul 1953 - May 1954)
         '1957-1958',  # (Aug 1957 - Apr 1958)
         '1960-1961',  # (Apr 1960 - Feb 1961)
         '1969-1970',  # (Dec 1969 - Nov 1970)
         '1973-1975',  # (Nov 1973 - Mar 1975)
         '1980',       # (Jan 1980 - Jul 1980)
         '1981-1982',  # (Jul 1981 - Nov 1982)
         '1990-1991',  # (Jul 1990 - Mar 1991)
         '2001',       # (Mar 2001 - Nov 2001)
         '2007-2009',  # (Dec 2007 - Jun 2009) Great Recession
         '2020-pres']  # (Feb 2020 - present) Coronavirus recession

    rec_label_yrmth_lst = ['Aug 1929 - Mar 1933',  # Great Depression
                           'May 1937 - Jun 1938',
                           'Feb 1945 - Oct 1945',
                           'Nov 1948 - Oct 1949',
                           'Jul 1953 - May 1954',
                           'Aug 1957 - Apr 1958',
                           'Apr 1960 - Feb 1961',
                           'Dec 1969 - Nov 1970',
                           'Nov 1973 - Mar 1975',
                           'Jan 1980 - Jul 1980',
                           'Jul 1981 - Nov 1982',
                           'Jul 1990 - Mar 1991',
                           'Mar 2001 - Nov 2001',
                           'Dec 2007 - Jun 2009',  # Great Recession
                           'Feb 2020 - present']  # Coronavirus recess'n

    rec_beg_yrmth_lst = ['Aug 1929', 'May 1937', 'Feb 1945', 'Nov 1948',
                         'Jul 1953', 'Aug 1957', 'Apr 1960', 'Dec 1969',
                         'Nov 1973', 'Jan 1980', 'Jul 1981', 'Jul 1990',
                         'Mar 2001', 'Dec 2007', 'Feb 2020']

    maxdate_rng_lst = [('1929-7-1', '1929-10-30'),
                       ('1937-3-1', '1937-7-1'),
                       ('1945-1-1', '1945-4-1'),
                       ('1948-9-1', '1949-1-31'),
                       ('1953-5-1', '1953-9-30'),
                       ('1957-6-1', '1957-10-31'),
                       ('1959-12-1', '1960-7-1'),
                       ('1969-10-1', '1970-1-31'),
                       ('1973-9-1', '1973-12-31'),
                       ('1979-12-1', '1980-3-1'),
                       ('1981-6-1', '1981-8-30'),
                       ('1990-6-1', '1991-8-31'),
                       ('2001-1-25', '2001-4-30'),
                       ('2007-10-1', '2008-1-31'),
                       ('2020-2-1', '2020-3-15')]

    # Create normalized peak series for each recession
    djia_close_pk = \
        pd.DataFrame(np.arange(-bkwd_days_max, frwd_days_max + 1, dtype=int),
                     columns=['days_frm_peak'])
    djia_close_pk_long = djia_close.copy()
    peak_vals = []
    peak_dates = []
    for i, maxdate_rng in enumerate(maxdate_rng_lst):
        # Identify peak closing value within two months (with only ?
        # exceptions) of the beginning month of the recession
        peak_val = \
            djia_close['Close'][(djia_close['Date'] >= maxdate_rng[0]) &
                                (djia_close['Date'] <=
                                 maxdate_rng[1])].max()
        peak_vals.append(peak_val)
        close_dv_pk_name = 'close_dv_pk' + str(i)
        djia_close_pk_long[close_dv_pk_name] = (djia_close_pk_long['Close'] /
                                                peak_val)
        # Identify date of peak closing value within two months (with
        # only ? exceptions) of the beginning month of the recession
        peak_date = \
            djia_close['Date'][(djia_close['Date'] >= maxdate_rng[0]) &
                               (djia_close['Date'] <= maxdate_rng[1]) &
                               (djia_close['Close'] == peak_val)].max()
        peak_dates.append(peak_date.strftime('%Y-%m-%d'))
        days_frm_pk_name = 'days_frm_pk' + str(i)
        djia_close_pk_long[days_frm_pk_name] = (djia_close_pk_long['Date'] -
                                                peak_date).dt.days
        print('peak_val ' + str(i) + ' is', peak_val, 'on date',
              peak_date.strftime('%Y-%m-%d'), '(Beg. rec. month:',
              rec_beg_yrmth_lst[i], ')')
        # I need to merge the data into this new djia_close_pk DataFrame
        # because weekends make these data have missing points relative to the
        # initial left DataFrame
        djia_close_pk = \
            pd.merge(djia_close_pk,
                     djia_close_pk_long[[days_frm_pk_name, 'Date', 'Close',
                                         close_dv_pk_name]],
                     left_on='days_frm_peak', right_on=days_frm_pk_name,
                     how='left')
        djia_close_pk.drop(columns=[days_frm_pk_name], inplace=True)
        djia_close_pk.rename(
            columns={'Date': f'Date{i}', 'Close': f'Close{i}'}, inplace=True)

    djia_close_pk.to_csv(filename_full, index=False)

    return (djia_close_pk, end_date_str2, peak_vals, peak_dates,
            rec_label_yr_lst, rec_label_yrmth_lst, rec_beg_yrmth_lst,
            maxdate_rng_lst)


def djia_npp(frwd_mths_main=6, bkwd_mths_main=1, frwd_mths_max=12,
             bkwd_mths_max=3, djia_end_date='today',
             download_from_internet=True, html_show=True):
    '''
    This function creates the HTML and JavaScript code for the dynamic
    visualization of the normalized peak plot of the last 15 recessions in the
    United States, from the Great Depression (Aug. 1929 - Mar. 1933) to the
    most recent COVID-19 recession (Feb. 2020 - present).

    Args:
        frwd_mths_main (int): number of months forward from the peak to plot in
            the default main window of the visualization
        bkwd_mths_maim (int): number of months backward from the peak to plot
            in the default main window of the visualization
        frwd_mths_max (int): maximum number of months forward from the peak to
            allow for the plot, to be seen by zooming out
        bkwd_mths_max (int): maximum number of months backward from the peak to
            allow for the plot, to be seen by zooming out
        djia_end_date (str): either 'today' or the end date of DJIA time series
            in 'YYYY-mm-dd' format
        download_from_internet (bool): =True if download data from Stooq.com,
            otherwise read date in from local directory
        html_show (bool): =True if open dynamic visualization in browser once
            created

    Other functions and files called by this function:
        get_djia_data()

    Files created by this function:
       images/DJIA_NPP_mth_[yyyy-mm-dd].html

    Returns: None
    '''
    # Create directory if images directory does not already exist
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    image_fldr = 'images'
    image_dir = os.path.join(cur_path, image_fldr)
    if not os.access(image_dir, os.F_OK):
        os.makedirs(image_dir)

    if djia_end_date == 'today':
        end_date = dt.date.today()  # Go through today
    else:
        end_date = dt.datetime.strptime(djia_end_date, '%Y-%m-%d')

    end_date_str = end_date.strftime('%Y-%m-%d')

    # Set main window and total data limits for monthly plot
    frwd_mths_main = int(frwd_mths_main)
    bkwd_mths_main = int(bkwd_mths_main)
    frwd_days_main = int(np.round(frwd_mths_main * 364.25 / 12))
    bkwd_days_main = int(np.round(bkwd_mths_main * 364.25 / 12))
    frwd_mths_max = int(frwd_mths_max)
    bkwd_mths_max = int(bkwd_mths_max)
    frwd_days_max = int(np.round(frwd_mths_max * 364.25 / 12))
    bkwd_days_max = int(np.round(bkwd_mths_max * 364.25 / 12))

    (djia_close_pk, end_date_str2, peak_vals, peak_dates, rec_label_yr_lst,
        rec_label_yrmth_lst, rec_beg_yrmth_lst, maxdate_rng_lst) = \
        get_djia_data(frwd_days_max, bkwd_days_max, end_date_str,
                      download_from_internet)
    if end_date_str2 != end_date_str:
        print('Updated end_date_str to ' + end_date_str2 + ' because ' +
              'original end_date_str ' + end_date_str + ' data was not ' +
              'available from Stooq.com')
        end_date_str = end_date_str2
        end_date = dt.datetime.strptime(end_date_str, '%Y-%m-%d')

    rec_cds_list = []
    min_main_val_lst = []
    max_main_val_lst = []
    for i in range(15):
        djia_close_pk_rec = \
            djia_close_pk[['days_frm_peak', f'Date{i}', f'Close{i}',
                           f'close_dv_pk{i}']].dropna()
        djia_close_pk_rec.rename(
                columns={f'Date{i}': 'Date', f'Close{i}': 'Close',
                         f'close_dv_pk{i}': 'close_dv_pk'}, inplace=True)
        rec_cds_list.append(ColumnDataSource(djia_close_pk_rec))
        # Find minimum and maximum close_dv_pk values as inputs to main plot
        # frame size
        min_main_val_lst.append(
            djia_close_pk_rec['close_dv_pk'][
                (djia_close_pk_rec['days_frm_peak'] >= -bkwd_days_main) &
                (djia_close_pk_rec['days_frm_peak'] <= frwd_days_main)].min())
        max_main_val_lst.append(
            djia_close_pk_rec['close_dv_pk'][
                (djia_close_pk_rec['days_frm_peak'] >= -bkwd_days_main) &
                (djia_close_pk_rec['days_frm_peak'] <= frwd_days_main)].max())

    # Create Bokeh plot of DJIA normalized peak plot figure
    fig_title = 'Progression of DJIA in last 15 recessions'
    filename = ('images/DJIA_NPP_mth_' + end_date_str + '.html')
    output_file(filename, title=fig_title)

    # Format the tooltip
    tooltips = [('Date', '@Date{%F}'),
                ('Days from peak', '$x{0.}'),
                ('Closing value', '@Close{0,0.00}'),
                ('Fraction of peak', '@close_dv_pk{0.0 %}')]

    # Solve for minimum and maximum DJIA/Peak values in monthly main display
    # window in order to set the appropriate xrange and yrange
    min_main_val = min(min_main_val_lst)
    max_main_val = max(max_main_val_lst)

    datarange_main_vals = max_main_val - min_main_val
    datarange_main_days = int(np.round((frwd_mths_main + bkwd_mths_main) *
                                       364.25 / 12))
    fig_buffer_pct = 0.07
    fig = figure(plot_height=450,
                 plot_width=800,
                 x_axis_label='Months from Peak',
                 y_axis_label='DJIA as fraction of Peak',
                 y_range=(min_main_val - fig_buffer_pct * datarange_main_vals,
                          max_main_val + fig_buffer_pct * datarange_main_vals),
                 x_range=((-np.round(bkwd_mths_main * 364.25 / 12) -
                          fig_buffer_pct * datarange_main_days),
                          (np.round(frwd_mths_main * 364.25 / 12) +
                          fig_buffer_pct * datarange_main_days)),
                 tools=['save', 'zoom_in', 'zoom_out', 'box_zoom',
                        'pan', 'undo', 'redo', 'reset', 'hover', 'help'],
                 toolbar_location='left')
    fig.title.text_font_size = '18pt'
    fig.toolbar.logo = None
    l0 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[0],
                  color='blue', line_width=5, alpha=0.7, muted_alpha=0.15)
    l1 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[1],
                  color=Category20[13][0], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l2 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[2],
                  color=Category20[13][1], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l3 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[3],
                  color=Category20[13][2], line_width=2,
                  alpha=0.7, muted_alpha=0.15)
    l4 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[4],
                  color=Category20[13][3], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l5 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[5],
                  color=Category20[13][4], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l6 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[6],
                  color=Category20[13][5], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l7 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[7],
                  color=Category20[13][6], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l8 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[8],
                  color=Category20[13][7], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l9 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[9],
                  color=Category20[13][8], line_width=2, alpha=0.7,
                  muted_alpha=0.15)
    l10 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[10],
                   color=Category20[13][9], line_width=2, alpha=0.7,
                   muted_alpha=0.15)
    l11 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[11],
                   color=Category20[13][10], line_width=2, alpha=0.7,
                   muted_alpha=0.15)
    l12 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[12],
                   color=Category20[13][11], line_width=2, alpha=0.7,
                   muted_alpha=0.15)
    l13 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[13],
                   color=Category20[13][12], line_width=2, alpha=0.7,
                   muted_alpha=0.15)
    l14 = fig.line(x='days_frm_peak', y='close_dv_pk', source=rec_cds_list[14],
                   color='black', line_width=5, alpha=0.7, muted_alpha=0.15)

    # Dashed vertical line at the peak DJIA value period
    fig.line(x=[0.0, 0.0], y=[-0.5, 2.0], color='black', line_width=2,
             line_dash='dashed', alpha=0.5)

    # Dashed horizontal line at DJIA as fraction of peak equals 1
    fig.line(x=[-np.round(bkwd_mths_max * 364.25 / 12),
                np.round(frwd_mths_max * 364.25 / 12)], y=[1.0, 1.0],
             color='black', line_width=2, line_dash='dashed', alpha=0.5)

    # Create the tick marks for the x-axis and set x-axis labels
    days_frm_pk_mth = []
    mths_frm_pk = []
    for i in range(-bkwd_mths_max, frwd_mths_max + 1):
        days_frm_pk_mth.append(int(np.round(i * 364.25 / 12)))
        if i < 0:
            mths_frm_pk.append(str(i) + 'mth')
        elif i == 0:
            mths_frm_pk.append('peak')
        elif i > 0:
            mths_frm_pk.append('+' + str(i) + 'mth')

    mth_label_dict = dict(zip(days_frm_pk_mth, mths_frm_pk))
    fig.xaxis.ticker = days_frm_pk_mth
    fig.xaxis.major_label_overrides = mth_label_dict

    # Add legend
    legend = Legend(items=[(rec_label_yrmth_lst[0], [l0]),
                           (rec_label_yrmth_lst[1], [l1]),
                           (rec_label_yrmth_lst[2], [l2]),
                           (rec_label_yrmth_lst[3], [l3]),
                           (rec_label_yrmth_lst[4], [l4]),
                           (rec_label_yrmth_lst[5], [l5]),
                           (rec_label_yrmth_lst[6], [l6]),
                           (rec_label_yrmth_lst[7], [l7]),
                           (rec_label_yrmth_lst[8], [l8]),
                           (rec_label_yrmth_lst[9], [l9]),
                           (rec_label_yrmth_lst[10], [l10]),
                           (rec_label_yrmth_lst[11], [l11]),
                           (rec_label_yrmth_lst[12], [l12]),
                           (rec_label_yrmth_lst[13], [l13]),
                           (rec_label_yrmth_lst[14], [l14])],
                    location='center')
    fig.add_layout(legend, 'right')

    # # Add label to current recession low point
    # fig.text(x=[12, 12, 12, 12], y=[0.63, 0.60, 0.57, 0.54],
    #          text=['2020-03-23', 'DJIA: 18,591.93', '63.3% of peak',
    #                '39 days from peak'],
    #          text_font_size='8pt', angle=0)

    # label_text = ('Recent low \n 2020-03-23 \n DJIA: 18,591.93 \n '
    #               '63\% of peak \n 39 days from peak')
    # fig.add_layout(Label(x=10, y=0.65, x_units='screen', text=label_text,
    #                      render_mode='css', border_line_color='black',
    #                      border_line_alpha=1.0,
    #                      background_fill_color='white',
    #                      background_fill_alpha=1.0))

    # Add title and subtitle to the plot
    fig.add_layout(Title(text=fig_title, text_font_style='bold',
                         text_font_size='16pt', align='center'), 'above')

    # Add source text below figure
    updated_date_str = end_date.strftime('%B %-d, %Y')
    fig.add_layout(Title(text='Source: Richard W. Evans (@RickEcon), ' +
                              'historical DJIA data from Stooq.com, ' +
                              'updated ' + updated_date_str + '.',
                         align='left',
                         text_font_size='3mm',
                         text_font_style='italic'),
                   'below')
    fig.legend.click_policy = 'mute'

    # Add the HoverTool to the figure
    fig.add_tools(HoverTool(tooltips=tooltips, toggleable=False,
                            formatters={'@Date': 'datetime'}))

    if html_show:
        show(fig)

    return fig, end_date_str


if __name__ == '__main__':
    # execute only if run as a script
    fig, end_date_str = djia_npp()
