#!/bin/bash
echo "🚀 TC-AGI grsqm.com Deployment Başlatılıyor..."

# Production server'ı başlat
echo "📍 Production Server: http://localhost:8000"
echo "🌐 Domain: grsqm.com (Cloudflare'de hazır)"
python3 production_server.py

echo "✅ TC-AGI Artık İnternette!"
echo "🔗 https://grsqm.com"
