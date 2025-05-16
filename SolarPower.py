import pandas as pd

# Load the dataset
inverter = pd.read_csv(r"C:\Users\User\Downloads\Project\Data Set (1)\Inverter dataset.csv")
inverter

# Display the first few rows and column names to understand the structure
inverter.head(), inverter.columns

# Set the second row as the header and remove the first row
inverter.columns = inverter.iloc[1]
inverter = inverter[2:].reset_index(drop=True)

# Rename the columns
inverter.columns = ['Date_Time', 'UNIT1_INV1', 'UNIT1_INV2', 'UNIT2_INV1', 'UNIT2_INV2']


# Convert 'Date_Time' column to datetime format
inverter['Date_Time'] = pd.to_datetime(inverter['Date_Time'], format='%d-%m-%Y %H:%M', errors='coerce')

# Reformat the datetime column to 'YYYY-MM-DD-HH-MM' format
inverter['Date_Time'] = inverter['Date_Time'].dt.strftime('%Y-%m-%d-%H-%M')

# --------------------------------- WMS_dataset ----------------------------------------
# Load the dataset from an Excel file
WMS_dataset = pd.read_excel(r"C:\Users\User\Downloads\Project\Data Set (1)\WMS_Report.xlsx")

# Convert 'DATE_TIME' column to datetime format
WMS_dataset['DATE_TIME'] = pd.to_datetime(WMS_dataset['DATE_TIME'], format='%d-%m-%Y %H:%M', errors='coerce')

# Reformat the 'DATE_TIME' column to 'YYYY-MM-DD-HH-MM' format
WMS_dataset['DATE_TIME'] = WMS_dataset['DATE_TIME'].dt.strftime('%Y-%m-%d-%H-%M')

# Display the cleaned dataset
WMS_dataset

# ---------------------------------- Merge the datasets -----------------------------------------
# Merge the datasets on the datetime column
merged_dataset = pd.merge(inverter, WMS_dataset, left_on='Date_Time', right_on='DATE_TIME', how='inner')

# Drop the duplicate datetime column
merged_dataset.drop(columns=['DATE_TIME'], inplace=True)


# --------------------------- Compute summary statistics ---------------------------
# Importing kurtosis and skewness from scipy.stats
from scipy.stats import kurtosis, skew

# Select numerical columns
numerical_columns = merged_dataset.select_dtypes(include=['number'])

 
stats_summary = {
    "Mean": numerical_columns.mean(),
    "Median": numerical_columns.median(),
    "Standard Deviation": numerical_columns.std(),
    "Variance": numerical_columns.var(),
    "Range": numerical_columns.max() - numerical_columns.min(),
    "Skewness": numerical_columns.apply(skew),
    "Kurtosis": numerical_columns.apply(kurtosis)
}

# Converting dictionary to DataFrame
stats_summary_df = pd.DataFrame(stats_summary)


# Display Summary Statistics
print(stats_summary_df)


# ------------------------ Checking Datatypes------------------------

# Displaying the data types of each column in the DataFrame
merged_dataset.dtypes 
merged_dataset.info()

# ------------------------ Checking for Duplicate Rows ------------------------

# Finding all duplicate rows in the DataFrame
duplicate = merged_dataset.duplicated(keep=False)
duplicate
sum(duplicate)

# ------------------------ Checking for Missing Values ------------------------

# Detecting missing values in each column
merged_dataset.isnull().sum()

# ------------------------ Data Type Conversions ------------------------
# Convert 'Date_Time' column to datetime format
merged_dataset['Date_Time'] = pd.to_datetime(merged_dataset['Date_Time'], format="%Y-%m-%d-%H-%M")

# Convert UNIT columns to numeric (if they contain numbers)
unit_columns = ['UNIT1_INV1', 'UNIT1_INV2', 'UNIT2_INV1', 'UNIT2_INV2']
merged_dataset[unit_columns] = merged_dataset[unit_columns].apply(pd.to_numeric, errors='coerce')

# Verify the changes
print(merged_dataset.dtypes)

#------------------------  Excel file data  -----------------------
# Save the data to an Excel file
output_file_path = r"C:\Users\User\Downloads\Project\Data Set (1)\Merged_dataset.xlsx" # Specify your desired path and filename
merged_dataset.to_excel(output_file_path, index=False)

merged_dataset.columns = merged_dataset.columns.str.strip().str.upper()  # Convert to uppercase and remove spaces
print(merged_dataset.columns)  # Verify column names
#--------------------------------------------------------------------------------------------------------------
merged_dataset.dtypes


#------------------------ Univariate Analysis ------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# Histograms for numerical columns
merged_dataset.hist(figsize=(12, 8), bins=30)
plt.suptitle("Univariate Analysis - Histograms", fontsize=14)
plt.show()

# Boxplots for numerical columns
plt.figure(figsize=(12, 6))
sns.boxplot(data=merged_dataset)
plt.title("Univariate Analysis - Boxplots")
plt.xticks(rotation=90)
plt.show()


# ---------------- Bivariate Analysis ----------------
# Scatterplot between two numerical variables
plt.figure(figsize=(8, 5))
sns.scatterplot(x=merged_dataset.columns[1], y=merged_dataset.columns[2], data=merged_dataset)
plt.title("Bivariate Analysis - Scatterplot")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(merged_dataset.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Bivariate Analysis - Correlation Heatmap")
plt.show()

# ---------------- Multivariate Analysis ----------------
# Pairplot (Scatterplots and Histograms together)
sns.pairplot(merged_dataset)
plt.suptitle("Multivariate Analysis - Pairplot", y=1.02)
plt.show()  



#------------------------ Replace outliers ------------------------
# Function to replace outliers using IQR method
def replace_outliers_iqr(merged_dataset, column):
    Q1 = merged_dataset[column].quantile(0.25)
    Q3 = merged_dataset[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Replace outliers with median (simplified)
    merged_dataset[column] = merged_dataset[column].mask((merged_dataset[column] < lower_bound) | (merged_dataset[column] > upper_bound), merged_dataset[column].median())

# Apply function to both columns
replace_outliers_iqr(merged_dataset, "MODULE_TEMP_1")
replace_outliers_iqr(merged_dataset, "RAIN")

#Boxplot Visualization After Outlier Treatment
plt.figure(figsize=(12, 6))
sns.boxplot(data=merged_dataset[["MODULE_TEMP_1","RAIN"]])
plt.title("Boxplot After Outlier Treatment")
plt.show()

#------------------------ connection to SQL -----------------------
from sqlalchemy import create_engine ,text
from urllib.parse import quote
import pymysql

merged_dataset.columns = merged_dataset.columns.str.strip()
user = 'root'
pw = 'Shruti2324'
db = 'solarPower'
engine = create_engine(f"mysql+pymysql://{user}:%s@localhost/{db}" % quote(f'{pw}'))
merged_dataset.to_sql('merged_dataset',con = engine,if_exists = 'replace',chunksize = None,index = False)
























