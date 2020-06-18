'''
Tests of djia_npp_bokey.py module

Three main tests:
* make sure that running the module as a script python djia_npp_bokey.py
  results in a saved html file and two csv data files in the correct
  directories
* data files are created with both download_from_internet==True and
  download_from_internet==False.
'''

import pytest
import datetime as dt
# import os
# import pathlib
# import runpy
import djia_npp_bokeh as djia


# Create function to validate datetime text


def validate(date_text):
    try:
        if date_text != dt.datetime.strptime(
                            date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


# Test whether running the script of the module results in an html figure and
# two datasets
# def test_html_fig_script():
#     script = pathlib.Path(__file__, '..',
#                           'scripts').resolve().glob('djia_npp_bokeh.py')
#     runpy.run_path(script)
#     assert fig

# Test that djia_npp() function returns html figure and valid string and saves
# html figure file and two csv files.
@pytest.mark.parametrize('frwd_mths_main', [6])
@pytest.mark.parametrize('bkwd_mths_main', [1])
@pytest.mark.parametrize('frwd_mths_max', [12])
@pytest.mark.parametrize('bkwd_mths_max', [4])
@pytest.mark.parametrize('djia_end_date', ['today', '2020-06-09'])
@pytest.mark.parametrize('download_from_internet', [True, False])
@pytest.mark.parametrize('html_show', [False])
def test_html_fig(frwd_mths_main, bkwd_mths_main, frwd_mths_max, bkwd_mths_max,
                  djia_end_date, download_from_internet, html_show):
    # The case when djia_end_date == 'today' and download_from_internet ==
    # False must be skipped because we don't have the data saved for every date
    if djia_end_date == 'today' and not download_from_internet:
        pytest.skip('Invalid case')
        assert True
    else:
        fig, end_date_str = djia.djia_npp(
            frwd_mths_main=frwd_mths_main, bkwd_mths_main=bkwd_mths_main,
            frwd_mths_max=frwd_mths_max, bkwd_mths_max=bkwd_mths_max,
            djia_end_date=djia_end_date,
            download_from_internet=download_from_internet,
            html_show=html_show)
        assert fig
        assert validate(end_date_str)
    # assert html file exists
    # assert djia series csv file exists
    # assert djia ColumnDataSource source DataFrame csv file exists
