# Monitor Docker Build Progress
Write-Host "🔍 Monitoring Docker build progress..." -ForegroundColor Yellow

# Check if build is still running
$buildRunning = $true
$checkCount = 0

while ($buildRunning -and $checkCount -lt 60) {
    $checkCount++
    Write-Host "⏳ Build in progress... (check $checkCount/60)" -ForegroundColor Cyan
    
    # Check if any containers are running
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null
    if ($containers -and $containers -notmatch "ai-schoolos") {
        Write-Host "✅ Build completed! Starting services..." -ForegroundColor Green
        $buildRunning = $false
        break
    }
    
    Start-Sleep -Seconds 30
}

if ($buildRunning) {
    Write-Host "⚠️  Build taking longer than expected. Starting services anyway..." -ForegroundColor Yellow
}

# Start optimized services
Write-Host "🚀 Starting optimized services..." -ForegroundColor Green
docker-compose -f docker-compose.optimized.yml up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Check service status
Write-Host "📊 Checking service status..." -ForegroundColor Cyan
docker-compose -f docker-compose.optimized.yml ps

Write-Host ""
Write-Host "✅ INTEGRATION TEST READY!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 API Gateway: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔍 Test Integration:" -ForegroundColor Yellow
Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "2. Check if frontend loads properly" -ForegroundColor White
Write-Host "3. Try logging in or accessing features" -ForegroundColor White
Write-Host "4. Check browser console for any errors" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitor services: docker-compose -f docker-compose.optimized.yml logs -f" -ForegroundColor Gray

# Keep script running to monitor
Write-Host "Press Ctrl+C to stop monitoring..." -ForegroundColor Yellow
try {
    while ($true) {
        Start-Sleep -Seconds 10
    }
} catch {
    Write-Host ""
    Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
    docker-compose -f docker-compose.optimized.yml down
    Write-Host "✅ Services stopped." -ForegroundColor Green
} 