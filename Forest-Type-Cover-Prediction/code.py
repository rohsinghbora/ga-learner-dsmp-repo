# --------------
import pandas as pd
from sklearn import preprocessing

#path : File path

# Code starts here
dataset = pd.read_csv(path)


# read the dataset



# look at the first five columns


# Check if there's any column which is not useful and remove it like the column id
dataset = dataset.drop(['Id'],axis=1)
print(dataset.head())
# check the statistical description
sd = dataset.describe()
print(sd)


# --------------
# We will visualize all the attributes using Violin Plot - a combination of box and density plots
import seaborn as sns
from matplotlib import pyplot as plt

#names of all the attributes 
cols = dataset.columns.values
print(cols)

#number of attributes (exclude target)
size = len(cols) - 1

#x-axis has target attribute to distinguish between classes
x = dataset['Cover_Type']
y = dataset.drop(['Cover_Type'],axis = 1)

#y-axis shows values of an attribute

#Plot violin for all attributes
count = 0
while (count < size):   
    sns.violinplot(x,y[y.columns.values[count]])
    plt.show()
    count = count + 1  
    







# --------------
import numpy
upper_threshold = 0.5
lower_threshold = -0.5


# Code Starts Here

subset_train = dataset.iloc[:, : 10]
data_corr = subset_train.corr(method='pearson')
sns.heatmap(data_corr)
plt.show()
correlation = data_corr.unstack().sort_values(kind='quicksort') 

count = 0
corr_var_list = []
print(len(correlation))
while count < len(correlation):
    if correlation[count] == 1:
        count = count + 1
    elif correlation[count] > upper_threshold:
        corr_var_list.append(correlation[count]) 
        count = count + 1
    elif correlation[count] < lower_threshold:
        corr_var_list.append(correlation[count]) 
        count = count + 1
    else:
        count = count + 1

print(corr_var_list)
# Code ends here




# --------------
#Import libraries
from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
# Identify the unnecessary columns and remove it
dataset.drop(columns=['Soil_Type7', 'Soil_Type15'], inplace=True)
r,c = dataset.shape
X = dataset.iloc[:,:-1]
Y = dataset.iloc[:,-1]
# Scales are not the same for all variables. Hence, rescaling and standardization may be necessary for some algorithm to be applied on it.
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)
#Standardized
scaler = StandardScaler()
#Apply transform only for continuous data
X_train_temp = scaler.fit_transform(X_train.iloc[:,:10])
X_test_temp = scaler.transform(X_test.iloc[:,:10])
#Concatenate scaled continuous data and categorical
X_train1 = numpy.concatenate((X_train_temp,X_train.iloc[:,10:c-1]),axis=1)
X_test1 = numpy.concatenate((X_test_temp,X_test.iloc[:,10:c-1]),axis=1)
scaled_features_train_df = pd.DataFrame(X_train1, index=X_train.index, columns=X_train.columns)
scaled_features_test_df = pd.DataFrame(X_test1, index=X_test.index, columns=X_test.columns)


# --------------
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import f_classif
import numpy as np 

# Write your solution here:
skb = SelectPercentile(score_func=f_classif, percentile=90)
predictors = skb.fit_transform(X_train1, Y_train)
scores = skb.scores_
Features = X_train.columns
dataframe = pd.DataFrame({'Features':Features, 'scores':scores})
dataframe.sort_values(by=['scores'], axis=0, ascending=False, inplace=True)
top_k_predictors = list(dataframe['Features'][:predictors.shape[1]])


# --------------
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score

clf = OneVsRestClassifier(LogisticRegression())
clf1 = OneVsRestClassifier(LogisticRegression())
model_fit_all_features = clf1.fit(X_train, Y_train)
predictions_all_features = clf1.predict(X_test)
score_all_features = accuracy_score(Y_test, predictions_all_features)
print('score_all_features: ',score_all_features)
print('~'*80)
model_fit_top_features = clf.fit(scaled_features_train_df[top_k_predictors], Y_train)
predictions_top_features = clf.predict(scaled_features_test_df[top_k_predictors])
score_top_features = accuracy_score(predictions_top_features, Y_test)
print('score_top_features: ',score_top_features)


