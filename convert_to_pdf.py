"""
Convert Markdown Documentation to Professional PDF
Handles proper formatting, page breaks, styling, and readability
"""

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def convert_md_to_pdf(md_file, pdf_file):
    """
    Convert markdown file to a professional, well-formatted PDF
    
    Args:
        md_file: Path to input markdown file
        pdf_file: Path to output PDF file
    """
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    
    # Create full HTML document with professional styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Disaster Data Preprocessing Documentation</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm 2cm 2.5cm 2cm;
                
                @top-center {{
                    content: "Disaster Data Preprocessing Documentation";
                    font-size: 9pt;
                    color: #666;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }}
                
                @bottom-right {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }}
            }}
            
            body {{
                font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
            }}
            
            h1 {{
                color: #1a1a1a;
                font-size: 24pt;
                font-weight: bold;
                margin-top: 0;
                margin-bottom: 20pt;
                padding-bottom: 10pt;
                border-bottom: 3px solid #2c5aa0;
                page-break-after: avoid;
            }}
            
            h2 {{
                color: #2c5aa0;
                font-size: 18pt;
                font-weight: bold;
                margin-top: 24pt;
                margin-bottom: 12pt;
                page-break-after: avoid;
                page-break-before: auto;
            }}
            
            h3 {{
                color: #2c5aa0;
                font-size: 14pt;
                font-weight: bold;
                margin-top: 18pt;
                margin-bottom: 10pt;
                page-break-after: avoid;
            }}
            
            h4 {{
                color: #444;
                font-size: 12pt;
                font-weight: bold;
                margin-top: 14pt;
                margin-bottom: 8pt;
                page-break-after: avoid;
            }}
            
            p {{
                margin: 8pt 0;
                text-align: justify;
                orphans: 3;
                widows: 3;
            }}
            
            strong {{
                font-weight: bold;
                color: #1a1a1a;
            }}
            
            em {{
                font-style: italic;
                color: #555;
            }}
            
            /* Tables */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 12pt 0;
                font-size: 9pt;
                page-break-inside: auto;
            }}
            
            thead {{
                background-color: #2c5aa0;
                color: white;
                font-weight: bold;
            }}
            
            th {{
                padding: 8pt 6pt;
                text-align: left;
                border: 1px solid #2c5aa0;
                page-break-after: avoid;
            }}
            
            td {{
                padding: 6pt;
                border: 1px solid #ddd;
                page-break-inside: avoid;
            }}
            
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            
            /* Code blocks */
            code {{
                background-color: #f5f5f5;
                padding: 2pt 4pt;
                border-radius: 3pt;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 9pt;
                color: #d63384;
            }}
            
            pre {{
                background-color: #f8f9fa;
                padding: 12pt;
                border-left: 4px solid #2c5aa0;
                border-radius: 4pt;
                overflow-x: auto;
                page-break-inside: avoid;
                margin: 12pt 0;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                color: #333;
                font-size: 8.5pt;
                line-height: 1.4;
            }}
            
            /* Lists */
            ul, ol {{
                margin: 8pt 0;
                padding-left: 20pt;
            }}
            
            li {{
                margin: 4pt 0;
                orphans: 2;
                widows: 2;
            }}
            
            /* Horizontal rules */
            hr {{
                border: none;
                border-top: 2px solid #ddd;
                margin: 20pt 0;
            }}
            
            /* Blockquotes */
            blockquote {{
                margin: 12pt 0;
                padding: 8pt 12pt;
                background-color: #f8f9fa;
                border-left: 4px solid #2c5aa0;
                font-style: italic;
                page-break-inside: avoid;
            }}
            
            /* Links */
            a {{
                color: #2c5aa0;
                text-decoration: none;
            }}
            
            a:hover {{
                text-decoration: underline;
            }}
            
            /* Special sections */
            .info-box {{
                background-color: #e7f3ff;
                border-left: 4px solid #2c5aa0;
                padding: 10pt;
                margin: 12pt 0;
                page-break-inside: avoid;
            }}
            
            .warning-box {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 10pt;
                margin: 12pt 0;
                page-break-inside: avoid;
            }}
            
            /* Checkmarks and icons */
            .checkmark {{
                color: #28a745;
                font-weight: bold;
            }}
            
            .cross {{
                color: #dc3545;
                font-weight: bold;
            }}
            
            /* Better page breaks */
            .page-break {{
                page-break-after: always;
            }}
            
            /* Table of contents */
            #table-of-contents {{
                background-color: #f8f9fa;
                padding: 15pt;
                margin: 20pt 0;
                border-radius: 5pt;
                page-break-after: always;
            }}
            
            /* First page styling */
            .title-page {{
                text-align: center;
                margin-top: 100pt;
                page-break-after: always;
            }}
            
            .title-page h1 {{
                font-size: 32pt;
                color: #2c5aa0;
                margin-bottom: 30pt;
                border: none;
            }}
            
            .title-page .meta {{
                font-size: 12pt;
                color: #666;
                line-height: 2;
                margin-top: 50pt;
            }}
            
            /* Ensure readability */
            img {{
                max-width: 100%;
                height: auto;
                page-break-inside: avoid;
            }}
            
            /* Fix for long table cells */
            td, th {{
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Convert HTML to PDF
    print("Converting to PDF...")
    HTML(string=full_html).write_pdf(
        pdf_file,
        stylesheets=[CSS(string='', font_config=font_config)],
        font_config=font_config
    )
    
    print(f"✅ PDF successfully created: {pdf_file}")
    print(f"   Size: {os.path.getsize(pdf_file) / 1024:.1f} KB")


if __name__ == "__main__":
    # File paths
    md_file = "PREPROCESSING_DOCUMENTATION.md"
    pdf_file = "PREPROCESSING_DOCUMENTATION.pdf"
    
    # Check if markdown file exists
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        exit(1)
    
    # Convert to PDF
    try:
        convert_md_to_pdf(md_file, pdf_file)
        print("\n📄 PDF generated successfully!")
        print(f"   Location: {os.path.abspath(pdf_file)}")
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        print("\nTrying alternative method...")
        
        # Fallback: Try using reportlab directly
        try:
            from reportlab.lib.pagesizes import A4, letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, cm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
            
            print("Using alternative PDF generation method...")
            print("Note: This method may not preserve all markdown formatting.")
            print("Consider installing: pip install weasyprint")
            
        except ImportError:
            print("\n⚠️  Required libraries not found.")
            print("Please install required packages:")
            print("   pip install markdown weasyprint")
            print("   or")
            print("   pip install markdown reportlab")
