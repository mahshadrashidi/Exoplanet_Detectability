import numpy as np
import pandas as pd
from astropy.io import fits
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===========================
# 1) Load FITS file
# ===========================

fits_path = "/home/mahshad/Documents/Thesis/Step2_realistic_targets/Table_1/asu.fit"

with fits.open(fits_path) as hdul:
    data = hdul[1].data
    df = pd.DataFrame(np.array(data).byteswap().newbyteorder())

# ===========================
# 2) Convert needed columns
# ===========================

df["fc"] = df["fc"].astype(str).astype(float)
df["Phimag"] = df["Phimag"].astype(str).astype(float)
df["Phikin"] = df["Phikin"].astype(str).astype(float)
df["PhiCME"] = df["PhiCME"].astype(str).astype(float)

# ===========================
# 3) STEP 1: select planets with fc > 1
# ===========================

mask_fc = df["fc"] > 1
df_fc = df.loc[mask_fc]

print(f"Planets with fc > 1 MHz: {len(df_fc)}")

# ===========================
# 4) STEP 2: among those, require at least one flux density > 1
# ===========================

mask_flux = (df_fc["Phimag"] > 1) | (
    df_fc["Phikin"] > 1) | (df_fc["PhiCME"] > 1)

df_filt = df_fc.loc[mask_flux, ["Planet", "fc", "Phimag", "Phikin", "PhiCME"]]

print(f"Planets with fc > 1 AND any flux > 1: {len(df_filt)}")

# ===========================
# 5) Add row-number column
# ===========================

df_filt.insert(0, "No", range(1, len(df_filt) + 1))

# Save CSV
df_filt.to_csv("exoplanets_fc_and_flux_over1.csv", index=False)

# ===========================
# 6) Export to PDF (No + 5 data columns)
# ===========================

output_pdf = "exoplanets_fc_and_flux_over1.pdf"
c = canvas.Canvas(output_pdf, pagesize=letter)

# Column positions
x_no = 40
x_planet = 80
x_fc = 260
x_phimag = 340
x_phikin = 430
x_phicme = 520

y = 750
line_h = 16

# ---- Title ----
c.setFont("Helvetica-Bold", 14)
c.drawString(x_no, y, "Exoplanets with fc > 1 MHz and any flux density > 1")
y -= 30

# ---- Header ----
c.setFont("Helvetica-Bold", 10)
c.drawString(x_no,     y, "No")
c.drawString(x_planet, y, "Planet")
c.drawString(x_fc,     y, "fc [MHz]")
c.drawString(x_phimag, y, "Phi_mag [mJy]")
c.drawString(x_phikin, y, "Phi_kin [mJy]")
c.drawString(x_phicme, y, "Phi_CME [mJy]")
y -= line_h

c.setFont("Helvetica", 9)

# ---- Rows ----
for _, row in df_filt.iterrows():

    if y < 40:   # new page if needed
        c.showPage()
        y = 750
        c.setFont("Helvetica-Bold", 12)
        c.drawString(
            x_no, y, "Exoplanets with fc > 1 MHz and any flux > 1 (cont.)")
        y -= 25
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_no,     y, "No")
        c.drawString(x_planet, y, "Planet")
        c.drawString(x_fc,     y, "fc [MHz]")
        c.drawString(x_phimag, y, "Phi_mag [mJy]")
        c.drawString(x_phikin, y, "Phi_kin [mJy]")
        c.drawString(x_phicme, y, "Phi_CME [mJy]")
        y -= line_h
        c.setFont("Helvetica", 9)

    no = str(row["No"])
    planet = str(row["Planet"])
    fc = f"{row['fc']:.2f}"
    phimag = f"{row['Phimag']:.2f}"
    phikin = f"{row['Phikin']:.2f}"
    phicme = f"{row['PhiCME']:.2f}"

    c.drawString(x_no,     y, no)
    c.drawString(x_planet, y, planet[:22])  # truncate long names
    c.drawString(x_fc,     y, fc)
    c.drawString(x_phimag, y, phimag)
    c.drawString(x_phikin, y, phikin)
    c.drawString(x_phicme, y, phicme)

    y -= line_h

c.save()

print("PDF created:", output_pdf)
print("CSV created:", "exoplanets_fc_and_flux_over1.csv")
