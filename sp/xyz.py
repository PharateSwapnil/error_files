if os.path.isdir(temp_dir):
            with ThreadPoolExecutor() as executor:
                for root, dirs, files in os.walk(self.path):
                    for filename in files:
                        print(f"Processing file: {filename}")
                        if any(filename.endswith(lang) for lang in self.supported_languages.keys()):
                            executor.submit(self.process_file, root, filename)

        # Re-zip the processed files
        with zipfile.ZipFile(zip_path, 'a') as zip_ref:  # Change 'w' to 'a'
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_ref.write(file_path, os.path.relpath(file_path, temp_dir))

        # Clone the re-zipped file
        cloned_zip_path = os.path.join(cloned_folder_path, os.path.basename(zip_path))
        
        # Ensure the directory exists
        os.makedirs(cloned_folder_path, exist_ok=True)
        
        shutil.copyfile(zip_path, cloned_zip_path)