# Spherical indexing (EMSphInx) on Supercomputer & Subcomputer User Manual

**Edition: Mar 2026**

Original author: Jorn Verstijnen  
Updated for Sirion use by Casper Mornout  
Updated for Tasan group by Alex Wang, Megan Cooper, and Amelia How

Department of Materials Science and Engineering  
Massachusetts Institute of Technology

---

Authors: Jorn Verstijnen, Tijmen Vermeij, Casper Mornout, Alex Wang, Megan Cooper, Amelia How  
Date: Aug 12, 2020. Date updated: Mar 10, 2026

Instead of a Hough transform on the bands in the EBSD pattern, you can determine orientations based on a dictionary indexing algorithm. Dictionary indexing uses the complete experimental pattern and correlates this to a simulated dictionary with either a spherical master pattern (EMSphInx) or a dictionary filled with 2D patterns (EMSoft).

Background: https://doi.org/10.1016/j.actamat.2020.02.025  
EMSphInx releases: https://github.com/EMsoft-org/EMSphInx/releases

These are instructions specific to using the program on the Tasan group supercomputer and a couple bits of added info for use on the subcomputer. This requires use of a Linux terminal (WSL) so some knowledge of unix commands will help. A list of useful unix commands can be found in appendix A, along with a few tips on using unix.

## Spherical Indexing Instructions

