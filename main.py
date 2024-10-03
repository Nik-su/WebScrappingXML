import os
import asyncio
import xml.etree.ElementTree as ET
from fpdf import FPDF
from crawl4ai import AsyncWebCrawler

class Scraper:
    def __init__(self, pdf_directory='pdf_texts'):
        # Create a directory for saving PDF texts
        self.pdf_directory = pdf_directory
        os.makedirs(self.pdf_directory, exist_ok=True)

    def extract_urls_from_xml(self, xml_file):
        """Extract URLs from the provided XML file."""
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Define the namespaces for XML parsing
        namespace = {'default': 'yoururlnamespaceforxml'}

        # Extract URLs from the XML file using XPath with the specified namespace
        urls = [elem.text for elem in root.findall('.//default:loc', namespaces=namespace)]
        return urls

    def save_text_to_pdf(self, text, filename):
        """Save extracted text content to a PDF file."""
        pdf = FPDF()
        pdf.add_page()

        # Load and set a Unicode font like DejaVuSans to handle non-ASCII characters
        font_path = "...dejavu-sans.book.ttf"  # Path to your font
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)

        # Add the extracted text to the PDF
        pdf.multi_cell(0, 10, text)

        # Save the PDF file in the designated directory
        pdf_output_path = os.path.join(self.pdf_directory, filename)
        pdf.output(pdf_output_path)
        print(f"PDF saved: {pdf_output_path}")

    async def scrape_and_save(self, urls):
        """Scrape content from URLs asynchronously and save it as PDF."""
        async with AsyncWebCrawler(verbose=True) as crawler:
            for url in urls:
                try:
                    # Use AsyncWebCrawler to fetch text from the given URL
                    result = await crawler.arun(url=url)
                    combined_text = result.markdown  # Extracted text from the website

                    # Clean and generate a valid filename from the URL
                    pdf_filename = f"{url.split('/')[-2]}_{url.split('/')[-1]}.pdf".replace(" ", "_").replace("?", "").replace(":", "_").replace("&", "_")

                    # Save the extracted content into a PDF
                    self.save_text_to_pdf(combined_text, pdf_filename)

                except Exception as e:
                    # Handle any errors during scraping and continue with the next URL
                    print(f"An error occurred while processing URL: {url}\nError: {str(e)}")

# Define the main async function
async def main():
    """Main function to load URLs from an XML file and initiate scraping."""
    # Initialize Scraper with the directory for saving PDF files
    scraper = Scraper(pdf_directory='pdf_texts')

    # Load URLs from the XML file
    xml_file = '...XML Sitemap.xml'  # Update the path to your XML file
    urls = scraper.extract_urls_from_xml(xml_file)
    print(f'URLs extracted: {urls}')
    print(f"Length of URLs: {len(urls)}")

    # Scrape the content from each URL and save it as PDF
    await scraper.scrape_and_save(urls)

# If this is run directly, execute the main function
if __name__ == "__main__":
    asyncio.run(main())
