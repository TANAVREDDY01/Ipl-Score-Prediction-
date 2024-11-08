# -*- coding: utf-8 -*-
"""Neural Network Architectures in IPL Score Prediction: Balancing Accuracy and Training Time".ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VtSuHRHsJMnllfHZsrNu0_kasAMvwOKk

# IPL 1st Inning Score Prediction using Machine Learning
The Dataset contains ball by ball information of the matches played between IPL Teams of **Season 1 to 10**, i.e. from 2008 to 2017.<br/>

# Import Necessary Libraries
"""

# Importing Necessary Libraries
import pandas as pd
import numpy as np
np.__version__

# Mounting GDrive and importing dataset
data = pd.read_csv('/content/ipl_data1.csv')
print(f"Dataset successfully Imported of Shape : {data.shape}")

"""# Exploratory Data Analysis"""

# First 5 Columns Data
data.head()

# Describing Numerical Values of the Dataset
data.describe()

# Information (not-null count and data type) About Each Column
data.info()

# Number of Unique Values in each column
data.nunique()

# Datatypes of all Columns
data.dtypes

"""# Data Cleaning

#### Removing Irrelevant Data colunms
"""

# Names of all columns
data.columns

"""Here, we can see that columns _['mid', 'date', 'venue', 'batsman', 'bowler', 'striker', 'non-striker']_ won't provide any relevant information for our model to train"""

irrelevant = ['mid', 'date', 'venue','batsman', 'bowler', 'striker', 'non-striker']
print(f'Before Removing Irrelevant Columns : {data.shape}')
data = data.drop(irrelevant, axis=1) # Drop Irrelevant Columns
print(f'After Removing Irrelevant Columns : {data.shape}')
data.head()

"""#### Keeping only Consistent Teams
(teams that never change even in current season)
"""

# Define Consistent Teams
const_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
              'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
              'Delhi Daredevils', 'Sunrisers Hyderabad']

print(f'Before Removing Inconsistent Teams : {data.shape}')
data = data[(data['batting_team'].isin(const_teams)) & (data['bowling_team'].isin(const_teams))]
print(f'After Removing Irrelevant Columns : {data.shape}')
print(f"Consistent Teams : \n{data['batting_team'].unique()}")
data.head()

"""#### Remove First 5 Overs of every match"""

print(f'Before Removing Overs : {data.shape}')
data = data[data['overs'] >= 5.0]
print(f'After Removing Overs : {data.shape}')
data.head()

"""Plotting a Correlation Matrix of current data"""

from seaborn import heatmap

# Select only numeric columns for correlation
numeric_data = data.select_dtypes(include=[np.number])

# Compute the correlation matrix
correlation_matrix = numeric_data.corr()

# Plot the heatmap
heatmap(data=correlation_matrix, annot=True)

"""# Data Preprocessing and Encoding

#### Performing Label Encoding
"""

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
le = LabelEncoder()
for col in ['batting_team', 'bowling_team']:
  data[col] = le.fit_transform(data[col])
data.head()

"""#### Performing One Hot Encoding and Column Transformation"""

from sklearn.compose import ColumnTransformer
columnTransformer = ColumnTransformer([('encoder',
                                        OneHotEncoder(),
                                        [0, 1])],
                                      remainder='passthrough')

data = np.array(columnTransformer.fit_transform(data))

"""Save the Numpy Array in a new DataFrame with transformed columns"""

cols = ['batting_team_Chennai Super Kings', 'batting_team_Delhi Daredevils', 'batting_team_Kings XI Punjab',
              'batting_team_Kolkata Knight Riders', 'batting_team_Mumbai Indians', 'batting_team_Rajasthan Royals',
              'batting_team_Royal Challengers Bangalore', 'batting_team_Sunrisers Hyderabad',
              'bowling_team_Chennai Super Kings', 'bowling_team_Delhi Daredevils', 'bowling_team_Kings XI Punjab',
              'bowling_team_Kolkata Knight Riders', 'bowling_team_Mumbai Indians', 'bowling_team_Rajasthan Royals',
              'bowling_team_Royal Challengers Bangalore', 'bowling_team_Sunrisers Hyderabad', 'runs', 'wickets', 'overs',
       'runs_last_5', 'wickets_last_5', 'total']
