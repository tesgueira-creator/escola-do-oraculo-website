#!/usr/bin/env python3
"""
Script para salvar a imagem da Rafaella Kally
INSTRUÇÕES:
1. Salva a imagem anexada no chat como 'rafaella.jpg' na mesma pasta deste script
2. Executa: python save_rafaella_image.py
3. A imagem será copiada para frontend/assets/images/rafaella-profile.jpg
"""
import shutil
import os

# Paths
source_image = "rafaella.jpg"  # Salva a imagem do chat com este nome
target_path = "frontend/assets/images/rafaella-profile.jpg"

if os.path.exists(source_image):
    shutil.copy(source_image, target_path)
    print(f"✅ Imagem salva com sucesso em: {target_path}")
    print(f"📸 A foto da Rafaella agora aparecerá no site!")
else:
    print(f"❌ Erro: Ficheiro '{source_image}' não encontrado.")
    print(f"Por favor, salva a imagem do chat como '{source_image}' primeiro.")
    print("\nPasso a passo:")
    print("1. Clica com botão direito na imagem no chat")
    print("2. Escolhe 'Salvar imagem como...'")
    print(f"3. Salva como: {os.path.abspath(source_image)}")
    print("4. Executa este script novamente")
