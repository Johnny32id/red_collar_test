#!/bin/bash
# Скрипт для проверки API функционала

TOKEN="36279d978a8bf22c62f7e79ed23188c91cd86e26"
BASE_URL="http://127.0.0.1:8000"

echo "=== 1. Проверка авторизации (без токена) ==="
curl -s -w "\nHTTP Status: %{http_code}\n" -X POST ${BASE_URL}/api/points/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "latitude": 55.7558, "longitude": 37.6173}'
echo ""

echo "=== 2. Создание точки (POST /api/points/) ==="
RESPONSE=$(curl -s -X POST ${BASE_URL}/api/points/ \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Москва", "description": "Столица России", "latitude": 55.7558, "longitude": 37.6173}')
echo "$RESPONSE"
POINT_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('id', 1))" 2>/dev/null || echo "1")
echo "Point ID: $POINT_ID"
echo ""

echo "=== 3. Создание сообщения (POST /api/points/messages/) ==="
curl -s -X POST ${BASE_URL}/api/points/messages/ \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"point_id\": ${POINT_ID}, \"text\": \"Привет из Москвы!\"}"
echo ""
echo ""

echo "=== 4. Поиск точек в радиусе (GET /api/points/search/) ==="
curl -s "${BASE_URL}/api/points/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token ${TOKEN}"
echo ""
echo ""

echo "=== 5. Поиск сообщений в радиусе (GET /api/messages/search/) ==="
curl -s "${BASE_URL}/api/messages/search/?latitude=55.7558&longitude=37.6173&radius=10" \
  -H "Authorization: Token ${TOKEN}"
echo ""

