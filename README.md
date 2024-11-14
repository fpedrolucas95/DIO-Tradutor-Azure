# Tradutor Multi-formato com Azure OpenAI

Este projeto foi desenvolvido como parte do desafio **Tradutor de Artigos Técnicos com Azure AI** da DIO, para o **Bootcamp Microsoft Certification Challenge #1 - AI 102**.

## 📝 Descrição do Projeto

Uma ferramenta de tradução versátil que permite traduzir:
- Textos simples
- Documentos Word (.docx)
- Sites completos

O projeto utiliza a API da Azure OpenAI para realizar as traduções, garantindo alta qualidade e precisão nas traduções.

## 🚀 Funcionalidades

- Tradução de texto simples
- Tradução de documentos Word (.docx)
- Tradução de conteúdo de websites
- Suporte a múltiplos idiomas (padrão: português)
- Interface via linha de comando

## 🛠️ Tecnologias Utilizadas

- Python 3.12
- Azure OpenAI
- Bibliotecas Python:
  - openai
  - python-docx
  - beautifulsoup4
  - requests
  - python-dotenv

## ⚙️ Como Configurar

1. Clone o repositório:
```bash
git clone https://github.com/fpedrolucas95/DIO-Tradutor-Azure.git
cd DIO-Tradutor-Azure
```

2. Instale as dependências:
```bash
pip install openai python-docx beautifulsoup4 requests python-dotenv
```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione seu token do GitHub:
```
GITHUB_TOKEN=seu_token_aqui
```

## 📖 Como Usar

### Traduzir Texto
```bash
python main.py "Hello, how are you?" --tipo texto --idioma português
```

### Traduzir Documento Word
```bash
python main.py documento.docx --tipo documento --idioma português
```

### Traduzir Website
```bash
python main.py www.example.com --tipo html --idioma português
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔗 Links Úteis

- [DIO - Digital Innovation One](https://www.dio.me/)
- [Documentação Azure OpenAI](https://learn.microsoft.com/pt-br/azure/cognitive-services/openai/)
- [Bootcamp Microsoft Azure AI Fundamentals](https://web.dio.me/track/microsoft-azure-ai-fundamentals)
