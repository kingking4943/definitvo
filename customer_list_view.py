#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vista "Liste Clienti" per Gestionale Gitemania
Sviluppato da TechExpresso
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable
from theme_manager import GiteManiTheme, ModernUIHelper

class CustomerListView(ttk.Frame):
    def __init__(self, parent, on_filter_apply: Callable, on_export: Callable, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_filter_apply = on_filter_apply
        self.on_export = on_export
        self.customer_data = []
        self._create_widgets()

    def _create_widgets(self):
        header = ModernUIHelper.create_header_frame(self, "👥 Liste Clienti per Prodotto")
        header.pack(fill='x', padx=10, pady=(10,5))

        self._create_filter_bar()

        table_container = ttk.Frame(self, style='Card.TFrame', padding=10)
        table_container.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('customer_name', 'customer_email', 'total_purchases', 'total_spent', 'last_purchase')
        self.tree = ttk.Treeview(table_container, columns=columns, show='headings')
        
        headings = {
            'customer_name': 'Nome Cliente',
            'customer_email': 'Email',
            'total_purchases': 'Acquisti',
            'total_spent': 'Totale Speso',
            'last_purchase': 'Ultimo Acquisto'
        }
        widths = {
            'customer_name': 250,
            'customer_email': 250,
            'total_purchases': 100,
            'total_spent': 150,
            'last_purchase': 180
        }
        
        for col, text in headings.items():
            self.tree.heading(col, text=text)
        for col, width in widths.items():
            self.tree.column(col, width=width, anchor='w')

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

    def _create_filter_bar(self):
        filter_frame = ttk.Frame(self, padding=(10, 5))
        filter_frame.pack(fill='x')

        ttk.Label(filter_frame, text="Prodotto:").pack(side='left', padx=(0, 5))
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(filter_frame, textvariable=self.product_var, state="readonly", width=40)
        self.product_combo.pack(side='left', padx=(0, 15))

        ttk.Label(filter_frame, text="Da:").pack(side='left', padx=(10, 5))
        self.date_from_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.date_from_var, width=12).pack(side='left')

        ttk.Label(filter_frame, text="A:").pack(side='left', padx=(10, 5))
        self.date_to_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.date_to_var, width=12).pack(side='left')

        apply_button = ttk.Button(filter_frame, text="Mostra Clienti", command=self.on_filter_apply, style="Primary.TButton")
        apply_button.pack(side='left', padx=15)
        
        export_button = ttk.Button(filter_frame, text="Esporta CSV", command=self._on_export_click, style="Success.TButton")
        export_button.pack(side='left', padx=5)

    def _on_export_click(self):
        if not self.customer_data:
            messagebox.showwarning("Nessun Dato", "Non ci sono dati da esportare. Applica un filtro prima.")
            return
        
        product_name = self.product_var.get()
        if not product_name:
            messagebox.showwarning("Nessun Prodotto", "Seleziona un prodotto prima di esportare.")
            return
            
        self.on_export(self.customer_data, product_name)

    def update_products_list(self, products: List[Dict]):
        self.product_list = products
        product_names = [p['name'] for p in products]
        self.product_combo['values'] = product_names

    def get_selected_product_id(self):
        selected_name = self.product_var.get()
        for product in self.product_list:
            if product['name'] == selected_name:
                return product['id']
        return None

    def update_customer_list(self, customers: List[Dict]):
        self.customer_data = customers
        self.tree.delete(*self.tree.get_children())
        if customers:
            for customer in customers:
                values = (
                    customer['customer_name'],
                    customer['customer_email'],
                    customer['total_purchases'],
                    f"€ {customer['total_spent']:.2f}",
                    customer['last_purchase']
                )
                self.tree.insert('', 'end', values=values)
