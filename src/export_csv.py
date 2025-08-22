import os

def export_to_csv(df, csv_filename):
    # Ensure the directory exists
    directory = os.path.dirname(csv_filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Export the DataFrame to CSV
    df.to_csv(csv_filename, index=False)
    print(f"Data exported to {csv_filename}")
