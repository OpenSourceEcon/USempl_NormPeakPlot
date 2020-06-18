[![OSE Lab cataloged](https://img.shields.io/badge/OSE%20Lab-catalogued-critical)](https://www.oselab.org/gallery)
[![Python 3.7.4+](https://img.shields.io/badge/python-3.7.4%2B-blue.svg)](https://www.python.org/downloads/release/python-374/)
[![Build Status](https://travis-ci.org/OpenSourceEcon/USempl_NormPeakPlot.svg?branch=master)](https://travis-ci.org/OpenSourceEcon/USempl_NormPeakPlot)
[![Codecov](https://codecov.io/gh/OpenSourceEcon/USempl_NormPeakPlot/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenSourceEcon/USempl_NormPeakPlot)

# Normalized Peak Plot of U.S. Nonfarm Payroll Employment (PAYEMS)
The code in this repository allows the user to create a normalized peak plot of U.S. nonfarm payroll employment (PAYEMS) over the last 15 recessions, from the Great Depression (Aug. 1929 to Mar. 1933) to the current COVID-19 recession (Feb. 2020 to present). The dynamic version of this plot, which is updated regularly, is available to manipulate and explore at [https://www.oselab.org/gallery/usempl_npp_mth](https://www.oselab.org/gallery/usempl_npp_mth). The core maintainer of this repository is [Richard Evans](https://sites.google.com/site/rickecon/) ([@RickEcon](https://github.com/rickecon)).

A normalized peak plot takes the maximum level of U.S. payroll employment at the beginning of a recession (within two months of the NBER declared beginning month) and normalizes the entire series so that the value at that peak equals 1.0. As such, the normalized time series shows the percent change from that peak. This is an intuitive way to compare the progression of average stock prices across recessions. The following figure is a screen shot of the normalized peak plot of the PAYEMS series from ?.

<!-- ![](readme_images/DJIA_NPP_mth_full.png)

This `README.md` is organized into the following three sections.
1. [Running the code and generating the dynamic visualization](README.md#1-running-the-code-and-generating-the-dynamic-visualization)
2. [Functionality of the dynamic visualization](README.md#2-functionality-of-the-dynamic-visualization)
3. [Contributing to this visualization code](README.md#3-contributing-to-this-visualization-code)

## 1. Running the code and generating the dynamic visualization
The code for creating this visualization is written in the [Python](https://www.python.org/) programming language. It requires the following file:
* [`djia_npp_bokeh.py`](djia_npp_bokeh.py): a Python module that defines two functions in order to create the HTML and JavaScript for the dynamic visualization of the DJIA normalized peak plot of the last 15 recessions.
    * [`get_djia_data()`](djia_npp_bokeh.py#L30) takes inputs for the date ranges to plot and whether to download the data directly from [Stooq.com](https://stooq.com/) or retrieve the data from a file saved previously on your local hard drive in the [data](data/) directory of this repository. Then the function collects, cleans, and returns the DJIA data.
    * [`djia_npp()`](djia_npp_bokeh.py#L222) creates the dynamic visualization of the normalized peak plot of the DJIA over the last 15 recessions. This script calls the [`get_djia_data()`](djia_npp_bokeh.py#L30) function. It then uses the [`Bokeh`](https://bokeh.org/) library to create a dynamic visualization using HTML and JavaScript to render the visualization in a web browser.

The most standard way to successfully run this code if you are using the [Anaconda distribution](https://www.anaconda.com/products/individual) of Python is to install and activate the `djia-npp-dev` [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html) defined in the [environment.yml](environment.yml) file, then run the [`djia_npp_bokeh.py`](djia_npp_bokeh.py) module as a script with the defaults or import the [`djia_npp_bokeh.py`](djia_npp_bokeh.py) module and run the [`djia_npp()`](djia_npp_bokeh.py#L222) function using the appropriate options. Use the following steps.
1. Either fork this repository then clone it to your local hard drive or clone it directly to your local hard drive from this repository.
2. Install the [Anaconda distribution](https://www.anaconda.com/products/individual) of Python to your local machine.
3. Update `conda` and `anaconda` by opening your terminal and typing `conda update conda` and following the instructions, then typing `conda update anaconda` and following the instructions.
4. From the terminal (or Conda command prompt), navigate to the directory to which you cloned this repository and run `conda env create -f environment.yml`. This will create the conda environment with all the necessary dependencies to run the script to create the dynamic visualization.
5. Activate the conda environment by typing in your terminal `conda activate djia-npp-dev`.
6. Create the visualization in one of two ways.
    * Run the [`djia_npp_bokeh.py`](djia_npp_bokeh.py) module as a script with the default settings of the [`djia_npp()`](djia_npp_bokeh.py#L222) function. This will produce the dynamic visualization in which the data are downloaded from the internet, the end date is either the current day or the most recent day with DJIA closing data, and then the default months from peak.
    * Import the  [`djia_npp_bokeh.py`](djia_npp_bokeh.py) and execute the [`djia_npp()`](djia_npp_bokeh.py#L222) function by typing something like the following:
    ```python
    import djia_npp_bokeh as djia

    djia.djia_npp(6, 1, 12, 3, '2020-03-23')
    ```
7. Executing the function [`djia_npp()`](djia_npp_bokeh.py#L222) will result in three output objects: the dynamic visualization HTML file, the original time series of the DJIA, and the organized dataset of each recession's variables time series for the periods specified in the function inputs.
    * [**images/DJIA_NPP_mth_[YYYY-mm-dd].html**](images/DJIA_NPP_mth_2020-06-09.html). This is the dynamic visualization. The code in the file is a combination of HTML and JavaScript. You can view this visualization by opening the file in a web browser window. A version of this visualization is updated regularly on the web at [https://www.oselab.org/gallery/djia_npp_mth](https://www.oselab.org/gallery/djia_npp_mth).
    * [**data/djia_close_[YYYY-mm-dd].csv**](data/djia_close_2020-06-09.csv). A comma separated values data file of the original time series of the DJIA from 1896-05-27 to whatever end date is specified in the [`djia_npp()`](djia_npp_bokeh.py#L222) function arguments, which is also the final 10 characters of the file name `YYYY-mm-dd`.
    * [**data/djia_close_pk_[YYYY-mm-dd].csv**](data/djia_close_pk_2020-06-09.csv).

## 2. Functionality of the dynamic visualization
This dynamic visualization allows the user to customize some different views and manipulations of the data using the following functionalities. The default view of the visualization is shown above.
* Highlight or mute specific recession time series by clicking on the series label in the legend on the right side of the plot. The screen shot below shows a version of the plot in which all the recession time series have been muted except for the current COVID-19 recession and the Great Depression. Note that even when muted, the time series are still faintly visible.
![](readme_images/DJIA_NPP_mth_muted.png)
* <img src="readme_images/Hover.png" width=18 align=center> Hovertool display. If you select the hovertool button <img src="readme_images/Hover.png" width=18 align=center> on the left side of the plot, which is the default for the plot, information about each point in each time series will be displayed when you hover your cursor over a given point in the plot area. The screen shot below shows a version of the plot in which the hovertool is selected and the information about the minimum point in the current recession is displayed.
![](readme_images/DJIA_NPP_mth_hover.png)
* <img src="readme_images/Pan.png" width=18 align=center> Pan different areas of the data. If you click on the pan button <img src="readme_images/Pan.png" width=18 align=center> on the left side of the plot, you can use your cursor to click and drag on the data window and change your view of the data.
* <img src="readme_images/BoxZoom.png" width=18 align=center> <img src="readme_images/ZoomIn.png" width=18 align=center> <img src="readme_images/ZoomOut.png" width=18 align=center> Zoom in or out on the data. You can zoom in or zoom out on the data series in three different ways. You can use the box zoom functionality by clicking on its button <img src="readme_images/BoxZoom.png" width=18 align=center> on the left side of the plot and clicking and dragging a box on the area of the plot that you want to zoom in on. You can also zoom in by clicking on the zoom in button <img src="readme_images/ZoomIn.png" width=18 align=center> on the left side of the plot, then clicking on the area of the plot you want to center your zoom in around. Or you can zoom out by clicking on the zoom out button <img src="readme_images/ZoomOut.png" width=18 align=center> on the left side of the plot, then clicking on the area of the plot you want to center your zoom out around. The screen shot below shows a zoomed out version of the plot.
![](readme_images/DJIA_NPP_mth_zoomout.png)
* <img src="readme_images/Save.png" width=18 align=center> Save current view of data as .png file. You can save your current view of the data as a .png file to your local hard drive by clicking on the save button <img src="readme_images/Save.png" width=18 align=center> on the left side of the plot.
* <img src="readme_images/Undo.png" width=18 align=center> <img src="readme_images/Redo.png" width=18 align=center> Undo and redo actions. You can undo or redo any of the plot changes that you make using the undo button <img src="readme_images/Undo.png" width=18 align=center> or the redo button <img src="readme_images/Redo.png" width=18 align=center> on the left side of the plot.
* <img src="readme_images/Reset.png" width=18 align=center> Reset the plot. After any changes you make to the plot, you can reset it to its original position by using the reset button <img src="readme_images/Reset.png" width=18 align=center> on the left side of the plot.

## 3. Contributing to this visualization code
If you wish to improve or enhance this code or if you find errors or bugs, please consider the following ways to contribute to this project.
* Browse the repository [Issues](issues) for known areas that need attention.
* Submit questions or suggestions by submitting a new issue in the repository [Issues](issues).
* Submit a pull request with your proposed changes. -->
