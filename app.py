# Importing the required libraries
import os
import csv
import PyPDF2
import pytesseract
from PIL import Image
from flask import Flask, request

# Creating a Flask app object
app = Flask(__name__)

# Defining a function to extract text from PDF files
def pdf_to_text(pdf_file):
    # Creating a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file.stream)
    # Initializing an empty string to store the text
    pdf_text = ""
    # Looping through all the pages of the PDF file
    for page in range(pdf_reader.numPages):
        # Getting the page object
        pdf_page = pdf_reader.getPage(page)
        # Extracting the text from the page
        pdf_text += pdf_page.extractText()
    # Returning the text
    return pdf_text

# Defining a function to extract text from image files using OCR
def image_to_text(image_file):
    # Opening the image file using PIL
    image = Image.open(image_file)
    # Converting the image to grayscale
    image = image.convert("L")
    # Extracting the text from the image using pytesseract
    image_text = pytesseract.image_to_string(image)
    # Returning the text
    return image_text

# Defining a route for the home page
@app.route("/")
def home():
    # Returning a simple HTML form to upload files
    return """
    <html>
        <head>
            <title>File to CSV Converter</title>
        </head>
        <body>
            <h1>File to CSV Converter</h1>
            <p>Select one or more files to upload and convert to CSV format.</p>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple>
                <input type="submit" value="Convert">
            </form>
        </body>
    </html>
    """

# Defining a route for the conversion process
@app.route("/convert", methods=["POST"])
def convert():
    # Getting the uploaded files from the request object
    uploaded_files = request.files.getlist("files")
    # Creating a list to store the extracted data
    data_list = []
    # Looping through all the uploaded files
    for file in uploaded_files:
        # Getting the file name and extension
        file_name, file_ext = os.path.splitext(file.filename)
        # Checking the file extension and calling the appropriate function to extract text
        if file_ext == ".pdf":
            # Extracting text from PDF file
            file_text = pdf_to_text(file)
        elif file_ext in [".jpg", ".png", ".bmp"]:
            # Extracting text from image file using OCR
            file_text = image_to_text(file)
        else:
            # Skipping other file types
            continue
        # Appending the file name and text to the data list as a tuple
        data_list.append((file_name, file_text))
    
    # Defining the output file path
    output_path = "C:/Users/edyk7/OneDrive/Desktop/app/output.csv"

    # Writing the data list to a csv file
    with open(output_path, "a", newline="", encoding="utf-16 BE") as output_file:
        # Creating a csv writer object
        csv_writer = csv.writer(output_file)
        # Writing the data rows
        csv_writer.writerows(data_list)

    # Printing a message to indicate completion
    return f"The program has finished running. The output csv file is updated at {output_path}"

# Running the app in debug mode on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
