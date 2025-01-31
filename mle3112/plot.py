"""
Author: Zeyu Deng
Email: dengzeyu@gmail.com
"""
import matplotlib.pyplot as plt
import pandas as pd
import ast
import numpy as np

def plot():
    """
    Reads data from 'data.csv', processes it, and generates plots.
    The function performs the following steps:
    1. Reads data from 'data.csv' into a pandas DataFrame.
    2. Converts the 'data' and 'wavelength' columns from string representations of lists to actual lists.
    3. Integrates the 'data' over the 'wavelength' for each row using the trapezoidal rule.
    4. Prints the DataFrame with the integrated data.
    5. Creates and saves a plot of 'position' vs 'integrated' data.
    6. For each unique position, creates and saves a plot of 'wavelength' vs 'data'.
    The generated plots are saved as 'integrated.png' and 'spectrum_position_<pos>.png' where <pos> is the position value.
    Note:
    - The 'data.csv' file should have columns: 'position', 'data', and 'wavelength'.
    - The 'data' and 'wavelength' columns should contain string representations of lists.
    Returns:
    None
    """
    # read data
    df = pd.read_csv('data.csv', index_col=0)
    df['data'] = df['data'].apply(lambda x: ast.literal_eval(x))
    df['wavelength'] = df['wavelength'].apply(lambda x: ast.literal_eval(x))
    # integrate wavelength 
    df['integrated'] = df.apply(lambda row: np.trapz(y=row['data'], x=row['wavelength']), axis=1)
    print(df)
    
    # Create the plot
    plt.figure(figsize=(5, 5))
    plt.plot(df['position'], df['integrated'], 'o-', markersize=8, linewidth=2, label='Integrated Data')
    
    # Customize the plot
    plt.xlabel('Position (degrees)', fontsize=14)
    plt.ylabel('Integrated Data (a.u.)', fontsize=14)
    plt.title('Position vs Integrated Data', fontsize=16)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('integrated.png', dpi=300)
    # Plot the spectrum for a few positions
    positions_to_plot = df['position'].unique()  # Plot all unique positions

    for pos in positions_to_plot:
        df_pos = df[df['position'] == pos]
        if not df_pos.empty:
            plt.figure(figsize=(5, 5))
            for index, row in df_pos.iterrows():
                plt.plot(row['wavelength'], row['data'], label=f'Position {row["position"]} degrees')
            
            plt.xlabel('Wavelength (nm)', fontsize=14)
            plt.ylabel('Intensity (a.u.)', fontsize=14)
            plt.title(f'Spectrum at Position {pos} degrees', fontsize=16)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(f'spectrum_position_{pos}.png', dpi=300)
            plt.close()
    
def plot_three_filters():
    """
    Reads data from 'data_three_filters.csv', processes it, and generates plots.
    The function performs the following steps:
    1. Reads the CSV file 'data_three_filters.csv' into a DataFrame.
    2. Converts the 'data' and 'wavelength' columns from string representations of lists to actual lists.
    3. Integrates the 'data' over the 'wavelength' for each row and stores the result in a new column 'integrated'.
    4. Creates a plot of 'position3' vs 'integrated' for unique combinations of 'position1' and 'position2'.
    5. Customizes the plot with labels, title, grid, and legend.
    6. Saves the plot as 'integrated_three_filters.png'.
    7. For a few unique positions, plots the spectrum (wavelength vs data) and saves each plot as 'spectrum_positions_<pos1>_<pos2>_<pos3>.png'.
    The CSV file is expected to have the following columns:
    - 'position1': Position 1 values (degrees)
    - 'position2': Position 2 values (degrees)
    - 'position3': Position 3 values (degrees)
    - 'data': String representation of a list of intensity values
    - 'wavelength': String representation of a list of wavelength values
    The function saves the generated plots as PNG files in the current working directory.
    """
    df_three_filters = pd.read_csv('data_three_filters.csv', index_col=0)
    df_three_filters['data'] = df_three_filters['data'].apply(lambda x: ast.literal_eval(x))
    df_three_filters['wavelength'] = df_three_filters['wavelength'].apply(lambda x: ast.literal_eval(x))
    # integrate wavelength 
    df_three_filters['integrated'] = df_three_filters.apply(lambda row: np.trapz(y=row['data'], x=row['wavelength']), axis=1)
    print(df_three_filters)
    
    # Create the plot
    plt.figure(figsize=(5, 5))
    for pos1 in df_three_filters['position1'].unique():
        for pos2 in df_three_filters['position2'].unique():
            df_pos = df_three_filters[(df_three_filters['position1'] == pos1) & (df_three_filters['position2'] == pos2)]
            if not df_pos.empty:
                plt.plot(df_pos['position3'], df_pos['integrated'], 'o-', markersize=8, linewidth=2, label=f'Pos1: {pos1}, Pos2: {pos2}')
    
    # Customize the plot
    plt.xlabel('Position 3 (degrees)', fontsize=14)
    plt.ylabel('Integrated Data (a.u.)', fontsize=14)
    plt.title('Position 3 vs Integrated Data', fontsize=16)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('integrated_three_filters.png', dpi=300)
    
    # Plot the spectrum for a few positions
    positions_to_plot = df_three_filters[['position1', 'position2', 'position3']].drop_duplicates()

    for _, pos in positions_to_plot.iterrows():
        df_pos = df_three_filters[(df_three_filters['position1'] == pos['position1']) & 
                                  (df_three_filters['position2'] == pos['position2']) & 
                                  (df_three_filters['position3'] == pos['position3'])]
        if not df_pos.empty:
            plt.figure(figsize=(5, 5))
            for index, row in df_pos.iterrows():
                plt.plot(row['wavelength'], row['data'], label=f'Pos1: {row["position1"]}, Pos2: {row["position2"]}, Pos3: {row["position3"]}')
            
            plt.xlabel('Wavelength (nm)', fontsize=14)
            plt.ylabel('Intensity (a.u.)', fontsize=14)
            plt.title(f'Spectrum at Positions {pos["position1"]}, {pos["position2"]}, {pos["position3"]} degrees', fontsize=16)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(f'spectrum_positions_{pos["position1"]}_{pos["position2"]}_{pos["position3"]}.png', dpi=300)
            plt.close()
