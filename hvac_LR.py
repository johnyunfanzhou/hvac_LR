import hvac_LoadData as ld;
from sklearn.model_selection import train_test_split;
from sklearn.linear_model import LogisticRegression;

k = 2;
    
err = [];
g = [];

for FileIndex in range (25):

    # data = ld.load_data(FileIndex);
    # X = ld.generate_features(data, k);
    # y = ld.generate_labels(data, k);
    # 
    # X_train, X_test, y_train, y_test = train_test_split(X, y);
    
    X_train, X_test, y_train, y_test = ld.load_tts(FileIndex, k);
    
    LR = LogisticRegression();
    LR.fit(X_train, y_train);
    
    for key in X_test.keys():
        errors = 0;
        predictions = LR.predict(X_test[key]);
        for i in range (len(predictions)):
            if (predictions[i] != y_test[key][i]):
                errors += 1;
        err.append(errors);
        g.append(FileIndex + 1);

print('Average prediction error is %f errors per day' % (sum(err) / len(err)));