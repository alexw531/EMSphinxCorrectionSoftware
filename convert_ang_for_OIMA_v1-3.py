import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def convert_emsphinx_to_oim():
    print(
        "This script takes the data output by EMSphInx's Spherical indexing"
        " and converts it to be readable by OIM analysis\n\n"
        "Original version written by Amelia How, updated by Alex Wang Aug. 2025\n" 
        "Version 1.3 (Aug. 1st, 2026)"
    )
    print(
        "This will require a pre-spherically indexed .ang file created by OIM Analysis.\n"
        "You can create this file by opening your scan in OIMA, right click the map, then hit "
        "Export->Scan Data... Then select *.ang for the file type.\n\n"
    )

    root = tk.Tk()
    root.withdraw()

    # Select the spherically indexed .ang file
    messagebox.showinfo("Step 1", "Select the SPHERICALLY INDEXED .ang file")
    fpathsi = filedialog.askopenfilename(title="Select SI .ang file", filetypes=[("ANG files", "*.ang")])
    if not fpathsi:
        print("User canceled spherically indexed file selection.")
        return

    # Select the non-spherically indexed .ang file
    messagebox.showinfo("Step 2", "Select the NOT SPHERICALLY INDEXED .ang file (made by OIMA)")
    fpathnosi = filedialog.askopenfilename(title="Select NON-SI .ang file", filetypes=[("ANG files", "*.ang")])
    if not fpathnosi:
        print("User canceled pre-spherically indexed file selection.")
        return

    # Check if files are the same
    if os.path.abspath(fpathsi) == os.path.abspath(fpathnosi):
        proceed = messagebox.askyesno("Warning", "The two files you selected seem to be the same file.\nDo you want to proceed anyway?")
        if not proceed:
            return

    # Choose output file location
    messagebox.showinfo("Step 3", "Choose where to save the OUTPUT .ang file")
    fpathout = filedialog.asksaveasfilename(title="Save output file as", defaultextension=".ang", filetypes=[("ANG files", "*.ang")])
    if not fpathout:
        print("User canceled output file selection.")
        return

    print("This may take a couple minutes. Please be patient...")

    # Read headers from both files (lines starting with '#')
    def read_headers(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        header_lines = [line for line in lines if line.strip().startswith("#")]
        return header_lines, len(header_lines)

    header_si, n_header_si = read_headers(fpathsi)
    header_nosi, n_header_nosi = read_headers(fpathnosi)
    
    #Determine if using a hexagonal grid. 1.3: no longer needed
    #hex=False
    #for line in header_nosi:
    #    if line.find("# GRID: HexGrid")!=-1:
    #        hex=True
    #        for line2 in header_nosi:
    #            if line2.find('# NCOLS_ODD:')!=-1:
    #                x_grid_size=int(line2.split()[len(line2.split())-1])
    #            if line2.find('# NROWS')!=-1:
    #                y_grid_size=int(line2.split()[len(line2.split())-1])
    #        break


    # Read data below headers
    si = pd.read_csv(fpathsi, skiprows=n_header_si, sep='\s+', header=None)
    nosi = pd.read_csv(fpathnosi, skiprows=n_header_nosi, sep='\s+', header=None)

    #adjust hex grid 1.3: no longer needed
    #if hex:
    #    si=si.drop(index=[(x+1)*2*x_grid_size-1 for x in (range(int(y_grid_size/2)))])

    # Check row count equality
    if si.shape[0] != nosi.shape[0]:
        print("ERROR: The number of rows in the spherically indexed and non-spherically indexed files do not match.")
        print("Ensure that the .ang file of the pre and post spherically indexed file correspond to the same scan.")
        if si.shape[0] < nosi.shape[0]:
            print("This could also occur due to the use of ROI in EMSphInx.")
        input("Press Enter to exit...")
        return

    # Replace orientation data (columns 0,1,2)
    nosi.iloc[:, 0:3] = si.iloc[:, 0:3]

    # Replace CI (column 6)
    nosi.iloc[:, 6] = si.iloc[:, 6]

    # Replace phase data (column 7), incremented by 1
    nosi.iloc[:, 7] = si.iloc[:, 7] + 1

    # Write header lines to output file
    with open(fpathout, 'w') as fout:
        fout.writelines(header_nosi)

    # Append modified data to output file
    nosi.to_csv(fpathout, sep=' ', index=False, header=False, mode='a')

    input("Output file has been successfully created and saved! Press Enter to exit...")

if __name__ == "__main__":
    convert_emsphinx_to_oim()
