from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os

def generate_inspection_report(row):
    pdf = FPDF()
    pdf.add_page()

    # Header background
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_xy(10, 10)
    pdf.cell(0, 10, 'AMPLYTICS', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_x(10)
    pdf.cell(0, 8, 'Smart Meter Intelligence Platform - Inspection Report', ln=True)

    # Reset
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, 50)

    # Metadata
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%d %B %Y, %I:%M %p")}', ln=True)
    pdf.cell(0, 6, f'Report ID: RPT-{row["meter_id"]}-{datetime.now().strftime("%Y%m%d")}', ln=True)
    pdf.ln(5)

    # Risk colors
    risk_colors = {
        'High': (220, 38, 38),
        'Medium': (234, 179, 8),
        'Low': (34, 197, 94)
    }
    color = risk_colors.get(row['risk_level'], (100, 100, 100))

    # Meter Details section
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Meter Details', ln=True, fill=True)
    pdf.ln(2)

    details = [
        ('Meter ID', str(row['meter_id'])),
        ('Feeder Zone', str(row['feeder_zone'])),
        ('Signals Triggered', str(row['signal_count'])),
    ]

    for label, value in details:
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(60, 8, label + ':', border=0)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, value, ln=True)

    # Risk level with color
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Risk Level:', border=0)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*color)
    pdf.cell(0, 8, str(row['risk_level']).upper(), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # Decision Support section
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Decision Support Analysis', ln=True, fill=True)
    pdf.ln(3)

    explanation = str(row['explanation']).replace('\\n', '\n')
    lines = explanation.split('\n')

    label_colors = {
        'WHY:': (220, 38, 38),
        'HOW SERIOUS:': (234, 179, 8),
        'WHAT TO DO:': (34, 197, 94)
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue
        matched = False
        for label, lcolor in label_colors.items():
            if line.startswith(label):
                # Print label in color
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_text_color(*lcolor)
                pdf.cell(0, 8, label, ln=True)
                # Print content indented
                pdf.set_font('Helvetica', '', 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(15)
                pdf.multi_cell(0, 8, line[len(label):].strip())
                pdf.ln(2)
                matched = True
                break
        if not matched:
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 8, line)

    # Footer
    pdf.set_y(-20)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, 'BESCOM - AI for Bharat 2026 | Amplytics Team', align='C')

    filename = f'reports/inspection_{row["meter_id"]}.pdf'
    pdf.output(filename)
    return filename

if __name__ == '__main__':
    os.makedirs('reports', exist_ok=True)
    df = pd.read_csv('../data/alerts_with_explanations.csv')
    high_risk = df[df['risk_level'] == 'High'].iloc[0]
    filename = generate_inspection_report(high_risk)
    print(f'Report generated: {filename}')