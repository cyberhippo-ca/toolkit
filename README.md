# Toolkit

The tools, services and references I use for my homelab, my domain and website, and security work. Each section says what I use the tool for.

Write-ups showing these in use: [cyberhippo.ca](https://cyberhippo.ca)

**Legend:** ✅ in use &nbsp;·&nbsp; 🛠️ part of the lab build &nbsp;·&nbsp; 🔖 bookmarked, not used yet

## Contents

- [Git and documentation](#git-and-documentation)
- [Domain and DNS](#domain-and-dns)
- [Email spoofing protection](#email-spoofing-protection)
- [Web hosting and security headers](#web-hosting-and-security-headers)
- [Accessibility and site quality](#accessibility-and-site-quality)
- [Firewall, VPN and network](#firewall-vpn-and-network)
- [Remote access](#remote-access)
- [Self-hosted services](#self-hosted-services)
- [macOS checks](#macos-checks)
- [Security lab](#security-lab)
- [Scripts in this repo](#scripts-in-this-repo)
- [Lists and references](#lists-and-references)

## Git and documentation

| | Tool | What I use it for |
|---|---|---|
| ✅ | [Git](https://git-scm.com/) | Version control for my homelab docs and site |
| ✅ | [GitHub commit signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) | SSH-signed commits, so every change shows as verified |
| ✅ | [EditorConfig](https://editorconfig.org/) | Consistent formatting across my Mac and Windows machines |
| ✅ | [Mermaid](https://mermaid.js.org/) | Network diagrams written as text in Markdown |

## Domain and DNS

| | Tool | What I use it for |
|---|---|---|
| ✅ | [Cloudflare DNSSEC](https://developers.cloudflare.com/dns/dnssec/) | Signing my zone |
| ✅ | `dig` | Checking DNS records from the command line (SPF, DMARC, DKIM, MX, DS) |
| 🔖 | [ICANN Lookup](https://lookup.icann.org/) | Checking what WHOIS/RDAP shows about a domain |
| 🔖 | [DNSViz](https://dnsviz.net/) | Visual check of the DNSSEC chain of trust |
| 🔖 | [CIRA WHOIS](https://www.cira.ca/whois) | WHOIS for `.ca` domains |

## Email spoofing protection

For a domain that sends no mail: reject anything that claims to come from it.

| | Tool | What I use it for |
|---|---|---|
| ✅ | [RFC 7489 (DMARC)](https://www.rfc-editor.org/rfc/rfc7489) | Reference for the DMARC record |
| ✅ | [RFC 7505 (Null MX)](https://www.rfc-editor.org/rfc/rfc7505) | Telling the world the domain accepts no mail |
| 🔖 | [MXToolbox SuperTool](https://mxtoolbox.com/SuperTool.aspx) | Quick SPF, DMARC, MX and blacklist lookups |
| 🔖 | [dmarcian DMARC Inspector](https://dmarcian.com/dmarc-inspector/) | Checking a DMARC record |
| 🔖 | [mail-tester](https://www.mail-tester.com/) | Deliverability score for a domain that does send mail |

## Web hosting and security headers

| | Tool | What I use it for |
|---|---|---|
| ✅ | [Cloudflare Pages](https://pages.cloudflare.com/) | Hosting my static site from a GitHub repo |
| ✅ | [Pages `_headers` file](https://developers.cloudflare.com/pages/configuration/headers/) | Security headers (CSP, COOP, CORP, etc.) |
| ✅ | [securityheaders.com](https://securityheaders.com/) | Grading the headers (A+) |
| 🔖 | [Mozilla HTTP Observatory](https://developer.mozilla.org/en-US/observatory) | Second opinion on headers and TLS |
| 🔖 | [SSL Labs](https://www.ssllabs.com/ssltest/) | TLS configuration test |
| 🔖 | [Internet.nl](https://internet.nl/) | Combined website and email standards test |
| 🔖 | [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Practical web security guidance |
| 🔖 | [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Most common web app risks |

## Accessibility and site quality

| | Tool | What I use it for |
|---|---|---|
| ✅ | [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) | Performance, accessibility, best practices and SEO scores |
| ✅ | [axe-core](https://github.com/dequelabs/axe-core) | Automated accessibility scan against WCAG |
| ✅ | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | The accessibility standard I test against |
| 🔖 | [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) | Checking colour contrast by hand |

## Firewall, VPN and network

| | Tool | What I use it for |
|---|---|---|
| ✅ | [OPNsense](https://opnsense.org/) | Edge firewall, NAT, DHCP, DNS (Unbound), VLANs |
| ✅ | [Protectli](https://protectli.com/) | Hardware the firewall runs on |
| ✅ | [WireGuard](https://www.wireguard.com/install/) | VPN for remote access, on OPNsense and my laptop and phone |
| ✅ | [OPNsense WireGuard road warrior guide](https://docs.opnsense.org/manual/how-tos/wireguard-client.html) | Reference for the VPN setup |
| ✅ | [canyouseeme.org](https://canyouseeme.org/) | Checking from outside whether a port is open |
| ✅ | [Pi-hole](https://pi-hole.net/) ([Docker image](https://github.com/pi-hole/docker-pi-hole)) | DNS-level ad and tracker blocking |
| 🛠️ | [Suricata](https://suricata.io/) | Intrusion detection on the WAN |

## Remote access

| | Tool | What I use it for |
|---|---|---|
| ✅ | macOS Screen Sharing | Remote desktop to my Mac mini, over WireGuard only |
| ✅ | [bVNC](https://github.com/iiordanov/remote-desktop-clients) | VNC from my Android phone, signing in with a macOS account |
| ✅ | [Cloudflare Tunnel (`cloudflared`)](https://github.com/cloudflare/cloudflared) | Publishing one self-hosted app without a port forward ([docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)) |
| ✅ | [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/) | Email one-time-code login in front of that app |

## Self-hosted services

Running in Docker on the Mac mini.

| | Tool | What I use it for |
|---|---|---|
| ✅ | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Running the containers |
| ✅ | [Homepage](https://github.com/gethomepage/homepage) | Dashboard for the lab |
| ✅ | [Uptime Kuma](https://github.com/louislam/uptime-kuma) | Uptime monitoring |
| ✅ | [Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker) | Tracking internet speed over time |
| ✅ | [Tautulli](https://github.com/Tautulli/Tautulli) | Plex monitoring |
| ✅ | Docker socket proxy (e.g. [Tecnativa](https://github.com/Tecnativa/docker-socket-proxy)) | Limited Docker API access for Homepage instead of the raw socket |
| 🛠️ | [Home Assistant](https://www.home-assistant.io/) | Home automation, on its own VLAN |

## macOS checks

| | Command | What I use it for |
|---|---|---|
| ✅ | `log show --predicate 'process == "screensharingd"' --last 7d \| grep -i auth` | Screen Sharing login history (successes and failures, with source IPs) |
| ✅ | `sudo lsof -nP -iTCP -sTCP:LISTEN` | Every program listening for network connections |
| ✅ | `ls /Library/LaunchDaemons /Library/LaunchAgents ~/Library/LaunchAgents` | Background services that start automatically (finds remote access tools) |
| ✅ | `docker ps --format '{{.Names}}\t{{.Ports}}'` | Which containers publish which ports |

## Security lab

Planned in my lab build. Not all running yet.

| | Tool | What I use it for |
|---|---|---|
| 🛠️ | [Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview) | Hypervisor for the lab hosts |
| 🛠️ | [Wazuh](https://wazuh.com/) | SIEM and vulnerability management |
| 🛠️ | [Kali Linux](https://www.kali.org/) | Attack box on an isolated lab VLAN |
| 🛠️ | [Keycloak](https://www.keycloak.org/) | Identity provider for the IAM lab (with Active Directory and Entra ID) |
| 🛠️ | [Wireshark](https://www.wireshark.org/) | Packet capture and analysis |
| 🛠️ | [Nmap](https://nmap.org/) | Scanning lab targets |
| 🛠️ | [Burp Suite Community](https://portswigger.net/burp/communitydownload) | Web app testing against lab targets |
| 🔖 | [Have I Been Pwned](https://haveibeenpwned.com/) | Checking emails and domains against known breaches |

## Scripts in this repo

| Script | What it does |
|---|---|
| [`scripts/opnsense-summary.py`](scripts/opnsense-summary.py) | Reads an OPNsense `config.xml` backup and prints a sanitized summary (interfaces, VLANs, rules, NAT, WireGuard, DNS, plugins). Redacts hostnames, password hashes, keys, MAC addresses, emails and public IPs, so a config can be reviewed or shared safely. |

```sh
python3 scripts/opnsense-summary.py ~/Downloads/config-OPNsense.xml > summary.md
```

Read `summary.md` before sharing it. Delete the raw backup when you're done; it contains secrets.

## Lists and references

| | Repo | What it is |
|---|---|---|
| 🔖 | [awesome-security](https://github.com/sbilly/awesome-security) | Curated security tools and resources |
| 🔖 | [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) | Self-hosted software, by category |
| 🔖 | [awesome](https://github.com/sindresorhus/awesome) | The index of awesome lists |
