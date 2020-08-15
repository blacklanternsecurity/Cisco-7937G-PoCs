# Cisco-7937G-PoCs
Proofs of concept for three vulnerabilities affecting the Cisco 7937G Conference Station

## All-In-One

This script will allow you to test all three of the vulnerabilities present in the 7937G device.
It will require you to have the following Python modules installed:

 * Paramiko
 * Requests
 * Random
 * String

## cve_2020_16137, cve_2020_16138, cve_2020_16139

These scripts are Python modules for use with metasploit-framework.
To use them, place them in your install location and they should import without issue.
Typical install location on a kali/debian build:
 * cve_2020_16137: `/usr/share/metasploit-framework/modules/exploit/linux/ssh/cve_2020_16137.py`
 * cve_2020_16138: `/usr/share/metasploit-framework/modules/auxiliary/dos/cisco/cve_2020_16138.py`
 * cve_2020_16139: `/usr/share/metasploit-framework/modules/auxiliary/dos/cisco/cve_2020_16139.py`
 
 # Background
 
 For further information about these exploits, please see [this](https://www.blacklanternsecurity.com/2020-08-07-Cisco-Unified-IP-Conference-Station-7937G/) blog post.
 
