# ☁️ Sky & Nettverksprotokoller

Dette prosjektet er en avansert implementasjon av et simulert nettverksmiljø utviklet med **Mininet** og Python. Her kombineres nettverkstopologi, socket-programmering, virtuelle maskiner og egendefinerte transportprotokoller for å analysere båndbredde, pakkefeil og pålitelighet.

---

## 🚀 Teknologi og verktøy

- 🐍 **Python** (socket, threading, argparse)
- 💻 **Mininet** (virtuell nettverksemulering)
- 🌐 **Custom transportprotokoller** (Stop-and-Wait, Go-Back-N, Selective Repeat)
- 🛰️ **Linux routing & ethtool** (finjustering av grensesnitt og flytkontroll)
- ⚙️ Virtuelle miljøer (f.eks. VirtualBox)

---

## ⚡ Funksjoner

✅ Design og konfigurasjon av dynamiske nettverk med flere routere, switcher og hosts  
✅ Implementasjon av pålitelige transportprotokoller (SAW, GBN, SR) for datastrømmer  
✅ Håndtering av avanserte testcases som *packet loss*, *reordering*, *duplicates*  
✅ Logging og analyse av båndbredde, RTT, tap og throughput  
✅ Avansert bruk av Mininet for delay, båndbredde og køkontroll

---

## 💡 Hvordan bruke

### Server

`python server.py -s --port 8088 --reliable SR --testcase SKIP_ACK --windowsize 5`


### Klient

`python client.py -c --ip 10.0.0.2 --port 8088 --file path/to/file.txt --reliable SR --windowsize 5`



📄 Dokumentasjon
Se PDF-rapportene og retningslinjene i repoet for detaljert topologi, testoppsett og analyser.
Eksempler: portfolio-guidelines.pdf, portfolio-topology.py

### 🌟 Læringsutbytte>
#### -Bygge komplekse nettverkstopologier og simulere virkelige feilscenarier

#### -Dyp forståelse av transportlagsprotokoller og pålitelig dataoverføring

#### -Avansert IP-routing og nettverksadministrasjon

####-Kombinasjon av teori og praktisk programmering for å analysere ytelse
