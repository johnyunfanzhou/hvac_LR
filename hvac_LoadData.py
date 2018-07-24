import os;
import csv;

os.chdir('../formed_data/tts_1/continous_sample/');

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
    Read CSV file and return all entries in a string matrix
    '''
    if ((FileIndex < 1) or (FileIndex > 25)):
        raise ValueError('Invalid file index.');
    result = [];
    with open(filename[FileIndex - 1], 'r', newline = '') as csvfile:
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
            result.append(row);
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
            if datacontinuous:
                y.append(data[i][2]);
            else:
                if HISTORY == None:
                    break;
                else:
                    y.append(data[i][2]);
            n -= 1;
    return y;