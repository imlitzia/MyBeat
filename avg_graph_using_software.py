import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from tkinter import Tk, filedialog


# Function to handle mouse wheel zoom
def zoom(event, ax):
    base_scale = 1.2
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    xdata = event.xdata  # Get mouse position
    ydata = event.ydata

    if xdata is None or ydata is None:
        return  # Ignore zoom if outside axes

    if event.button == 'up':  # Zoom in
        scale_factor = 1 / base_scale
    elif event.button == 'down':  # Zoom out
        scale_factor = base_scale
    else:  # Ignore other scroll events
        return

    # Adjust limits
    new_xlim = [xdata - (xdata - cur_xlim[0]) * scale_factor,
                xdata + (cur_xlim[1] - xdata) * scale_factor]
    new_ylim = [ydata - (ydata - cur_ylim[0]) * scale_factor,
                ydata + (cur_ylim[1] - ydata) * scale_factor]

    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    ax.figure.canvas.draw_idle()  # Redraw the canvas


# Load the spreadsheet
def process_spreadsheet():
    # Open a file dialog to select the spreadsheet
    Tk().withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(title="Select an Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_path:
        print("No file selected. Exiting program.")
        return

    try:
        # Read the Excel file (load the first sheet by default)
        df = pd.read_excel(file_path)

        # Normalize column names to lowercase for case-insensitive matching
        df.columns = df.columns.str.lower()

        # Required columns (case-insensitive)
        required_columns = {'time', 'phase', 'lf/hf'}

        # Check for missing required columns
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"File is missing the following required columns: {', '.join(missing_columns)}. Exiting.")
            return

        # Convert the `time` column to datetime format
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce')

        if df['time'].isna().all():
            print("The 'time' column has invalid or missing values. Exiting.")
            return

        # Calculate elapsed time in minutes from the first timestamp
        start_time = df['time'].iloc[0]
        df['elapsed_minutes'] = (df['time'] - start_time).dt.total_seconds() / 60

        # Calculate the average LF/HF for each phase
        phase_averages = df.groupby('phase')['lf/hf'].mean()

        print("Average LF/HF per Phase:")
        print(phase_averages)

        # Create the figure and axes for interactive plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        legend_labels = []
        for phase, phase_data in df.groupby('phase'):
            ax.plot(phase_data['elapsed_minutes'], phase_data['lf/hf'], label=f'Phase {phase}')
            legend_labels.append(f'Phase {phase} (Avg: {phase_averages[phase]:.2f})')

        # Customize the plot
        ax.set_title(f'LF/HF Ratio Over Time by Phase\nFile: {file_path.split("/")[-1]}')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('LF/HF Values')
        ax.legend(legend_labels, loc='upper left')
        ax.grid(True)

        # Add interactivity: enable zooming and panning
        ax.set_xlim(df['elapsed_minutes'].min(), df['elapsed_minutes'].max())
        ax.set_ylim(df['lf/hf'].min() * 0.9, df['lf/hf'].max() * 1.1)

        # Add a cursor for easier tracking
        cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

        # Connect mouse wheel event for zooming
        fig.canvas.mpl_connect('scroll_event', lambda event: zoom(event, ax))

        # Enable tight layout to handle resizing better
        plt.tight_layout()

        # Show the interactive plot
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
# Run the program
process_spreadsheet()
