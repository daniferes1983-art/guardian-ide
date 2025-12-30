# 🛡️ Guardián IDE - Specialized Cybersecurity IDE with AI

A powerful, modern IDE specifically designed for cybersecurity professionals and developers. Guardián IDE combines a custom domain-specific language (Guardián), artificial intelligence capabilities, and an intuitive web interface for creating security bots and managing network protection.

## ✨ Features

### 🔐 Custom Guardián Language
- **16+ Commands**: 6 basic commands + 10 AI-powered commands
- **Pseudonatural Syntax**: Intuitive syntax designed for cybersecurity tasks
- **Real-time Validation**: Syntax checking as you type
- **Contextual Autocomplete**: Smart suggestions based on context

### 🤖 AI Integration
- **Threat Analysis**: Real-time threat detection and analysis
- **Anomaly Detection**: Identify unusual network patterns
- **Attack Prediction**: Predict potential attacks based on historical data
- **Intelligent Firewall Rules**: Auto-generate firewall rules
- **Policy Optimization**: Automatically optimize security policies
- **Risk Assessment**: Generate comprehensive risk reports

### 🤖 Bot Creation System
- **Pre-built Templates**: Network Monitoring Bot, Incident Response Bot
- **Custom Bot Builder**: Create personalized security bots with AI guidance
- **AI Assistant**: Interactive guidance for bot configuration
- **Automated Generation**: AI-powered code generation

### 💻 Advanced Editor
- **Syntax Highlighting**: Color-coded command syntax
- **Real-time Validation**: Error detection while typing
- **Autocompletion**: Ctrl+Space for smart suggestions
- **Line Numbers**: Easy code navigation
- **Multiple Tabs**: Editor, Output, Dashboard, Bot Creator, Documentation

### 📊 AI Dashboard
- **Real-time Monitoring**: Live threat level assessment
- **Traffic Analysis**: Network packet analysis
- **Vulnerability Assessment**: Identify security weaknesses
- **Predictive Analytics**: AI-powered attack predictions
- **Automated Recommendations**: Smart mitigation suggestions

### 📱 Responsive Design
- **Desktop**: Full-featured interface
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly interface with hamburger menu
- **Smooth Scrolling**: Native scroll with momentum

## 🚀 Quick Start

### Online Access
Visit the live IDE at: https://8080-is1ddd9r7juq3a3cnz6jt-63294c54.manusvm.computer

### Local Installation

```bash
# Clone the repository
git clone https://github.com/daniferes1983-art/guardian-ide.git
cd guardian-ide

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` in your browser.

## 📖 Usage Examples

### Basic Port Scanning
```
analizar puertos de 192.168.1.1
```

### Create Firewall Rule
```
crear regla firewall puerto: 22 protocolo: TCP accion: bloquear
```

### Monitor Network Traffic
```
monitorear trafico en eth0
```

### AI-Powered Threat Analysis
```
analizar amenazas en tiempo real en eth0
```

### Detect Anomalies
```
detectar anomalias en trafico de eth0
```

### Predict Attacks
```
predecir ataques basado en patrones historicos
```

## 🏗️ Project Structure

```
guardian-ide/
├── app.py                      # Flask application
├── guardian_parser.py          # Guardián language parser
├── guardian_interpreter.py     # Command interpreter
├── guardian_ai_enhanced.py     # AI module
├── real_time_validator.py      # Real-time syntax validation
├── custom_bot_ai_assistant.py  # Bot creation AI
├── static/
│   ├── index.html             # Main UI
│   ├── styles.css             # Responsive styling
│   ├── script.js              # Frontend logic
│   ├── autocomplete.js        # Autocomplete system
│   ├── real_time_validation.js # Validation
│   └── custom_bot_form.js     # Bot form handler
├── bot_templates/             # Bot templates
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite
- **AI/ML**: Custom machine learning module
- **Language**: Custom Guardián DSL

## 📋 Commands Reference

### Basic Commands
| Command | Description |
|---------|-------------|
| `analizar puertos de <IP>` | Scan ports on IP address |
| `crear regla firewall` | Create firewall rule |
| `leer logs de <RUTA>` | Read log files |
| `monitorear trafico en <INTERFAZ>` | Monitor network traffic |
| `alertar <MENSAJE>` | Send security alert |
| `ver procesos activos` | List active processes |

### AI Commands
| Command | Description |
|---------|-------------|
| `analizar amenazas en tiempo real` | Real-time threat analysis |
| `detectar anomalias en trafico` | Detect traffic anomalies |
| `evaluar vulnerabilidades` | Assess vulnerabilities |
| `predecir ataques` | Predict potential attacks |
| `generar reglas firewall inteligentes` | Auto-generate firewall rules |
| `optimizar politicas de seguridad` | Optimize security policies |

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + Enter | Execute code |
| Ctrl + L | Clear editor |
| F1 | Show help |
| Tab | Autocomplete |
| Ctrl + Space | Show suggestions |

## 🔒 Security Features

- ✅ HTTPS/SSL encryption
- ✅ Input validation
- ✅ Real-time threat detection
- ✅ Anomaly detection
- ✅ Attack prediction
- ✅ Automated responses
- ✅ Policy optimization

## 📦 Deployment

### Docker
```bash
docker-compose up
```

### Render.com
```bash
# Connect GitHub repository to Render
# Automatic deployment on push
```

### Heroku
```bash
git push heroku main
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Dani Féres** - daniferes1983-art

## 🙏 Acknowledgments

- Cybersecurity community for inspiration
- AI/ML researchers for algorithms
- Open source contributors

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🔗 Links

- **Live IDE**: https://8080-is1ddd9r7juq3a3cnz6jt-63294c54.manusvm.computer
- **GitHub**: https://github.com/daniferes1983-art/guardian-ide
- **Documentation**: See DEPLOYMENT.md and other .md files

---

**Made with ❤️ for cybersecurity professionals**
