#!/usr/bin/env python3
"""
opnsense-summary.py: print a sanitized summary of an OPNsense config.xml.

Reads the backup locally and prints only structure: interfaces, VLANs,
firewall rules, DHCP ranges, NAT/port forwards, WireGuard layout, DNS
settings and installed plugins.

Never printed: passwords or hashes, API keys, WireGuard private keys and
pre-shared keys, certificates, MAC addresses, public IP addresses, email
addresses. A final pass redacts anything that still looks like one of those.

Usage:
    python3 opnsense-summary.py ~/Downloads/config-OPNsense.xml > summary.md
Then READ summary.md before sharing it.
"""
import ipaddress
import re
import sys
import xml.etree.ElementTree as ET

# Only these ranges are shown; every other IPv4 address is treated as public.
SAFE_NETS = [ipaddress.ip_network(n) for n in (
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "100.64.0.0/10",
    "127.0.0.0/8", "169.254.0.0/16", "0.0.0.0/32")]


def is_safe_ip(value):
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return True
    return any(ip in n for n in SAFE_NETS)

if len(sys.argv) != 2:
    sys.exit("usage: python3 opnsense-summary.py <config.xml>")

root = ET.parse(sys.argv[1]).getroot()
out = []


def p(line=""):
    out.append(line)


def t(el, path, default=""):
    if el is None:
        return default
    found = el.find(path)
    return (found.text or "").strip() if found is not None and found.text else default


def flag(el, path):
    return el is not None and el.find(path) is not None


def iface_names():
    names = {}
    ifs = root.find("interfaces")
    if ifs is not None:
        for i in ifs:
            names[i.tag] = t(i, "descr") or i.tag.upper()
    return names


NAMES = iface_names()


def nice_if(tag):
    return ", ".join(NAMES.get(x, x) for x in tag.split(",")) if tag else "any"


def addr(el):
    """Describe a rule source/destination without leaking public IPs."""
    if el is None:
        return "any"
    if flag(el, "any"):
        base = "any"
    elif t(el, "network"):
        n = t(el, "network")
        base = NAMES.get(n.replace("ip", ""), n) + (" address" if n.endswith("ip") else " net")
    elif t(el, "address"):
        base = t(el, "address")
    else:
        base = "any"
    if flag(el, "not"):
        base = "NOT " + base
    port = t(el, "port")
    return f"{base}:{port}" if port else base


p("# OPNsense configuration summary (sanitized)")
p()
p(f"- OPNsense version in backup: {t(root, 'version', 'unknown')}")
p(f"- Hostname: (redacted). Domain: {'set' if t(root, 'system/domain') else 'not set'}")
p(f"- Time zone: {t(root, 'system/timezone', 'unknown')}")
p(f"- DNS servers configured: {len(root.findall('system/dnsserver'))}")
p(f"- SSH enabled: {'yes' if flag(root, 'system/ssh/enabled') or t(root, 'system/ssh/enabled') == 'enabled' else 'no'}"
  f", root login: {'permitted' if flag(root, 'system/ssh/permitrootlogin') else 'not permitted'}"
  f", password auth: {'on' if flag(root, 'system/ssh/passwordauth') else 'off'}")
webgui = root.find("system/webgui")
p(f"- Web GUI protocol: {t(webgui, 'protocol', 'unknown')}, "
  f"listen interfaces: {nice_if(t(webgui, 'interfaces')) if t(webgui, 'interfaces') else 'all'}")
p(f"- Users: {len(root.findall('system/user'))} (names and hashes not shown)")
p()

p("## Interfaces")
p("| Interface | Device | IPv4 | Enabled | Block private / bogon |")
p("|---|---|---|---|---|")
ifs = root.find("interfaces")
if ifs is not None:
    for i in ifs:
        ip = t(i, "ipaddr")
        sub = t(i, "subnet")
        if ip and ip not in ("dhcp", "pppoe"):
            ip = f"{ip}/{sub}" if is_safe_ip(ip) else "(public, redacted)"
        p(f"| {NAMES[i.tag]} ({i.tag}) | {t(i, 'if')} | {ip or 'none'} | "
          f"{'yes' if flag(i, 'enable') else 'no'} | "
          f"{'yes' if flag(i, 'blockpriv') else 'no'} / {'yes' if flag(i, 'blockbogons') else 'no'} |")
p()

vlans = root.findall("vlans/vlan")
p("## VLANs")
if vlans:
    p("| Tag | Parent | Device | Description |")
    p("|---|---|---|---|")
    for v in vlans:
        p(f"| {t(v, 'tag')} | {t(v, 'if')} | {t(v, 'vlanif')} | {t(v, 'descr')} |")
else:
    p("None configured.")
p()

p("## DHCP (ISC)")
dhcpd = root.find("dhcpd")
if dhcpd is not None and len(dhcpd):
    p("| Interface | Enabled | Range | Static mappings |")
    p("|---|---|---|---|")
    for d in dhcpd:
        p(f"| {NAMES.get(d.tag, d.tag)} | {'yes' if flag(d, 'enable') else 'no'} | "
          f"{t(d, 'range/from')} – {t(d, 'range/to')} | {len(d.findall('staticmap'))} |")
else:
    p("No ISC DHCP config found (may use Kea or Dnsmasq instead).")
kea = root.find(".//Kea")
if kea is not None:
    subnets = kea.findall(".//subnet4")
    p(f"- Kea DHCP present: {len(subnets)} subnet(s), {len(kea.findall('.//reservation'))} reservation(s)")
