from commons import getFileData
import numpy as np
from sklearn import preprocessing
from sklearn import metrics

from sklearn.neighbors import KNeighborsClassifier
from kfold import kfold

def splitInformation(folded_data:list):
    label = list()
    features = list()
    for fold in folded_data:
        fold_labels = [item[0] for item in fold]
        fold_features = [item[1:] for item in fold]
        label.append(fold_labels)
        features.append(fold_features)
    return label,features

def main():
    cmct_data_file  = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_texture_result\\cmct_results.csv'
    ecmct_data_file = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_texture_result\\ecmct_results.csv'
    lbp_data_file   = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_texture_result\\lbp_results.csv'
    data_file = [cmct_data_file,ecmct_data_file,lbp_data_file]
    for algorithm_file in data_file:
        algorithm_name = algorithm_file.split('\\')[-1][:-4].split('_')[0]
        print(f'CLASSIFICATION USING  {algorithm_name} AS EXTRACTOR')
        algorithm_data = getFileData(algorithm_file)
        print('K-NN: 2')
        folded_data = kfold(algorithm_data,fold_num=10)
        fold_labels, fold_features = splitInformation(folded_data)
        classification_result = list()
        for i in range(len(folded_data)):
            # Getting test information
            test_label = fold_labels[i]
            test_features = fold_features[i]
            # Getting train information
            train_label = list()
            train_features = list()
            for j in range(len(folded_data)):
                if j != i:
                    train_label.extend(fold_labels[j])
                    train_features.extend(fold_features[j])
            model = KNeighborsClassifier(n_neighbors=2)
            model.fit(train_features,train_label)
            classification_result.append(model.score(test_features,test_label))
            print(f'KNN: {model.score(test_features,test_label)}')
        print(sum(classification_result)/10)
    #createFuzzyMatrix(predictions,test_label,f'./confusion_matrix/{algorithm_name}_knn{neighbor_number}_fold{i}.csv')

if __name__ == '__main__':
    main()

#  SECTION WITH ALL WORK FLOW BASED ON SKLEARN
# from sklearn.model_selection import train_test_split
# label = list()
# features = list()
# for current_data in algorithm_data:
#     label.append(current_data[0])
#     features.append(current_data[1:])
# x_train, x_test, y_train, y_test = train_test_split(features, label,test_size=0.1)
# knn_model = KNeighborsClassifier(n_neighbors=4,metric='euclidean')
# knn_model.fit(x_train,y_train)
# print(f'KNN: {knn_model.score(x_test,y_test)}')