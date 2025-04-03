import os
import shutil
from split_delimiter import markdown_to_html_node

def main():
    
    src = "static"  # Directory containing source files
    dest = "public"  # Directory to copy files into

    print(f"Copying files from '{src}' to '{dest}'...")

    # Call file-copying function
    copy_files_from_static(src, dest)
    generate_page("content/index.md","template.html", "public/index.html")

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

def extract_title(markdown):
        for line in markdown.splitlines():
            if line.startswith("# "):
                # Remove just the first "# " and trim any remaining whitespace
                header_text = line[2:].strip()
                return header_text
        # This will execute if no H1 header is found
        raise Exception("No H1 header found in the markdown")

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
     # Read markdown file
    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()
    
    # Read template file
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)
    





if __name__ =="__main__":
    main()