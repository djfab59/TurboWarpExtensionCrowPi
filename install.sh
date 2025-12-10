#!/usr/bin/env bash

# ===============================
# CrowPi Bridge installer
# ===============================

set -Eeuo pipefail
trap 'echo "❌ Error on line $LINENO"; exit 1' ERR

echo "== CrowPi Bridge installer =="

# ---------- Root check ----------
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root:"
  echo "   sudo ./install.sh"
  exit 1
fi

# ---------- Constants ----------
SERVICE_NAME="crowpi-bridge"

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

PROJECT_DIR="$(pwd)"
CONFIG_FILE="${REAL_HOME}/.crowpi-bridge.yml"

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOCKET_FILE="/etc/systemd/system/${SERVICE_NAME}.socket"

echo "✔ User        : ${REAL_USER}"
echo "✔ Home        : ${REAL_HOME}"
echo "✔ Project dir : ${PROJECT_DIR}"

# ---------- Sanity checks ----------
if [ ! -f "${PROJECT_DIR}/run.py" ]; then
  echo "❌ run.py not found in ${PROJECT_DIR}"
  exit 1
fi

if ! command -v systemctl >/dev/null 2>&1; then
  echo "❌ systemd not available on this system"
  exit 1
fi

# ---------- Detect python ----------
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 not found"
  exit 1
fi
PYTHON_BIN="$(command -v python3)"
echo "✔ Python      : ${PYTHON_BIN}"

# ---------- Detect gunicorn ----------
echo "🔍 Detecting gunicorn..."

if command -v gunicorn3 >/dev/null 2>&1; then
  GUNICORN_BIN="$(command -v gunicorn3)"
elif command -v gunicorn >/dev/null 2>&1; then
  GUNICORN_BIN="$(command -v gunicorn)"
elif [ -x "${PROJECT_DIR}/.venv/bin/gunicorn" ]; then
  GUNICORN_BIN="${PROJECT_DIR}/.venv/bin/gunicorn"
else
  echo ""
  echo "❌ Gunicorn CLI not found."
  echo ""
  echo "➡ On CrowPi OS, the recommended solution is a local venv:"
  echo "   cd ${PROJECT_DIR}"
  echo "   python3 -m venv .venv"
  echo "   .venv/bin/pip install gunicorn"
  echo ""
  exit 1
fi

echo "✔ Gunicorn    : ${GUNICORN_BIN}"

# ---------- Stop previous units ----------
echo "🛑 Stopping existing units (if any)..."
systemctl stop ${SERVICE_NAME}.service 2>/dev/null || true
systemctl stop ${SERVICE_NAME}.socket 2>/dev/null || true
systemctl disable ${SERVICE_NAME}.service 2>/dev/null || true

# ---------- Write socket ----------
echo "➡ Writing systemd socket..."

cat << EOF > "${SOCKET_FILE}"
[Unit]
Description=CrowPi Bridge Socket

[Socket]
ListenStream=127.0.0.1:3232
ReusePort=true

[Install]
WantedBy=sockets.target
EOF

# ---------- Write service ----------
echo "➡ Writing systemd service..."

cat << EOF > "${SERVICE_FILE}"
[Unit]
Description=CrowPi TurboWarp Hardware Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_DIR}
ExecStart=${GUNICORN_BIN} --bind fd://3 run:app
User=${REAL_USER}
Restart=on-failure
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
EOF

# ---------- Reload systemd ----------
echo "🔄 Reloading systemd..."
systemctl daemon-reexec
systemctl daemon-reload

# ---------- Enable ONLY socket ----------
echo "✅ Enabling socket (on-demand start only)"
systemctl enable --now ${SERVICE_NAME}.socket

# ---------- Write config file ----------
echo "📝 Writing config file: ${CONFIG_FILE}"

cat << EOF > "${CONFIG_FILE}"
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
echo ""
echo "Behaviour:"
echo " - The service does NOT start at boot"
echo " - The socket is active"
echo " - The service starts automatically on first HTTP request"
echo ""
echo "Useful commands:"
echo "  systemctl status ${SERVICE_NAME}.socket"
echo "  systemctl status ${SERVICE_NAME}.service"
echo "  journalctl -u ${SERVICE_NAME}.service -f"
