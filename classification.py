from commons import getFileData
from kfold import kfold
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


def main():
    cmct_data_file  = 'D:\Documents\GIT\graniteTexture\cmct_results.csv'
    ecmct_data_file = 'D:\Documents\GIT\graniteTexture\ecmct_result.csv'
    lbp_data_file   = 'D:\Documents\GIT\graniteTexture\lbp_results.csv'
    data_file = [cmct_data_file,ecmct_data_file,lbp_data_file]
    for algorithm_file in data_file:
        print('Prediciton File:',algorithm_file)
        algorithm_data = getFileData(algorithm_file)
        folded_data = kfold(algorithm_data,10)
        for i in range(len(folded_data)):
            test_data = folded_data[i]
            train_data = list()
            for j in range(len(folded_data)):
                if j != i:
                    train_data.extend(folded_data[j])
            test_label = [item[0] for item in test_data]
            test_features = [item[1:] for item in test_data]
            train_label = [item[0] for item in train_data]
            train_features = [item[1:] for item in train_data]
            encolder = preprocessing.LabelEncoder()
            train_label_encode = encolder.fit_transform(train_label)
            test_label_encode = encolder.fit_transform(test_label)
            model = KNeighborsClassifier(n_neighbors=5)
            model.fit(train_features,train_label_encode)
            type_prediction = model.predict(test_features)
            print('Accuracy:',metrics.accuracy_score(test_label_encode,type_prediction))
            
    

if __name__ == '__main__':
    main()