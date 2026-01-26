UPLOAD_DIR = "uploads/certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)

file_path = os.path.join(UPLOAD_DIR, file_hash + "_" + file.filename)

with open(file_path, "wb") as f:
    f.write(content)
