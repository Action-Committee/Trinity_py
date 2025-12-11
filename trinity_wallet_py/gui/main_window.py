"""
Windows GUI for Trinity Wallet using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import threading
from typing import Optional
from ..core.wallet import Wallet
from ..core.key import validate_address


class TrinityWalletGUI:
    """Main GUI window for Trinity Wallet."""
    
    def __init__(self):
        """Initialize the GUI."""
        self.wallet: Optional[Wallet] = None
        self.root = tk.Tk()
        self.root.title("Trinity Wallet")
        self.root.geometry("900x700")
        
        # Set up the GUI
        self.setup_ui()
        
        # Initialize wallet
        try:
            self.wallet = Wallet()
        except:
            # Create new wallet if loading fails
            self.wallet = Wallet()
        
        # Auto-connect to local node
        self.connect_to_default_node()
        
        # Initial update
        self.update_balance()
        self.update_addresses()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Wallet menu
        wallet_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Wallet", menu=wallet_menu)
        wallet_menu.add_command(label="New Address", command=self.new_address)
        wallet_menu.add_command(label="Import Private Key", command=self.import_key)
        wallet_menu.add_command(label="Export Private Key", command=self.export_key)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Connect to Node", command=self.connect_to_node)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Balance section
        balance_frame = ttk.LabelFrame(main_frame, text="Balance", padding="10")
        balance_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.balance_label = ttk.Label(balance_frame, text="0.00000000 TRINITY", 
                                       font=("Arial", 16, "bold"))
        self.balance_label.pack()
        
        ttk.Button(balance_frame, text="Refresh", command=self.update_balance).pack(pady=5)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Send tab
        send_frame = ttk.Frame(notebook, padding="10")
        notebook.add(send_frame, text="Send")
        self.setup_send_tab(send_frame)
        
        # Receive tab
        receive_frame = ttk.Frame(notebook, padding="10")
        notebook.add(receive_frame, text="Receive")
        self.setup_receive_tab(receive_frame)
        
        # Transactions tab
        transactions_frame = ttk.Frame(notebook, padding="10")
        notebook.add(transactions_frame, text="Transactions")
        self.setup_transactions_tab(transactions_frame)
        
        # Addresses tab
        addresses_frame = ttk.Frame(notebook, padding="10")
        notebook.add(addresses_frame, text="Addresses")
        self.setup_addresses_tab(addresses_frame)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Status: Ready", 
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def setup_send_tab(self, parent):
        """Set up the Send tab."""
        # To address
        ttk.Label(parent, text="Pay To:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.send_to_entry = ttk.Entry(parent, width=50)
        self.send_to_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Amount
        ttk.Label(parent, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.send_amount_entry = ttk.Entry(parent, width=20)
        self.send_amount_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Send button
        ttk.Button(parent, text="Send", command=self.send_coins).grid(row=2, column=1, 
                                                                       sticky=tk.W, pady=10)
        
        parent.columnconfigure(1, weight=1)
    
    def setup_receive_tab(self, parent):
        """Set up the Receive tab."""
        ttk.Label(parent, text="Your Addresses:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        # Listbox for addresses
        listbox_frame = ttk.Frame(parent)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.receive_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, 
                                          font=("Courier", 10))
        self.receive_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.receive_listbox.yview)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="New Address", command=self.new_address).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy Selected", command=self.copy_address).pack(side=tk.LEFT, padx=5)
    
    def setup_transactions_tab(self, parent):
        """Set up the Transactions tab."""
        # Transaction list
        self.tx_text = scrolledtext.ScrolledText(parent, height=20, width=80, font=("Courier", 9))
        self.tx_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(parent, text="Refresh", command=self.update_transactions).pack(pady=5)
    
    def setup_addresses_tab(self, parent):
        """Set up the Addresses tab."""
        # Address list with labels
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for addresses
        columns = ('address', 'label')
        self.addresses_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        self.addresses_tree.heading('address', text='Address')
        self.addresses_tree.heading('label', text='Label')
        self.addresses_tree.column('address', width=400)
        self.addresses_tree.column('label', width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.addresses_tree.yview)
        self.addresses_tree.configure(yscrollcommand=scrollbar.set)
        
        self.addresses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Set Label", command=self.set_address_label).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.update_addresses).pack(side=tk.LEFT, padx=5)
    
    def connect_to_default_node(self):
        """Connect to local Trinity node with default settings."""
        try:
            self.wallet.connect_to_node(host='127.0.0.1', port=6420, 
                                       username='rpcuser', password='rpcpassword')
            self.status_label.config(text="Status: Connected to local node")
        except Exception as e:
            self.status_label.config(text=f"Status: Not connected - {str(e)}")
    
    def connect_to_node(self):
        """Show dialog to connect to a node."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Connect to Node")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        host_entry = ttk.Entry(dialog, width=30)
        host_entry.insert(0, "127.0.0.1")
        host_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Port:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        port_entry = ttk.Entry(dialog, width=30)
        port_entry.insert(0, "6420")
        port_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Username:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        user_entry = ttk.Entry(dialog, width=30)
        user_entry.insert(0, "rpcuser")
        user_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Password:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        pass_entry = ttk.Entry(dialog, width=30, show="*")
        pass_entry.insert(0, "rpcpassword")
        pass_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def do_connect():
            try:
                host = host_entry.get()
                port = int(port_entry.get())
                username = user_entry.get()
                password = pass_entry.get()
                
                self.wallet.connect_to_node(host, port, username, password)
                messagebox.showinfo("Success", "Connected to node successfully!")
                dialog.destroy()
                self.update_balance()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to connect: {str(e)}")
        
        ttk.Button(dialog, text="Connect", command=do_connect).grid(row=4, column=1, 
                                                                    pady=10, sticky=tk.E)
    
    def update_balance(self):
        """Update balance display."""
        def update():
            try:
                balance = self.wallet.get_balance()
                self.balance_label.config(text=f"{balance:.8f} TRINITY")
                self.status_label.config(text="Status: Balance updated")
            except Exception as e:
                self.balance_label.config(text="0.00000000 TRINITY")
                self.status_label.config(text=f"Status: Error - {str(e)}")
        
        # Run in background thread
        thread = threading.Thread(target=update, daemon=True)
        thread.start()
    
    def update_addresses(self):
        """Update the addresses list."""
        # Clear existing
        self.receive_listbox.delete(0, tk.END)
        for item in self.addresses_tree.get_children():
            self.addresses_tree.delete(item)
        
        # Add addresses
        for address in self.wallet.get_addresses():
            label = self.wallet.get_label(address)
            display = f"{address} ({label})" if label else address
            self.receive_listbox.insert(tk.END, display)
            self.addresses_tree.insert('', tk.END, values=(address, label))
    
    def update_transactions(self):
        """Update the transactions list."""
        def update():
            try:
                self.tx_text.delete(1.0, tk.END)
                txs = self.wallet.get_transactions(count=50)
                
                if not txs:
                    self.tx_text.insert(tk.END, "No transactions found.\n")
                else:
                    for tx in txs:
                        category = tx.get('category', 'unknown')
                        amount = tx.get('amount', 0)
                        address = tx.get('address', 'N/A')
                        confirmations = tx.get('confirmations', 0)
                        txid = tx.get('txid', 'N/A')
                        
                        line = f"{category:10} {amount:15.8f} TRINITY  {address:40} ({confirmations} conf)\n"
                        self.tx_text.insert(tk.END, line)
                        self.tx_text.insert(tk.END, f"           TxID: {txid}\n\n")
                
                self.status_label.config(text="Status: Transactions updated")
            except Exception as e:
                self.tx_text.insert(tk.END, f"Error loading transactions: {str(e)}\n")
        
        thread = threading.Thread(target=update, daemon=True)
        thread.start()
    
    def new_address(self):
        """Generate a new address."""
        label = simpledialog.askstring("New Address", "Enter label (optional):")
        if label is not None:  # User didn't cancel
            try:
                address = self.wallet.add_new_key(label)
                self.update_addresses()
                messagebox.showinfo("Success", f"New address created:\n{address}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create address: {str(e)}")
    
    def import_key(self):
        """Import a private key."""
        wif = simpledialog.askstring("Import Key", "Enter private key (WIF format):")
        if wif:
            label = simpledialog.askstring("Label", "Enter label (optional):")
            try:
                address = self.wallet.import_private_key(wif, label or '')
                self.update_addresses()
                messagebox.showinfo("Success", f"Key imported successfully:\n{address}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import key: {str(e)}")
    
    def export_key(self):
        """Export a private key."""
        # Get selected address
        selection = self.addresses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an address first")
            return
        
        item = self.addresses_tree.item(selection[0])
        address = item['values'][0]
        
        # Confirm
        if not messagebox.askyesno("Confirm", 
                                    "Are you sure you want to export the private key?\n\n"
                                    "WARNING: Anyone with access to this key can spend your funds!"):
            return
        
        try:
            wif = self.wallet.export_private_key(address)
            
            # Show in dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Private Key")
            dialog.geometry("600x150")
            
            ttk.Label(dialog, text="Private Key (WIF format):", font=("Arial", 10, "bold")).pack(pady=10)
            
            key_text = tk.Text(dialog, height=2, width=70, font=("Courier", 10))
            key_text.insert(1.0, wif)
            key_text.config(state=tk.DISABLED)
            key_text.pack(pady=5)
            
            ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export key: {str(e)}")
    
    def copy_address(self):
        """Copy selected address to clipboard."""
        selection = self.receive_listbox.curselection()
        if selection:
            text = self.receive_listbox.get(selection[0])
            address = text.split()[0]  # Get just the address part
            self.root.clipboard_clear()
            self.root.clipboard_append(address)
            messagebox.showinfo("Copied", f"Address copied to clipboard:\n{address}")
        else:
            messagebox.showwarning("Warning", "Please select an address first")
    
    def set_address_label(self):
        """Set label for selected address."""
        selection = self.addresses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an address first")
            return
        
        item = self.addresses_tree.item(selection[0])
        address = item['values'][0]
        current_label = item['values'][1]
        
        label = simpledialog.askstring("Set Label", f"Enter label for address:\n{address}", 
                                      initialvalue=current_label)
        if label is not None:
            self.wallet.set_label(address, label)
            self.update_addresses()
    
    def send_coins(self):
        """Send coins to an address."""
        to_address = self.send_to_entry.get().strip()
        amount_str = self.send_amount_entry.get().strip()
        
        # Validate inputs
        if not to_address:
            messagebox.showwarning("Warning", "Please enter a destination address")
            return
        
        if not validate_address(to_address):
            messagebox.showwarning("Warning", "Invalid Trinity address")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Warning", "Amount must be positive")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Invalid amount")
            return
        
        # Confirm
        if not messagebox.askyesno("Confirm", 
                                    f"Send {amount:.8f} TRINITY to:\n{to_address}\n\n"
                                    "Are you sure?"):
            return
        
        # Send
        def do_send():
            try:
                txid = self.wallet.send_to_address(to_address, amount)
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                                                                f"Transaction sent!\n\nTxID:\n{txid}"))
                self.root.after(0, self.update_balance)
                self.send_to_entry.delete(0, tk.END)
                self.send_amount_entry.delete(0, tk.END)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                                                                 f"Failed to send: {str(e)}"))
        
        thread = threading.Thread(target=do_send, daemon=True)
        thread.start()
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("About Trinity Wallet", 
                           "Trinity Wallet v1.0.0\n\n"
                           "A Python-based Windows wallet for Trinity cryptocurrency.\n\n"
                           "Trinity uses three mining algorithms:\n"
                           "- SHA256D\n"
                           "- Scrypt\n"
                           "- Groestl\n\n"
                           "For more information, visit the Trinity website.")
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
