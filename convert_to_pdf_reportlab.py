"""
Convert Markdown Documentation to Professional PDF using ReportLab
Windows-compatible solution that doesn't require external libraries
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import os


def parse_markdown_to_flowables(md_file, styles):
    """
    Parse markdown file and convert to ReportLab flowables
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    flowables = []
    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    in_table = False
    table_lines = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                # Add code block
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    code_para = Paragraph(
                        f'<font name="Courier" size="8" color="#333333">{escape_html(code_text)}</font>',
                        styles['Code']
                    )
                    flowables.append(Spacer(1, 0.1*inch))
                    flowables.append(code_para)
                    flowables.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue
        
        # Tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        elif in_table and not ('|' in line):
            # End of table
            in_table = False
            if len(table_lines) > 1:
                table = create_table_from_markdown(table_lines, styles)
                if table:
                    flowables.append(Spacer(1, 0.1*inch))
                    flowables.append(table)
                    flowables.append(Spacer(1, 0.2*inch))
            table_lines = []
        
        # Skip if still in table
        if in_table:
            i += 1
            continue
        
        # Empty lines
        if not line.strip():
            flowables.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Horizontal rules
        if line.strip() in ['---', '***', '___']:
            flowables.append(Spacer(1, 0.15*inch))
            i += 1
            continue
        
        # Headers
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            text = format_markdown_text(text)
            
            if level == 1:
                flowables.append(PageBreak())
                flowables.append(Spacer(1, 0.3*inch))
                flowables.append(Paragraph(text, styles['Heading1']))
                flowables.append(Spacer(1, 0.2*inch))
            elif level == 2:
                flowables.append(Spacer(1, 0.3*inch))
                flowables.append(Paragraph(text, styles['Heading2']))
                flowables.append(Spacer(1, 0.15*inch))
            elif level == 3:
                flowables.append(Spacer(1, 0.2*inch))
                flowables.append(Paragraph(text, styles['Heading3']))
                flowables.append(Spacer(1, 0.1*inch))
            elif level == 4:
                flowables.append(Spacer(1, 0.15*inch))
                flowables.append(Paragraph(text, styles['Heading4']))
                flowables.append(Spacer(1, 0.08*inch))
            i += 1
            continue
        
        # Lists
        if re.match(r'^[\-\*\+]\s+', line) or re.match(r'^\d+\.\s+', line):
            text = re.sub(r'^[\-\*\+\d\.]+\s+', '', line)
            text = format_markdown_text(text)
            bullet = '•'
            para = Paragraph(f'{bullet} {text}', styles['BodyText'])
            flowables.append(para)
            i += 1
            continue
        
        # Regular paragraphs
        if line.strip():
            text = format_markdown_text(line)
            para = Paragraph(text, styles['BodyText'])
            flowables.append(para)
            flowables.append(Spacer(1, 0.08*inch))
        
        i += 1
    
    return flowables


def create_table_from_markdown(lines, styles):
    """
    Convert markdown table to ReportLab Table
    """
    # Parse table data
    data = []
    for line in lines:
        # Skip separator lines (e.g., |---|---|)
        if re.match(r'^\|[\s\-:]+\|', line):
            continue
        
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells:
            # Format cell text
            formatted_cells = []
            for cell in cells:
                cell = format_markdown_text(cell)
                formatted_cells.append(cell)
            data.append(formatted_cells)
    
    if not data or len(data) < 2:
        return None
    
    # Create table with alternating row colors
    table_data = []
    for row in data:
        table_row = []
        for cell in row:
            para = Paragraph(f'<font size="8">{cell}</font>', styles['BodyText'])
            table_row.append(para)
        table_data.append(table_row)
    
    # Calculate column widths
    num_cols = len(data[0])
    col_widths = [A4[0] * 0.85 / num_cols] * num_cols
    
    # Create table
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Style table
    table_style = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # All cells
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    
    # Alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.append(
                ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
            )
    
    table.setStyle(TableStyle(table_style))
    
    return table


