import os
import shutil
from split_delimiter import markdown_to_html_node

def main():
    import sys
    
    # Get the base path from command line or use default
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    src = "static"  # Directory containing source files
    dest = "docs"  # Directory to copy files into

    print(f"Copying files from '{src}' to '{dest}'...")

    # Call file-copying function
    copy_files_from_static(src, dest)
    process_content_directory("content", "template.html", dest, basepath)

    print("Static files copied successfully!")



def copy_files_from_static(src, dest):
    # Clean and recreate destination directory if it doesn't exist
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Loop through all items in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item) 
        dest_path = os.path.join(dest, item)
        
        if os.path.isdir(src_path):  # If the item is a directory
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)  
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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
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

        # Replace root-relative URLs with base path
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)

def process_content_directory(content_dir, template_path, output_dir, basepath="/"):
    print(f"Processing content directory: {content_dir}")
    for root, dirs, files in os.walk(content_dir):
        print(f"Checking directory: {root}")
        print(f"Files found: {files}")
        for file in files:
            # Only process markdown files
            if file.endswith('.md'):
                print(f"Processing markdown file: {file}")
                # Get the full path to the markdown file
                md_path = os.path.join(root, file)
                
                # Calculate the relative path from content_dir
                rel_path = os.path.relpath(md_path, content_dir)
                print(f"Relative path: {rel_path}")
                
                # Determine the destination path in public_dir
                dest_rel_path = os.path.splitext(rel_path)[0] + '.html'
                dest_path = os.path.join(output_dir, dest_rel_path)
                print(f"Destination path: {dest_path}")
                
                # Generate the HTML page
                generate_page(md_path, template_path, dest_path, basepath)

if __name__ =="__main__":
    main()