import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json

# Load the dataset
file_path = 'datasets/updated_dataset.csv'
data = pd.read_csv(file_path)

# Function to format symptoms by removing underscores and capitalizing first letters
def format_symptom(symptom):
    if pd.isna(symptom):
        return symptom
    return symptom.replace('_', ' ').title()

# Apply the formatting function to all symptom columns
symptom_columns = [col for col in data.columns if col.startswith('Symptom')]
for col in symptom_columns:
    data[col] = data[col].apply(format_symptom)

# Prepare the data
# Encode the Disease column
label_encoder = LabelEncoder()
data['Disease'] = label_encoder.fit_transform(data['Disease'])

# Fill NaN values with a placeholder
data.fillna('None', inplace=True)

# Encode the symptom columns
for col in symptom_columns:
    data[col] = label_encoder.fit_transform(data[col])

# Split the data into features and target variable
X = data[symptom_columns]
y = data['Disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy}')

# Save the model
model_file_path = 'random_forest_model.pkl'
joblib.dump(model, model_file_path)

# Save the label encoder
encoder_file_path = 'label_encoder.pkl'
joblib.dump(label_encoder, encoder_file_path)

# Save the model in JSON format
model_json = {
    'model_params': model.get_params(),
    'classes': label_encoder.classes_.tolist()
}
model_json_file_path = 'random_forest_model.json'
with open(model_json_file_path, 'w') as f:
    json.dump(model_json, f)

print(f'Model saved to {model_file_path}')
print(f'Label encoder saved to {encoder_file_path}')
print(f'Model JSON saved to {model_json_file_path}')
