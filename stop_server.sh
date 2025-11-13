#!/bin/bash
# Script para parar o servidor Flask na porta 5001

PORT=5001
PID=$(lsof -ti:$PORT)

if [ -z "$PID" ]; then
    echo "✅ Nenhum processo rodando na porta $PORT"
else
    echo "🛑 Encerrando processo $PID na porta $PORT..."
    kill -9 $PID
    sleep 1
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo "❌ Erro ao encerrar o processo"
    else
        echo "✅ Porta $PORT está livre agora!"
    fi
fi

