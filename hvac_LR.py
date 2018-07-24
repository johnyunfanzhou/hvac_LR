import hvac_LoadData as ld;
from sklearn import LogisticRegression;

FileIndex = 1;
k = 1;

data = ld.load_data(FileIndex);

X = ld.generate_features(data, k);

y = ld.generate_labels(data, k);