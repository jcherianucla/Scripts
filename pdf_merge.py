"""
Author: Jahan Kuruvilla Cherian
Version: 1.0
Created at: 11/9/2017
Email: jcherian@ucla.edu
Purpose:
    Unzips an archive of all the resumes (as stored on Google Drive)
    and then gets all the pdf files and merges them together.
Bugs/Future Improvements:
    Only works with .pdf files, and so ignores .doc(x) resumes - try convert this to PDF and continue
    EOF failures with some resumes - Due to an issue with PyPDF2, some resumes face issues. These have to be manually merged
"""

import shutil, zipfile
import sys, glob, os

WORK_DIR = os.getcwd()
RESUME_DIR = WORK_DIR + "/resumes"
FINAL = "resume_book.pdf"
# Manually merge all the corrupt pdfs with resume_book.pdf
corrupt_pdfs = []

def unzip(filename):
    zip_ref = zipfile.ZipFile(filename, 'r')
    for member in zip_ref.namelist():
        m_filename = os.path.basename(member)
        # Skip directories
        if not m_filename:
            continue
        # Copy over each zip file content into file
        src = zip_ref.open(member)
        dst = file(os.path.join(RESUME_DIR, m_filename), "wb")
        with src, dst:
            shutil.copyfileobj(src, dst)
    zip_ref.close()

def filterPDFs(directory):
    os.chdir(RESUME_DIR)
    # Only get all the pdf files
    return [f for f in glob.glob("*.pdf")]

def merge(files):
    from PyPDF2 import PdfFileReader, PdfFileWriter, utils
    writer = PdfFileWriter()
    for pdf in files:
        print "Reading " + pdf + " ..."
        try:
            doc = PdfFileReader(open(pdf, 'rb'), strict=False)
        except utils.PdfReadError:
            # Couldn't find EOF, manually handle these files
            corrupt_pdfs.append(pdf)
            continue
        # Write each page in the current pdf
        for i in xrange(doc.getNumPages()):
            writer.addPage(doc.getPage(i))
        print "Wrote " + pdf + " ..."
    # Move back to working directory
    os.chdir(WORK_DIR)
    # Create a file of all pdf content
    with open(FINAL, 'wb') as out:
        writer.write(out)

def main():
    if len(sys.argv) != 2:
        print "Usage: python pdf_merge <zipfile>"
        return
    if not os.path.exists(RESUME_DIR):
        os.makedirs(RESUME_DIR)
    zip_loc = sys.argv[1]
    unzip(zip_loc)
    merge(filterPDFs(RESUME_DIR))
    print corrupt_pdfs
if __name__ == "__main__":
    main()
