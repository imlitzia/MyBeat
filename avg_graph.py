import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog

# Load and process multiple spreadsheets
def process_spreadsheets():
    # Open a file dialog to select multiple spreadsheets
    Tk().withdraw()  # Hide the main tkinter window
    file_paths = filedialog.askopenfilenames(title="Select Excel Files", filetypes=[("Excel files", "*.xlsx *.xls")])

    if not file_paths:
        print("No files selected. Exiting program.")
        return

    # Create an output folder for saving graphs
    output_folder = "Processed_Graphs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Required columns (case insensitive)
    required_columns = {'time', 'phase', 'lf/hf'}

    for file_path in file_paths:
        try:
            print(f"Processing file: {os.path.basename(file_path)}")
            
            # Read the data (assuming the sheet name is consistent or load the first sheet)
            df = pd.read_excel(file_path)

            # Normalize column names to lowercase for case-insensitive matching
            df.columns = df.columns.str.lower()

            # Check for missing columns
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                print(f"File {os.path.basename(file_path)} is missing the following columns: {', '.join(missing_columns)}. Skipping.")
                continue

            # Rename columns to match expected capitalization
            column_mapping = {
                'time': 'Time',
                'phase': 'Phase',
                'lf/hf': 'LF/HF'
            }
            df.rename(columns=column_mapping, inplace=True)

            # Convert the Time column to datetime format
            df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')

            if df['Time'].isna().all():
                print(f"File {os.path.basename(file_path)} has invalid or missing 'Time' values. Skipping.")
                continue

            # Calculate elapsed time in minutes from the first timestamp
            start_time = df['Time'].iloc[0]
            df['Elapsed_Minutes'] = (df['Time'] - start_time).dt.total_seconds() / 60

            # Calculate the average LF/HF for each phase
            phase_averages = df.groupby('Phase')['LF/HF'].mean()

            print("Average LF/HF per Phase:")
            print(phase_averages)

            # Plot the time series
            plt.figure(figsize=(10, 6))
            legend_labels = []

            for phase, phase_data in df.groupby('Phase'):
                plt.plot(phase_data['Elapsed_Minutes'], phase_data['LF/HF'], label=f'Phase {phase}')
                legend_labels.append(f'Phase {phase} (Avg: {phase_averages[phase]:.2f})')

            # Customize the plot
            plt.title(f'LF/HF Ratio Over Time by Phase ({os.path.basename(file_path)})')
            plt.xlabel('Time (minutes)')
            plt.ylabel('LF/HF Values')
            plt.legend(legend_labels, loc='upper left')
            plt.grid(True)

            # Save the plot
            output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_graph.png")
            plt.savefig(output_file)
            plt.close()
            print(f"Saved graph: {output_file}")

        except Exception as e:
            print(f"Error processing file {os.path.basename(file_path)}: {e}")

    print("Processing completed. All graphs saved in the 'Processed_Graphs' folder.")

# Run the program
process_spreadsheets()
