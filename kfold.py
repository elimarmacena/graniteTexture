from random import seed
from random import randrange #default python random library
def kfold(data_sample:list, fold_num = 4):
    seed(16)
    final_dataset = []
    data_keeper = data_sample.copy()
    fold_size = len(data_sample) // fold_num #if the number of records isn't divisible for the number of folds we lose records.
    for i in range(fold_num):
        fold_data = []
        for j in range(fold_size):
            index = randrange(0,len(data_keeper))
            fold_data.append(data_keeper.pop(index))
        final_dataset.append(fold_data)
    return final_dataset