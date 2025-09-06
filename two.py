import pandas as pd
import numpy as np
import os

def load_all_csv_files(folder_path):
    all_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            try:
                df = pd.read_csv(file_path)
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
    if not all_data:
        print("No CSV files found in the folder.")
        return None
    return pd.concat(all_data, ignore_index=True)

def reshape_data(df):
    month_columns = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    df_melted = pd.melt(
        df,
        id_vars=['STN_ID'],
        value_vars=month_columns,
        var_name='Month',
        value_name='Temperature'
    )
    month_map = {month: i+1 for i, month in enumerate(month_columns)}
    df_melted['Month'] = df_melted['Month'].map(month_map)
    df_melted['Temperature'] = pd.to_numeric(df_melted['Temperature'], errors='coerce')
    df_melted = df_melted.dropna(subset=['Temperature'])
    return df_melted

def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    elif month in [9, 10, 11]:
        return "Spring"
    return None

def calculate_seasonal_averages(df):
    df['Season'] = df['Month'].apply(get_season)
    seasonal_avgs = df.groupby('Season')['Temperature'].mean().round(1)
    seasons = ['Summer', 'Autumn', 'Winter', 'Spring']
    result = {season: seasonal_avgs.get(season, float('nan')) for season in seasons}
    with open("average_temp.txt", "w", encoding="utf-8") as f:
        for season in seasons:
            avg = result[season]
            if not np.isnan(avg):
                f.write(f"{season}: {avg}°C\n")
            else:
                f.write(f"{season}: No data\n")
    print("Seasonal averages written to average_temp.txt")

def find_largest_temp_range(df):
    station_stats = df.groupby('STN_ID')['Temperature'].agg(['min', 'max'])
    station_stats['Range'] = station_stats['max'] - station_stats['min']
    max_range = station_stats['Range'].max()
    max_range_stations = station_stats[station_stats['Range'] == max_range].index.tolist()
    
    with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
        for station in max_range_stations:
            max_temp = station_stats.loc[station, 'max']
            min_temp = station_stats.loc[station, 'min']
            range_val = station_stats.loc[station, 'Range']
            f.write(f"Station {station}: Range {range_val:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")
    print("Largest temperature range written to largest_temp_range_station.txt")

def find_temperature_stability(df):
    station_std = df.groupby('STN_ID')['Temperature'].std().round(1)
    min_std = station_std.min()
    max_std = station_std.max()
    most_stable = station_std[station_std == min_std].index.tolist()
    most_variable = station_std[station_std == max_std].index.tolist()
    
    with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
        f.write("Most Stable:\n")
        for station in most_stable:
            f.write(f"Station {station}: StdDev {min_std:.1f}°C\n")
        f.write("Most Variable:\n")
        for station in most_variable:
            f.write(f"Station {station}: StdDev {max_std:.1f}°C\n")
    print("Temperature stability written to temperature_stability_stations.txt")

def main():
    folder_path = "temperatures"
    df = load_all_csv_files(folder_path)
    if df is None:
        print("Exiting due to no data.")
        return
    
    df = reshape_data(df)
    if df.empty:
        print("No valid temperature data found.")
        return
    
    calculate_seasonal_averages(df)
    find_largest_temp_range(df)
    find_temperature_stability(df)

if __name__ == "__main__":
    main()