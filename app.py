import os
from flask import Flask, redirect, render_template, request
from main import generate_keys, save_keys, load_private_key, load_public_key, sign_document, verify_document

app = Flask(__name__, static_folder=os.path.abspath("static"))
app.config["UPLOAD"] = os.path.abspath("upload")

@app.route("/", methods=["GET", "POST"])
def main():
   if request.method == "POST":
      try:
         document = request.files["file-input"]
         document_path = os.path.join(app.config["UPLOAD"], document.filename) # type: ignore
         document.save(document_path)
      except Exception as e:
         print(f"Error saving uploaded file: {e}")

      try:
         key = request.files["private-key"]
         key_path = os.path.join(app.config["UPLOAD"], key.filename) # type: ignore
         key.save(key_path)
         print(key_path)
         
      except Exception as e:
         print(f"Error saving key file: {e}")
         
      result = sign_document(document_path)
      
      return render_template("index.html", result=result)
   return render_template("index.html")

@app.route("/generatekey")
def generate_key_page():
   private_key, public_key = generate_keys()
   save_keys(private_key, public_key, "private_key.pem", "public_key.pem")
   
   return redirect("/")

@app.route("/validasi", methods=["GET", "POST"])
def validate_page():
   if request.method == "POST":
      
      try:
         document = request.files["file-input"]
         document_path = os.path.join(app.config["UPLOAD"], document.filename) # type: ignore
         document.save(document_path)
      except Exception as e:
         print(f"Error saving uploaded file: {e}")

      try:
         key = request.files["public-key"]
         key_path = os.path.join(app.config["UPLOAD"], key.filename) # type: ignore
         key.save(key_path)
         print(key_path)
         
      except Exception as e:
         print(f"Error saving key file: {e}")
         
      result = verify_document(document_path)
      
      return render_template("validasi.html", result=result)
   
   return render_template("validasi.html")

