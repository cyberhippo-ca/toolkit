# Toolkit

Tools, services and references I use for my homelab, my domain and website, and security work.

Write-ups showing these in use: **[cyberhippo.ca](https://cyberhippo.ca)**

✅ in use · 🛠️ part of the lab build · 🔖 bookmarked, not used yet

**Jump to:** [Git](#git-and-docs) · [DNS](#domain-and-dns) · [Email](#email-spoofing-protection) · [Web security](#web-hosting-and-security-headers) · [Accessibility](#accessibility-and-site-quality) · [Network](#firewall-vpn-and-network) · [Remote access](#remote-access) · [Self-hosted](#self-hosted-services) · [macOS](#macos-checks) · [Security lab](#security-lab) · [Scripts](#scripts-in-this-repo) · [Lists](#lists-and-references)

---

## Git and docs

- ✅ **[Git](https://git-scm.com/)**: version control for my homelab docs and site
- ✅ **[GitHub commit signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)**: SSH-signed commits, so every change shows as verified
- ✅ **[EditorConfig](https://editorconfig.org/)**: the same formatting on Mac and Windows
- ✅ **[Mermaid](https://mermaid.js.org/)**: network diagrams written as text in Markdown

## Domain and DNS

- ✅ **[Cloudflare DNSSEC](https://developers.cloudflare.com/dns/dnssec/)**: signing my zone
- ✅ **`dig`**: checking SPF, DMARC, DKIM, MX and DS records from the command line
- 🔖 **[DNSViz](https://dnsviz.net/)**: visual check of the DNSSEC chain of trust
- 🔖 **[ICANN Lookup](https://lookup.icann.org/)**: what WHOIS/RDAP shows about a domain
- 🔖 **[CIRA WHOIS](https://www.cira.ca/whois)**: WHOIS for `.ca` domains

## Email spoofing protection

For a domain that sends no mail: reject anything that claims to come from it.

- ✅ **[RFC 7489 (DMARC)](https://www.rfc-editor.org/rfc/rfc7489)**: reference for the DMARC record
- ✅ **[RFC 7505 (Null MX)](https://www.rfc-editor.org/rfc/rfc7505)**: telling the world the domain takes no mail
- 🔖 **[MXToolbox SuperTool](https://mxtoolbox.com/SuperTool.aspx)**: quick SPF, DMARC, MX and blacklist lookups
- 🔖 **[dmarcian DMARC Inspector](https://dmarcian.com/dmarc-inspector/)**: checking a DMARC record
- 🔖 **[mail-tester](https://www.mail-tester.com/)**: deliverability score, for a domain that does send mail

## Web hosting and security headers

- ✅ **[Cloudflare Pages](https://pages.cloudflare.com/)**: hosting my static site from a GitHub repo
- ✅ **[Pages `_headers` file](https://developers.cloudflare.com/pages/configuration/headers/)**: CSP, COOP, CORP and the other security headers
- ✅ **[securityheaders.com](https://securityheaders.com/)**: grading the headers (A+)
- 🔖 **[Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory)**: second opinion on headers
- 🔖 **[SSL Labs](https://www.ssllabs.com/ssltest/)**: TLS configuration test
- 🔖 **[Internet.nl](https://internet.nl/)**: website and email standards in one test
- 🔖 **[OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)**: practical web security guidance
- 🔖 **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**: the most common web app risks

## Accessibility and site quality

- ✅ **[Lighthouse](https://developer.chrome.com/docs/lighthouse/overview)**: performance, accessibility, best practices and SEO scores
- ✅ **[axe-core](https://github.com/dequelabs/axe-core)**: automated accessibility scan against WCAG
- ✅ **[WCAG 2.2](https://www.w3.org/TR/WCAG22/)**: the standard I test against
- 🔖 **[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)**: checking colour contrast by hand

## Firewall, VPN and network

- ✅ **[OPNsense](https://opnsense.org/)**: edge firewall, NAT, DHCP, DNS (Unbound) and VLANs
- ✅ **[Protectli](https://protectli.com/)**: the hardware the firewall runs on
- ✅ **[WireGuard](https://www.wireguard.com/install/)**: VPN for remote access, on OPNsense, my laptop and my phone ([OPNsense guide](https://docs.opnsense.org/manual/how-tos/wireguard-client.html))
- ✅ **[canyouseeme.org](https://canyouseeme.org/)**: checking from outside whether a port is open
- ✅ **[Pi-hole](https://pi-hole.net/)**: DNS-level ad and tracker blocking ([Docker image](https://github.com/pi-hole/docker-pi-hole))
- 🛠️ **[Suricata](https://suricata.io/)**: intrusion detection on the WAN

## Remote access

- ✅ **macOS Screen Sharing**: remote desktop to my Mac mini, over WireGuard only
- ✅ **[bVNC](https://github.com/iiordanov/remote-desktop-clients)**: VNC from my Android phone, signing in with a macOS account
- ✅ **[Cloudflare Tunnel](https://github.com/cloudflare/cloudflared)**: publishing one self-hosted app with no port forward ([docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/))
- ✅ **[Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)**: an email one-time-code login in front of that app

## Self-hosted services

Running in Docker on my Mac mini.

- ✅ **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: running the containers
- ✅ **[Homepage](https://github.com/gethomepage/homepage)**: dashboard for the lab
- ✅ **[Uptime Kuma](https://github.com/louislam/uptime-kuma)**: uptime monitoring
- ✅ **[Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker)**: internet speed over time
- ✅ **[Tautulli](https://github.com/Tautulli/Tautulli)**: Plex monitoring
- ✅ **Docker socket proxy** (e.g. [Tecnativa](https://github.com/Tecnativa/docker-socket-proxy)): limited Docker API access for Homepage, instead of the raw socket
- 🛠️ **[Home Assistant](https://www.home-assistant.io/)**: home automation on its own VLAN

## macOS checks

Commands I used to audit remote access on a Mac.

```sh
# Screen Sharing login history: successes, failures and source IPs
log show --predicate 'process == "screensharingd"' --last 7d | grep -i auth

# Every program listening for network connections
sudo lsof -nP -iTCP -sTCP:LISTEN

# Background services that start automatically (finds remote access tools)
ls /Library/LaunchDaemons /Library/LaunchAgents ~/Library/LaunchAgents

# Which containers publish which ports
docker ps --format '{{.Names}}\t{{.Ports}}'
```

## Security lab

Planned in my lab build; not all running yet.

- 🛠️ **[Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview)**: hypervisor for the lab hosts
- 🛠️ **[Wazuh](https://wazuh.com/)**: SIEM and vulnerability management
- 🛠️ **[Kali Linux](https://www.kali.org/)**: attack box on an isolated lab VLAN
- 🛠️ **[Keycloak](https://www.keycloak.org/)**: identity provider for the IAM lab, alongside Active Directory and Entra ID
- 🛠️ **[Wireshark](https://www.wireshark.org/)**: packet capture and analysis
- 🛠️ **[Nmap](https://nmap.org/)**: scanning lab targets
- 🛠️ **[Burp Suite Community](https://portswigger.net/burp/communitydownload)**: web app testing against lab targets
- 🔖 **[Have I Been Pwned](https://haveibeenpwned.com/)**: checking emails and domains against known breaches

## Scripts in this repo

**[`scripts/opnsense-summary.py`](scripts/opnsense-summary.py)**: reads an OPNsense `config.xml` backup and prints a sanitized summary (interfaces, VLANs, rules, NAT, WireGuard, DNS, plugins). It redacts hostnames, password hashes, keys, MAC addresses, emails and public IPs, so a config can be reviewed or shared safely.

```sh
python3 scripts/opnsense-summary.py ~/Downloads/config-OPNsense.xml > summary.md
```

Read `summary.md` before sharing it, and delete the raw backup when you're done: it contains secrets.

## Lists and references

- 🔖 **[awesome-security](https://github.com/sbilly/awesome-security)**: curated security tools and resources
- 🔖 **[awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)**: self-hosted software by category
- 🔖 **[awesome](https://github.com/sindresorhus/awesome)**: the index of awesome lists