def format_markdown_text(text):
    """
    Convert markdown formatting to ReportLab XML tags
    """
    # Escape HTML entities first
    text = escape_html(text)
    
    # Bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    
    # Italic (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    
    # Inline code (`code`) - Note: backColor instead of backgroundColor for ReportLab
    text = re.sub(
        r'`(.+?)`', 
        r'<font name="Courier" size="9" color="#d63384"> \1 </font>', 
        text
    )
    
    # Checkmarks and crosses
    text = text.replace('✅', '<font color="green">✓</font>')
    text = text.replace('❌', '<font color="red">✗</font>')
    
    return text


def escape_html(text):
    """Escape HTML special characters"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def create_custom_styles():
    """
    Create custom styles for the PDF
    """
    styles = getSampleStyleSheet()
    
    # Modify existing Heading 1
    styles['Heading1'].fontSize = 24
    styles['Heading1'].textColor = colors.HexColor('#1a1a1a')
    styles['Heading1'].spaceAfter = 12
    styles['Heading1'].spaceBefore = 0
    styles['Heading1'].fontName = 'Helvetica-Bold'
    styles['Heading1'].keepWithNext = True
    
    # Modify existing Heading 2
    styles['Heading2'].fontSize = 18
    styles['Heading2'].textColor = colors.HexColor('#2c5aa0')
    styles['Heading2'].spaceAfter = 10
    styles['Heading2'].spaceBefore = 20
    styles['Heading2'].fontName = 'Helvetica-Bold'
    styles['Heading2'].keepWithNext = True
    
    # Add Heading 3
    if 'Heading3' not in styles:
        styles.add(ParagraphStyle(
            name='Heading3',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=8,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            keepWithNext=True
        ))
    else:
        styles['Heading3'].fontSize = 14
        styles['Heading3'].textColor = colors.HexColor('#2c5aa0')
        styles['Heading3'].spaceAfter = 8
        styles['Heading3'].spaceBefore = 15
        styles['Heading3'].fontName = 'Helvetica-Bold'
        styles['Heading3'].keepWithNext = True
    
    # Add Heading 4
    if 'Heading4' not in styles:
        styles.add(ParagraphStyle(
            name='Heading4',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#444444'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            keepWithNext=True
        ))
    else:
        styles['Heading4'].fontSize = 12
        styles['Heading4'].textColor = colors.HexColor('#444444')
        styles['Heading4'].spaceAfter = 6
        styles['Heading4'].spaceBefore = 12
        styles['Heading4'].fontName = 'Helvetica-Bold'
        styles['Heading4'].keepWithNext = True
    
    # Body text
    if 'BodyText' not in styles:
        styles.add(ParagraphStyle(
            name='BodyText',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
    
    # Code
    styles['Code'].fontSize = 8
    styles['Code'].leading = 11
    styles['Code'].leftIndent = 20
    styles['Code'].rightIndent = 20
    styles['Code'].backgroundColor = colors.HexColor('#f8f9fa')
    styles['Code'].fontName = 'Courier'
    styles['Code'].textColor = colors.HexColor('#333333')
    
    return styles


def add_page_number(canvas, doc):
    """
    Add page numbers and header to each page
    """
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    canvas.drawString(
        2.5*cm, 
        A4[1] - 1.5*cm, 
        "Disaster Data Preprocessing Documentation"
    )
    
    # Page number
    page_num = f"Page {canvas.getPageNumber()}"
    canvas.drawRightString(
        A4[0] - 2*cm,
        1.5*cm,
        page_num
    )
    
    canvas.restoreState()


def convert_md_to_pdf(md_file, pdf_file):
    """
    Main conversion function
    """
    print(f"📄 Reading markdown file: {md_file}")
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )
    
    # Create styles
    styles = create_custom_styles()
    
    # Parse markdown and create flowables
    print("🔄 Converting markdown to PDF format...")
    flowables = parse_markdown_to_flowables(md_file, styles)
    
    # Build PDF
    print("📝 Generating PDF...")
    doc.build(flowables, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    print(f"✅ PDF successfully created: {pdf_file}")
    print(f"   Size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
    print(f"   Location: {os.path.abspath(pdf_file)}")


if __name__ == "__main__":
    md_file = "PREPROCESSING_DOCUMENTATION.md"
    pdf_file = "PREPROCESSING_DOCUMENTATION.pdf"
    
    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        exit(1)
    
    try:
        convert_md_to_pdf(md_file, pdf_file)
        print("\n✨ PDF generation complete!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
