import logging

from flask import Flask, request, jsonify

from edk_autocomplete import execute
from load_data import load_all_pkl_files

import config

config.setup_logging()

app = Flask(__name__)

loaded_data=load_all_pkl_files()
logging.info("Data successfully deserialized.")
   
@app.route("/", methods=["GET", "POST"])
   
def run_autocomplete():

   """
   Flask sunucusunun ana rotasıdır ve kullanıcının girdiği kelimeyi alıp, öneri listesini döndürür.
   """

   try:

      count = int(request.form.get("count"))
      word = request.form.get("word")

      if "I" in word:
         mytable=str.maketrans("I","ı")
         word=word.translate(mytable)
      elif "İ" in word:
         mytable=str.maketrans("İ","i")
         word=word.translate(mytable)

      word=word.lower().strip()
      
      suggestions,execTime = execute(word, count,loaded_data)

      logging.info("Code executed successfully.")
      
      return jsonify({"Oneriler": suggestions,"Execution Time":execTime}), 200

   except Exception as e:

      logging.error(f"app.py--> {e}")
      return jsonify({"Error": f"{e}"}), 500

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=False)
