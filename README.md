# DJI Srt Stripper
Removes or retains the desired variables from a DJI FPV .srt file

## REQUIREMENTS
- Python 3 (I'm using 3.7)
## USAGE
(if the `python3` command doesn't work for you, try just `python`)

- Interactively select the variables you want in the output file
    - `python3 srt_strip.py --in_file DJIG0001.srt --out_file DJIG0001.filtered.srt --interactive`  
- Non-Interactively select the variables you want in the output file
    - `python3 srt_strip.py -i DJIG0001.srt -o DJIG0001.filtered.srt --keep_vars flightTime --keep_vars uavBat --keep_vars delay`
- Non-Interactively select the variables you don't want in the output file
    - `python3 srt_strip.py -i DJIG0001.srt -o DJIG0001.filtered.srt --drop_vars ch --drop_vars rcSignal --drop_vars glsBat`
- Interactively select the variables you want in the output file with some variables pre-deselected
    - `python3 srt_strip.py -i DJIG0001.srt -o DJIG0001.filtered.srt --interactive --drop_vars ch --drop_vars rcSignal --drop_vars glsBat`
- Interactively select the variables you want in the output file with some variables pre-selected
    - `python3 srt_strip.py -i DJIG0001.srt -o DJIG0001.filtered.srt --interactive --keep_vars flightTime --keep_vars uavBat --keep_vars delay`
