from tenacity import retry, stop_after_attempt, wait_exponential
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat, AnalyzeResult, DocumentAnalysisFeature

# Configure logging
import logging
from config import DefaultConfig
import fitz  # PyMuPDF



logger = logging.getLogger("orix-poc-logger")

def initialize_document_intelligence_client(endpoint: str, key: str) -> DocumentIntelligenceClient:
    """
    Initializes the Azure Document Intelligence Client.

    Args:
        endpoint (str): The endpoint URL for the Azure Document Intelligence service.
        key (str): The API key for the Azure Document Intelligence service.

    Returns:
        DocumentIntelligenceClient: The initialized client.
    """
    try:
        client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
        return client
    except Exception as e:
        logger.error("Exception while initializing Document Intelligence client: %s", e)
        raise



@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_text_from_pdf_with_doc_intelligence(pdf_file_path: str):
    try:

        config = DefaultConfig()
        MAX_PAGES_PROCESSED_PER_PDF = int(config.MAX_PAGES_PROCESSED_PER_PDF)

        doc = fitz.open(pdf_file_path)

        # Get the number of pages
        num_pages = doc.page_count

        if num_pages < MAX_PAGES_PROCESSED_PER_PDF:
            MAX_PAGES_PROCESSED_PER_PDF = num_pages



        document_intelligence_client = initialize_document_intelligence_client(config.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT_1, config.AZURE_DOCUMENT_INTELLIGENCE_KEY_1)

        with open(pdf_file_path, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout",
                analyze_request=f,
                pages=f"1-{int(MAX_PAGES_PROCESSED_PER_PDF)}",
                output_content_format=ContentFormat.MARKDOWN,
                # features=[DocumentAnalysisFeature.OCR_HIGH_RESOLUTION],
                content_type="application/octet-stream",
            )

        result: AnalyzeResult = poller.result()

        # Initialize a string to hold the full text with page numbers
        extracted_text = ""
        PAGE_SEPARATOR = "\n==============================\n"
        # Iterate through each page in the result
        for page in result.pages:
            page_number = page.page_number
            # Extract the content for the current page using spans
            page_text = ""
            for span in page.spans:
                offset = span.offset
                length = span.length
                page_text += result.content[offset : offset + length]
            # Insert the page number and page content into the text
            extracted_text += PAGE_SEPARATOR
            extracted_text += f"<!-- PdfDocumentPageNumber {page_number} -->"
            extracted_text += PAGE_SEPARATOR
            extracted_text += page_text
            extracted_text += "\n\n"

        # text = result.content
        return extracted_text, result.as_dict()

    except Exception as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to trigger the retry logic