dnsmasq = root.find(".//dnsmasq")
if dnsmasq is not None:
    p(f"- Dnsmasq present: enabled={'yes' if t(dnsmasq, 'enable') in ('1', 'yes') or flag(dnsmasq, 'enable') else 'no'}")
p()

p("## Firewall rules (in order)")
rules = root.findall("filter/rule")
p(f"{len(rules)} rule(s) in the legacy rules table.")
if rules:
    p("| # | Interface | Action | Proto | Source | Destination | Description | Enabled |")
    p("|---|---|---|---|---|---|---|---|")
    for n, r in enumerate(rules, 1):
        p(f"| {n} | {nice_if(t(r, 'interface'))} | {t(r, 'type', 'pass')} | {t(r, 'protocol', 'any')} | "
          f"{addr(r.find('source'))} | {addr(r.find('destination'))} | {t(r, 'descr')} | "
          f"{'no' if flag(r, 'disabled') else 'yes'} |")
new_rules = root.findall(".//Firewall/Filter/rules/rule")
if new_rules:
    p()
    p(f"{len(new_rules)} rule(s) in the newer automation rules table:")
    for r in new_rules:
        p(f"- {t(r, 'action')} {t(r, 'protocol')} on {nice_if(t(r, 'interface'))}: "
          f"{t(r, 'source_net', 'any')} → {t(r, 'destination_net', 'any')}:{t(r, 'destination_port')} "
          f"({t(r, 'description')})")
p()

p("## NAT")
pf = root.findall("nat/rule")
p(f"- Port forwards: {len(pf)}")
for r in pf:
    p(f"  - {nice_if(t(r, 'interface'))} {t(r, 'protocol')} port {t(r, 'destination/port')} → "
      f"local port {t(r, 'local-port')} ({t(r, 'descr')})")
p(f"- Outbound NAT mode: {t(root, 'nat/outbound/mode', 'automatic (default)')}")
p()

p("## Aliases")
aliases = root.findall(".//Firewall/Alias/aliases/alias") or root.findall("aliases/alias")
for a in aliases:
    content = t(a, "content")
    count = len([c for c in re.split(r"[\s,]+", content) if c]) if content else 0
    p(f"- {t(a, 'name')} ({t(a, 'type')}): {count} entr{'y' if count == 1 else 'ies'} – {t(a, 'description') or t(a, 'descr')}")
if not aliases:
    p("None found.")
p()

p("## WireGuard")
wg = root.find(".//wireguard")
if wg is not None:
    servers = wg.findall(".//server/servers/server")
    peers = wg.findall(".//client/clients/client")
    p(f"- Enabled: {'yes' if t(wg, 'general/enabled') == '1' else 'no'}")
    p(f"- Instances: {len(servers)}")
    for s in servers:
        tunnel = t(s, "tunneladdress")
        p(f"  - {t(s, 'name')}: listen port {t(s, 'port')}, tunnel {tunnel}, "
          f"peers linked: {len([x for x in t(s, 'peers').split(',') if x])}")
    p(f"- Peers: {len(peers)} (names, keys and endpoints not shown)")
    for c in peers:
        p(f"  - allowed IPs: {t(c, 'tunneladdress')}, keepalive: {t(c, 'keepalive') or 'off'}")
else:
    p("No WireGuard config found.")
p()

p("## DNS (Unbound)")
ub = root.find(".//unboundplus")
if ub is not None:
    p(f"- Enabled: {t(ub, 'general/enabled')}")
    p(f"- DNSSEC: {t(ub, 'general/dnssec')}")
    p(f"- Listening interfaces: {nice_if(t(ub, 'general/active_interface')) or 'all'}")
    p(f"- Query forwarding: {t(ub, 'forwarding/enabled') or 'off'}")
    p(f"- DNS over TLS forwarders: {len(ub.findall('.//dots/dot'))}")
    p(f"- Host overrides: {len(ub.findall('.//hosts/host'))}")
    bl = ub.find("dnsbl")
    if bl is not None:
        p(f"- Blocklists enabled: {t(bl, 'enabled')}, lists: {t(bl, 'type') or 'none'}")
        p(f"- Custom blocklist URLs: {len([x for x in t(bl, 'lists').split(',') if x])}")
    p(f"- Query logging/stats: {t(ub, 'general/stats') or 'off'}")
else:
    p("No Unbound (unboundplus) config found.")
p()

p("## Intrusion detection (Suricata)")
ids = root.find(".//IDS")
if ids is not None:
    p(f"- Enabled: {t(ids, 'general/enabled')}, IPS mode: {t(ids, 'general/ips')}, "
      f"interfaces: {nice_if(t(ids, 'general/interfaces'))}")
    p(f"- Rulesets enabled: {len([f for f in ids.findall('.//files/file') if t(f, 'enabled') == '1'])}")
else:
    p("Not configured.")
p()

p("## Remote logging")
targets = root.findall(".//Syslog/destinations/destination")
for d in targets:
    p(f"- {t(d, 'transport')} to {t(d, 'hostname')}:{t(d, 'port')}, enabled {t(d, 'enabled')}")
if not targets:
    p("None configured.")
p()

p("## Plugins installed")
plugins = t(root, "system/firmware/plugins")
p(", ".join(sorted(plugins.split(","))) if plugins else "None listed.")

text = "\n".join(out)

# Final safety pass: redact anything that still looks sensitive.
text = re.sub(r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b", "(mac redacted)", text)
text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "(email redacted)", text)
text = re.sub(r"\b[A-Za-z0-9+/]{40,}={0,2}", "(key-like value redacted)", text)


def redact_public(m):
    return m.group(0) if is_safe_ip(m.group(0)) else "(public IP redacted)"


text = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", redact_public, text)
print(text)
