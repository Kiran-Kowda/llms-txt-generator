# LLMs.txt Generator

A web application that generates structured llms.txt files from any website. Try it now at [llms-txt-generator.streamlit.app](https://llms-txt-generator.streamlit.app/)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llms-txt-generator.streamlit.app/)

## Overview

The LLMs.txt Generator automatically extracts and structures website content into a format optimized for Large Language Models (LLMs). It creates a comprehensive llms.txt file that includes:

- Page title and description
- Content summary
- Main topics and sections
- Document structure
- Important internal links with context
- Key topics and keywords
- Metadata and usage guidelines

## Usage

Access the tool directly at [llms-txt-generator.streamlit.app](https://llms-txt-generator.streamlit.app/)

Or run locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `streamlit run app.py`
2. Open your web browser and navigate to http://localhost:8501
3. Enter a website URL in the input field
4. Click "Generate LLMs.txt" to create the structured content
5. View the generated content in either Preview or Raw Text format
6. Download the generated llms.txt file

## Features

- Smart Content Extraction : Automatically identifies and extracts main content while filtering out navigation, ads, and other non-essential elements
- Structured Output : Organizes content into clear, hierarchical sections
- Link Context : Provides contextual information for important internal links
- Keyword Extraction : Identifies key topics and themes from the content
- Documentation Detection : Automatically detects if the page contains documentation
- Clean Interface : User-friendly interface with preview and download options
- Ethical Guidelines : Includes attribution and usage guidelines in generated files

## Generated File Structure

The generated llms.txt file includes these sections:

1. Title and Description
   
   - Page title
   - Meta description
2. Overview
   
   - Brief introduction
   - Content summary
3. Main Topics
   
   - Primary headings (H1)
   - Key subject areas
4. Document Structure
   
   - Section headings (H2)
   - Subsections (H3)
5. Important Links
   
   - Internal links with context
   - Navigation structure
6. Key Topics
   
   - Extracted keywords
   - Important phrases
7. Metadata
   
   - Last updated timestamp
   - Source URL
   - Content type
   - Statistical information
8. Usage Guidelines
   
   - Attribution requirements
   - Usage recommendations

## Best Practices

- Ensure the target website is accessible
- Allow sufficient time for content analysis
- Review generated content before deployment
- Respect robots.txt and website terms of service
- Update llms.txt files periodically to maintain accuracy

## Technical Details

- Built with Streamlit
- Uses BeautifulSoup4 for HTML parsing
- Implements intelligent content extraction algorithms
- Follows markdown formatting standards
- Includes error handling and timeout protection

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - Feel free to use this tool for any purpose.