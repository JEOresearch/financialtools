import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from tkinter import filedialog
from tkinter import Tk

def calculate_cagr(end_value, start_value, periods):
    cagr = (end_value / start_value) ** (1/periods) - 1
    if np.isnan(cagr):
        print(f"Invalid CAGR calculation: end_value={end_value}, start_value={start_value}, periods={periods}")
    return cagr

def select_file():
    root = Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename

def plot_trend_data(data_file, position, num_future_years=10, trading_days_per_year=260):
    # Read in the CSV file
    data = pd.read_csv(data_file)

    # Convert the 'Date' column to a datetime object, handling different formats dynamically
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Automatically infer the date format

    # Drop rows with invalid dates
    data = data[data['Date'].notna()].reset_index(drop=True)

    # Ensure data is sorted in ascending order by date
    if not data['Date'].is_monotonic_increasing:
        data = data.sort_values('Date').reset_index(drop=True)

    # Now use the 'Date' column directly for further operations
    date_col = data['Date']


    # Extract the fifth column
    col_data = data.iloc[:, 4]
    # Convert the data to a numeric type after removing any $ symbols if necessary
    if col_data.dtype == 'object':  # Check if the column is of type object (likely string)
        col_data = col_data.str.replace('$', '', regex=False)  # Remove $ if present
    col_data = pd.to_numeric(col_data)  # Convert to numeric regardless of the initial format


    # Calculate the max, min and average values for the last 1000 data points
    last_series = col_data[-1000:]
    max_val, min_val, average_val = np.max(last_series), np.min(last_series), (np.max(last_series) + np.min(last_series)) / 2

    # Prepare the x-axis for plotting the trendlines with extended future points
    num_future_points = num_future_years * trading_days_per_year
    x_extended = np.arange(len(col_data) + num_future_points)

    # Calculate the trendlines
    trendlines = {}
    cagr = {}  # Stores the Compound Annual Growth Rate for each scenario
    for label, value in [('good', max_val), ('poor', min_val), ('average', average_val)]:
        exponent = (np.log(value) - np.log(col_data.iloc[0])) / (len(col_data) - 1)
        trendline = [col_data.iloc[0]]
        for i in range(1, len(x_extended)):
            trendline.append(trendline[-1] * (1 + exponent))
        trendlines[label] = trendline
        if label == 'average':
            cagr[label] = calculate_cagr(trendline[-1], col_data.iloc[0], len(col_data)/trading_days_per_year + num_future_years)
            #cagr_text = ax.text(len(x_extended), trendline[-1], f"CAGR: {cagr[label]*100:.2f}%", color='blue', fontsize=9, ha='right', va='bottom')

    # Create a new figure and plot the curves
    fig, ax = plt.subplots()
    cagr['average'] = calculate_cagr(trendlines['average'][-1], col_data.iloc[-1], num_future_years)
    cagr_text = ax.text(len(x_extended)-1, trendlines['average'][-1], f"Compounded Growth: {cagr['average']*100:.2f}%", color='blue', fontsize=12, ha='right', va='bottom')

    colors = {'good': 'green', 'poor': 'red', 'average': 'blue'}
    for label, trendline in trendlines.items():
        ax.plot(x_extended, trendline, label=f'Long term trend in {label} case', color=colors[label], alpha=0.3)

    # Extract the filename without extension for use as the plot title
    file_title = os.path.splitext(os.path.basename(data_file))[0]

    # Plot the data
    ax.plot(col_data, linewidth=.5, label=file_title, color='black')

    # Add vertical lines for each year
    for x_val in np.arange(0, len(x_extended), 260):
        ax.axvline(x_val, color='gray', linewidth=0.5, linestyle='--', alpha=0.3)

    # Set x-axis label and tick properties
    ax.set_xlabel('Date')
    ax.set_xticks(np.arange(0, len(x_extended), 260))
    ax.tick_params(axis='x', which='major', labelsize=1.0 * ax.xaxis.get_ticklabels()[0].get_size())

    # Add "click to adjust" text to the blue line
    last_data_x = len(col_data) - 1
    last_data_y = trendlines['average'][last_data_x]
    ax.annotate('click to adjust', xy=(last_data_x, last_data_y), xycoords='data',
            fontsize=12, color='blue', ha='center', va='center', alpha=0.4)

    # Prepare x-axis labels with only the year
    date_ticks = date_col.iloc[np.arange(0, len(col_data), 260)].dt.year.astype(str)
    last_valid_date = date_col.dropna().iloc[-1]
    date_ticks_extended = pd.concat([date_ticks, pd.Series([(last_valid_date + pd.DateOffset(months=i * 12)).strftime('%Y') for i in range(0, num_future_years)])]).reset_index(drop=True)
    ax.set_xticklabels(date_ticks_extended, rotation=45, ha='right')

    # Set y-axis label and plot title
    ax.set_ylabel('Price')
    ax.set_title(file_title)

    # Add a legend to the plot
    ax.legend()

    # Allow moving the average trendline by selecting a point on the plot
    def onclick(event):
        if event.inaxes == ax:
            x_val = event.xdata  # The x-coordinate of the click
            y_val = event.ydata  # The y-coordinate of the click
            if x_val is not None and y_val is not None:
                # Calculate the exponent that would make the line pass through the clicked point
                exponent = (np.log(y_val) - np.log(col_data.iloc[0])) / x_val
                # Generate new values for the average trendline passing through the clicked point
                trendlines['average'] = [col_data.iloc[0] * np.exp(exponent * i) for i in range(len(x_extended))]
                ax.lines[2].set_ydata(trendlines['average'])  # Update the trendline in the plot
                # Update the CAGR display
                cagr['average'] = calculate_cagr(trendlines['average'][-1], col_data.iloc[-1], num_future_years)
                cagr_text.set_text(f"Compounded Growth: {cagr['average']*100:.2f}%")
                cagr_text.set_position((len(x_extended)-1, trendlines['average'][-1]))
                fig.canvas.draw()  # Refresh the plot with the new trendline


    # Connect the onclick function to the figure
    fig.canvas.mpl_connect('button_press_event', onclick)

    # Show the plot
    plt.show(block=False)


# Plot the data from the first file in one window
data_file_path = select_file()
plot_trend_data(data_file_path, position=None)

# Keep the plot window open
plt.pause(0.1)
plt.show()
