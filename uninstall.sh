#!/bin/bash

set -e

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"
CONFIG_FILE="${REAL_HOME}/.crowpi-bridge.yml"

echo "== CrowPi Hardware Bridge uninstall =="

if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root: sudo ./uninstall.sh"
  exit 1
fi

if [ ! -f "${CONFIG_FILE}" ]; then
  echo "❌ Config file not found: ${CONFIG_FILE}"
  echo "Nothing to uninstall."
  exit 1
fi

# Simple YAML parsing (safe here)
SERVICE_NAME=$(grep "name:" ${CONFIG_FILE} | head -1 | awk '{print $2}')
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOCKET_FILE="/etc/systemd/system/${SERVICE_NAME}.socket"

echo "🔍 Found service: ${SERVICE_NAME}"

echo "🛑 Stopping service and socket..."
systemctl stop ${SERVICE_NAME}.service 2>/dev/null || true
systemctl stop ${SERVICE_NAME}.socket 2>/dev/null || true

echo "❌ Disabling socket..."
systemctl disable ${SERVICE_NAME}.socket 2>/dev/null || true

echo "🧹 Removing systemd files..."
rm -f ${SERVICE_FILE}
rm -f ${SOCKET_FILE}

echo "🔄 Reloading systemd..."
systemctl daemon-reexec
systemctl daemon-reload

echo "🗑 Removing config file..."
rm -f ${CONFIG_FILE}

echo "✅ Uninstall complete"
