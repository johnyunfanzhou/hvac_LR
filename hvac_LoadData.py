import os;
import csv;

filename = ['1d0733906f57440ecade6f8d3f091630de8c24ec.csv', 
    '5a582fd2839fc31dbc553389cf8e65b8b845aa7c.csv', 
    '6d195551c1ef0ca9bf855903cdfd9dd6b71a6ff5.csv', 
    '7a805f75e7a914388de0fb8308227c7ba627271c.csv', 
    '8bb1a09d4729c4908f4a7dfc173de7f7d0d3642c.csv', 
    '11e9aff05e9dadce7aa8292f13fe7187ea5a3037.csv', 
    '78c451cc556e71801bc66686fbc075cdd895dde6.csv', 
    '80b98d4c69fc7c6d89facafb1580454016f46f20.csv', 
    '83ed059e2bd6f36735a871c924fa74caa55f4878.csv', 
    '110dda328a521cd41d3771feaf994a9faa966b1e.csv', 
    '3200f9aa03bfedc80533b273d6dc2de839f8343e.csv', 
    '7310f1a63efce1496ad98bb8149a05e93ad4292f.csv', 
    '84607b6dce9e34641814db21a0bb5882d5375814.csv', 
    'a722b876dcf882b0c0412d535ab98943cd4a1846.csv', 
    'ab23b4f49689c5dd4bf205210bf3877126b115ef.csv', 
    'ac37d357c0d4436d5077a6c91a4634939514086f.csv', 
    'ae064b908ecfc8ec21028722ed86661c2b59d7c7.csv', 
    'c0d48ccbe55cc94acdebe3b4b5f35dd85e92b26a.csv', 
    'd805f6abf5c22a5e0582b29905468f735682ea0d.csv', 
    'd6753e2c7717cda160070bed00183cb722951f5f.csv', 
    'dd489fa33b229e50a89170159107ab2c3ca7369d.csv',  
    'e56deb5addea10ecc6b962cb2e8f4a57442b52ee.csv', 
    'e79039a7615153cfebfda4669160c06ad3a5658d.csv', 
    'f17826dce7c323c15e8f1e91cb7543f10b09520d.csv', 
    'fb4d3fa98447464e0d38ba15b6928ed5ca072eef.csv'];
    
def load_data(FileIndex):
    '''
    Read CSV file and return all entries in a matrix
    The set parameter indicate which set of data should be loaded:
    set = 'test_1': test data in the first train-test-set
    set = 'test_2': test data in the second train-test-set
    set = 'train_1': train data in the first train-test-set
    set = 'train_1': train data in the second train-test-set
    else: continuous sample (default)
    '''
    if ((FileIndex < 0) or (FileIndex > 24)):
        raise ValueError('Invalid file index.');
        
    result = [];
    
    os.chdir('../formed_data/tts_1/continuous_sample/');

    with open(filename[FileIndex], 'r', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',');
        first = True;
        for row in reader:
            '''
            Ignore first row
            '''
            if first:
                first = False;
                continue;
            row[1] = int(row[1]);
            row[2] = int(row[2]);
            row[3] = int(row[3]); 
            row[4] = int(row[4]);
            if not (row in result):
                result.append(row);
    os.chdir(os.path.dirname(__file__))
    return result;
    
def generate_features(data, k, HISTORY = None):
    '''
    Given training data (data) and training degree (k),
    output the feature matrix
    If discontinuous data is detected, use history average (HISTORY) to guess 
    the missing data.
    If there is no history average (HISTORY == None), delete the sample.
    '''
    datasize = len(data);
    X = [];
    for i in range (datasize):
        x = [];
        x.append(data[i][2]);
        x.append(data[i][3]);
        x.append(data[i][4]);
        n = i;
        datacontinuous = True;
        for j in range (k):
            if datacontinuous:
                if (n == 1):
                    datacontinuous = False;
                elif ((data[n][3] - data[n - 1][3]) % 48 != 1):
                    datacontinuous = False;
                elif (data[n][3] != 0):
                    if ((data[n][2] != data[n - 1][2]) or (data[n][4] != data[n - 1][4])):
                        datacontinuous = False;
            if datacontinuous:
                x.append(data[n - 1][1]);
            else:
                if HISTORY == None:
                    break;
                else:
                    x.append(HISTORY[data[n][2]][data[n][3] - 1][data[n][4]]); ##
            n -= 1;
        if (len(x) == 3 + k):
            X.append(x);
    return X;

def generate_labels(data, k, HISTORY = None):
    '''
    Given training data (data) and training degree (k),
    output the label vector
    If discontinuous data is detected, and no history average (HISTORY) is used, 
    delete the sample.
    '''
    datasize = len(data);
    y = [];
    for i in range (datasize):
        n = i;
        datacontinuous = True;
        for j in range (k):
            if datacontinuous:
                if (n == 1):
                    datacontinuous = False;
                elif ((data[n][3] - data[n - 1][3]) % 48 != 1):
                    datacontinuous = False;
                elif (data[n][3] != 0):
                    if ((data[n][2] != data[n - 1][2]) or (data[n][4] != data[n - 1][4])):
                        datacontinuous = False;
            n -= 1;
        if datacontinuous:
            y.append(data[i][1]);
        else:
            if HISTORY == None:
                continue;
            else:
                y.append(data[i][1]);
    return y;
    
def load_tts(FileIndex, k):
    data = load_data(FileIndex);
    X = generate_features(data, k);
    y = generate_labels(data, k);
    datasize = len(X);

    test_entries = [];
    
    os.chdir('../formed_data/tts_1/test_1/');
    
    with open('test_' + filename[FileIndex], 'r', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',');
        first = True;
        for row in reader:
            '''
            Ignore first row
            '''
            if first:
                first = False;
                continue;
            test_entries.append(row[0][:10]);
    
    X_train = [];
    X_test = {};
    y_train = [];
    y_test = {};
    
    for i in range (datasize):
        date = data[i][0][:10];
        if date in test_entries:
            if date not in X_test.keys():
                X_test[date] = [];
                y_test[date] = [];
            X_test[date].append(X[i]);
            y_test[date].append(y[i]);
        else:
            X_train.append(X[i]);
            y_train.append(y[i]);
    
    os.chdir(os.path.dirname(__file__));
    return X_train, X_test, y_train, y_test;