| Step | Instruction |
|------|-------------|
| **0.** | **Preparing scan for spherical indexing:**<br>● Check "Save patterns" and select .up1<br>● Use Square grids during the EBSD scan. If it's absolutely critical to use a Hexagonal grids, or if you would like a previously scanned hexagonal grid to be indexed, contact Alex (alexw531@mit.edu) but there's no guarantee it will work.<br>● NOTE: The signal to noise ratio is more important than the amount of pixels in the EBSP. Therefore, it is recommended to increase exposure time (lower the FPS) instead of lowering the binning to increase the quality of the EBSD. |
| **1.** | **OIM Software:**<br>Note: For small files ( ~1 GB or less), it is preferable to reindex square grid scans using an .h5 file because EMSphInx can automatically import data about the scan from this file type. However, there are many issues with generating the .h5 files for large scans. In this case, .up1 files can instead be directly processed with EMSphInx.<br>Note: Hexagonal grids cannot be converted to .h5<br>● If using .h5 files:<br>&nbsp;&nbsp;o Fix the .up1 file using the "fix_up1.exe" file on the Tescan EBSD PC's desktop.<br>&nbsp;&nbsp;o Export the .osc to hdf5 (.h5) using OIM analysis (this can only be done on Tescan EBSD PC).<br>&nbsp;&nbsp;o The .h5 can be exported through opening the map with OIM (.osc), then right clicking the map, hit "Export" then "Scan Data":<br>&nbsp;&nbsp;o Select h5 for the file type<br>&nbsp;&nbsp;o If exporting was successful, delete both .up1 files afterwards (except when HR-EBSD might be used)<br>● Open the corresponding .osc file in OIM Analysis. A text file will automatically open in the software summarizing the scan information<br>&nbsp;&nbsp;o Take note of the order of your phases (i.e. Beta-Ti then Alpha-Ti)<br>🔴 Steps that are only required for .up1 files will have a red dot<br>🔴 If using a .up1 file:<br>&nbsp;&nbsp;🔴 Take note of the calibrated detector center coordinates, which are listed on the second line as:<br>&nbsp;&nbsp;&nbsp;&nbsp;🔴 Calibration: [x*] [y*] [z*]<br>&nbsp;&nbsp;&nbsp;&nbsp;🔴 (e.g. Calibration: 0.4935 0.7438 0.6148)<br>&nbsp;&nbsp;🔴 Take note of the Step size (e.g. 60 nm, 0.060 um)<br>&nbsp;&nbsp;🔴 If a hexagonal grid was used, the x step is the Step size while the y step size is step*0.866<br>&nbsp;&nbsp;🔴 Calculate the pixel dimensions of your scan along x and y<br>&nbsp;&nbsp;&nbsp;&nbsp;🔴 Scan Width = (X Max)/(Step) + 1<br>&nbsp;&nbsp;&nbsp;&nbsp;🔴 Scan Height = (Y Max)/(Step) + 1 |
| **2.** | **Move .h5 file (or .up1 file) into the Linux directory:**<br>● There is a shortcut to the directory on the desktop labelled EMSphInx shortcut (top right of the left screen on the supercomputer, top right of subcomputer)<br>● Otherwise, the file path is in appendix B<br>🔵 Steps that are only required when using the Subcomputer will have a blue dot<br>🔵 If using the subcomputer:<br>&nbsp;&nbsp;🔵 keep track of every file you move in and every folder you make. You will need to add permissions to each in step 4<br>&nbsp;&nbsp;🔵 (after step 3, you can also make your own directories in the Linux window with permissions already added with the mkdir command) |
| **3.** | **Open WSL:**<br>● Ensure that you are logged in as "TasanGroupUser"; this will not work as "TasanGroupAdmin"<br>● Find and run WSL on the top right of the left desktop (top right of the subcomputer)<br>● Otherwise, search windows for "WSL" |
| **4.** | 🔵**Add permissions:**<br>🔵 Go to userdata directory:<br>`cd ~/EMSphInxBuild/userdata`<br>🔵 For every file and every folder you added in step 2, move to their location<br>🔵 Add read, write and execute permissions for user<br>🔵 For example, if you added folder alexwang and file 20240510EBSDScan.h5 within the folder:<br>`chmod u+rwx alexwang`<br>`cd alexwang`<br>`chmod u+rwx 20240510EBSDScan.h5` |
| **5.** | **Run EMSphInx:**<br>● Enter the EMSphInxBuild directory<br>`cd ~/EMSphInxBuild`<br>● Run EMSphInx:<br>`./EMSphInxEBSD`<br>🔵 On the subcomputer you may experience an error saying:<br>`Unable to initialize GTK+, is DISPLAY set properly?`<br>🔵 If this happens, run "XMing" on the top right of the desktop |
| **6.** | **Open indexing wizard (ctrl+w)**<br>● Alternatively, click "File" then "Wizard…" |
| **7.** | **Page 1:**<br>● Choose pattern file (.h5 or .up1)<br>🔵 If you get an error with some statement of permissions, refer to step 4<br>● Press Preview<br>&nbsp;&nbsp;o Circular Mask Radius (usually 0 for full radius)<br>&nbsp;&nbsp;o Turn on Gaussian Background<br>● Set Histogram Equalization (usually 6 or 7) |
| **8.** | **Page 2:**<br>● Select master pattern(s), using correct phase and electron voltage<br>The master patterns are optimized for a tilt of 70 degree, so it is best to also have the scan in these conditions. Otherwise, a tilt correction needs to be performed after reindexing.<br>● The order of pattern selections will dictate the order that these patterns are listed. |
| **9.** | **Page 3:**<br>● Enter Binning (e.g. if you used 5x5 binning, enter 5)<br>● Enter Binned Pixel Size = 50<br>&nbsp;&nbsp;o You can check that your information is correct if the detector width comes out to 24mm<br>&nbsp;&nbsp;o Note: this is mathematically equivalent to entering your binning as 1 and inputting "Binned Pixel Size" as 50 x binning, both will have a resultant detector width of 24mm<br>● If using an .h5 file, the calibration data should automatically be imported as x*, y*, and z* values. If not, follow the instructions in red as well<br>🔴 If using a .up1 file:<br>&nbsp;&nbsp;🔴 Change the scan type as EDAX using the dropdown menu<br>&nbsp;&nbsp;🔴 Enter the x*, y*, and z* calibration values in the text boxes<br>&nbsp;&nbsp;🔴 Set the Detector Tilt to 0 deg |
| **10.** | **Page 4:**<br>🔴 If using a .up1 file:<br>&nbsp;&nbsp;🔴 Enter the Scan Width and Scan Height<br>&nbsp;&nbsp;🔴 Enter the Step sizes into X Step and Y Step (for square grid, X step = Y step = Step size)<br>&nbsp;&nbsp;🔴 Note: Sometimes .up1 files have one less row of data than they are supposed to. In this case, you will see an error at the bottom saying "not enough patterns". A workaround for this is to reduce the Scan Height by 1. At the bottom, it should now say that there is one more pattern than pixel. Finally, check the box "Ignore Extra Patterns"<br>&nbsp;&nbsp;&nbsp;&nbsp;▪ To check if the scan is distorted from this dimensional change, click "Select ROI…" and verify that the IQ map looks correct<br>● Select region of interest (ROI), if necessary<br>&nbsp;&nbsp;o Note: Currently, the script that allows the output to be readable by OIM Analysis does not fully support ROI. If you plan to do your analysis in OIMA or use a hexagonal grid, select a ROI at your own risk. |
| **11.** | **Page 5:**<br>● Set Bandwidth — lowest tolerable value should be used, the time it takes scales as<br>*t ∝ bw³ * ln(bw³)*<br>&nbsp;&nbsp;o 41, 53, 63, 68, 74 – fast but somewhat noise sensitive<br>&nbsp;&nbsp;o 88, 95, 113, 123 – trade-off between noise tolerance and speed<br>&nbsp;&nbsp;o Bandwidths greater than 123 have been shown to crash EMSphInx during the beginning of indexing. It is suggested to save the namelist (see step 13) before you begin indexing at higher bandwidths<br>&nbsp;&nbsp;o 158, 172, 203, 221, 263 – maximum noise robustness but slow<br>● Check Refinement (improves scan quality for speed, generally beneficial)<br>● DON'T CHECK Normalized (was recommended for multiphase materials but seems to lower quality)<br>● Set output files:<br>&nbsp;&nbsp;o New data file (.h5)<br>&nbsp;&nbsp;o Vendor file (.ang)<br>&nbsp;&nbsp;o IPF (.png)<br>&nbsp;&nbsp;o CI (.png)<br>Make sure to add file extensions in the name (i.e., name the data file data.h5 and not just data). Failure to do so may cause a crash at the end of the scan |
| **12.** | Check summary and press finish |
| **13.** | If you would like to save the values you've input for this scan, you can click File->Save As, on the top left of the window. Save the file with the extension .nml and then you can use File->Open to open the same parameters later.<br>● Press Start:<br>The bottom left should say "Initializing indexes" for a while then give time estimates and speed as it begins indexing<br><br>Best practices: If you are running a long scan, you can get the most out of your scan by testing various settings at a low bandwidth (41) and a small ROI, then seeing which one works best. Then run the longer scan with optimized parameters. Some options include:<br>● Adding normalization<br>● Changing histogram equalization<br>● Add the gaussian background back<br>A bandwidth of 41 will run about 35 times faster than a bandwidth of 123. A 35 hour scan and a ROI a 1/3rd of the view field can run in 7 min. Take 30 min to try 4 different options and optimize your 1.5 day scan. |
| **14.** | **Once indexing is done, please remove your large input files from the supercomputer and the EBSD PC!**<br>Almost all the time, the large input file with the patterns is no longer necessary. Only the output file with the orientations will be needed. The exception may be for HREBSD. However, in that case, the scan should have been optimized for HREBSD in the first place. |

