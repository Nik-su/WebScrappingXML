import os
import PyPDF2

def merge_pdfs_from_folder(folder_path, output_file):
    # Create a PDF merger object
    pdf_merger = PyPDF2.PdfMerger()

    # Get a sorted list of all PDF files in the folder
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])

    # Iterate over the PDF files and append them to the merger
    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        with open(pdf_path, 'rb') as f:
            pdf_merger.append(f)

    # Write the merged PDF to the output file
    with open(output_file, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)

    print(f"Merged {len(pdf_files)} PDFs into {output_file}")

# Example usage:
if __name__ == "__main__":
    # Folder containing the PDF files
    folder_name = 'C:\\Users\\nikhi\\Downloads\\XML Task\\CrawlAI\\pdf_texts'
    output_pdf_name = 'merged_output.pdf'

    # Call the function to merge PDFs
    merge_pdfs_from_folder(folder_name, output_pdf_name)