df = pd.DataFrame(data, columns=cols)

# Visualize Encoded Data
df.head()

"""# Model Building

## Prepare Train and Test Splits
"""

features = df.drop(['total'], axis=1)
labels = df['total']

# Perform 80 : 20 Train-Test split
from sklearn.model_selection import train_test_split
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.20, shuffle=True)
print(f"Training Set : {train_features.shape}\nTesting Set : {test_features.shape}")

"""## Model Algorithms
Training and Testing on different Machine Learning Algorithms for the best algorithm to choose from
"""

# Keeping track of model perfomances
models = dict()

"""#### Neural Networks"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error as mae, mean_squared_error as mse
import time

# Define layer configurations with up to 4 hidden layers
layer_configs = [
    (5,), (10,), (20,),                   # 1 hidden layer
    (5, 5), (10, 10), (20, 20),           # 2 hidden layers
    (5, 5, 5), (10, 10, 10), (20, 20, 20),  # 3 hidden layers
    (5, 5, 5, 5), (10, 10, 10, 10), (20, 20, 20, 20)  # 4 hidden layers
]

# Lists to store performance metrics and training times for each configuration
train_scores = []
test_scores = []
train_times = []
mae_scores = []
mse_scores = []
rmse_scores = []

for layers in layer_configs:
    # Initialize the model with the current layer configuration
    neural_net = MLPRegressor(hidden_layer_sizes=layers, activation='logistic', max_iter=500, random_state=1)

    # Record the start time
    start_time = time.time()

    # Train the model
    neural_net.fit(train_features, train_labels)

    # Record the end time and calculate training time
    end_time = time.time()
    training_time = end_time - start_time
    train_times.append(training_time)

    # Calculate and store scores
    train_score = neural_net.score(train_features, train_labels) * 100
    test_score = neural_net.score(test_features, test_labels) * 100
    test_predictions = neural_net.predict(test_features)

    # Calculate error metrics
    test_mae = mae(test_labels, test_predictions)
    test_mse = mse(test_labels, test_predictions)
    test_rmse = np.sqrt(test_mse)

    # Append scores and metrics to lists
    train_scores.append(train_score)
    test_scores.append(test_score)
    mae_scores.append(test_mae)
    mse_scores.append(test_mse)
    rmse_scores.append(test_rmse)

# Plot the performance metrics for each layer configuration
plt.figure(figsize=(18, 6))

# Train and Test Scores
plt.subplot(1, 3, 1)
plt.plot([str(l) for l in layer_configs], train_scores, label='Train Score', marker='o')
plt.plot([str(l) for l in layer_configs], test_scores, label='Test Score', marker='o')
plt.xlabel('Layer Configuration')
plt.ylabel('Score (%)')
plt.title('Train vs Test Score by Layer Configuration')
plt.xticks(rotation=45)
plt.legend()

# MAE
plt.subplot(1, 3, 2)
plt.plot([str(l) for l in layer_configs], mae_scores, label='MAE', color='orange', marker='o')
plt.xlabel('Layer Configuration')
plt.ylabel('Mean Absolute Error')
plt.title('MAE by Layer Configuration')
plt.xticks(rotation=45)

# RMSE
plt.subplot(1, 3, 3)
plt.plot([str(l) for l in layer_configs], rmse_scores, label='RMSE', color='red', marker='o')
plt.xlabel('Layer Configuration')
plt.ylabel('Root Mean Squared Error')
plt.title('RMSE by Layer Configuration')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Plot Training Time vs Accuracy (Test Score)
plt.figure(figsize=(10, 6))
plt.scatter(train_times, test_scores, color='purple', marker='o')
for i, txt in enumerate([str(l) for l in layer_configs]):
    plt.annotate(txt, (train_times[i], test_scores[i]))
plt.xlabel('Training Time (seconds)')
plt.ylabel('Test Score (%)')
plt.title('Training Time vs Test Accuracy for Different Layer Configurations')
plt.grid(True)
plt.show()

# Display the results in text
for idx, layers in enumerate(layer_configs):
    print(f'Configuration: {layers}')
    print(f'Train Score: {train_scores[idx]:.2f}%')
    print(f'Test Score: {test_scores[idx]:.2f}%')
    print(f'Training Time: {train_times[idx]:.4f} seconds')
    print(f'MAE: {mae_scores[idx]:.4f}')
    print(f'MSE: {mse_scores[idx]:.4f}')
    print(f'RMSE: {rmse_scores[idx]:.4f}\n')

# Store the final model with the best test score
best_index = test_scores.index(max(test_scores))
models["neural_net"] = test_scores[best_index]

"""# Predictions"""

