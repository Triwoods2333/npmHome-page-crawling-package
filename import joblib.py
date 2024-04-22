import joblib
import pandas as pd

model_path = "C:/Users/97091/Desktop/getgithub/JS_monolanguage_model.pkl"
model = joblib.load(model_path)
joblib.dump(model, 'my_model.joblib')
model = joblib.load('my_model.joblib')

csv_path = 'C:/Users/97091/Desktop/getgithub/npm_feature_extracted.csv'
data = pd.read_csv(csv_path)
X_test = data.iloc[:, 1:-1]  
print(X_test)
y_pred = model.predict(X_test)

data.insert(0, 'Malicious', y_pred) 
data.to_excel('Predicted_Labelled_Dataset.xlsx', index=False)