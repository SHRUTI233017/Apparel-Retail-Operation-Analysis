# -------------------------- 1. Import Libraries --------------------------
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------- 2. Load Dataset --------------------------
df = pd.read_csv(r"C:\Users\User\Downloads\Power Bi project\dataset\dataset.csv")

#-------------------------- 3. Basic Info--------------------------
print(df.describe())            # Summary statistics
print(df.info())                # Data types and null counts
print(df.dtypes)                # Data types
print(df.isnull().sum())        # Count of missing values
print(df.duplicated().sum())    # Count of duplicate rows

# -------------------------- 6. Clean & Convert Data --------------------------
# Remove commas and convert to numeric
df['Ctn Qty'] = df['Ctn Qty'].str.replace(',', '', regex=False).astype(float)
df['Dlv Qty'] = df['Dlv Qty'].str.replace(',', '', regex=False).astype(float)

# Convert date columns to datetime
df['Ctn Dt'] = pd.to_datetime(df['Ctn Dt'], errors='coerce')
df['Ship Dt'] = pd.to_datetime(df['Ship Dt'], errors='coerce')
df['Contrct Dt'] = pd.to_datetime(df['Contrct Dt'], errors='coerce')
df['Dlv Dt'] = pd.to_datetime(df['Dlv Dt'], errors='coerce')

# -------------------------- 4. Drop Duplicates & Remaining Nulls--------------------------
df.drop_duplicates(inplace=True)
df.dropna(inplace=True) 

# -------------------------- 5. Fill Missing Dates with Median --------------------------
df['Dlv Dt'].fillna(df['Dlv Dt'].median(), inplace=True)
df['Ship Dt'].fillna(df['Ship Dt'].median(), inplace=True)
df['Ctn Dt'].fillna(df['Ctn Dt'].median(), inplace=True)




#-------------------------- 7. Boxplot Before Outlier Removal --------------------------
plt.figure(figsize=(12, 8))
df[['Ctn Qty', 'Dlv Qty']].boxplot()
plt.title('Before Outlier Removal')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.show()

# -------------------------- 8. Remove Outliers ------------------------------------
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

# Apply outlier removal to both columns
df_cleaned = remove_outliers(df, 'Ctn Qty')
df_cleaned = remove_outliers(df_cleaned, 'Dlv Qty')

# ------------------------- 9. Boxplot After Outlier Removal --------------------------
plt.figure(figsize=(12, 8))
df_cleaned[['Ctn Qty', 'Dlv Qty']].boxplot()
plt.title('After Outlier Removal')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.show()

#-------------------------- 10. Export Cleaned Data --------------------------
df_cleaned.to_csv(r"C:\Users\User\Downloads\Power Bi project\cleaned_data.csv", index=False)