# Ensure you have imported necessary libraries
import numpy as np

# Define or load your model here (this is an example; ensure 'forest' is a trained model)
# Example: forest = RandomForestRegressor().fit(X_train, y_train)

# Define the prediction function
def predict_score(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5, model=neural_net):
    prediction_array = []

    # Batting Team Encoding
    if batting_team == 'Chennai Super Kings':
        prediction_array += [1,0,0,0,0,0,0,0]
    elif batting_team == 'Delhi Daredevils':
        prediction_array += [0,1,0,0,0,0,0,0]
    elif batting_team == 'Kings XI Punjab':
        prediction_array += [0,0,1,0,0,0,0,0]
    elif batting_team == 'Kolkata Knight Riders':
        prediction_array += [0,0,0,1,0,0,0,0]
    elif batting_team == 'Mumbai Indians':
        prediction_array += [0,0,0,0,1,0,0,0]
    elif batting_team == 'Rajasthan Royals':
        prediction_array += [0,0,0,0,0,1,0,0]
    elif batting_team == 'Royal Challengers Bangalore':
        prediction_array += [0,0,0,0,0,0,1,0]
    elif batting_team == 'Sunrisers Hyderabad':
        prediction_array += [0,0,0,0,0,0,0,1]

    # Bowling Team Encoding
    if bowling_team == 'Chennai Super Kings':
        prediction_array += [1,0,0,0,0,0,0,0]
    elif bowling_team == 'Delhi Daredevils':
        prediction_array += [0,1,0,0,0,0,0,0]
    elif bowling_team == 'Kings XI Punjab':
        prediction_array += [0,0,1,0,0,0,0,0]
    elif bowling_team == 'Kolkata Knight Riders':
        prediction_array += [0,0,0,1,0,0,0,0]
    elif bowling_team == 'Mumbai Indians':
        prediction_array += [0,0,0,0,1,0,0,0]
    elif bowling_team == 'Rajasthan Royals':
        prediction_array += [0,0,0,0,0,1,0,0]
    elif bowling_team == 'Royal Challengers Bangalore':
        prediction_array += [0,0,0,0,0,0,1,0]
    elif bowling_team == 'Sunrisers Hyderabad':
        prediction_array += [0,0,0,0,0,0,0,1]

    # Add other match features
    prediction_array += [runs, wickets, overs, runs_last_5, wickets_last_5]

    # Convert to numpy array
    prediction_array = np.array([prediction_array])

    # Make prediction
    pred = model.predict(prediction_array)

    # Return rounded prediction
    return int(round(pred[0]))

# First Prediction
batting_team = 'Delhi Daredevils'
bowling_team = 'Chennai Super Kings'
overs = 10.2
runs = 68
wickets = 3
runs_last_5 = 29
wickets_last_5 = 1

score1 = predict_score(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5)
print(f'Predicted Score : {score1} || Actual Score : 147')

# Second Prediction
batting_team = 'Mumbai Indians'
bowling_team = 'Kings XI Punjab'
overs = 12.3
runs = 113
wickets = 2
runs_last_5 = 55
wickets_last_5 = 0

score2 = predict_score(batting_team, bowling_team, runs, wickets, overs, runs_last_5, wickets_last_5)
print(f'Predicted Score : {score2} || Actual Score : 176')