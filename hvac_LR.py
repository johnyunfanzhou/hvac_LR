import hvac_LoadData as ld;
from sklearn.model_selection import train_test_split;
from sklearn.linear_model import LogisticRegression;

for k in range (4):

    print('Degree of training is ' + str(k) + '.\n');
    score = [];
    
    for FileIndex in range (25):
    
        data = ld.load_data(FileIndex);
        
        X = ld.generate_features(data, k);
        
        y = ld.generate_labels(data, k);
        
        X_train, X_test, y_train, y_test = train_test_split(X, y);
        
        LR = LogisticRegression();
        
        LR.fit(X_train, y_train);
        
        score.append(LR.score(X_test, y_test));
    
    print('Predict accuracy is ' + str(sum(score) / 25) + '.\n');
    