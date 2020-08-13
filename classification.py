from utils.commons import getFileData,getAllStoneType,getAllTextureTypes
from utils.kfold import kfold
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plotConfusionMatrix(matrix_conf,list_classes,filename):
    fig,axs = plt.subplots()
    # Heat map definition
    ax = sns.heatmap(matrix_conf,xticklabels=list_classes,
    yticklabels=list_classes,annot=True,
    cbar=False, cmap="YlOrBr",
    linecolor='grey',linewidths=0.1)
    #plt.show()
    fig.savefig(f'./heatmap/{filename}', dpi = 200, bbox_inches='tight')

def createBaseConfusionMatrix(predicted_data,expected_data,list_classes):
    fuzzy_matrix = np.zeros((len(list_classes),len(list_classes)),dtype=int)
    # Matrix value definition
    for i in range(len(predicted_data)):
        result = predicted_data[i]
        expected = expected_data[i]
        index_result = list_classes.index(result)
        index_expected = list_classes.index(expected)
        fuzzy_matrix[index_expected][index_result] += 1
    return fuzzy_matrix

def createGeneralConfussionMatrix(predicted_data,expected_data,list_classes):
    fuzzy_matrix = np.zeros((len(list_classes),len(list_classes)),dtype=int)
    # As expected both parameters have the same size
    for i in range(len(expected_data)):
        original_current = expected_data[i]
        predict_current = predicted_data[i]
        # Again both information have the same size here
        confusion_matrix = createBaseConfusionMatrix(predict_current,original_current,list_classes)
        fuzzy_matrix = fuzzy_matrix + confusion_matrix
    return np.array(fuzzy_matrix)

def exportMatrixCsv(matrix,list_classes,filename):
    np.savetxt(filename,matrix,delimiter=',',fmt='%.2f',header=(', '.join(list_classes)),comments='')
    return 0

def splitInformation(folded_data:list):
    """
        Divide the descriptor data into label and feature
    """
    label = list()
    features = list()
    for fold in folded_data:
        fold_labels = [item[0] for item in fold]
        fold_features = [item[1:] for item in fold]
        label.append(fold_labels)
        features.append(fold_features)
    return label,features


def main():
    
    # Granite source
    #cmct_data_file  = 'D:\\Documents\\GIT\\graniteTexture\\granite_extraction\\cmct_results.csv'
    #ecmct_data_file = 'D:\\Documents\\GIT\\graniteTexture\\granite_extraction\\ecmct_results.csv'
    #lbp_data_file   = 'D:\\Documents\\GIT\\graniteTexture\\granite_extraction\\lbp_results.csv'
    #=============================================================================================

    # Texture source
    cmct_data_file  = 'D:\\Documents\\GIT\\graniteTexture\\texture_extraction\\cmct_results.csv'
    ecmct_data_file = 'D:\\Documents\\GIT\\graniteTexture\\texture_extraction\\ecmct_results.csv'
    lbp_data_file   = 'D:\\Documents\\GIT\\graniteTexture\\texture_extraction\\lbp_results.csv'
    #=============================================================================================
    
    data_file = [cmct_data_file,ecmct_data_file,lbp_data_file]
    k_neighbors = [3,5,7]
    for neighbor_number in k_neighbors:
        print(f'CURRENT K-NEIGHBOR: {neighbor_number}')
        for algorithm_file in data_file:
            # Variable used to check results after k-fold process
            test_label_sequence = list()
            prediction_sequence = list()
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

                # Getting training batchs
                train_label = list()
                train_features = list()
                for j in range(len(folded_data)):
                    if j != i:
                        train_label.extend(fold_labels[j])
                        train_features.extend(fold_features[j])
                
                # Classifier definition
                model = KNeighborsClassifier(n_neighbors=neighbor_number,metric='manhattan')
                model.fit(train_features,train_label)
                predictions = model.predict(test_features)
                algorithm_accuracy.append(model.score(test_features,test_label))
                test_label_sequence.append(test_label)
                prediction_sequence.append(predictions)

                # Exportation and creation of confusion matrix
                confusion_matrix = createBaseConfusionMatrix(predictions,test_label,getAllTextureTypes())
                exportMatrixCsv(confusion_matrix,getAllTextureTypes(),f'./confusion_matrix/texture_{algorithm_name}_knn{neighbor_number}_fold{i}.csv')
            general_confusion = createGeneralConfussionMatrix(prediction_sequence,test_label_sequence,getAllTextureTypes())
            exportMatrixCsv(general_confusion,getAllTextureTypes(),f'./confusion_matrix/texture_{algorithm_name}_knn{neighbor_number}.csv')
            plotConfusionMatrix(general_confusion,getAllTextureTypes(),f'texture_{algorithm_name}_knn{neighbor_number}.png')
            print(algorithm_accuracy)
            print(f'Mean Accuray: {sum(algorithm_accuracy)/10}')
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