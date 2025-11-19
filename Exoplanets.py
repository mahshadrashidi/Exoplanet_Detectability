import numpy as np
import pandas as pd
from astropy.io import fits
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===========================
# 1) Load the FITS file
# ===========================

fits_path = "/home/mahshad/Documents/Thesis/Step2_realistic_targets/Table_1/asu.fit"

with fits.open(fits_path) as hdul:
    data = hdul[1].data
    df = pd.DataFrame(np.array(data).byteswap().newbyteorder())

# ===========================
# 2) Clean needed columns
# ===========================

# Make sure these are the exact column names (they matched your screenshot)
cols = ["Planet", "fc", "Phimag", "Phikin", "PhiCME"]

# Convert fc and the Phi* to numeric where possible (for nicer formatting)
df["fc"] = df["fc"].astype(str).astype(float)
df["Phimag"] = df["Phimag"].astype(str).astype(float)
df["Phikin"] = df["Phikin"].astype(str).astype(float)
df["PhiCME"] = df["PhiCME"].astype(str).astype(float)

# Reduced table with only the 5 columns
df5 = df[cols]

# (Optional) also save as CSV
df5.to_csv("exoplanets_5columns.csv", index=False)

# ===========================
# 3) Create PDF with 5 columns
# ===========================

output_pdf = "exoplanets_5columns.pdf"
c = canvas.Canvas(output_pdf, pagesize=letter)

# Column x-positions (adjust spacing if you like)
x_planet = 40
x_fc = 220
x_phimag = 310
x_phikin = 410
x_phicme = 510

y = 750
line_h = 16

# Title
c.setFont("Helvetica-Bold", 14)
c.drawString(x_planet, y, "Exoplanets: Planet, fc, Phimag, Phikin, PhiCME")
y -= 30

# Header row
c.setFont("Helvetica-Bold", 10)
c.drawString(x_planet, y, "Planet")
c.drawString(x_fc,     y, "fc [MHz]")
c.drawString(x_phimag, y, "Phi_mag")
c.drawString(x_phikin, y, "Phi_kin")
c.drawString(x_phicme, y, "Phi_CME")
y -= line_h
c.setFont("Helvetica", 9)

for _, row in df5.iterrows():
    # New page if needed
    if y < 40:
        c.showPage()
        y = 750
        c.setFont("Helvetica-Bold", 12)
        c.drawString(
            x_planet, y, "Exoplanets: Planet, fc, Phimag, Phikin, PhiCME (cont.)")
        y -= 25
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_planet, y, "Planet")
        c.drawString(x_fc,     y, "fc [MHz]")
        c.drawString(x_phimag, y, "Phi_mag")
        c.drawString(x_phikin, y, "Phi_kin")
        c.drawString(x_phicme, y, "Phi_CME")
        y -= line_h
        c.setFont("Helvetica", 9)

    # Row values (formatted a bit)
    planet = str(row["Planet"])
    fc = f"{row['fc']:.2f}"
    phimag = f"{row['Phimag']:.2f}"
    phikin = f"{row['Phikin']:.2f}"
    phicme = f"{row['PhiCME']:.2f}"

    c.drawString(x_planet, y, planet[:25])  # truncate very long names
    c.drawString(x_fc,     y, fc)
    c.drawString(x_phimag, y, phimag)
    c.drawString(x_phikin, y, phikin)
    c.drawString(x_phicme, y, phicme)

    y -= line_h

c.save()

print("PDF created:", output_pdf)
print("CSV created:", "exoplanets_5columns.csv")
