# Impar Automacoes - Login Facebook Interativo
# Execute este script para abrir navegador e fazer login

Write-Host "`n================================" -ForegroundColor Green
Write-Host "Impar Automacoes - Login Facebook" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Green

# Verificar diretorio
if (-not (Test-Path "scripts\login-facebook.py")) {
    Write-Host "❌ ERRO: Nao estou no diretorio correto!" -ForegroundColor Red
    Write-Host "   Execute este arquivo de: impar-automations\" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar venv
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "❌ ERRO: venv nao encontrado!" -ForegroundColor Red
    Write-Host "   Execute primeiro: ..\install-windows-auto.bat" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Ativar venv
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Executar script de login
Write-Host "`n🌐 Abrindo navegador para login no Facebook..." -ForegroundColor Cyan
Write-Host "   Aguarde...`n" -ForegroundColor Yellow

& venv\Scripts\python.exe scripts\login-facebook.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================" -ForegroundColor Green
    Write-Host "✅ SUCESSO! Login realizado!" -ForegroundColor Green
    Write-Host "================================`n" -ForegroundColor Green

    Write-Host "📝 Proximos passos:" -ForegroundColor Cyan
    Write-Host "   1. Gerar fila marketplace:" -ForegroundColor White
    Write-Host "      python scripts\generate_queue.py" -ForegroundColor Yellow
    Write-Host "   2. Gerar fila de grupos:" -ForegroundColor White
    Write-Host "      python scripts\generate_group_queue.py" -ForegroundColor Yellow
    Write-Host "   3. Publicar nos grupos:" -ForegroundColor White
    Write-Host "      python scripts\publish_groups_playwright.py --headed" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "`n❌ ERRO! Algo deu errado." -ForegroundColor Red
    Write-Host "   Tente novamente`n" -ForegroundColor Yellow
}

Read-Host "Pressione Enter para sair"
