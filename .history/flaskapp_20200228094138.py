# IMPORTS
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import boto3
import datetime
from flask_restful import Api as FlaskRestfulAPI, Resource, reqparse, abort
from werkzeug.datastructures import FileStorage
# CONFIG
app = Flask(__name__)

AWS_ACCESS_KEY_ID = 'AKIA37EQCWV5L44OVLEL'
AWS_SECRET_ACCESS_KEY = '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'


def upload_s3(file, bucket_name, object_key=None):
  
    # create connection
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    if object_key is None:
        date_obj = datetime.date.today()
        object_key = ('{}/{}/{}/{}'.format(date_obj.strftime('%Y'), date_obj.strftime('%m'), date_obj.strftime('%d'), file))

    try:
        s3.upload_file(file, bucket_name, object_key)
        print("Upload Successful")
        os.remove(file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False

    return True



@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # put_parser = reqparse.RequestParser()
        # put_parser.add_argument('image', required=True, type=FileStorage, location='files')
        # There is no file selected to upload
        if "file" not in request.files:
            return "No user_file key in request.files"
        print(request.files)
        file = request.files['file']
        file_n = file
        file_n.save(file.filename)
        # print(file_n)

        # There is no file selected to upload
        if file.filename == "":
            return "Please select a file"
        
        file.save(file.filename)

        # File is selected, upload to S3 and show S3 URL
        # if file and allowed_file(file.filename):
        print(type(file.filename))
        file.filename = secure_filename(file.filename)
        output = upload_s3(file.filename, "rishabh--netscout")
        return str(output)
    else:
        print("Not allowed")
    return "Success"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

    # http://32162952.ngrok.io
    # curl -X POST -F 'file=@/Users/rish/Desktop/boto3_s3/flask_file.py' 'http://32162952.ngrok.io/upload'