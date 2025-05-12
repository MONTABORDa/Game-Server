# 🎮 GameServer Hub
[![Déploiement facile](https://img.shields.io/badge/Déploiement-1%20clic-4caf50?logo=docker&logoColor=white)](#pour-les-nulles--déploiement-sur-un-serveur-vierge-ubuntu)

## 🚀 Pour les nulles : déploiement sur un serveur vierge (Ubuntu)

Copiez-collez les commandes suivantes dans votre terminal (avec les droits sudo) :

```bash
# 1. Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# 2. Installer Docker et Docker Compose
sudo apt install -y docker.io docker-compose git

# 3. Autoriser votre utilisateur à utiliser Docker sans sudo (optionnel)
sudo usermod -aG docker $USER
newgrp docker

# 4. Cloner le dépôt
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo

# 5. Lancer le projet
docker compose up -d --build

# 6. Accéder à l'interface depuis un navigateur :
# http://192.168.1.100
```

---
