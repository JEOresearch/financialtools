The purpose of this tool is to help investors determine whether a stock or index has deviated from a long term trend.

To help support this software and other open-source projects, please consider subscribing to my YouTube channel: https://www.youtube.com/@jeoresearch

TrendPlotter is a program that takes in a csv file with stock data and plots the data with long term trend lines representing a good, poor, and average case scenario. The average case (blue trend line) is adjustable by clicking on any point in the .csv data. The algorithm for fitting the line finds the compound interest rate such that if applied to the first data point will end up at the average price over the last three years in the average case or at the price occurring at the click. Similarly, the green and red (good and poort) trend lines show this tendencey for the high and low points over the last three years, respectively.  


The output should look like the graph in this video: https://youtu.be/XZvwtC5Y3QY


A sample csv file of MMM is included for reference, which was downloaded from Yahoo finance. 
***Note that Yahoo Finance no longer provides free historical data downloads. Boo.... I have updated the script to work with https://stooq.com/q/. 

Running the program will open a browse window to select the csv file. In addition, the end of the average trend line computes the 10 year compounded interest from the end of the source (csv) data to the end of the trend line.  In other words, this is the expected rate of return for the ten years of the extended trendline. 

![plot image](https://github.com/NuncObdurat/financialtools/blob/main/Stock%20Analysis/pointer.png)

Python instructions and dependencies are below the image. 

![plot image](https://github.com/NuncObdurat/financialtools/blob/main/Stock%20Analysis/MMM.png)



The TrendPlotter.py file is a Python script that requires Python and the following dependencies:

- os
- pandas
- numpy
- matplotlib
- math
- tkinter

To install dependencies, you can use the `pip` command. E.g.:

- pip install pandas
- pip install numpy
- pip install ....
