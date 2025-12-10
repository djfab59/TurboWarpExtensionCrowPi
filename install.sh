#!/bin/bash
set -e

SERVICE_NAME="crowpi-bridge"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOCKET_FILE="/etc/systemd/system/${SERVICE_NAME}.socket"

PROJECT_DIR="$(pwd)"
PYTHON_BIN="$(which python3)"

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

CONFIG_FILE="${REAL_HOME}/.crowpi-bridge.yml"

echo "== CrowPi TurboWarp Hardware Bridge installer =="

# Root check
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root:"
  echo "   sudo ./install.sh"
  exit 1
fi

if [ ! -f "${PROJECT_DIR}/run.py" ]; then
  echo "❌ run.py not found in current directory"
  exit 1
fi

echo "✔ Project directory: ${PROJECT_DIR}"
echo "✔ Python binary   : ${PYTHON_BIN}"

# Stop existing units if any
echo "🛑 Stopping existing units (if any)..."
systemctl stop ${SERVICE_NAME}.service 2>/dev/null || true
systemctl stop ${SERVICE_NAME}.socket 2>/dev/null || true

# ---------- SOCKET ----------
echo "➡ Creating systemd socket..."

cat << EOF > ${SOCKET_FILE}
[Unit]
Description=CrowPi Hardware Bridge Socket

[Socket]
ListenStream=127.0.0.1:3232
ReusePort=true

[Install]
WantedBy=sockets.target
EOF

# ---------- SERVICE ----------
echo "➡ Creating systemd service..."

cat << EOF > ${SERVICE_FILE}
[Unit]
Description=CrowPi TurboWarp Hardware Bridge
After=network.target

[Service]
Type=simple
ExecStart=${PYTHON_BIN} ${PROJECT_DIR}/run.py
WorkingDirectory=${PROJECT_DIR}
User=pi
Restart=on-failure
TimeoutStopSec=600

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Reloading systemd..."
systemctl daemon-reexec
systemctl daemon-reload

echo "✅ Enabling socket (NOT the service)..."
systemctl enable --now ${SERVICE_NAME}.socket

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

CONFIG_FILE="${REAL_HOME}/.crowpi-hw-bridge.yml"

echo "📝 Writing config file to ${CONFIG_FILE}"

cat << EOF > "${CONFIG_FILE}"
service:
  name: ${SERVICE_NAME}
  socket: ${SERVICE_NAME}.socket
  service_file: ${SERVICE_NAME}.service
project:
  path: ${PROJECT_DIR}
  python: ${PYTHON_BIN}
network:
  host: 127.0.0.1
  port: 3232
installed_at: $(date -Iseconds)
EOF

chown "${REAL_USER}:${REAL_USER}" "${CONFIG_FILE}"
chmod 600 "${CONFIG_FILE}"

echo ""
echo "✅ Installation complete"
echo ""
echo "ℹ️ Behaviour:"
echo " - The bridge service starts ON DEMAND"
echo " - It starts when TurboWarp sends the first HTTP request"
echo " - It stops automatically when unused"
echo ""
echo "📌 Useful commands:"
echo "  systemctl status ${SERVICE_NAME}.service"
echo "  systemctl status ${SERVICE_NAME}.socket"
echo "  journalctl -u ${SERVICE_NAME}.service -f"
