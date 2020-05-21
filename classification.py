from commons import getFileData,getAllStoneType
from kfold import kfold
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

def plotMetric(metric_data:list, img_name:str, neighbors_number:int,algorithm_name):
    img_title = f'{algorithm_name.upper()}-KNN({neighbors_number})'
    mean_accuracy = sum(metric_data)/(len(metric_data))
    fig,axs = plt.subplots()
    axs.plot(range(10),metric_data,marker='o',linestyle='solid',label='Accuracy')
    axs.plot(range(10),[mean_accuracy]*10,linestyle='--',label='Mean')
    axs.set(title= img_title,xlabel='FOLD INTERACTION', ylabel='%')
    axs.legend()
    #plt.show()
    fig.savefig(f'./plot_images/{img_name}')

def createFuzzyMatrix(result_pred,train_data, filename):
    stone_types = getAllStoneType()
    fuzzy_matrix = np.zeros((len(stone_types),len(stone_types)),dtype=int)
    for i in range(len(result_pred)):
        result = result_pred[i]
        expected = train_data[i]
        index_result = stone_types.index(result)
        index_expected = stone_types.index(expected)
        fuzzy_matrix[index_expected][index_result] += 1
    np.savetxt(filename,fuzzy_matrix,delimiter=',',fmt='%.2f',header=(', '.join(stone_types)),comments='')

def createSumConfusionMatrix(original_data, predict_data,filename):
    stone_types = getAllStoneType()
    fuzzy_matrix = np.zeros((len(stone_types),len(stone_types)),dtype=int)
    # As expected both parameters have the same size
    for i in range(len(original_data)):
        original_current = original_data[i]
        predict_current = predict_data[i]
        # Again both information have the same size here
        for j in range(len(original_current)):
            original_index = stone_types.index(original_current[j])
            predict_index = stone_types.index(predict_current[j])
            fuzzy_matrix[original_index][predict_index] += 1
    np.savetxt(filename,fuzzy_matrix,delimiter=',',fmt='%.2f',header=(', '.join(stone_types)),comments='')

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
    cmct_data_file  = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_data_result\\cmct_results.csv'
    ecmct_data_file = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_data_result\\ecmct_result.csv'
    lbp_data_file   = 'D:\\Documents\\GIT\\graniteTexture\\algorithm_data_result\\lbp_results.csv'
    data_file = [cmct_data_file,ecmct_data_file,lbp_data_file]
    k_neighbors = [3,5,7]
    for neighbor_number in k_neighbors:
        print(f'CURRENT K-NEIGHBOR: {neighbor_number}')
        for algorithm_file in data_file:
            # Variable used to check results after k-fold process
            order_test = list()
            order_predict = list()
            algorithm_accuracy = list()
            # ====================================================
            algorithm_data = getFileData(algorithm_file)
            algorithm_name = algorithm_file.split('\\')[-1][:-4].split('_')[0]
            print(f'CLASSIFICATION USING  {algorithm_name} AS EXTRACTOR')
            folded_data = kfold(algorithm_data,fold_num=10)
            fold_labels, fold_features = splitInformation(folded_data)
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
                model = KNeighborsClassifier(n_neighbors=neighbor_number)
                model.fit(train_features,train_label)
                predictions = model.predict(test_features)
                algorithm_accuracy.append(model.score(test_features,test_label))
                order_test.append(test_label)
                order_predict.append(predictions)
                #createFuzzyMatrix(predictions,test_label,f'./confusion_matrix/{algorithm_name}_knn{neighbor_number}_fold{i}.csv')
            #createSumConfusionMatrix(order_test,order_predict,f'./confusion_matrix/{algorithm_name}_knn{neighbor_number}.csv')
            print(algorithm_accuracy)
            print(f'Mean Accuray{sum(algorithm_accuracy)/10}')
            print('EXTRACTOR END\n')

if __name__ == '__main__':
    main()

# SECTION WITH ALL WORK FLOW BASED ON SKLEARN
# from sklearn.model_selection import train_test_split
# algorithm_data = getFileData(algorithm_file)
# label = list()
# features = list()
# for current_data in algorithm_data:
    # label.append(current_data[0])
    # features.append(current_data[1:])
# x_train, x_test, y_train, y_test = train_test_split(features, label,test_size=0.9)
# model = KNeighborsClassifier(n_neighbors=neighbor_number)
# model.fit(x_train,y_train)
# print(model.score(x_test,y_test))