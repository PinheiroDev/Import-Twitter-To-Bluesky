# Importar Posts do X(Twitter) para o Bluesky
Importe automaticamente seus posts do seu perfil do Twitter para o seu perfil do Bluesky!

O programa utiliza API do Bluesky juntamente com instâncias do Nitter, permitindo obter seus posts do Twitter sem o uso de VPN.

## Problemas Conhecidos
- Não foi realizado testes com perfil com muitos posts, a princípio a API do Bluesky não está aplicando nenhum tipo de Timeout MAS são ações que poderão ser aplicadas no futuro, dito isso, NÃO recomendo o uso em perfis com muitos Tweets.

- Devido uma limitação por parte do Bluesky, não é possível importar vídeos pois o Bluesky não possui suporte no momento. Devido a isso, posts com vídeos serão ignorados.

## Como Instalar?

- **Passo 1:** Você precisará ter a última versão do Python instalado no seu computador, para isso, baixe e instale a última versão do Python diretamente do site oficial clicando [AQUI](https://www.python.org/downloads/).

Obs: Após ter o Python instalado no seu computador talvez seja necessário reiniciar seu computador.



- **Passo 2:** Caso você possua git no seu computador basta utilizar o comando em um terminal:

```javascript
git clone https://github.com/PinheiroDev/Import-Twitter-To-Bluesky.git
```

Não se preocupe, caso você NÃO possua git no seu computador basta clicar em **CODE** e **Download Zip**. Após isso, basta extrair os arquivos para uma pasta em qualquer lugar do seu computador.

## Como Utilizar?
A utilização é simples, se você estiver utilizando Windows 10 ou superior, basta segurar SHIFT+Botão DIREITO do mouse na pasta onde o projeto se encontra, logo em seguida clique em **'Abrir Janela do PowerShell Aqui'**

- Com a Janela do PowerShell aberta na pasta do projeto(Certifique-se disso, ou dará erro), utilize o seguinte comando:
```javascript
pip install -r requirements.txt
```
Com esse comando o python irá baixar todas as dependências necessárias, esse processo poderá levar alguns minutos.

**IMPORTANTE: Em alguns casos o windows pode não reconhecer o comando 'pip', para corrigir isso basta seguir o tutorial clicando [AQUI](https://www.youtube.com/watch?v=OSDhc8PsEWE)**.

- Após concluido esse processo, utilize o seguinte comando:
```javascript
python main.py
```
- Siga as instruções do programa e pronto!
