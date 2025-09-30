#!/usr/bin/env bash

npm run build

set -e

SRC_DIR="/root/React_practice/react_app/dist"
DST_DIR="/var/www/react_practice"

echo "[1/4] Проверка, есть ли билд..."
if [ ! -d "$SRC_DIR" ]; then
  echo "Нет папки $SRC_DIR. Сначала собери проект (npm run build)."
  exit 1
fi

echo "[2/4] Копирую файлы..."
mkdir -p "$DST_DIR"
rm -rf "$DST_DIR"/*
cp -r "$SRC_DIR"/* "$DST_DIR"/

echo "[3/4] Проверяю права..."
chown -R www-data:www-data "$DST_DIR"
find "$DST_DIR" -type d -exec chmod 755 {} \;
find "$DST_DIR" -type f -exec chmod 644 {} \;

echo "[4/4] Проверка конфига и перезапуск Nginx..."
if nginx -t; then
  systemctl reload nginx
  echo " Nginx конфиг валиден, перезапуск выполнен."
else
  echo "Ошибка в конфиге Nginx! Перезапуск отменён."
  exit 1
fi

echo "Deploy complete! dist → $DST_DIR"