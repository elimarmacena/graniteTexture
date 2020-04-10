from commons import getFileData
from kfold import kfold
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
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

def main():
    cmct_data_file  = 'D:\Documents\GIT\graniteTexture\cmct_results.csv'
    ecmct_data_file = 'D:\Documents\GIT\graniteTexture\ecmct_result.csv'
    lbp_data_file   = 'D:\Documents\GIT\graniteTexture\lbp_results.csv'
    data_file = [cmct_data_file,ecmct_data_file,lbp_data_file]
    neighbors_number = 5
    for algorithm_file in data_file:
        algorithm_name = algorithm_file.split('\\')[-1][:-4].split('_')[0]
        print('Prediciton File:',algorithm_name)
        algorithm_data = getFileData(algorithm_file)
        folded_data = kfold(algorithm_data,10)
        algorithm_accuracy = list()
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
            model = KNeighborsClassifier(n_neighbors=neighbors_number)
            model.fit(train_features,train_label_encode)
            type_prediction = model.predict(test_features)
            algorithm_accuracy.append(metrics.accuracy_score(test_label_encode,type_prediction) * 100)
        plotMetric(algorithm_accuracy,(f'{algorithm_name}_KNN{neighbors_number}.png'),neighbors_number,algorithm_name)

            
    

if __name__ == '__main__':
    main()