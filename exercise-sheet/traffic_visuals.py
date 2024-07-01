import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Suppress warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Ensure the directory to save the PDF files exists
output_dir = './'
os.makedirs(output_dir, exist_ok=True)

# Load Kaggle data
file_path = './database.csv'
data = pd.read_csv(file_path)

# Randomly sample 100,000 rows without replacement (we have lots of data)
data = data.sample(n=100000, random_state=1)

# Filter the data for latitude between 40 and 41 and longitude between -74 and -73.5
data = data[(data['LATITUDE'] >= 40) & (data['LATITUDE'] <= 41) &
            (data['LONGITUDE'] >= -74.5) & (data['LONGITUDE'] <= -73.5)]

# Plot daily patterns (number of accidents for each hour of the day)
data['DATE'] = pd.to_datetime(data['DATE'], format='%m/%d/%Y')
data['HOUR'] = pd.to_datetime(data['TIME'], format='%H:%M').dt.hour
plt.figure(figsize=(14, 6))
sns.histplot(data['HOUR'], bins=24, kde=False)
plt.title('Daily Pattern of Vehicle Collisions')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Collisions')
plt.xticks(ticks=range(24), labels=[f'{i:02d}:00' for i in range(24)])
plt.savefig(os.path.join(output_dir, 'daily_patterns.pdf'), format='pdf')

# Plot weekly patterns (number of accidents for each week of the year)
data['WeekOfYear'] = data['DATE'].dt.isocalendar().week
plt.figure(figsize=(14, 6))
sns.histplot(data['WeekOfYear'], bins=52, kde=False)
plt.title('Weekly Pattern of Vehicle Collisions')
plt.xlabel('Week of the Year')
plt.ylabel('Number of Collisions')
plt.savefig(os.path.join(output_dir, 'weekly_patterns.pdf'), format='pdf')

# Combine DATE and TIME into a single datetime column
data['DATETIME'] = pd.to_datetime(data['DATE'].astype(str) + ' ' + data['TIME'].astype(str))

# Filter out rows with missing latitude or longitude
spatial_data = data.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Plot spatial patterns with color indicating time
plt.figure(figsize=(10, 10))
sc = plt.scatter(spatial_data['LONGITUDE'], spatial_data['LATITUDE'], c='blue', alpha=0.05, s=4)
plt.title('Spatial Distribution of Vehicle Collisions with Time Indication')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig(os.path.join(output_dir, 'spatial_patterns.pdf'), format='pdf')
