import pandas as pd
from tkinter import Tk, filedialog

# Load and process multiple spreadsheets
def process_spreadsheets_and_save_averages_by_phase():
    # Open a file dialog to select multiple spreadsheets
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    root.attributes('-topmost', True)  # Bring the file dialog to the front

    file_paths = filedialog.askopenfilenames(
        title="Select Excel Files",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    root.destroy()  # Destroy the Tkinter root window after selection

    if not file_paths:
        print("No files selected. Exiting program.")
        return

    results = []  # To store the average values for each file

    for file_path in file_paths:
        print(f"Processing file: {file_path}")

        # Read the first sheet of the Excel file
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"Error reading Excel file '{file_path}': {e}")
            continue

        # Ensure required columns are present
        required_columns = {'Phase', 'LF/HF'}
        if not required_columns.issubset(df.columns):
            print(f"The spreadsheet '{file_path}' must contain the following columns: {', '.join(required_columns)}")
            continue

        # Calculate the average LF/HF for each phase
        phase_averages = df.groupby('Phase')['LF/HF'].mean()

        # Append averages for this file to results
        file_name = file_path.split("/")[-1]  # Extract file name
        result_entry = {"File name": file_name}
        result_entry.update(phase_averages.to_dict())
        results.append(result_entry)

    # Save the averages to a new Excel file
    if results:
        output_df = pd.DataFrame(results).fillna(0)  # Fill missing phases with 0
        output_file = "averages_by_phase_output.xlsx"
        output_df.to_excel(output_file, index=False)
        print(f"Averages by phase saved to '{output_file}'.")
    else:
        print("No valid data to save.")

# Run the program
process_spreadsheets_and_save_averages_by_phase()
