import os
import argparse
import pyfiglet
import random
from pyfiglet import Figlet
import subprocess

font_list = [
    'stop', 'georgi16', 'xsansi', 'xsansb', 'xsans', 'xhelvi', 'xhelvb', 
    'xhelv', 'xcouri', 'xchartri', 'xbrite', 'wet_letter', 'weird', 
    'utopiai', 'univers', 'tubular', 'train', 'tombstone', 'tinker-toy', 
    'tiles', 'this', 'the_edge', 'test1', 'sweet', 'swamp_land', 'sub-zero'
]

def figlet_text(text):
    font = random.choice(font_list)
    f = Figlet(font=font)
    return f.renderText(text)

def main():
    # Display the header and menu
    print(figlet_text('FileSec - By Khadeer'))
    print("File Integrity Monitor")
    print("Author - Khadeer")

    print("1) Create Baseline")
    print("2) Update Baseline")
    print("3) Start Monitoring")

    # Get user input
    try:
        res = int(input("Enter your choice (1-3): "))
        if res < 1 or res > 3:
            print("Invalid choice. Please enter a number between 1 and 3.")
            return

        tbm = input("Enter the file or directory to monitor: ")

        # Check if the PowerShell script exists
        script_path = './fim.ps1'
        if not os.path.exists(script_path):
            print(f"Error: The script {script_path} does not exist.")
            return

        # Run the PowerShell script with the arguments
        subprocess.run(['powershell', '-File', script_path, tbm, str(res)], check=True)
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the PowerShell script: {e}")

if __name__ == "__main__":
    main()
