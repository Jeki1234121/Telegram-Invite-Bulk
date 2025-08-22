import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, UserNotMutualContactError
import time
import random
import re
import threading
import asyncio
from pyrogram import Client as PyrogramClient

class TelegramInviteTool:
    def __init__(self, root):  # Fixed method name with double underscores
        self.root = root
        self.root.title("Telegram Bulk Invite Tool (Pentest)")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # API Configuration
        self.api_id = 21077650
        self.api_hash = "e356ac84737cd5264f86301fcdc2bc0d"
        self.group_link = "https://t.me/+HMs3hkGVYx9hN2I8"
        
        # Variables
        self.processed_usernames = []
        self.is_inviting = False
        
        # GUI Elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File Processing Tab
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="File Processing")
        
        # Invite Tab
        self.invite_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.invite_tab, text="Bulk Invite")
        
        # Member Extraction Tab
        self.extract_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.extract_tab, text="Extract Members")
        
        # File Processing Tab Content
        self.setup_file_processing_tab()
        
        # Invite Tab Content
        self.setup_invite_tab()
        
        # Member Extraction Tab Content
        self.setup_extract_tab()
        
    def setup_file_processing_tab(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.file_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File Selection Section
        file_section = ttk.LabelFrame(main_frame, text="File Selection", padding=10)
        file_section.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_section, text="Select Input File:").pack(anchor=tk.W)
        
        file_frame = ttk.Frame(file_section)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_entry = ttk.Entry(file_frame)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Processing Options Section
        options_section = ttk.LabelFrame(main_frame, text="Processing Options", padding=10)
        options_section.pack(fill=tk.X, pady=(0, 10))
        
        self.remove_duplicates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_section, text="Remove Duplicates", variable=self.remove_duplicates_var).pack(anchor=tk.W)
        
        self.remove_invalid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_section, text="Remove Invalid Usernames", variable=self.remove_invalid_var).pack(anchor=tk.W)
        
        self.sort_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_section, text="Sort Alphabetically", variable=self.sort_var).pack(anchor=tk.W)
        
        # Process Button
        ttk.Button(options_section, text="Process File", command=self.process_file).pack(pady=10)
        
        # Output Section
        output_section = ttk.LabelFrame(main_frame, text="Processed Results", padding=10)
        output_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(output_section)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.processed_text = tk.Text(text_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.processed_text.yview)
        self.processed_text.configure(yscrollcommand=scrollbar.set)
        
        self.processed_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Save Button
        ttk.Button(output_section, text="Save Processed File", command=self.save_processed_file).pack(pady=5)
        
    def setup_invite_tab(self):
        main_frame = ttk.Frame(self.invite_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration Section
        config_section = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_section.pack(fill=tk.X, pady=(0, 10))
        
        # Group Link
        ttk.Label(config_section, text="Group Link:").pack(anchor=tk.W)
        self.group_link_entry = ttk.Entry(config_section)
        self.group_link_entry.insert(0, self.group_link)
        self.group_link_entry.pack(fill=tk.X, pady=5)
        
        # Usernames File
        ttk.Label(config_section, text="Usernames File:").pack(anchor=tk.W, pady=(10, 0))
        
        usernames_frame = ttk.Frame(config_section)
        usernames_frame.pack(fill=tk.X, pady=5)
        
        self.usernames_file_entry = ttk.Entry(usernames_frame)
        self.usernames_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(usernames_frame, text="Browse", command=self.browse_usernames_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Settings Section
        settings_section = ttk.LabelFrame(main_frame, text="Invite Settings", padding=10)
        settings_section.pack(fill=tk.X, pady=(0, 10))
        
        settings_frame = ttk.Frame(settings_section)
        settings_frame.pack(fill=tk.X)
        
        # Left column
        left_frame = ttk.Frame(settings_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(left_frame, text="Delay between invites (seconds):").pack(anchor=tk.W)
        self.delay_entry = ttk.Entry(left_frame, width=10)
        self.delay_entry.insert(0, "30")
        self.delay_entry.pack(anchor=tk.W, pady=2)
        
        ttk.Label(left_frame, text="Max invites per session:").pack(anchor=tk.W, pady=(10, 0))
        self.max_invites_entry = ttk.Entry(left_frame, width=10)
        self.max_invites_entry.insert(0, "200")
        self.max_invites_entry.pack(anchor=tk.W, pady=2)
        
        # Right column
        right_frame = ttk.Frame(settings_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.use_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right_frame, text="Use Proxy", variable=self.use_proxy_var).pack(anchor=tk.W)
        
        self.handle_invisible_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_frame, text="Handle Invisible Members", variable=self.handle_invisible_var).pack(anchor=tk.W)
        
        # Control Buttons
        button_frame = ttk.Frame(settings_section)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Inviting", command=self.start_inviting)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_inviting, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Progress Section
        progress_section = ttk.LabelFrame(main_frame, text="Progress", padding=10)
        progress_section.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Ready to start")
        ttk.Label(progress_section, textvariable=self.progress_var).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_section, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Log Section
        log_section = ttk.LabelFrame(main_frame, text="Activity Log", padding=10)
        log_section.pack(fill=tk.BOTH, expand=True)
        
        log_frame = ttk.Frame(log_section)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=12, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear log button
        ttk.Button(log_section, text="Clear Log", command=self.clear_log).pack(pady=5)
        
    def setup_extract_tab(self):
        main_frame = ttk.Frame(self.extract_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Source Group Section
        source_section = ttk.LabelFrame(main_frame, text="Source Group", padding=10)
        source_section.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(source_section, text="Source Group Link/Username:").pack(anchor=tk.W)
        self.source_group_entry = ttk.Entry(source_section)
        self.source_group_entry.pack(fill=tk.X, pady=5)
        
        # Extract Settings
        extract_settings = ttk.LabelFrame(main_frame, text="Extract Settings", padding=10)
        extract_settings.pack(fill=tk.X, pady=(0, 10))
        
        self.extract_visible_only_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(extract_settings, text="Extract Visible Members Only", variable=self.extract_visible_only_var).pack(anchor=tk.W)
        
        self.extract_with_usernames_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(extract_settings, text="Extract Only Users with Usernames", variable=self.extract_with_usernames_var).pack(anchor=tk.W)
        
        # Extract Button
        ttk.Button(extract_settings, text="Extract Members", command=self.extract_members).pack(pady=10)
        
        # Results Section
        results_section = ttk.LabelFrame(main_frame, text="Extracted Members", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True)
        
        results_frame = ttk.Frame(results_section)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.extract_text = tk.Text(results_frame, height=15, wrap=tk.WORD)
        extract_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.extract_text.yview)
        self.extract_text.configure(yscrollcommand=extract_scrollbar.set)
        
        self.extract_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        extract_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Save extracted members button
        ttk.Button(results_section, text="Save Extracted Members", command=self.save_extracted_members).pack(pady=5)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            
    def browse_usernames_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Usernames File",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.usernames_file_entry.delete(0, tk.END)
            self.usernames_file_entry.insert(0, file_path)
            
    def process_file(self):
        input_file = self.file_entry.get()
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Selected file does not exist")
            return
            
        try:
            # Read file
            usernames = []
            
            if input_file.endswith('.csv'):
                df = pd.read_csv(input_file, header=None)
                usernames = df[0].astype(str).tolist()
            else:
                with open(input_file, 'r', encoding='utf-8') as f:
                    usernames = [line.strip() for line in f.readlines()]
            
            # Remove empty lines
            usernames = [u for u in usernames if u.strip()]
            
            # Remove duplicates
            if self.remove_duplicates_var.get():
                usernames = list(dict.fromkeys(usernames))  # Preserve order while removing duplicates
                
            # Remove invalid usernames
            if self.remove_invalid_var.get():
                valid_usernames = []
                for username in usernames:
                    clean_username = username.strip('@').strip()
                    # Basic Telegram username validation
                    if re.match(r'^[a-zA-Z0-9_]{5,32}$', clean_username):
                        valid_usernames.append(clean_username)
                usernames = valid_usernames
                
            # Sort
            if self.sort_var.get():
                usernames.sort()
                
            # Display results
            self.processed_text.delete(1.0, tk.END)
            self.processed_text.insert(tk.END, "\n".join(usernames))
            self.processed_usernames = usernames
            
            messagebox.showinfo("Success", f"Processed {len(usernames)} valid usernames")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")
            
    def save_processed_file(self):
        if not self.processed_usernames:
            messagebox.showerror("Error", "No processed usernames to save")
            return
            
        save_path = filedialog.asksaveasfilename(
            title="Save Processed File",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
        )
        
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(self.processed_usernames))
                messagebox.showinfo("Success", f"File saved successfully with {len(self.processed_usernames)} usernames")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def log_message(self, message):
        """Add a message to the log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def stop_inviting(self):
        self.is_inviting = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_var.set("Stopped by user")
        self.log_message("Invite process stopped by user")
        
    def start_inviting(self):
        usernames_file = self.usernames_file_entry.get()
        group_link = self.group_link_entry.get()
        
        if not usernames_file or not group_link:
            messagebox.showerror("Error", "Please provide both usernames file and group link")
            return
            
        if not os.path.exists(usernames_file):
            messagebox.showerror("Error", "Usernames file does not exist")
            return
            
        try:
            delay = int(self.delay_entry.get())
            max_invites = int(self.max_invites_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for delay and max invites")
            return
            
        # Start inviting in a separate thread
        self.is_inviting = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        thread = threading.Thread(target=self.invite_users_thread, args=(usernames_file, group_link, delay, max_invites))
        thread.daemon = True
        thread.start()
        
    def invite_users_thread(self, usernames_file, group_link, delay, max_invites):
        try:
            # Extract invite hash from link
            if "t.me/joinchat/" in group_link:
                invite_hash = group_link.split("t.me/joinchat/")[1]
            elif "t.me/+" in group_link:
                invite_hash = group_link.split("t.me/+")[1]
            else:
                self.log_message("Error: Invalid group invite link format")
                return
                
            # Read usernames
            with open(usernames_file, 'r', encoding='utf-8') as f:
                usernames = [line.strip().strip('@') for line in f.readlines() if line.strip()]
                
            if not usernames:
                self.log_message("Error: No valid usernames found in file")
                return
                
            # Limit usernames to max_invites
            usernames = usernames[:max_invites]
            total_users = len(usernames)
            
            self.log_message(f"Starting invite process for {total_users} users...")
            self.progress_var.set(f"Initializing Telegram client...")
            self.progress_bar['maximum'] = total_users
            
            # Initialize Telegram client
            client = TelegramClient('pentest_session', self.api_id, self.api_hash)
            client.start()
            
            self.log_message("Telegram client initialized successfully")
            
            # Join the group first
            try:
                client(ImportChatInviteRequest(invite_hash))
                self.log_message("Successfully joined the target group")
            except Exception as e:
                self.log_message(f"Note: Could not join group (might already be a member): {str(e)}")
            
            # Get group entity
            try:
                group_entity = client.get_entity(invite_hash)
                self.log_message(f"Group entity retrieved: {group_entity.title}")
            except Exception as e:
                self.log_message(f"Error getting group entity: {str(e)}")
                return
            
            invited_count = 0
            failed_count = 0
            
            for i, username in enumerate(usernames):
                if not self.is_inviting:
                    break
                    
                try:
                    # Get user entity
                    user_entity = client.get_entity(username)
                    
                    # Add user to group
                    client(InviteToChannelRequest(
                        channel=group_entity,
                        users=[user_entity]
                    ))
                    
                    invited_count += 1
                    self.log_message(f"✓ Successfully invited @{username}")
                    
                    # Update progress
                    self.progress_bar['value'] = i + 1
                    self.progress_var.set(f"Invited {invited_count}/{total_users} users")
                    
                except FloodWaitError as e:
                    wait_time = e.seconds
                    self.log_message(f"⚠ Flood wait error. Waiting {wait_time} seconds...")
                    for remaining in range(wait_time, 0, -1):
                        if not self.is_inviting:
                            break
                        self.progress_var.set(f"Flood wait: {remaining}s remaining")
                        time.sleep(1)
                    continue
                    
                except UserPrivacyRestrictedError:
                    failed_count += 1
                    self.log_message(f"✗ @{username}: Privacy settings prevent invitation")
                    
                except UserNotMutualContactError:
                    failed_count += 1
                    self.log_message(f"✗ @{username}: Not a mutual contact")
                    
                except Exception as e:
                    failed_count += 1
                    self.log_message(f"✗ Failed to invite @{username}: {str(e)}")
                
                # Random delay between invites
                if self.is_inviting and i < len(usernames) - 1:
                    actual_delay = delay + random.randint(-5, 5)
                    for remaining in range(actual_delay, 0, -1):
                        if not self.is_inviting:
                            break
                        self.progress_var.set(f"Next invite in {remaining}s...")
                        time.sleep(1)
                
            client.disconnect()
            
            # Final summary
            if self.is_inviting:
                self.log_message(f"\n=== SUMMARY ===")
                self.log_message(f"Total processed: {total_users}")
                self.log_message(f"Successfully invited: {invited_count}")
                self.log_message(f"Failed invitations: {failed_count}")
                self.progress_var.set(f"Completed! {invited_count} invited, {failed_count} failed")
            else:
                self.log_message("Process stopped by user")
                
        except Exception as e:
            self.log_message(f"Critical error: {str(e)}")
            
        finally:
            self.is_inviting = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
    def extract_members(self):
        source_group = self.source_group_entry.get()
        
        if not source_group:
            messagebox.showerror("Error", "Please provide source group link/username")
            return
            
        # Start extraction in a separate thread
        thread = threading.Thread(target=self.extract_members_thread, args=(source_group,))
        thread.daemon = True
        thread.start()
        
    def extract_members_thread(self, source_group):
        try:
            self.extract_text.delete(1.0, tk.END)
            self.extract_text.insert(tk.END, "Initializing Telegram client...\n")
            
            # Initialize Telegram client
            client = TelegramClient('extract_session', self.api_id, self.api_hash)
            client.start()
            
            self.extract_text.insert(tk.END, "Getting group members...\n")
            
            # Get group entity
            group_entity = client.get_entity(source_group)
            
            # Get all participants
            participants = client.get_participants(group_entity, limit=None)
            
            extracted_usernames = []
            visible_count = 0
            total_count = len(participants)
            
            self.extract_text.insert(tk.END, f"Found {total_count} total members. Processing...\n")
            
            for participant in participants:
                # Check if user has username
                if self.extract_with_usernames_var.get() and not participant.username:
                    continue
                    
                # Check visibility (basic check - if user has username, they're likely visible)
                if self.extract_visible_only_var.get():
                    if not participant.username:
                        continue
                    visible_count += 1
                
                if participant.username:
                    extracted_usernames.append(participant.username)
                    
            client.disconnect()
            
            # Display results
            self.extract_text.delete(1.0, tk.END)
            self.extract_text.insert(tk.END, f"=== EXTRACTION RESULTS ===\n")
            self.extract_text.insert(tk.END, f"Total members in group: {total_count}\n")
            self.extract_text.insert(tk.END, f"Extracted usernames: {len(extracted_usernames)}\n\n")
            self.extract_text.insert(tk.END, "Usernames:\n")
            self.extract_text.insert(tk.END, "\n".join(extracted_usernames))
            
            self.extracted_usernames = extracted_usernames
            
        except Exception as e:
            self.extract_text.insert(tk.END, f"Error during extraction: {str(e)}\n")
            
    def save_extracted_members(self):
        if not hasattr(self, 'extracted_usernames') or not self.extracted_usernames:
            messagebox.showerror("Error", "No extracted members to save")
            return
            
        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Members",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
        )
        
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(self.extracted_usernames))
                messagebox.showinfo("Success", f"Extracted members saved successfully ({len(self.extracted_usernames)} usernames)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":  # Fixed the __name__ check
    root = tk.Tk()
    app = TelegramInviteTool(root)
    root.mainloop()