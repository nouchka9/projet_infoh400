# Script d'audit (security_audit.py)
import re
import datetime
from collections import defaultdict

def analyze_security_logs():
    """Analyse les logs de sécurité"""
    
    failed_connections = defaultdict(int)
    successful_connections = defaultdict(int)
    
    with open("logs/hl7_messenger.log", "r") as f:
        for line in f:
            # Détecter tentatives de connexion échouées
            if "Connection refused" in line or "Authentication failed" in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    failed_connections[ip_match.group(1)] += 1
            
            # Détecter connexions réussies
            if "Connection established" in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    successful_connections[ip_match.group(1)] += 1
    
    # Détecter tentatives suspectes (>10 échecs)
    suspicious_ips = {ip: count for ip, count in failed_connections.items() if count > 10}
    
    if suspicious_ips:
        print("🚨 ACTIVITÉ SUSPECTE DÉTECTÉE:")
        for ip, count in suspicious_ips.items():
            print(f"   IP {ip}: {count} tentatives échouées")
    else:
        print("✅ Aucune activité suspecte détectée")
    
    print(f"\n📊 Statistiques connexions:")
    print(f"   Connexions réussies: {sum(successful_connections.values())}")
    print(f"   Tentatives échouées: {sum(failed_connections.values())}")

if __name__ == "__main__":
    analyze_security_logs()