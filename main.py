import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from docx import Document
from bs4 import BeautifulSoup
import argparse
import sys
from urllib.parse import urlparse

load_dotenv()

class ServicoTraducao:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN não encontrado nas variáveis de ambiente")
            
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "o1-mini"
        self.client = OpenAI(base_url=self.endpoint, api_key=self.token)

    def _traduzir_com_openai(self, texto: str, idioma_destino: str) -> str:
        try:
            prompt = f"Traduza o seguinte texto para {idioma_destino}: {texto}"
            resposta = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name
            )
            return resposta.choices[0].message.content
        except Exception as e:
            print(f"Erro na tradução: {e}")
            sys.exit(1)

    def traduzir_texto(self, texto: str, idioma_destino: str) -> str:
        return self._traduzir_com_openai(texto, idioma_destino)

    def traduzir_documento(self, caminho_arquivo: str, idioma_destino: str) -> list:
        try:
            doc = Document(caminho_arquivo)
            paragrafos_traduzidos = []
            
            for paragrafo in doc.paragraphs:
                if paragrafo.text.strip():
                    texto_traduzido = self.traduzir_texto(paragrafo.text, idioma_destino)
                    paragrafos_traduzidos.append(texto_traduzido)
            
            return paragrafos_traduzidos
            
        except Exception as e:
            print(f"Erro ao processar documento: {e}")
            sys.exit(1)

    def traduzir_site(self, url: str, idioma_destino: str) -> dict:
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            resposta = requests.get(url, headers=headers, timeout=10)
            resposta.raise_for_status()
            
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            for script in soup(['script', 'style']):
                script.decompose()

            traducoes = []
            
            tags_texto = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']
            
            for tag in soup.find_all(tags_texto):
                if tag.string and tag.string.strip():
                    texto = tag.string.strip()
                    if len(texto) > 3 and not texto.isdigit():
                        texto_traduzido = self.traduzir_texto(texto, idioma_destino)
                        traducoes.append({
                            'tag': tag.name,
                            'original': texto,
                            'traduzido': texto_traduzido
                        })

            return traducoes
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o site: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao processar o site: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Ferramenta de Tradução Multi-formato usando OpenAI')
    parser.add_argument('entrada', help='Texto, arquivo, URL ou HTML para traduzir')
    parser.add_argument('--idioma', default='português', help='Idioma de destino (padrão: português)')
    parser.add_argument('--tipo', choices=['texto', 'documento', 'html'], 
                       default='texto', help='Tipo de conteúdo a ser traduzido')
    
    args = parser.parse_args()
    
    try:
        tradutor = ServicoTraducao()
        
        if args.tipo == 'texto':
            resultado = tradutor.traduzir_texto(args.entrada, args.idioma)
            print(f"\nTradução: {resultado}\n")
            
        elif args.tipo == 'documento':
            paragrafos_traduzidos = tradutor.traduzir_documento(args.entrada, args.idioma)
            print("\nConteúdo do documento traduzido:\n")
            for i, paragrafo in enumerate(paragrafos_traduzidos, 1):
                print(f"Parágrafo {i}:")
                print(f"{paragrafo}\n")
            
        elif args.tipo == 'html':
            traducoes = tradutor.traduzir_site(args.entrada, args.idioma)
            print(f"\nTraduções do site {args.entrada}:\n")
            for item in traducoes:
                print(f"Tag <{item['tag']}>:")
                print(f"Original: {item['original']}")
                print(f"Tradução: {item['traduzido']}")
                print("-" * 80 + "\n")
            
    except Exception as e:
        print(f"Um erro foi encontrado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()