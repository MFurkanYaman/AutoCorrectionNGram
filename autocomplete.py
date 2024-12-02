
import time
import editdistance

import logging
import config
from nltk import ngrams

def load_dataset(loaded_data):
    """Veri setini yükleyip, kullanıcının girdiği kelimenin ilk harfine göre ilgili n-gram sözlüğünü döndürür."""
    global word
    
    try:
            letter=word[0]
            loaded_ngram_dict=loaded_data[letter]
          
            return loaded_ngram_dict #dict dönüyorr
    except Exception as e:
        logging.error(f"Error in data loading--> {e}")
             
def sortAndMatch(rateLevenshtein,count,loaded_ngram_dict): #OK
    """
    Levenshtein mesafelerine göre sıralanmış olan n-gram eşleşmelerini döndürür.
    En düşük mesafeye sahip count kadar sonuç döndürülür. Bu fonksiyon, önerileri sıralamak ve filtrelemek için kullanılır.
    """
    matchedWords=[]
   
    try:
        sorted_by_values_levenshtein = sorted(rateLevenshtein.items(), key=lambda item: item[1], reverse=True)[:count]

        for matchKey in sorted_by_values_levenshtein:
            matchedWords.append(loaded_ngram_dict[matchKey[0]])
        
        return matchedWords
    
    except Exception as e:
        print("Error in success ranking",e)

def get_similarity_suggestions(loaded_ngram_dict,input_ngram,count,rateLevenshtein,threshold,distanceThreshold): #maks 2 adet hata varsa geri dönüş yapıyor ve genelde 1 adet öneri sunuyor ? Değiştirilmeli mi ?  
    """
    Kullanıcının girdiği n-gram ile veri setindeki n-gramlar arasındaki benzerliği hesaplar. 
    threshold (benzerlik yüzdesi) ve distanceThreshold (maksimum Levenshtein mesafesi) eşik değerlerine göre filtreleme yapar.
    Bulunan eşleşmeleri rateLevenshtein sözlüğünde tutar ve yeterli sonuç elde edildiğinde önerileri döndürür.
    """
    global word
  
    dictValueNum=0
    try:
        rateLevenshtein.clear()

        isExact=findExactMatch(input_ngram,loaded_ngram_dict)
        if isExact is True:
                return True

        for data_ngram,data in loaded_ngram_dict.items():
            
            rate_L=levenshteinDistance(input_ngram, data_ngram)-1 #OK
            
            if rate_L>distanceThreshold:
                continue

            similarity_percentage=(1-rate_L/max(len(word),len(data_ngram)+1))*100
            
            if similarity_percentage>=threshold: #Benzerliği %75'den fazla olanları al
                rateLevenshtein[tuple(data_ngram)] = similarity_percentage    
                dictValueNum+=1

            if dictValueNum==count:
                ngramToWords_L=sortAndMatch(rateLevenshtein,count,loaded_ngram_dict)
                return ngramToWords_L
    
    except Exception as e:
         logging.error("Error in similarity detection--> {e}")
        
def findExactMatch(input_ngram,loaded_ngram_dict):
    """
    Kullanıcının girdisinin veri setinde tam olarak bulunup bulunmadığını kontrol eder. 
    Eğer tam eşleşme varsa True, aksi takdirde False döner.
    """
    if tuple(input_ngram) in loaded_ngram_dict:
        return True
    else:
        return False

def levenshteinDistance(input_ngram, data_ngram): #OK
    """
    Kullanıcının girdisiyle veri setindeki n-gram arasında Levenshtein mesafesini hesaplar. 
    İki n-gram arasındaki düzenleme maliyetini döndürür.
    """
    try:

        input_ngram = list(input_ngram) 
        data_ngram = list(data_ngram)    
        
        return editdistance.eval(input_ngram, data_ngram)
    except Exception as e:
        logging.error("Error in levenshtein distance--> {e}")

def inputToNgram(word,n=2):
    """Kullanıcının girdiği kelimeyi n-gramlara böler. 
    Varsayılan olarak 2-gram kullanır. Girdi kelimenin n-gram listesi döndürülür."""
    try:
        input_ngram = list(ngrams(word, n)) 
        return input_ngram
    
    except Exception as e:
        print(f"Error in converting input to n-grams--> {e}")

def getResults(suggestions,executeTime):
    """
    Öneriler ve çalışma süresini düzenli bir çıktı formatında döndürür. 
    Tam eşleşme varsa boş bir liste döner, öneri bulunmazsa "Not Found" mesajını içerir.
    """
    try:   
        if suggestions is True :
            return [],executeTime
        elif suggestions is None:
            return ["Not Found"],executeTime
        else:
            return suggestions,executeTime
    except Exception as e:
        pass


def execute(input_word,count,loaded_data):

    """
    Kullanıcı girdisini işleyerek öneri listesini döndürür. Kelimeyi n-gramlara dönüştürür
    ilgili veri setini yükler ve benzerlik önerilerini get_similarity_suggestions ile toplar. 
    Eşik değerler, kelime uzunluğuna veya diğer kriterlere göre ayarlanır. Çalışma süresini ölçerek önerilerle birlikte döndürür
    """
    
    rateLevenshtein = {}
    global word
    threshold=config.THRESHOLD
    distanceThreshold=config.DISTANCE_THRESHOLD
    word=input_word
    
    executeTime=0

    if count>=5:
        threshold=65
        distanceThreshold=6
   

    try:
        start=time.time()

        input_ngram=inputToNgram(word) #OK

        loaded_ngram_dict = load_dataset(loaded_data) #dict dönüyor
        
        if loaded_ngram_dict is None:
            return []       

        suggestions=get_similarity_suggestions(loaded_ngram_dict,input_ngram,count,rateLevenshtein,threshold,distanceThreshold) #OK

        end=time.time()
        
        executeTime=end-start   

        return getResults(suggestions,executeTime) 


    except Exception as e:
        print(f"Error in execute--> {e}")


