import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, MultiLabelBinarizer
from wordcloud import WordCloud



# Carrega arquivo csv
data = pd.read_csv("music_sentiment_dataset.csv")

# Data Analysis
print("=============# INSPECTING DATA ============= \n")
print("---------- #  FIRST 5 ROWS # -----------\n",data.head())
print("---------- #  SUMMARY OF THE DATAFRAME # -----------\n",data.info())
print("---------- #  STATISTICS OF NUMERICAL COLUMNS # -----------\n",data.describe().T)
print("---------- #  SHAPE OF THE DATAFRAME # -----------\n",data.shape)
print("---------- #  LIST OF COLUMN NAMES # -----------\n",data.columns)
print("---------- #  DATA TYPES OF COLUMNS # -----------\n",data.dtypes)

#Data Cleaning

print("---------- #  DUPLICATES # -----------\n",data.duplicated().sum())
print("---------- #  DROPING DUPLICATES # -----------\n",data.drop_duplicates())


# Missing Values
print("---------- #  MISSING VALUES # -----------\n", data.isnull().sum())

# Checking for inconsistent categorical values
categorical_columns = data.select_dtypes(include=['object']).columns
for col in categorical_columns:
    print(f"---------- # UNIQUE VALUES IN {col} # -----------\n", data[col].unique())

#Checking for negative or zero values in numerical columns (if not expected)
numerical_columns = data.select_dtypes(include=['number']).columns
for col in numerical_columns:
    if (data[col] < 0).any():
        print(f"WARNING: Column '{col}' contains negative values!")
    if (data[col] == 0).any():
        print(f"NOTE: Column '{col}' contains zero values. Check if this is expected.")

# Checking Null Columns
print("---------- #  NULL VALUES INFO # -----------\n",data.isnull().sum())

# Encoding Data

data['User_ID'] = data['User_ID'].str.replace('U', '')
data['User_ID'] = data['User_ID'].astype(int)

data['Recommended_Song_ID'] = data['Recommended_Song_ID'].str.replace('S', '')
data['Recommended_Song_ID'] = data['Recommended_Song_ID'].astype(int)

Label_Encoder = LabelEncoder() 
Ordinal_Encoder = OrdinalEncoder()
Multilabel_Encoder = MultiLabelBinarizer()

# Classifying Nominal and Ordinal Columns

Nominal_Columns =['User_Text','Sentiment_Label', 'Song_Name','Artist','Genre','Mood']
Ordinal_Columns =['Tempo (BPM)','Energy','Danceability']
Multilabel_Columns =[]

# Encoding Data
print(" \n NOW DATA WILL BE ENCODED \n")
for col in Nominal_Columns:
    data[col] =Label_Encoder.fit_transform(data[col])
    print(f"ENCODED >>> {col}")

for col in Ordinal_Columns:
    data[col]= Ordinal_Encoder.fit_transform(data[[col]])
    print(f"ENCODED >>> {col}")

for col in Multilabel_Columns:
    data[col]= Multilabel_Encoder.fit_transform(data[[col]])
    print(f"ENCODED >>> {col}")



#save arquivo
data.to_csv('MusicData_Cleaned.csv',index=False)
print(">>> NEW FILE CREATED WITH CLEAN DATA")


# Visualization

# Creating Subplots
fig, axes = plt.subplots(4, 3, figsize=(20, 15))
fig.suptitle("Exploratory Data Analysis - Visualizations", fontsize=18)

# 1. Histogram for numerical features
data.select_dtypes(include=['number']).hist(ax=axes[0, 0], bins=20, color='blue', edgecolor='black')
axes[0, 0].set_title("Histogram of Numerical Columns")

# 2. Boxplot for numerical features (Outlier Detection)
sns.boxplot(data=data.select_dtypes(include=['number']), ax=axes[0, 1])
axes[0, 1].set_title("Boxplot of Numerical Columns")

# 3. Countplot for a categorical feature (assuming 'sentiment' column exists)
if 'sentiment' in data.columns:
    sns.countplot(x=data['sentiment'], palette="viridis", ax=axes[0, 2])
    axes[0, 2].set_title("Sentiment Distribution")

# 4. Pairplot of numerical variables (Limited to first 5 columns for performance)
sns.pairplot(data.select_dtypes(include=['number']).iloc[:, :5])
plt.title("Pairplot of First 5 Numerical Features")

# 5. Correlation Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()

# 6. Violin Plot (First numerical column vs sentiment if exists)
if 'sentiment' in data.columns:
    sns.violinplot(x=data['sentiment'], y=data.select_dtypes(include=['number']).columns[0], data=data, ax=axes[1, 0])
    axes[1, 0].set_title("Violin Plot of First Numerical Feature")

# 7. Bar Chart of Categorical Values (Limited to First Categorical Column)
cat_cols = data.select_dtypes(include=['object']).columns
if len(cat_cols) > 0:
    sns.barplot(x=data[cat_cols[0]].value_counts().index, y=data[cat_cols[0]].value_counts().values, ax=axes[1, 1])
    axes[1, 1].set_title(f"Bar Plot of {cat_cols[0]}")

# 8. WordCloud (Assuming 'lyrics' or text column exists)
if 'lyrics' in data.columns:
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(' '.join(data['lyrics'].dropna()))
    axes[1, 2].imshow(wordcloud, interpolation='bilinear')
    axes[1, 2].axis("off")
    axes[1, 2].set_title("WordCloud of Lyrics")

# 9. Scatter Plot (First two numerical columns)
num_cols = data.select_dtypes(include=['number']).columns
if len(num_cols) >= 2:
    sns.scatterplot(x=data[num_cols[0]], y=data[num_cols[1]], ax=axes[2, 0])
    axes[2, 0].set_title(f"Scatter Plot: {num_cols[0]} vs {num_cols[1]}")

# 10. KDE Plot for Distribution
sns.kdeplot(data.select_dtypes(include=['number']).iloc[:, 0], fill=True, ax=axes[2, 1], color='red')
axes[2, 1].set_title(f"KDE Plot of {data.select_dtypes(include=['number']).columns[0]}")

# 11. Pie Chart of a Categorical Feature
if len(cat_cols) > 0:
    data[cat_cols[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[2, 2])
    axes[2, 2].set_title(f"Pie Chart of {cat_cols[0]}")

# 12. Line Chart for First Numerical Column
sns.lineplot(data=data[num_cols[0]].sort_values(), ax=axes[3, 0])
axes[3, 0].set_title(f"Line Plot of {num_cols[0]}")

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout for title space
plt.show()

