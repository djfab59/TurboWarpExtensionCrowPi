#!/usr/bin/env bash

# ===============================
# CrowPi Bridge uninstall
# ===============================

set -u
trap 'echo "❌ Error on line $LINENO"; exit 1' ERR

echo "== CrowPi Bridge uninstall =="

# ---------- Root check ----------
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root:"
  echo "   sudo ./uninstall.sh"
  exit 1
fi

# ---------- Detect real user ----------
REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

CONFIG_FILE="${REAL_HOME}/.crowpi-bridge.yml"

echo "✔ User : ${REAL_USER}"
echo "✔ Home : ${REAL_HOME}"

# ---------- Check config ----------
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "❌ Config file not found:"
  echo "   ${CONFIG_FILE}"
  echo ""
  echo "Nothing to uninstall."
  exit 1
fi

echo "✔ Config file found"

# ---------- Extract service name ----------
SERVICE_NAME="$(grep -E '^  name:' "${CONFIG_FILE}" | awk '{print $2}')"

if [ -z "${SERVICE_NAME}" ]; then
  echo "❌ Service name not found in config file"
  exit 1
fi

SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOCKET_FILE="/etc/systemd/system/${SERVICE_NAME}.socket"

echo "✔ Service name : ${SERVICE_NAME}"

# ---------- Stop units ----------
echo "🛑 Stopping service and socket (if running)..."
systemctl stop "${SERVICE_NAME}.service" 2>/dev/null || true
systemctl stop "${SERVICE_NAME}.socket" 2>/dev/null || true

# ---------- Disable socket ----------
echo "❌ Disabling socket..."
systemctl disable "${SERVICE_NAME}.socket" 2>/dev/null || true

# ---------- Remove unit files ----------
echo "🧹 Removing systemd unit files..."
rm -f "${SERVICE_FILE}"
rm -f "${SOCKET_FILE}"

# ---------- Reload systemd ----------
echo "🔄 Reloading systemd..."
systemctl daemon-reexec
systemctl daemon-reload

# ---------- Remove config ----------
echo "🗑 Removing config file..."
rm -f "${CONFIG_FILE}"

echo ""
echo "✅ UNINSTALL COMPLETE"
echo ""
echo "The CrowPi Bridge has been fully removed from this system."
