# Usage Instructions

This document provides instructions on how to use the ransomware scripts for encrypting and decrypting files.

## Encrypting Files

To encrypt files in a specified folder, follow these steps:

1. Open the src/ransomware.py script in a text editor.
2. Modify the target folder path within the script to point to the directory you want to encrypt.
   - Look for a line in the script that defines the target folder, and replace it with your desired folder path. For example:
     python
     target_folder = "/path/to/your/folder"  # Replace with your target folder
     
3. Run the encryption script using the following command:
   ```bash
   python src/ransomware.py
