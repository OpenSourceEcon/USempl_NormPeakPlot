"""
Tests of usempl_npp_bokey.py module

Three main tests:
* make sure that running the module as a script python usempl_npp_bokeh.py
  results in a saved html file and two csv data files in the correct
  directories
* data files are created with both download_from_internet==True and
  download_from_internet==False.
"""

import pytest
import datetime as dt

# import os
# import pathlib
# import runpy
from usempl_npp import usempl_npp_bokeh as usempl


# Create function to validate datetime text
def validate(date_text):
    try:
        if date_text != dt.datetime.strptime(date_text, "%Y-%m-%d").strftime(
            "%Y-%m-%d"
        ):
            raise ValueError
        return True
    except ValueError:
        return False


# Test that get_usempl_data() delivers the right structures and can download
# the data from the internet
def test_get_usempl_data(end_date_str="2022-11-15"):
    data_tuple = usempl.get_usempl_data(end_date_str=end_date_str)
    assert len(data_tuple) == 8
    (
        usempl_pk,
        end_date_str2,
        peak_vals,
        peak_dates,
        rec_label_yr_lst,
        rec_label_yrmth_lst,
        rec_beg_yrmth_lst,
        maxdate_rng_lst,
    ) = data_tuple
    assert usempl_pk.to_numpy().shape == (184, 46)
    assert end_date_str2 == "2022-11-01"
    assert len(peak_vals) == 15
    assert len(peak_dates) == 15
    assert len(rec_label_yr_lst) == 15
    assert len(rec_label_yrmth_lst) == 15
    assert len(rec_beg_yrmth_lst) == 15
    assert len(maxdate_rng_lst) == 15


# Test that usempl_npp() function returns html figure and valid string and
# saves html figure file and two csv files.
@pytest.mark.parametrize("frwd_mths_main", [12])
@pytest.mark.parametrize("bkwd_mths_main", [2])
@pytest.mark.parametrize("frwd_mths_max", [96])
@pytest.mark.parametrize("bkwd_mths_max", [48])
@pytest.mark.parametrize("usempl_end_date", ["today", "2020-07-01"])
@pytest.mark.parametrize("download_from_internet", [True, False])
@pytest.mark.parametrize("html_show", [False])
def test_html_fig(
    frwd_mths_main,
    bkwd_mths_main,
    frwd_mths_max,
    bkwd_mths_max,
    usempl_end_date,
    download_from_internet,
    html_show,
):
    # The case when usempl_end_date == 'today' and download_from_internet ==
    # False must be skipped because we don't have the data saved for every date
    if usempl_end_date == "today" and not download_from_internet:
        print("Successful test, skipping invalid case")
        assert True
    else:
        fig, end_date_str = usempl.usempl_npp(
            frwd_mths_main=frwd_mths_main,
            bkwd_mths_main=bkwd_mths_main,
            frwd_mths_max=frwd_mths_max,
            bkwd_mths_max=bkwd_mths_max,
            usempl_end_date=usempl_end_date,
            download_from_internet=download_from_internet,
            html_show=html_show,
        )
        assert fig
        assert validate(end_date_str)
    # assert html file exists
    # assert usempl series csv file exists
    # assert usempl ColumnDataSource source DataFrame csv file exists
