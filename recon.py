#!/usr/bin/env python3
import argparse, csv, datetime as dt, html, os, subprocess, tempfile, xml.etree.ElementTree as ET
from pathlib import Path

def run_nmap(targets, profile, udp, timing, rate, out_xml):
    args = ["nmap"]
    # profiles
    if profile == "quick":
        args += ["-sV", "-T"+timing]          # top-1000, service detection
    elif profile == "full":
        args += ["-sC", "-sV", "-O", "-T"+timing]  # default scripts, service, OS
    if udp:
        args += ["-sU"]                       # note: slower
    if rate:
        args += ["--min-rate", str(rate)]
    args += ["-oX", out_xml]
    args += targets
    subprocess.run(args, check=True)
    return out_xml

def parse_xml(xml_path):
    rows = []
    root = ET.parse(xml_path).getroot()
    for host in root.findall("host"):
        addr = host.find("address")
        ip = addr.get("addr") if addr is not None else "unknown"
        for port in host.findall("./ports/port"):
            state = port.find("state").get("state")
            svc = port.find("service")
            rows.append({
                "ip": ip,
                "port": port.get("portid"),
                "proto": port.get("protocol"),
                "state": state,
                "service": "" if svc is None else svc.get("name", ""),
                "product": "" if svc is None else svc.get("product", ""),
                "version": "" if svc is None else svc.get("version", ""),
            })
    return rows

def write_csv(rows, out_csv):
    if not rows:
        Path(out_csv).write_text("", encoding="utf-8"); return
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def html_report(rows, targets, started_at):
    title = "Network Recon Report"
    ts = started_at.strftime("%Y-%m-%d %H:%M UTC")
    target_str = ", ".join(html.escape(t) for t in targets)
    style = """
<!doctype html><meta charset="utf-8"><title>{}</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#f7f9fc;margin:24px}}
h1{{color:#13294b;margin:0 0 8px}}
small{{color:#5b6876}}
table{{border-collapse:collapse;width:100%;margin-top:16px;background:#fff}}
th,td{{border:1px solid #e6e9ef;padding:8px 10px;font-size:14px}}
th{{background:#eef2f8;text-align:left}}
tr:nth-child(even){{background:#fbfdff}}
.badge{{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef2f8;color:#13294b;font-size:12px}}
</style>""".format(title)
    header = f"<h1>{title}</h1><small>Targets: <b>{target_str}</b> • Generated: {ts}</small>"
    if not rows:
        return style + header + "<p>No open ports found or scan returned no data.</p>"

    # Summary
    host_count = len({r['ip'] for r in rows})
    port_count = len(rows)
    summary = f"<p><span class='badge'>{host_count} host(s)</span> <span class='badge'>{port_count} open/service entries</span></p>"

    # Table
    table = ["<table><tr><th>IP</th><th>Port</th><th>Proto</th><th>State</th><th>Service</th><th>Product</th><th>Version</th></tr>"]
    for r in rows:
        table.append(
            f"<tr><td>{r['ip']}</td><td>{r['port']}</td><td>{r['proto']}</td>"
            f"<td>{r['state']}</td><td>{html.escape(r['service'])}</td>"
            f"<td>{html.escape(r['product'])}</td><td>{html.escape(r['version'])}</td></tr>"
        )
    table.append("</table>")
    return style + header + summary + "".join(table)

def main():
    p = argparse.ArgumentParser(description="Nmap wrapper that outputs HTML + CSV.")
    p.add_argument("targets", nargs="+", help="Target(s) or CIDR (e.g., 192.168.1.10 or 10.0.0.0/24)")
    p.add_argument("-p", "--profile", choices=["quick","full"], default="quick", help="Scan profile")
    p.add_argument("--udp", action="store_true", help="Include UDP scan (slower)")
    p.add_argument("-t", "--timing", choices=list("012345"), default="4", help="Nmap T0–T5 (default T4)")
    p.add_argument("--rate", type=int, default=0, help="--min-rate packets/sec")
    p.add_argument("-o", "--outdir", default="reports", help="Output directory (default: reports)")
    args = p.parse_args()

    started = dt.datetime.utcnow()
    outdir = Path(args.outdir) / started.strftime("%Y%m%d_%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)
    xml_path = str(outdir / "scan.xml")
    csv_path = str(outdir / "results.csv")
    html_path = str(outdir / "report.html")

    run_nmap(args.targets, args.profile, args.udp, args.timing, args.rate, xml_path)
    rows = parse_xml(xml_path)
    write_csv(rows, csv_path)
    Path(html_path).write_text(html_report(rows, args.targets, started), encoding="utf-8")

    print("✔ Done")
    print(f"  HTML : {html_path}")
    print(f"  CSV  : {csv_path}")
    print("Note: Only scan systems you own or have permission to test.")

if __name__ == "__main__":
    main()