---

## Post-processing

After you're done spherically indexing, you will likely need to perform some post-processing to obtain the data you want. This can be done in two ways: MTEX or OIM analysis. Here is a quick comparison:

*I (Alex) have not used much OIM analysis. I may be incorrect about certain aspects. Use this just to guide your decision of which software to use

| MTEX | OIM analysis |
|------|--------------|
| ● Mostly code-based (MATLAB)<br>&nbsp;&nbsp;o Experience using MATLAB is useful<br>&nbsp;&nbsp;o Some GUI helps set up the code<br>&nbsp;&nbsp;o Easy to script so that different data undergoes the same exact processing<br>&nbsp;&nbsp;o Extremely flexible (font, color scheme, chart options)<br>&nbsp;&nbsp;o Easier to implement more unique analysis (e.g. find every grain boundary which has a specific misorientation+plane and has high Schmid factor given a specific loading)<br>● Open source<br>&nbsp;&nbsp;o Many other people have written scripts to do specific things<br>&nbsp;&nbsp;o Debugging resources are limited to volunteers on the internet forums. Usefulness varies<br>&nbsp;&nbsp;o Can be done on any computer with MATLAB (including supercomputer and subcomputer)<br>● Can be used for other types of data (e.g. XRD)<br>&nbsp;&nbsp;o Ensures visual similarity between data collected from different sources | ● Can directly take the output of spherical indexing<br>● User-interface<br>&nbsp;&nbsp;o No programming knowledge required<br>&nbsp;&nbsp;o More manual and difficult to script the same processing to different data<br>&nbsp;&nbsp;o Less flexibility<br>&nbsp;&nbsp;o Difficult to implement more unique analysis<br>● Proprietary software<br>&nbsp;&nbsp;o Help pages exist and there is likely a tech support line or something similar. Currently unsure about how useful it is<br>&nbsp;&nbsp;o Must be done on the EBSD computer, Gatan stage computer, or the Subcomputer (the Subcomputer has a network drive mapped to the EBSD computer to make it easier to transfer files)<br>● Just for EBSD<br>● Spherical indexing output requires a bit of processing |

