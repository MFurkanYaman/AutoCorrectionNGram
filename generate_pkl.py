import time
import os
import logging
import dill

from nltk import ngrams

import config 

# 86 saniye sürdü.

def generate_bigrams_from_words(datasetPath):

    """
    Verileri okur ve biagramlara dönüştürerek word_dict parametresine atar.  
    """

    try:
        data = open(datasetPath, 'r',encoding="utf-8").read().splitlines()
    except Exception as e:
        logging.error(f"Dataset dosyası açılırken hata: {e}")
        return []

    word_dict={}

    for value in data:
        ngrammer=list(ngrams(value,n=2))
        if not ngrammer:
            continue
        word_dict[value]=ngrammer
        
    return word_dict
    
def save_words_by_first_letter(word_dict,save_file,fileExtension):

    """
    Kelimeleri ilk harflerine göre gruplar ve her grubu bir .pkl dosyasına kaydeder.
    
    Parametreler:
        word_dict (list): Bigram listelerini içeren kelime listesi.
        save_file (str): Kaydedilecek dosyaların dizini.
        fileExtension (str): Dosyaların uzantısı.
    """

    if not os.path.exists(save_file):
        os.makedirs(save_file)

    
    

    try:
        save_dict={}
        first_letter="a"
        isLetterChange=False
        for wordKey,wordValue in word_dict.items():
            

            if isLetterChange==True:
                first_letter=wordKey[0]
                isLetterChange=False
                print("Harf Değişti: ",first_letter)
       
            if first_letter==wordKey[0]:
                
                save_dict[tuple(wordValue)]=wordKey
              
            else:
                
                file_name=first_letter+fileExtension
                save_path=save_file+file_name

                # print(save_dict)
                

                with open(save_path,"wb") as f:
                    dill.dump(save_dict,f)

                save_dict={}

                first_letter=wordKey[0]

                save_dict[tuple(wordValue) ] = [wordKey] 
                isLetterChange=True


        file_name=first_letter+fileExtension
        save_path=save_file+file_name

    
        with open(save_path,"wb") as f:
            dill.dump(save_dict,f)

    except Exception as e:
        logging.error(f"{file_name} kaydedilirken hata: {e}")





def main():
    start=time.time()
    

    word_dict=generate_bigrams_from_words(r"C:\Users\MFY\Desktop\NLP_Exercise\dataset\full_words_tr.txt")

    
    
    save_words_by_first_letter(word_dict,config.SAVEFILE,config.FILEEXTENSION)

    end=time.time()
    print("Execution Time: ", end-start)




main()