"""
PDF Converter Tool
==================
Converts text files (CV and cover letter) to PDF format using ReportLab.
This tool is designed to be used by the Job Seeker Agent.
"""

from pathlib import Path
from typing import Type, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas


class PDFConverterInput(BaseModel):
    """Input schema for PDF conversion"""
    txt_file_path: str = Field(description="Path to the txt file to convert (CV or cover letter)")
    output_pdf_path: str = Field(description="Path where the PDF should be saved")
    document_type: str = Field(
        description="Type of document: 'cv' or 'cover_letter'",
        default="cv"
    )


def convert_txt_to_pdf(
    txt_file_path: str,
    output_pdf_path: str,
    document_type: str = "cv"
) -> str:
    """
    Converts a text file to a professionally formatted PDF.
    
    Args:
        txt_file_path: Path to the input txt file
        output_pdf_path: Path for the output PDF file
        document_type: Type of document ('cv' or 'cover_letter')
        
    Returns:
        Success message with PDF path
    """
    try:
        # Read the text file
        txt_path = Path(txt_file_path)
        if not txt_path.exists():
            return f"Error: File not found: {txt_file_path}"
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf_path = Path(output_pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for the 'Flowable' objects
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles for better formatting
        style_normal = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )
        
        style_heading = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=14,
            leading=16,
            spaceAfter=12,
            spaceBefore=12,
            textColor='#000000',
            fontName='Helvetica-Bold'
        )
        
        style_name = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=16,
            leading=20,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor='#1a1a1a',
            fontName='Helvetica-Bold'
        )
        
        style_contact = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor='#333333',
        )
        
        # Process content line by line
        lines = content.strip().split('\n')
        
        # For CV, first line is usually the name
        if document_type == "cv" and lines:
            # First line as name (larger, bold)
            name_line = lines[0].strip()
            if name_line and not name_line.startswith('---'):
                story.append(Paragraph(name_line, style_name))
                lines = lines[1:]
            
            # Next few lines might be contact info
            contact_lines = []
            for i, line in enumerate(lines[:5]):  # Check first 5 lines
                line = line.strip()
                if line and ('|' in line or '@' in line or '+' in line or 'linkedin' in line.lower() or 'github' in line.lower()):
                    contact_lines.append(line)
                elif line and not line.startswith('---'):
                    break
            
            if contact_lines:
                contact_text = '<br/>'.join(contact_lines)
                story.append(Paragraph(contact_text, style_contact))
                lines = lines[len(contact_lines):]
                story.append(Spacer(1, 0.2*inch))
        
        # Process remaining lines
        for line in lines:
            line = line.strip()
            
            if not line:
                # Empty line - add small space
                story.append(Spacer(1, 0.1*inch))
            elif line.startswith('---'):
                # Separator line - add space
                story.append(Spacer(1, 0.15*inch))
            elif line.isupper() and len(line) < 50:
                # Section header (all caps, short)
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(line, style_heading))
            elif line.startswith('#'):
                # Markdown-style header
                header_text = line.lstrip('#').strip()
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(header_text, style_heading))
            else:
                # Regular paragraph
                # Escape special characters for ReportLab
                line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(line, style_normal))
        
        # Build PDF
        doc.build(story)
        
        # Get file size for confirmation
        file_size_kb = pdf_path.stat().st_size / 1024
        
        return f"✅ PDF created successfully: {pdf_path.name} ({file_size_kb:.1f} KB)"
        
    except Exception as e:
        return f"❌ Error converting to PDF: {str(e)}"


@tool("convert_to_pdf", return_direct=False)
def convert_to_pdf_tool(
    txt_file_path: str,
    output_pdf_path: str,
    document_type: str = "cv"
) -> str:
    """
    Converts a text file (CV or cover letter) to a professionally formatted PDF.
    Use this tool after generating CV and cover letter to create PDF versions.
    
    Args:
        txt_file_path: Path to the txt file to convert
        output_pdf_path: Path where the PDF should be saved
        document_type: Type of document - 'cv' or 'cover_letter'
        
    Returns:
        Success message with PDF path
    """
    return convert_txt_to_pdf(txt_file_path, output_pdf_path, document_type)


class PDFConverterTool(BaseTool):
    """
    LangChain tool for converting text files to PDF format.
    Optimized for CV and cover letter formatting.
    """
    name: str = "convert_to_pdf"
    description: str = """Converts a text file (CV or cover letter) to a professionally formatted PDF. 
Use this after generating the CV and cover letter txt files. 
Provide the txt file path and desired PDF output path."""
    args_schema: Type[BaseModel] = PDFConverterInput
    return_direct: bool = False
    
    def _run(
        self,
        txt_file_path: str,
        output_pdf_path: str,
        document_type: str = "cv"
    ) -> str:
        """Synchronous run"""
        return convert_txt_to_pdf(txt_file_path, output_pdf_path, document_type)
    
    def _arun(
        self,
        txt_file_path: str,
        output_pdf_path: str,
        document_type: str = "cv"
    ) -> str:
        """Async run (not implemented, raises error)"""
        raise NotImplementedError("Async not supported for PDF conversion")


# Standalone function for direct use (non-agent usage)
def convert_application_materials_to_pdf(job_folder: str) -> dict:
    """
    Convenience function to convert both CV and cover letter in a job folder.
    
    Args:
        job_folder: Path to the job application folder
        
    Returns:
        Dictionary with conversion results for cv and cover_letter
    """
    folder_path = Path(job_folder)
    results = {}
    
    # Convert CV
    cv_txt = folder_path / "cv.txt"
    if cv_txt.exists():
        cv_pdf = folder_path / "cv.pdf"
        results['cv'] = convert_txt_to_pdf(str(cv_txt), str(cv_pdf), "cv")
    else:
        results['cv'] = "CV txt file not found"
    
    # Convert cover letter
    cover_txt = folder_path / "cover_letter.txt"
    if cover_txt.exists():
        cover_pdf = folder_path / "cover_letter.pdf"
        results['cover_letter'] = convert_txt_to_pdf(str(cover_txt), str(cover_pdf), "cover_letter")
    else:
        results['cover_letter'] = "Cover letter txt file not found"
    
    return results
