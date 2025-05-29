# Script de rapport (generate_report.py)
import json
import datetime
from collections import Counter

def generate_daily_report():
    """Génère un rapport d'activité quotidien"""
    
    today = datetime.date.today().strftime("%Y%m%d")
    
    # Charger les messages du jour
    with open("resources/messages.json", "r") as f:
        messages = json.load(f)
    
    daily_messages = [
        msg for msg in messages 
        if msg.get("timestamp", "").startswith(today)
    ]
    
    # Statistiques
    stats = {
        "total_messages": len(daily_messages),
        "types_distribution": Counter(msg.get("type", "") for msg in daily_messages),
        "departments": Counter(msg.get("source", "") for msg in daily_messages),
        "success_rate": len([m for m in daily_messages if m.get("status") == "SUCCESS"]) / len(daily_messages) * 100 if daily_messages else 0
    }
    
    # Générer rapport HTML
    report_html = f"""
    <html>
    <head><title>Rapport HL7 - {today}</title></head>
    <body>
        <h1>📊 Rapport d'activité HL7 - {today}</h1>
        <h2>Statistiques générales</h2>
        <ul>
            <li>Total messages: {stats['total_messages']}</li>
            <li>Taux de succès: {stats['success_rate']:.1f}%</li>
        </ul>
        
        <h2>Répartition par type</h2>
        <ul>
        {"".join(f"<li>{type_}: {count}</li>" for type_, count in stats['types_distribution'].items())}
        </ul>
        
        <h2>Activité par département</h2>
        <ul>
        {"".join(f"<li>{dept}: {count}</li>" for dept, count in stats['departments'].items())}
        </ul>
    </body>
    </html>
    """
    
    with open(f"reports/rapport_{today}.html", "w") as f:
        f.write(report_html)
    
    print(f"📋 Rapport généré: reports/rapport_{today}.html")

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    generate_daily_report()