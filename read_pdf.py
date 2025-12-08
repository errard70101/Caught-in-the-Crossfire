import pypdf
import sys

pdf_path = 'references/Davidson_Hou_Koop_2025_Investigating-Economic-Uncertainty-Using-Stochastic-Volatility-in-Mean-VARs-The-Importance-of-Model-Size-Order-Invariance-and-Classification.pdf'
output_path = 'pdf_content.txt'

try:
    reader = pypdf.PdfReader(pdf_path)
    with open(output_path, 'w') as f:
        for page in reader.pages:
            f.write(page.extract_text())
            f.write('\n\n')
    print(f"Successfully wrote PDF content to {output_path}")
except Exception as e:
    print(f"Error reading PDF: {e}")
