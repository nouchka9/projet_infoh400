# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class BetterCombobox(ttk.Combobox):
    """Combobox avec meilleur comportement des touches"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configurer les événements
        self.bind("<<ComboboxSelected>>", self._on_selection)
        self.bind("<Return>", self._on_return)
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<FocusOut>", self._on_focus_out)
        
    def _on_selection(self, event=None):
        """Quand un élément est sélectionné"""
        # Passer au prochain widget
        self.tk_focusNext().focus()
    
    def _on_return(self, event=None):
        """Quand la touche Entrée est pressée"""
        # Si la liste est affichée, sélectionner l'élément courant
        if self.winfo_viewable():
            self.selection_clear()
            self.focus_set()
            
        # Passer au widget suivant
        self.tk_focusNext().focus()
        return "break"  # Empêcher la propagation
    
    def _on_double_click(self, event=None):
        """Quand un double-clic est effectué"""
        # Valider explicitement la sélection
        self.selection_clear()
        
        # Passer au widget suivant
        self.after(100, lambda: self.tk_focusNext().focus())
    
    def _on_focus_out(self, event=None):
        """Quand le focus quitte le widget"""
        # S'assurer que la liste déroulante est fermée
        self.selection_clear()
