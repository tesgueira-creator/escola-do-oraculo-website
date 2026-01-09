@echo off
REM Script to prepare GitHub repository

cd /d "C:\Users\XKELU27\Downloads\escola-do-oraculo-website"

REM Copy the main index file
copy "..\Escola do Oráculo Website (1).html" "index.html"

REM Copy module files
copy "..\modulo-1.html" "modulo-1.html"
copy "..\modulo-2.html" "modulo-2.html"
copy "..\modulo-3.html" "modulo-3.html"

REM Copy other pages
copy "..\circulo.html" "circulo.html"
copy "..\checkout.html" "checkout.html"
copy "..\Tarot_Real_Cards.html" "tarot-reader.html"

REM Initialize Git repository
git init

REM Add all files
git add .

REM Create initial commit
git commit -m "Initial commit: Escola do Oráculo Website - Complete tarot school platform"

echo.
echo ====================================================
echo Repositório Git inicializado com sucesso!
echo ====================================================
echo.
echo Ficheiros adicionados:
echo - index.html (página principal)
echo - modulo-1.html, modulo-2.html, modulo-3.html
echo - circulo.html (comunidade)
echo - checkout.html (inscrição)
echo - tarot-reader.html (leitor standalone)
echo - README.md (documentação)
echo - .gitignore
echo.
echo Próximos passos:
echo 1. Criar novo repositório em GitHub: https://github.com/new
echo 2. Copiar o HTTPS URL do repositório
echo 3. Executar: git remote add origin [URL-DO-REPOSITORIO]
echo 4. Executar: git branch -M main
echo 5. Executar: git push -u origin main
echo.
echo ====================================================
pause
