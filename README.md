---

### Passo 1: Instalar o Python 3 e pip (se ainda não estiver instalado)

Verifique se o Python 3 e o pip (gerenciador de pacotes do Python) estão instalados:

```bash
python3 --version
pip3 --version
```

Se não estiverem instalados, você pode instalá-los com os seguintes comandos (para sistemas baseados em Debian/Ubuntu):

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Passo 2: Configurar um Ambiente Virtual

Crie e ative um ambiente virtual para o projeto. Isso garante que as dependências sejam isoladas do sistema principal.

#### 2.1. Criar o ambiente virtual:

```bash
python3 -m venv .venv
```

#### 2.2. Ativar o ambiente virtual:

Para sistemas Linux/macOS:

```bash
source .venv/bin/activate
```

Para sistemas Windows:

```bash
.venv\Scripts\activate
```

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias. Use o comando abaixo para instalar todas as bibliotecas:

```bash
pip install flask langchain openai faiss-cpu langchain_community langchain_openai python-dotenv
```

### Passo 4: Configurar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto (no mesmo diretório onde está o `app.py`). Este arquivo deve conter sua chave de API da OpenAI.

#### 4.1. Criar o arquivo `.env`:

```bash
touch .env
```

#### 4.2. Editar o arquivo `.env` e adicionar sua chave de API:

```bash
nano .env
```

Adicione o seguinte conteúdo:

```env
OPENAI_API_KEY=sk-<sua-chave-api-aqui>
```

Salve e feche o arquivo.

### Passo 5: Configurar o Layout da Interface

Se você estiver utilizando a versão mais recente do HTML com o layout atualizado, certifique-se de que o arquivo `index.html` esteja corretamente colocado no diretório `templates/`.

### Passo 6: Executar o Projeto

Com o ambiente virtual ativado e todas as dependências instaladas, execute o arquivo `app.py` para iniciar o servidor Flask:

```bash
python3 app.py
```

O servidor deve estar rodando em `http://127.0.0.1:5000`. Você pode abrir essa URL no navegador para interagir com a interface.

### Passo 7: Desativar o Ambiente Virtual (Opcional)

Depois de terminar, você pode desativar o ambiente virtual com:

```bash
deactivate
```

### Passo 8: Reativar o Ambiente Virtual no Futuro

Sempre que você precisar trabalhar no projeto novamente, reative o ambiente virtual com:

Para sistemas Linux/macOS:

```bash
source .venv/bin/activate
```

Para sistemas Windows:

```bash
.venv\Scripts\activate
```

Depois, você pode executar `python3 app.py` novamente para rodar o servidor Flask.

---

### Resumo dos Passos:

1. Instalar Python 3 e pip (se necessário).
2. Criar e ativar o ambiente virtual.
3. Instalar as dependências com pip.
4. Criar e configurar o arquivo `.env` com a chave da OpenAI.
5. Verificar se o layout do `index.html` está correto.
6. Executar o projeto com `python3 app.py`.
7. Desativar o ambiente virtual ao finalizar (opcional).
8. Reativar o ambiente virtual no futuro antes de rodar o projeto novamente.

