# SpywareDemo — Academic Security Project
 
> **Educational purposes only.** This project was developed as part of a college cybersecurity course to demonstrate how spyware operates at a conceptual and technical level. It is not intended for, and should not be used for, any real-world deployment.
 
---
 
## Overview
 
This project demonstrates the core components of a spyware attack chain — from delivery to data exfiltration — in a controlled academic context. It consists of three parts:
 
1. **Fake Delivery Website** — A convincing-looking website used to socially engineer a victim into downloading a malicious executable
2. **Spyware Client** — A Python-based spyware payload (redacted, binary not included) that captures keystrokes and screenshots and exfiltrates them to a remote server
3. **C2 Server** — A TCP server that receives and logs the exfiltrated data
The goal was to understand the full attack lifecycle, not to create a deployable tool.
 
---
 
## Project Structure
 
```
main/
├── data/                         # data captured by spyware
├── static/
│   └── assets/
│   │   └── hero-3d-DiO74YaU.jpg
│   │   ├── index-5LgWr_zl.js     # js file
│   │   ├── index-6vMSOtdn.css    # css file
│   ├── favicon.ico
│   ├── index.html
│   ├── logs.html
│   ├── placeholder.svg
│   ├── robots.txt   
├── tcp-server/
│   └── tcp-server.py             # tcp endpoint for data receiving
├──  web-server.py
├── DISCLAIMER.md
└── README.md
```
 
---
 
## Components
 
### Website
A static site designed to look like a legitimate software download page. Demonstrates how social engineering is used as a delivery mechanism. Built with plain HTML/CSS.
 
### C2 Server
A TCP server that listens for incoming connections from the client. Implements a simple binary protocol:
- `KEYS` header — receives keylog data
- `IMAG` header — receives screenshot data
Data is length-prefixed (`!I` struct format) for reliable framing over TCP.
 
### Spyware Client *(redacted)*
Written in Python. Demonstrates the following spyware concepts:
 
| Feature | Status |
|---|---|
| Keystroke logging (`pynput`) | Shown |
| Periodic screenshots (`pyautogui`) | Shown |
| Data exfiltration over TCP | Shown |
| Exfil state tracking (resume on restart) | Shown |
| VM detection | **Redacted** |
| Persistence mechanism | **Redacted** |
| Process concealment | **Redacted** |
| C2 endpoint | **Redacted** |
 
> **Binary not included.** The `.exe` is excluded from this repository intentionally.
 
---
 
## Dependencies
 
```
pynput
pyautogui
Pillow
```
 
---
 
## What We Learned
 
- How spyware components fit together as an attack chain
- TCP socket programming and binary protocol design
- How social engineering (fake websites) lowers the barrier to infection
- Why VM detection and persistence are what make spyware dangerous in the real world (and why we removed them from this demo)
---
 
## Course Context
 
This was developed as a project at VIT University in 2025.  
