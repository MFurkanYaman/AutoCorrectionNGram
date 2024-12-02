import os
import dill

import config

saveFile = config.SAVEFILE
fileExtension = config.FILEEXTENSION

loaded_data = {} 
def load_all_pkl_files():
    """
        Bu fonksiyon, belirli bir dizinden (SAVEFILE) pkl dosyalarını yükler ve bellekte tutar. 
        loaded_data adlı küresel değişkende, harfler bazında veriler saklanır. Her harf için belirli bir dosya yüklenir.
    """
    global loaded_data
    for letter in "abcçdefghıijklmnoöprsştuüvyz":
        file_path = os.path.join(saveFile, f"{letter}{fileExtension}")
        try:
            with open(file_path, "rb") as f:
                loaded_data[letter] = dill.load(f)
            
        except Exception as e:
            print(f"Hata oluştu ({file_path}): {e}")
    return loaded_data