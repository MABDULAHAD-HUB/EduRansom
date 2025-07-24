import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os
from encryption import generate_key, load_key, encrypt_folder, decrypt_folder, KEY_FILE

RANSOM_NOTE_FILE = 'ransom_note.txt'
LOG_FILE = 'activity.log'

# Ransom note template
RANSOM_NOTE_TEMPLATE = """
Your files have been encrypted!
To recover them, send 0.001 BTC to a fake address.
Enter the decryption key below to recover your files.
(Time remaining: {timer})
"""

class EduRansomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('EduRansom - Educational Ransomware Simulator')
        self.root.geometry('700x600')
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.folder_path = tk.StringVar()
        self.key_var = tk.StringVar()
        self.timer_var = tk.StringVar(value='02:00:00')
        self.timer_running = False
        self.current_mode = tk.StringVar(value='select')  # 'select', 'attacker', 'victim'
        
        self.create_mode_selection()

    def create_mode_selection(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Mode selection screen
        self.root.title('EduRansom - Select Mode')
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=50)
        
        # Title
        title_label = ttk.Label(main_frame, text='🛡 EduRansom', style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text='Educational Ransomware Simulation Tool', 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Mode selection
        mode_frame = tk.Frame(main_frame, bg='#2c3e50')
        mode_frame.pack(expand=True)
        
        tk.Label(mode_frame, text='Select Simulation Mode:', 
                font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#2c3e50').pack(pady=(0, 30))
        
        # Attacker mode button
        attacker_frame = tk.Frame(mode_frame, bg='#e74c3c', relief='raised', bd=3)
        attacker_frame.pack(fill='x', pady=10)
        
        tk.Label(attacker_frame, text='💀 ATTACKER MODE', 
                font=('Arial', 18, 'bold'), fg='white', bg='#e74c3c').pack(pady=10)
        
        tk.Label(attacker_frame, text='Deploy ransomware • Encrypt files • Generate ransom note', 
                font=('Arial', 11), fg='white', bg='#e74c3c').pack(pady=(0, 5))
        
        tk.Button(attacker_frame, text='Enter Attacker Mode', 
                 command=self.enter_attacker_mode,
                 font=('Arial', 12, 'bold'), bg='#c0392b', fg='white',
                 relief='raised', bd=2, padx=30, pady=5).pack(pady=10)
        
        # Victim mode button
        victim_frame = tk.Frame(mode_frame, bg='#3498db', relief='raised', bd=3)
        victim_frame.pack(fill='x', pady=10)
        
        tk.Label(victim_frame, text='😰 VICTIM MODE', 
                font=('Arial', 18, 'bold'), fg='white', bg='#3498db').pack(pady=10)
        
        tk.Label(victim_frame, text='View ransom note • Attempt file recovery • Enter decryption key', 
                font=('Arial', 11), fg='white', bg='#3498db').pack(pady=(0, 5))
        
        tk.Button(victim_frame, text='Enter Victim Mode', 
                 command=self.enter_victim_mode,
                 font=('Arial', 12, 'bold'), bg='#2980b9', fg='white',
                 relief='raised', bd=2, padx=30, pady=5).pack(pady=10)
        
        # Educational notice
        notice_frame = tk.Frame(main_frame, bg='#27ae60', relief='raised', bd=2)
        notice_frame.pack(fill='x', pady=(30, 0))
        
        tk.Label(notice_frame, 
                text='⚠ EDUCATIONAL USE ONLY - This is a safe simulation for learning purposes',
                font=('Arial', 10, 'bold'), fg='white', bg='#27ae60').pack(pady=8)
        
        # Help button
        help_frame = tk.Frame(main_frame, bg='#2c3e50')
        help_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(help_frame, text='ℹ Help & About', command=self.show_help,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=2, padx=20).pack()

    def enter_attacker_mode(self):
        self.current_mode.set('attacker')
        self.create_attacker_interface()
    
    def enter_victim_mode(self):
        self.current_mode.set('victim')
        self.create_victim_interface()

    def create_attacker_interface(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title('EduRansom - 💀 ATTACKER MODE')
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with back button
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Button(header_frame, text='← Back to Mode Selection', 
                 command=self.create_mode_selection,
                 font=('Arial', 10), bg='#95a5a6', fg='white',
                 relief='raised', bd=1).pack(side='left')
        
        # Title
        title_label = tk.Label(main_frame, text='💀 ATTACKER CONTROL PANEL', 
                              font=('Arial', 20, 'bold'), fg='#e74c3c', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Target selection frame
        target_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        target_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(target_frame, text='🎯 SELECT TARGET FOLDER', 
                font=('Arial', 12, 'bold'), fg='white', bg='#e74c3c').pack(pady=(10, 5))
        
        path_frame = tk.Frame(target_frame, bg='#e74c3c')
        path_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.path_entry = tk.Entry(path_frame, textvariable=self.folder_path, 
                                  font=('Arial', 10), width=50, relief='solid', bd=1)
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(path_frame, text='Browse', command=self.browse_folder,
                 font=('Arial', 10, 'bold'), bg='#c0392b', fg='white',
                 relief='raised', bd=1).pack(side='right')
        
        # Attack controls
        attack_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        attack_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(attack_frame, text='⚔ DEPLOY RANSOMWARE', 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10, 5))
        
        tk.Button(attack_frame, text='🔐 ENCRYPT TARGET FILES', 
                 command=self.encrypt_files_attacker,
                 font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                 relief='raised', bd=2, padx=30, pady=10).pack(pady=10)
        
        # Timer display in attacker mode
        timer_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        timer_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(timer_frame, text='⏰ ATTACK TIMER:', 
                font=('Arial', 12, 'bold'), fg='white', bg='#e74c3c').pack(pady=(10, 5))
        
        self.timer_display = tk.Label(timer_frame, textvariable=self.timer_var, 
                                     font=('Arial', 18, 'bold'), fg='#ffffff', bg='#e74c3c')
        self.timer_display.pack(pady=(0, 10))
        
        # Status and logs
        status_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        status_frame.pack(fill='x')
        
        tk.Label(status_frame, text='📊 ATTACK STATUS', 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10, 5))
        
        button_frame = tk.Frame(status_frame, bg='#34495e')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text='View Activity Log', command=self.view_log,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=1, padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='Show Ransom Note', command=self.show_ransom_note,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=1, padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='ℹ Help', command=self.show_help,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=1, padx=20).pack(side='left', padx=5)

    def create_victim_interface(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title('EduRansom - 😰 VICTIM MODE')
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with back button
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Button(header_frame, text='← Back to Mode Selection', 
                 command=self.create_mode_selection,
                 font=('Arial', 10), bg='#95a5a6', fg='white',
                 relief='raised', bd=1).pack(side='left')
        
        # Title
        title_label = tk.Label(main_frame, text='😰 VICTIM RECOVERY PANEL', 
                              font=('Arial', 20, 'bold'), fg='#3498db', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Encrypted files info
        info_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(info_frame, text='🚨 YOUR FILES HAVE BEEN ENCRYPTED!', 
                font=('Arial', 14, 'bold'), fg='white', bg='#e74c3c').pack(pady=10)
        
        # Timer display
        timer_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        timer_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(timer_frame, text='⏰ TIME REMAINING:', 
                font=('Arial', 12, 'bold'), fg='white', bg='#e74c3c').pack(pady=(10, 5))
        
        self.timer_display = tk.Label(timer_frame, textvariable=self.timer_var, 
                                     font=('Arial', 24, 'bold'), fg='#ffffff', bg='#e74c3c')
        self.timer_display.pack(pady=(0, 10))
        
        # Folder selection for decryption
        folder_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        folder_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(folder_frame, text='� SELECT ENCRYPTED FOLDER', 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10, 5))
        
        path_frame = tk.Frame(folder_frame, bg='#34495e')
        path_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.victim_path_entry = tk.Entry(path_frame, textvariable=self.folder_path, 
                                         font=('Arial', 10), width=50, relief='solid', bd=1)
        self.victim_path_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(path_frame, text='Browse', command=self.browse_folder,
                 font=('Arial', 10), bg='#3498db', fg='white',
                 relief='raised', bd=1).pack(side='right')
        
        # Recovery section
        recovery_frame = tk.Frame(main_frame, bg='#27ae60', relief='raised', bd=2)
        recovery_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(recovery_frame, text='🔑 FILE RECOVERY', 
                font=('Arial', 12, 'bold'), fg='white', bg='#27ae60').pack(pady=(10, 5))
        
        tk.Label(recovery_frame, text='Enter decryption key:', 
                font=('Arial', 11), fg='white', bg='#27ae60').pack()
        
        self.key_entry = tk.Entry(recovery_frame, textvariable=self.key_var, 
                                 font=('Arial', 12), width=50, relief='solid', bd=1,
                                 show='*')  # Hide key for security
        self.key_entry.pack(padx=10, pady=5)
        
        button_frame = tk.Frame(recovery_frame, bg='#27ae60')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text='🔓 DECRYPT FILES', 
                 command=self.decrypt_files_victim,
                 font=('Arial', 12, 'bold'), bg='#2ecc71', fg='white',
                 relief='raised', bd=2, padx=30).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='📋 View Ransom Note', 
                 command=self.show_ransom_note,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=1, padx=20).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='ℹ Help', command=self.show_help,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 relief='raised', bd=1, padx=20).pack(side='left', padx=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def configure_styles(self):
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Arial', 24, 'bold'), 
                           foreground='#e74c3c',
                           background='#2c3e50')
        
        self.style.configure('Subtitle.TLabel', 
                           font=('Arial', 12), 
                           foreground='#ecf0f1',
                           background='#2c3e50')

    def encrypt_files_attacker(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror('Error', 'Please select a target folder first.')
            return
        
        # Attacker confirmation
        result = messagebox.askyesno('Deploy Ransomware', 
                                   f'💀 DEPLOY RANSOMWARE ATTACK 💀\n\nTarget: {folder}\n\nThis will encrypt all files in the target directory.\nContinue with attack?',
                                   icon='warning')
        if not result:
            return
            
        try:
            key = generate_key()
            encrypt_folder(folder, key)
            self.log_event(f'[ATTACKER] Deployed ransomware on: {folder}')
            
            # Start the timer immediately after encryption
            self.start_timer()
            
            # Show ransom note popup immediately
            self.show_ransom_note()
            
            messagebox.showinfo('Attack Successful', 
                              f'💀 RANSOMWARE DEPLOYED SUCCESSFULLY!\n\n✅ Files encrypted\n✅ Ransom note displayed\n✅ Timer started\n✅ Key saved to {KEY_FILE}\n\nThe attack is complete. Switch to Victim Mode to see the full impact.')
            
        except Exception as e:
            messagebox.showerror('Attack Failed', f'Ransomware deployment failed:\n{str(e)}')

    def decrypt_files_victim(self):
        folder = self.folder_path.get()
        key = self.key_var.get().encode() if self.key_var.get() else None
        
        if not folder or not key:
            messagebox.showerror('Recovery Failed', 
                               '❌ Cannot recover files!\n\nPlease:\n• Select the encrypted folder\n• Enter the correct decryption key\n\nWithout the key, your files cannot be recovered.')
            return
        
        # Show progress dialog for victim
        progress_window = tk.Toplevel(self.root)
        progress_window.title('Attempting File Recovery...')
        progress_window.geometry('450x180')
        progress_window.configure(bg='#3498db')
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        tk.Label(progress_window, text='🔓 Attempting to recover your files...', 
                font=('Arial', 14, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        tk.Label(progress_window, text='Please wait while we try to decrypt your data...', 
                font=('Arial', 11), fg='white', bg='#3498db').pack()
        
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(padx=50, pady=15, fill='x')
        progress_bar.start()
        
        def decrypt_thread():
            try:
                decrypt_folder(folder, key)
                self.log_event(f'[VICTIM] Successfully recovered files from: {folder}')
                progress_window.destroy()
                self.timer_running = False
                self.timer_var.set('00:00:00')
                
                # Victory dialog for victim
                success_window = tk.Toplevel(self.root)
                success_window.title('🎉 Files Recovered!')
                success_window.geometry('450x250')
                success_window.configure(bg='#27ae60')
                success_window.resizable(False, False)
                success_window.transient(self.root)
                success_window.grab_set()
                
                tk.Label(success_window, text='🎉 SUCCESS!', 
                        font=('Arial', 20, 'bold'), fg='white', bg='#27ae60').pack(pady=20)
                
                tk.Label(success_window, text='Your files have been successfully recovered!\nThe ransomware has been defeated!', 
                        font=('Arial', 12), fg='white', bg='#27ae60').pack(pady=10)
                
                tk.Label(success_window, text='✅ All files decrypted\n✅ System cleaned\n✅ Threat neutralized', 
                        font=('Arial', 11), fg='white', bg='#27ae60').pack(pady=10)
                
                tk.Button(success_window, text='Celebration Mode!', command=success_window.destroy,
                         font=('Arial', 12, 'bold'), bg='#2ecc71', fg='white',
                         relief='raised', bd=2).pack(pady=15)
                
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror('Recovery Failed', 
                                   f'❌ FILE RECOVERY FAILED!\n\nError: {str(e)}\n\nPossible causes:\n• Wrong decryption key\n• Files already decrypted\n• Corrupted files\n\nPlease check your key and try again.')
        
        threading.Thread(target=decrypt_thread, daemon=True).start()

    def decrypt_files(self):
        folder = self.folder_path.get()
        key = self.key_var.get().encode() if self.key_var.get() else None
        
        if not folder or not key:
            messagebox.showerror('Decryption Error', 
                               'Please select a folder and enter the decryption key.')
            return
        
        # Show progress dialog
        progress_window = tk.Toplevel(self.root)
        progress_window.title('Decrypting Files...')
        progress_window.geometry('400x150')
        progress_window.configure(bg='#3498db')
        progress_window.resizable(False, False)
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        tk.Label(progress_window, text='🔓 Decrypting Files...', 
                font=('Arial', 14, 'bold'), fg='white', bg='#3498db').pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(padx=50, pady=10, fill='x')
        progress_bar.start()
        
        def decrypt_thread():
            try:
                decrypt_folder(folder, key)
                self.log_event(f'Decrypted folder: {folder}')
                progress_window.destroy()
                self.timer_running = False
                self.timer_var.set('00:00:00')
                
                # Success dialog
                success_window = tk.Toplevel(self.root)
                success_window.title('✅ Decryption Successful')
                success_window.geometry('400x200')
                success_window.configure(bg='#27ae60')
                success_window.resizable(False, False)
                success_window.transient(self.root)
                success_window.grab_set()
                
                tk.Label(success_window, text='🎉 FILES RECOVERED!', 
                        font=('Arial', 16, 'bold'), fg='white', bg='#27ae60').pack(pady=30)
                
                tk.Label(success_window, text='All files have been successfully decrypted.\nThe simulation is complete!', 
                        font=('Arial', 12), fg='white', bg='#27ae60').pack(pady=10)
                
                tk.Button(success_window, text='Close', command=success_window.destroy,
                         font=('Arial', 12, 'bold'), bg='#2ecc71', fg='white',
                         relief='raised', bd=2).pack(pady=20)
                
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror('Decryption Failed', 
                                   f'Failed to decrypt files:\n{str(e)}\n\nPlease check your decryption key.')
        
        threading.Thread(target=decrypt_thread, daemon=True).start()

    def show_ransom_note(self):
        timer = self.timer_var.get()
        note = RANSOM_NOTE_TEMPLATE.format(timer=timer)
        with open(RANSOM_NOTE_FILE, 'w') as f:
            f.write(note)
        
        # Create FULLSCREEN terrifying ransom note window
        top = tk.Toplevel(self.root)
        top.title('⚠ YOUR COMPUTER HAS BEEN LOCKED ⚠')
        top.geometry('1920x1080')
        top.configure(bg='#000000')
        top.resizable(False, False)
        top.attributes('-topmost', True)  # Always on top
        top.attributes('-fullscreen', True)  # Fullscreen mode
        
        # Center the window and grab focus
        top.transient(self.root)
        top.grab_set()
        top.focus_force()
        
        # Main container
        container = tk.Frame(top, bg='#000000')
        container.pack(fill='both', expand=True)
        
        # Top warning banner
        warning_banner = tk.Frame(container, bg='#ff0000', height=100)
        warning_banner.pack(fill='x', pady=(0, 20))
        warning_banner.pack_propagate(False)
        
        tk.Label(warning_banner, text='💀 YOUR FILES HAVE BEEN ENCRYPTED 💀', 
                font=('Arial', 32, 'bold'), fg='#ffffff', bg='#ff0000').pack(expand=True)
        
        # Skull and bones decoration
        skull_frame = tk.Frame(container, bg='#000000')
        skull_frame.pack(pady=20)
        
        tk.Label(skull_frame, text='☠️💀☠️💀☠️💀☠️💀☠️💀☠️💀☠️', 
                font=('Arial', 40), fg='#ff0000', bg='#000000').pack()
        
        # Main threatening message
        main_frame = tk.Frame(container, bg='#1a0000', relief='raised', bd=5)
        main_frame.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Title
        tk.Label(main_frame, text='🔒 ATTENTION! YOUR COMPUTER IS LOCKED! 🔒', 
                font=('Arial', 28, 'bold'), fg='#ff0000', bg='#1a0000').pack(pady=30)
        
        # Main threatening text
        threat_text = """
⚠️ ALL YOUR IMPORTANT FILES HAVE BEEN ENCRYPTED! ⚠️

📁 Documents, Photos, Videos, Databases, and Other Files are No Longer Accessible
🔐 Your Files are Encrypted with Military-Grade AES-256 Encryption
� Only WE Have the Decryption Key to Unlock Your Files

💰 TO RECOVER YOUR FILES, YOU MUST PAY THE RANSOM:
• Send 0.5 Bitcoin (BTC) to: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
• Email Transaction ID to: recovery@eduransom-fake.onion
• You Will Receive Decryption Key Within 24 Hours

⏰ TIME IS RUNNING OUT! PAY NOW OR LOSE YOUR FILES FOREVER!
        """
        
        message_label = tk.Label(main_frame, text=threat_text, 
                                font=('Arial', 16, 'bold'), fg='#ffffff', bg='#1a0000',
                                justify='center')
        message_label.pack(pady=20)
        
        # Timer section with large countdown
        timer_frame = tk.Frame(main_frame, bg='#ff0000', relief='raised', bd=3)
        timer_frame.pack(fill='x', padx=100, pady=30)
        
        tk.Label(timer_frame, text='⏰ TIME REMAINING BEFORE PERMANENT FILE DELETION:', 
                font=('Arial', 18, 'bold'), fg='#ffffff', bg='#ff0000').pack(pady=10)
        
        # Large timer display
        timer_display = tk.Label(timer_frame, textvariable=self.timer_var, 
                                font=('Arial', 64, 'bold'), fg='#ffff00', bg='#ff0000')
        timer_display.pack(pady=20)
        
        # Warning messages
        warning_text = """
⚠️ WARNING! DO NOT:
• Turn Off Your Computer (Files Will Be Permanently Deleted)
• Remove Hard Drive or USB Devices
• Run Antivirus Software (Will Corrupt Encrypted Files)
• Try to Decrypt Files Yourself (Will Cause Permanent Data Loss)

✅ WHAT YOU CAN DO:
• Pay the Ransom Immediately
• Contact Us via Email for Payment Instructions
• Keep Your Computer Running and Connected to Internet
        """
        
        warning_label = tk.Label(main_frame, text=warning_text, 
                                font=('Arial', 14), fg='#ffff00', bg='#1a0000',
                                justify='left')
        warning_label.pack(pady=20)
        
        # Fake payment section
        payment_frame = tk.Frame(main_frame, bg='#800000', relief='raised', bd=3)
        payment_frame.pack(fill='x', padx=50, pady=20)
        
        tk.Label(payment_frame, text='💳 PAYMENT PORTAL', 
                font=('Arial', 20, 'bold'), fg='#ffffff', bg='#800000').pack(pady=15)
        
        tk.Label(payment_frame, text='Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\nAmount Required: 0.5 BTC (~$15,000 USD)', 
                font=('Arial', 14, 'bold'), fg='#ffff00', bg='#800000').pack(pady=10)
        
        # Button frame at bottom
        button_frame = tk.Frame(container, bg='#000000')
        button_frame.pack(side='bottom', fill='x', pady=20)
        
        # Close button (more visible)
        tk.Button(button_frame, text='✕ CLOSE', command=top.destroy,
                 font=('Arial', 14, 'bold'), bg='#ff0000', fg='#ffffff',
                 relief='raised', bd=2, width=8, padx=10, pady=5).pack(side='right', padx=20)
        
        # Educational disclaimer (small text)
        tk.Label(button_frame, text='This is an educational simulation - Your files are safe!', 
                font=('Arial', 10), fg='#006600', bg='#000000').pack(side='left', padx=20)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            threading.Thread(target=self.countdown, daemon=True).start()

    def countdown(self):
        h, m, s = map(int, self.timer_var.get().split(':'))
        total_seconds = h * 3600 + m * 60 + s
        while total_seconds > 0 and self.timer_running:
            time.sleep(1)
            total_seconds -= 1
            h, rem = divmod(total_seconds, 3600)
            m, s = divmod(rem, 60)
            self.timer_var.set(f'{h:02}:{m:02}:{s:02}')
        if total_seconds == 0:
            self.timer_var.set('00:00:00')
            self.timer_running = False

    def log_event(self, event):
        with open(LOG_FILE, 'a') as log:
            log.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {event}\n')

    def view_log(self):
        if not os.path.exists(LOG_FILE):
            messagebox.showinfo('Activity Log', 'No log entries found yet.')
            return
        
        with open(LOG_FILE, 'r') as log:
            content = log.read()
            
        # Create professional log viewer
        top = tk.Toplevel(self.root)
        top.title('📊 Activity Log - EduRansom')
        top.geometry('700x500')
        top.configure(bg='#2c3e50')
        
        # Header
        header_frame = tk.Frame(top, bg='#34495e', relief='raised', bd=2)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        tk.Label(header_frame, text='📋 EduRansom Activity Log', 
                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=8)
        
        # Text area with scrollbar
        text_frame = tk.Frame(top, bg='#2c3e50')
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        text_widget = tk.Text(text_frame, font=('Consolas', 10), 
                             bg='#1a1a1a', fg='#00ff00', relief='sunken', bd=2,
                             wrap='word')
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        text_widget.insert('1.0', content if content else 'No activities logged yet.')
        text_widget.config(state='disabled')
        
        # Close button
        button_frame = tk.Frame(top, bg='#2c3e50')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(button_frame, text='Close', command=top.destroy,
                 font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                 relief='raised', bd=2, padx=20).pack()

    def show_help(self):
        # Create comprehensive help window
        help_window = tk.Toplevel(self.root)
        help_window.title('ℹ EduRansom - Help & About')
        help_window.geometry('800x700')
        help_window.configure(bg='#2c3e50')
        help_window.resizable(True, True)
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Main container with scrollbar
        main_frame = tk.Frame(help_window, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(header_frame, text='🛡 EduRansom - Help & Information', 
                font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=15)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(main_frame, bg='#2c3e50')
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, font=('Arial', 11), 
                             bg='#ecf0f1', fg='#2c3e50', relief='sunken', bd=2,
                             wrap='word', padx=15, pady=15)
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Help content
        help_content = """🛡 EDURANSOM - EDUCATIONAL RANSOMWARE SIMULATOR

📖 OVERVIEW:
EduRansom is a safe, educational tool designed to demonstrate how ransomware works without causing any real harm. It simulates the complete ransomware attack lifecycle for cybersecurity education and awareness training.

🎯 PURPOSE:
• Educate students and professionals about ransomware threats
• Demonstrate attack methodology and victim experience
• Provide hands-on learning in a controlled environment
• Raise awareness about cybersecurity best practices

🎭 DUAL-MODE SIMULATION:

💀 ATTACKER MODE:
• Select target folders for encryption simulation
• Deploy ransomware with realistic attack interface
• Monitor attack progress and timing
• View activity logs and ransom notes
• Experience the attacker's perspective

😰 VICTIM MODE:
• Experience being a ransomware victim
• See encrypted files and threatening messages
• Feel time pressure from countdown timer
• Attempt file recovery with decryption keys
• Understand victim psychology and decision-making

🔧 HOW TO USE:

1. MODE SELECTION:
   - Choose between Attacker or Victim mode
   - Each mode provides different perspective and interface

2. ATTACKER WORKFLOW:
   - Select target folder (use test_data folder)
   - Click "ENCRYPT TARGET FILES"
   - Ransom note will appear fullscreen
   - Timer starts automatically
   - Switch to Victim mode to see impact

3. VICTIM WORKFLOW:
   - Select the encrypted folder
   - View the terrifying ransom note
   - Watch countdown timer pressure
   - Enter decryption key to recover files
   - Experience relief of successful recovery

🔐 TECHNICAL FEATURES:
• AES-256 encryption (industry standard)
• Secure key generation and storage
• Real-time countdown timer
• Fullscreen ransom note (1920x1080)
• Activity logging and audit trail
• Safe, reversible file operations
• Professional GUI with role-specific themes

⚠ SAFETY & ETHICS:
• NO system-level access or persistence
• NO network communication or spreading
• NO data theft or malicious behavior
• ONLY affects user-selected folders
• ALWAYS recoverable with proper key
• Educational disclaimers throughout


⚖ LEGAL DISCLAIMER:
This software is created strictly for educational purposes. Any misuse for actual malicious activities is strictly prohibited and may violate local, national, and international laws. The authors assume no responsibility for misuse of this educational tool.

🌟 ABOUT THE PROJECT:
EduRansom represents a breakthrough in cybersecurity education, providing the most realistic ransomware simulation possible while maintaining complete safety. It bridges the gap between theoretical knowledge and practical experience.

👨‍💻 AUTHOR INFORMATION:
─────────────────────────────────────────────────────────
Project: EduRansom - Educational Ransomware Simulator
Developed: 2025

🧑‍💻 Author: M ABDUL AHAD
📧 Contact: abdulahadneriya@gmail.com

"Education is the most powerful weapon against cyber threats."
─────────────────────────────────────────────────────────

© 2025 EduRansom Project. All rights reserved.
This is educational software released for academic and training purposes.
"""
        
        text_widget.insert('1.0', help_content)
        text_widget.config(state='disabled')
        
        # Close button
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=(15, 0))
        
        tk.Button(button_frame, text='Close Help', command=help_window.destroy,
                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                 relief='raised', bd=2, padx=30, pady=5).pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = EduRansomGUI(root)
    root.mainloop()
