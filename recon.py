import sys, subprocess, tempfile, xml.etree.ElementTree as ET, datetime, html

def run_nmap(target):
    tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
    xml_path = tmp.name
    tmp.close()
    subprocess.run(["nmap", "-sV", "-T4", "-oX", xml_path, target], check=True)
    return xml_path

def parse(xml_path):
    rows = []
    root = ET.parse(xml_path).getroot()
    for h in root.findall("host"):
        addr = h.find("address")
        ip = addr.get("addr") if addr is not None else "unknown"
        for p in h.findall("./ports/port"):
            state_el = p.find("state")
            svc_el = p.find("service")
            rows.append({
                "ip": ip,
                "port": p.get("portid"),
                "proto": p.get("protocol"),
                "state": state_el.get("state") if state_el is not None else "",
                "service": (svc_el.get("name") if svc_el is not None else ""),
                "version": (svc_el.get("version") if svc_el is not None else "")
            })
    return rows

def to_html(rows, target):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    head = """<!doctype html><meta charset="utf-8"><title>Recon Report</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;background:#f7f9fc;margin:20px}
h1{color:#13294b} table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ddd;padding:8px} th{background:#eef2f8;text-align:left}
tr:nth-child(even){background:#fff}
</style>"""
    intro = f"<h1>Recon Report</h1><p>Target: <b>{html.escape(target)}</b><br>Generated: {now}</p>"
    table = "<table><tr><th>IP</th><th>Port</th><th>Proto</th><th>State</th><th>Service</th><th>Version</th></tr>"
    for r in rows:
        table += f"<tr><td>{r['ip']}</td><td>{r['port']}</td><td>{r['proto']}</td><td>{r['state']}</td><td>{html.escape(r['service'])}</td><td>{html.escape(r['version'])}</td></tr>"
    table += "</table>"
    return head + intro + table

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 recon.py <target_or_cidr>")
        sys.exit(1)
    target = sys.argv[1]
    xml_path = run_nmap(target)
    rows = parse(xml_path)
    open("report.html", "w", encoding="utf-8").write(to_html(rows, target))
    print("✔ report.html created")
    print("Note: Only scan systems you own or have permission to test.")
