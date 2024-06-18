import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import seaborn as sns
from matplotlib import pyplot as plt
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.ensemble import RandomForestClassifier
import numpy as np

base = "D:\manualCDmanagement\codes\Projects\VMs\skl algorithms\Logistic Regression/00_datasets/bmi.1"
save_path = "D:\manualCDmanagement\codes\Projects\VMs\skl algorithms\Logistic Regression/bmi.1/Storage/Figures"
file_name = "bmi.csv"
path = os.path.join(base, file_name)
df = pd.read_csv(path)


# cleaning dataframe
df.Gender = df.Gender.map({'Male': 1, 'Female': 0})


X = df.drop('Index', axis=1)
y = df['Index']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# balance the data
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

model = LogisticRegression(max_iter=1000, multi_class='ovr', class_weight='balanced') #ovr for One-vs-Rest or 'multinomial' for softmax (classification)
model.fit(X_train_resampled, y_train_resampled)

y_pred = model.predict(X_test)

accu = accuracy_score(y_test, y_pred)
conf = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, zero_division=0)


class_names = ['BMI 0', 'BMI 1', 'BMI 2', 'BMI 3', 'BMI 4', 'BMI 5']

#mask for the diagonal elements
mask = np.zeros_like(conf, dtype=bool)
np.fill_diagonal(mask, True)

#colormap for the heatmap
cmap = sns.diverging_palette(220, 300, as_cmap=True)

plt.figure(figsize=(5,5))
sns.heatmap(conf, annot=True, fmt='d', cmap=cmap, xticklabels=class_names, yticklabels=class_names, mask=~mask, cbar=False, linewidths=.5)
sns.heatmap(conf, annot=True, fmt='d', cmap='Greens', xticklabels=class_names, yticklabels=class_names, mask=mask, cbar=False, linewidths=.5)

plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
save_name = 'confusion_matrix.png'
# plt.savefig(os.path.join(save_path, save_name))
plt.show()