This manual will help with both the installation and some tips in using MTEX as well as the process of preparing data for use in OIM analysis in the next couple pages.

---

## MTEX Installation and Setup

| Step | Instruction |
|------|-------------|
| **1.** | Install latest version of MTEX from MTEX website.<br>● Instructions from MTEX installation guide: |
| **2.** | In the command line: `import_wizard('EBSD')` |
| **3.** | Select the plus (+) button. Find the .ang file for your data and press open. Select 'Next>>' on the bottom right of the import wizard. (.h5 files do not work) |
| **4.** | Enter crystal types – must be entered in the order that EMSphInx exported them (i.e. the order that they were selected in the master pattern list).<br>● Select indexed for phases that you are trying to index.<br>● CIF files can be uploaded to load parameters of the lattice.<br>● You can name this crystal in the mineral name field and select the plotting color. |
| **5.** | Select 'Plot' in the bottom left corner of the import wizard. This will produce a plot of phases. |
| **6.** | Select 'Finish' to generate a MATLAB file (.m). |

### Relevant MTEX Commands

| Command | Description |
|---------|-------------|
| `ebsd` | Outputs phase fraction and other info about ebsd scan |
| `plot(ebsd,ebsd.ci)`<br>`colormap gray`<br>`mtexColorbar` | Generates a grayscale map of CI |
| `plot(ebsd)` | Generates phase map of all EBSD data |
| `filt = ebsd(ebsd.ci>#CI#)` | Removes all data with a CI less than #CI# |

---

## OIM Analysis Processing

Note: Hexagonal grids must undergo this process as well. The resultant ang file can be opened in either OIMA or MTEX

| Step | Instruction |
|------|-------------|
| **1.** | Move the .ang file back to any computer with OIMA. |
| **2.** | Use OIM Analysis to export the original (pre-spherically indexed) data to a separate .ang file.<br>● This can be done in the same way as the .h5 files was exported, other than the file type.<br>● Keep track of which .ang file has the spherically indexed data and which one was the original data. |
| **3.** | Run the "convert_ang_for_OIMA.exe" file on the computer's desktop and follow its instructions. |
| **4.** | You should be able to open the output in OIM Analysis |

---

## Appendix A: basic unix tips and commands

Commands and file names are case sensitive

Tab will autocomplete names of directories and files

The help command can be a good starting point sometimes

If you find yourself where you can't enter new commands and hitting things like enter just says [return], try hitting q

| Command | Description |
|---------|-------------|
| `cd directoryname` | Move into directoryname |
| `cd ~` or just `cd` | Moves to home directory |
| `cd ..` | Moves up a directory |
| `ls` | List directories and files in current directory.<br>Add flag -l to see permissions:<br>`ls -l` |
| `chmod permissions filename` | Changes permissions of a file or directory. The permissions flag specified either the user, group or other to give(+) set(=) or remove(-) either read write or execute permissions.<br>For examples, to give the users and group all permissions but others only read permission use the following:<br>`chmod ug=rwx,o=r filename` |
| `./filename` | Execute filename |
| `mkdir directoryname` | Makes a new directory |
| `rm filename` | Removes file |
| `rmdir directoryname` | Removes directory |

## Appendix B: More useful info:

**WSL filepath for subcomputer:**  
`C:\Users\TasanGroupUser\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs\home\tasangroupuser\EMSphInxBuild\userdata`

**WSL filepath for supercomputer:**  
`\\wsl.localhost\Ubuntu\home\tasangroup\EMSphInxBuild\userdata`

**Master patterns:**  
https://github.com/EMsoft-org/SHTdatabase

**EMSphInx documentation (specifically about bandwidth):**  
https://emsphinx.readthedocs.io/en/latest/emsphinxebsd.html#indexing-parameters

Cover for this manual is a spherically indexed IPF map of copper deposited on sapphire by Alex Wang
