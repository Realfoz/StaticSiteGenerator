import os
import shutil

def main():
    
    src = "/home/scott/projects/github.com/bootdotdev/StaticSiteGenerator/static"  # Directory containing source files
    dest = "/home/scott/projects/github.com/bootdotdev/StaticSiteGenerator/public"  # Directory to copy files into

    print(f"Copying files from '{src}' to '{dest}'...")

    # Call file-copying function
    copy_files_from_static(src, dest)

    print("Static files copied successfully!")



def copy_files_from_static(src, dest):
    # Clean and recreate destination directory
    if os.path.exists(dest):
        shutil.rmtree(dest)  # Delete destination directory to start fresh
    os.mkdir(dest)  # Recreate the root directory 

    # Loop through all items in the source directory
    for item in os.listdir(src):
        
        src_path = os.path.join(src, item) 
        dest_path = os.path.join(dest, item)
        

        if os.path.isdir(src_path):  # If the item is a directory
            
            os.mkdir(dest_path)  
            # Recursively copy the contents of the directory
            copy_files_from_static(src_path, dest_path)
        else:  # If the item is a file
            
            shutil.copy(src_path, dest_path)  # Copy the file to the destination
        

if __name__ =="__main__":
    main()