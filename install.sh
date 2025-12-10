#!/bin/bash
set -e

SERVICE_NAME="crowpi-bridge"

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOCKET_FILE="/etc/systemd/system/${SERVICE_NAME}.socket"
CONFIG_FILE="${REAL_HOME}/.crowpi-bridge.yml"

PROJECT_DIR="$(pwd)"
PYTHON_BIN="$(which python3)"
GUNICORN_BIN="$(which gunicorn)"

echo "== CrowPi Hardware Bridge installer =="

# Root check
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root: sudo ./install.sh"
  exit 1
fi

if [ ! -f "${PROJECT_DIR}/run.py" ]; then
  echo "❌ run.py not found in ${PROJECT_DIR}"
  exit 1
fi

echo "🔍 Checking gunicorn..."

if ! command -v gunicorn >/dev/null 2>&1; then
  echo "⚠ Gunicorn not found. Installing python3-gunicorn..."
  apt update
  apt install -y python3-gunicorn
else
  echo "✔ Gunicorn already installed"
fi

GUNICORN_BIN="$(which gunicorn)"

echo "✔ Project     : ${PROJECT_DIR}"
echo "✔ User        : ${REAL_USER}"
echo "✔ Python      : ${PYTHON_BIN}"
echo "✔ Gunicorn    : ${GUNICORN_BIN}"

# Stop old units if present
systemctl stop ${SERVICE_NAME}.service 2>/dev/null || true
systemctl stop ${SERVICE_NAME}.socket 2>/dev/null || true

# -------- SOCKET --------
echo "➡ Writing socket unit..."

cat << EOF > ${SOCKET_FILE}
[Unit]
Description=CrowPi Hardware Bridge Socket

[Socket]
ListenStream=127.0.0.1:3232
ReusePort=true

[Install]
WantedBy=sockets.target
EOF

# -------- SERVICE --------
echo "➡ Writing service unit..."

cat << EOF > ${SERVICE_FILE}
[Unit]
Description=CrowPi TurboWarp Hardware Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_DIR}
ExecStart=${GUNICORN_BIN} --bind fd://3 run:app
User=${REAL_USER}
Restart=on-failure
TimeoutStopSec=600

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reexec
systemctl daemon-reload

# Enable ONLY socket
systemctl enable --now ${SERVICE_NAME}.socket

# -------- CONFIG FILE --------
echo "📝 Writing config file ${CONFIG_FILE}"

cat << EOF > ${CONFIG_FILE}
service:
  name: ${SERVICE_NAME}
  socket: ${SERVICE_NAME}.socket
  service_file: ${SERVICE_NAME}.service

project:
  path: ${PROJECT_DIR}
  python: ${PYTHON_BIN}
  gunicorn: ${GUNICORN_BIN}

network:
  host: 127.0.0.1
  port: 3232

installed_at: $(date -Iseconds)
EOF

chown "${REAL_USER}:${REAL_USER}" "${CONFIG_FILE}"
chmod 600 "${CONFIG_FILE}"

echo ""
echo "✅ INSTALL COMPLETE"
echo "ℹ️ The service runs ON DEMAND via systemd socket activation"
echo "ℹ️ It does NOT start at boot"
echo ""
echo "Useful commands:"
echo "  systemctl status ${SERVICE_NAME}.socket"
echo "  systemctl status ${SERVICE_NAME}.service"
echo "  journalctl -u ${SERVICE_NAME}.service -f"
