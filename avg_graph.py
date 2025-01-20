import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Load the spreadsheet
def process_spreadsheet():
    # Open a file dialog to select the spreadsheet
    Tk().withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(title="Select an Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_path:
        print("No file selected. Exiting program.")
        return

    # Read the data
    df = pd.read_excel(file_path, sheet_name='junseong_spatial')

    # Convert the Time column to datetime format
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

    # Calculate elapsed time in minutes from the first timestamp
    start_time = df['Time'].iloc[0]
    df['Elapsed_Minutes'] = (df['Time'] - start_time).dt.total_seconds() / 60

    # Calculate the average LF/HF for each phase
    phase_averages = df.groupby('Phase')['LF/HF'].mean()

    print("Average LF/HF per Phase:")
    print(phase_averages)

    # Plot the time series
    plt.figure(figsize=(10, 6))
    
    for phase, phase_data in df.groupby('Phase'):
        plt.plot(phase_data['Elapsed_Minutes'], phase_data['LF/HF'], label=f'Phase {phase}')

    # Customize the plot
    plt.title('LF/HF Ratio Over Time by Phase')
    plt.xlabel('Time (minutes)')
    plt.ylabel('LF/HF Values')
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig('LFHF_TimeSeries.png')
    plt.show()

# Run the program
process_spreadsheet()
