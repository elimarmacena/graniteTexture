import glob
def getAllImages():
    # images are currently divided into folders inside the master folder
    master_folder = '.\\GraniteImgs\\*\\*'
    image_path = glob.glob(master_folder)
    return image_path