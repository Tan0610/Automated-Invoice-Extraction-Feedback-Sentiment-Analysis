#!/usr/bin/env python3
"""Generate 5 sample invoice PDFs using fpdf2."""

from fpdf import FPDF
import os

OUTPUT_DIR = "/mnt/d/NLP_PROJECT/sample_invoices"


class InvoicePDF(FPDF):
    def header(self):
        pass  # We handle headers manually per invoice

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def draw_invoice(pdf, invoice_data):
    pdf.add_page()
    page_width = pdf.w - 20  # 10mm margin each side

    # ── Company Name (logo placeholder) ──
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 12, invoice_data["from_company"], ln=True)

    # Thin accent line
    pdf.set_draw_color(25, 60, 120)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 10 + page_width, pdf.get_y())
    pdf.ln(4)

    # ── INVOICE title + number / dates (right-aligned block) ──
    y_top = pdf.get_y()

    # Left side: From address
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "From:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    for line in invoice_data["from_address"]:
        pdf.cell(95, 5, line, ln=True)

    y_after_from = pdf.get_y()

    # Right side: Invoice metadata
    pdf.set_y(y_top)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 8, f"INVOICE  {invoice_data['invoice_no']}", align="R", ln=True)
    pdf.ln(2)

    meta_labels = ["Date:", "Due Date:", "Payment Terms:"]
    meta_values = [
        invoice_data["date"],
        invoice_data["due_date"],
        invoice_data.get("payment_terms", "Net 30"),
    ]
    for label, value in zip(meta_labels, meta_values):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(80, 80, 80)
        # Right-align a label-value pair
        pdf.set_x(pdf.w - 10 - 75)
        pdf.cell(35, 5, label, align="R")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(40, 5, f"  {value}", ln=True)

    pdf.set_y(max(y_after_from, pdf.get_y()) + 4)

    # ── Bill To ──
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Bill To:", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, invoice_data["to_company"], ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    for line in invoice_data["to_address"]:
        pdf.cell(95, 5, line, ln=True)

    pdf.ln(6)

    # ── Items Table ──
    col_widths = {
        "sno": 12,
        "desc": page_width - 12 - 20 - 30 - 30,
        "qty": 20,
        "unit": 30,
        "total": 30,
    }

    # Table header
    pdf.set_fill_color(25, 60, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(col_widths["sno"], 8, "#", border=1, align="C", fill=True)
    pdf.cell(col_widths["desc"], 8, "Description", border=1, fill=True)
    pdf.cell(col_widths["qty"], 8, "Qty", border=1, align="C", fill=True)
    pdf.cell(col_widths["unit"], 8, "Unit Price", border=1, align="R", fill=True)
    pdf.cell(col_widths["total"], 8, "Amount", border=1, align="R", fill=True)
    pdf.ln()

    # Table rows
    pdf.set_text_color(40, 40, 40)
    fill = False
    for idx, item in enumerate(invoice_data["items"], 1):
        if fill:
            pdf.set_fill_color(240, 244, 250)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_font("Helvetica", "", 9)
        pdf.cell(
            col_widths["sno"], 7, str(idx), border="LR", align="C", fill=True
        )
        pdf.cell(
            col_widths["desc"], 7, item["desc"], border="LR", fill=True
        )
        pdf.cell(
            col_widths["qty"], 7, str(item["qty"]), border="LR", align="C", fill=True
        )
        pdf.cell(
            col_widths["unit"],
            7,
            f"Rs.{item['unit_price']:,.0f}",
            border="LR",
            align="R",
            fill=True,
        )
        pdf.cell(
            col_widths["total"],
            7,
            f"Rs.{item['total']:,.0f}",
            border="LR",
            align="R",
            fill=True,
        )
        pdf.ln()
        fill = not fill

    # Close bottom border of table
    pdf.cell(page_width, 0, "", border="T")
    pdf.ln(4)

    # ── Totals block (right-aligned) ──
    totals_x = pdf.w - 10 - 75
    totals_label_w = 40
    totals_value_w = 35

    def total_row(label, amount, bold=False, bg=None):
        pdf.set_x(totals_x)
        font_style = "B" if bold else ""
        pdf.set_font("Helvetica", font_style, 10 if bold else 9)
        pdf.set_text_color(60, 60, 60)
        if bg:
            pdf.set_fill_color(*bg)
            pdf.cell(totals_label_w, 7, label, align="R", fill=True)
            pdf.set_text_color(25, 60, 120)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(totals_value_w, 7, f"Rs.{amount:,.0f}", align="R", fill=True)
        else:
            pdf.cell(totals_label_w, 7, label, align="R")
            pdf.cell(totals_value_w, 7, f"Rs.{amount:,.0f}", align="R")
        pdf.ln()

    total_row("Subtotal:", invoice_data["subtotal"])
    total_row("GST (18%):", invoice_data["gst"])
    pdf.set_draw_color(25, 60, 120)
    pdf.set_line_width(0.4)
    pdf.line(totals_x, pdf.get_y(), totals_x + totals_label_w + totals_value_w, pdf.get_y())
    pdf.ln(1)
    total_row("Grand Total:", invoice_data["grand_total"], bold=True, bg=(230, 238, 250))

    pdf.ln(10)

    # ── Payment Terms ──
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 10 + page_width, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Payment Terms & Notes:", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 100, 100)
    for note in invoice_data.get("notes", []):
        pdf.cell(0, 4, f"  - {note}", ln=True)

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(0, 5, "This is a computer-generated invoice and does not require a physical signature.", align="C")


# ──────────────────────────────────────────
# Invoice data definitions
# ──────────────────────────────────────────

invoices = [
    {
        "invoice_no": "INV-301",
        "from_company": "TechNova Solutions Pvt Ltd",
        "from_address": ["42 MG Road", "Bangalore 560001", "Karnataka, India"],
        "to_company": "Sharma Electronics",
        "to_address": ["15 FC Road", "Pune 411005", "Maharashtra, India"],
        "date": "15-Mar-2026",
        "due_date": "15-Apr-2026",
        "payment_terms": "Net 30",
        "items": [
            {"desc": "Mechanical Keyboard", "qty": 3, "unit_price": 2500, "total": 7500},
            {"desc": "Wireless Mouse", "qty": 5, "unit_price": 800, "total": 4000},
            {"desc": "USB-C Hub", "qty": 2, "unit_price": 1200, "total": 2400},
        ],
        "subtotal": 13900,
        "gst": 2502,
        "grand_total": 16402,
        "notes": [
            "Payment due within 30 days of invoice date.",
            "Please transfer to: HDFC Bank, A/C 501020304050, IFSC HDFC0001234.",
            "Late payments attract 1.5% interest per month.",
        ],
    },
    {
        "invoice_no": "INV-302",
        "from_company": "CloudMinds India Technologies",
        "from_address": ["78 Whitefield", "Bangalore 560066", "Karnataka, India"],
        "to_company": "Patel IT Services",
        "to_address": ["23 SG Highway", "Ahmedabad 380015", "Gujarat, India"],
        "date": "20-Feb-2026",
        "due_date": "20-Mar-2026",
        "payment_terms": "Net 30",
        "items": [
            {"desc": "Annual Software License", "qty": 10, "unit_price": 5000, "total": 50000},
            {"desc": "Server Maintenance Contract", "qty": 1, "unit_price": 25000, "total": 25000},
            {"desc": "Cloud Storage 1TB Plan", "qty": 5, "unit_price": 3000, "total": 15000},
        ],
        "subtotal": 90000,
        "gst": 16200,
        "grand_total": 106200,
        "notes": [
            "Payment due within 30 days of invoice date.",
            "Bank: ICICI Bank, A/C 112233445566, IFSC ICIC0006789.",
            "Software licenses activate upon payment confirmation.",
        ],
    },
    {
        "invoice_no": "INV-303",
        "from_company": "Bharat Electronics & Peripherals",
        "from_address": ["56 Nehru Place", "New Delhi 110019", "Delhi, India"],
        "to_company": "Gupta Computer Academy",
        "to_address": ["89 Civil Lines", "Jaipur 302006", "Rajasthan, India"],
        "date": "10-Jan-2026",
        "due_date": "10-Feb-2026",
        "payment_terms": "Net 30",
        "items": [
            {"desc": "Dell Monitor 24 inch", "qty": 15, "unit_price": 12000, "total": 180000},
            {"desc": "Monitor Stand", "qty": 15, "unit_price": 1500, "total": 22500},
            {"desc": "HDMI Cable 2m", "qty": 30, "unit_price": 300, "total": 9000},
        ],
        "subtotal": 211500,
        "gst": 38070,
        "grand_total": 249570,
        "notes": [
            "Payment due within 30 days of invoice date.",
            "Bank: SBI, A/C 9876543210, IFSC SBIN0005432.",
            "Warranty claims to be filed within 1 year of purchase.",
            "Bulk order discount of 5% already applied.",
        ],
    },
    {
        "invoice_no": "INV-304",
        "from_company": "Wipro Peripherals Division",
        "from_address": ["12 Hinjewadi Phase 2", "Pune 411057", "Maharashtra, India"],
        "to_company": "Reddy Tech Solutions",
        "to_address": ["45 HITEC City", "Hyderabad 500081", "Telangana, India"],
        "date": "01-Mar-2026",
        "due_date": "01-Apr-2026",
        "payment_terms": "Net 30",
        "items": [
            {"desc": "HP LaserJet Printer", "qty": 2, "unit_price": 18000, "total": 36000},
            {"desc": "Ink Cartridge Set", "qty": 10, "unit_price": 2200, "total": 22000},
            {"desc": "A4 Paper Ream 500 sheets", "qty": 5, "unit_price": 350, "total": 1750},
        ],
        "subtotal": 59750,
        "gst": 10755,
        "grand_total": 70505,
        "notes": [
            "Payment due within 30 days of invoice date.",
            "Bank: Axis Bank, A/C 667788990011, IFSC UTIB0002345.",
            "Printer warranty: 2 years on-site support included.",
        ],
    },
    {
        "invoice_no": "INV-305",
        "from_company": "Reliance Digital Wholesale",
        "from_address": ["101 Bandra Kurla Complex", "Mumbai 400051", "Maharashtra, India"],
        "to_company": "Singh Infotech",
        "to_address": ["67 Rajpur Road", "Dehradun 248001", "Uttarakhand, India"],
        "date": "05-Apr-2026",
        "due_date": "05-May-2026",
        "payment_terms": "Net 30",
        "items": [
            {"desc": "Lenovo ThinkPad Laptop", "qty": 5, "unit_price": 55000, "total": 275000},
            {"desc": "Laptop Bag", "qty": 5, "unit_price": 1500, "total": 7500},
            {"desc": "Wireless Mouse", "qty": 5, "unit_price": 900, "total": 4500},
            {"desc": "External HDD 2TB", "qty": 1, "unit_price": 5500, "total": 5500},
        ],
        "subtotal": 292500,
        "gst": 52650,
        "grand_total": 345150,
        "notes": [
            "Payment due within 30 days of invoice date.",
            "Bank: Kotak Mahindra Bank, A/C 223344556677, IFSC KKBK0003456.",
            "Laptops carry 3-year manufacturer warranty.",
            "Free shipping included for orders above Rs.1,00,000.",
        ],
    },
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, inv in enumerate(invoices, 1):
        pdf = InvoicePDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.set_margins(10, 10, 10)
        draw_invoice(pdf, inv)
        out_path = os.path.join(OUTPUT_DIR, f"invoice_{i}.pdf")
        pdf.output(out_path)
        print(f"Created: {out_path}")

    print(f"\nAll {len(invoices)} invoices generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
