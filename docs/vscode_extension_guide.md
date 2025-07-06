# Guia da Extensão VSCode para MelodyScript

Este guia apresenta instruções detalhadas para instalar, configurar e usar a extensão VSCode para MelodyScript.

## Instalação

### Pré-requisitos
- Visual Studio Code 1.60.0 ou superior
- Node.js e npm (para desenvolvimento ou instalação a partir do código-fonte)
- Python 3.8 ou superior com MelodyScript instalado

### Método 1: Instalação a partir do arquivo VSIX

1. **Obtenha o arquivo VSIX**
   - Se você já tem o arquivo `.vsix`: Vá para o passo 2
   - Para criar o arquivo `.vsix`:
     ```bash
     # No Linux/macOS
     cd linter
     ./install.sh
     npm run package
     
     # No Windows
     cd linter
     install.bat
     npm run package
     ```
     Isso criará um arquivo `melodyscript-language-0.1.0.vsix` na pasta `linter`.

2. **Instale a extensão no VSCode**:
   - Abra o VSCode
   - Vá para a aba de extensões (Ctrl+Shift+X)
   - Clique no ícone "..." no topo da barra de extensões
   - Selecione "Instalar a partir do VSIX..."
   - Navegue até o arquivo `.vsix` e selecione-o

### Método 2: Execução em Modo de Desenvolvimento

1. **Clone o repositório e instale as dependências**:
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd [NOME_DO_DIRETÓRIO]/linter
   
   # No Linux/macOS
   ./install.sh
   
   # No Windows
   install.bat
   ```

2. **Abra a pasta no VSCode**:
   - Abra o VSCode
   - Vá para File > Open Folder... (ou Ctrl+K Ctrl+O)
   - Navegue até a pasta `linter` e selecione-a

3. **Execute a extensão**:
   - Pressione F5
   - Isso abrirá uma nova janela do VSCode com a extensão carregada

## Desenvolvimento e Manutenção

### Modificando e Recompilando a Extensão

Após fazer qualquer modificação no código da extensão, é necessário recompilá-la para que as alterações tenham efeito:

1. **Recompilação manual**:
   ```bash
   # No diretório linter
   npm run compile
   ```

2. **Usando scripts de automação**:
   ```bash
   # No Linux/macOS
   ./rebuild_extension.sh
   
   # No Windows
   rebuild_extension.bat
   ```

Esses scripts automatizam o processo de recompilação e verificam se tudo está funcionando corretamente.

### Ciclo de Desenvolvimento

1. Modifique os arquivos da extensão (ex: `linter/src/extension.ts`)
2. Recompile a extensão usando um dos métodos acima
3. Reinicie a extensão no VSCode:
   - Se estiver em modo de depuração (F5), pressione Ctrl+Shift+F5
   - Ou use o comando "Developer: Reload Window" na paleta de comandos (Ctrl+Shift+P)
4. Teste as alterações
5. **Verifique a saída** no terminal para diagnóstico

### Empacotando para Distribuição

Após finalizar as alterações, você pode criar um novo pacote VSIX:

```bash
# No diretório linter
npm run package
```

## Uso da Extensão

### Destaque de Sintaxe

O destaque de sintaxe é aplicado automaticamente a arquivos com extensão `.mscr`. Ele coloriza diferentes elementos:
- **Palavras-chave** (azul): `melodia`, `tocar`, `pausa`, `repetir`, etc.
- **Notas musicais** (verde): `do`, `re`, `mi`, `fa`, `sol`, `la`, `si`, etc.
- **Durações** (laranja): `breve`, `semibreve`, `minima`, `seminima`, etc.
- **Modificadores** (vermelho): `#` (sustenido), `b` (bemol)
- **Comentários** (cinza): Linhas iniciadas com `#`

### Snippets

Para usar snippets, digite o prefixo e pressione Tab ou clique na sugestão:

| Prefixo | Descrição |
|---------|-----------|
| `melodia` | Cria uma nova melodia |
| `tocar` | Insere comando para tocar uma nota |
| `tocar#` | Insere comando para tocar uma nota alterada |
| `pausa` | Insere comando de pausa |
| `repetir` | Cria um bloco de repetição |
| `tempo` | Define o tempo (BPM) |
| `instrumento` | Define o instrumento |
| `envelope` | Define envelope ADSR global |
| `configurar_envelope` | Configura envelope ADSR na melodia |
| `configurar_forma_onda` | Configura forma de onda |
| `frere` | Template da música Frère Jacques |
| `escala` | Template de escala maior de Dó |

### Validação de Código

A extensão valida o código MelodyScript automaticamente quando você salva o arquivo. Erros e avisos são exibidos:
- Erros são sublinhados em vermelho
- Avisos são sublinhados em amarelo
- Passe o mouse sobre um erro/aviso para ver mais detalhes

### Execução de Código

Para executar um arquivo MelodyScript:
1. Abra o arquivo `.mscr` no editor
2. Use um dos métodos:
   - Pressione F5 (atalho padrão)
   - Abra a paleta de comandos (Ctrl+Shift+P) e digite "MelodyScript: Executar Arquivo"
   - Clique com o botão direito no editor e selecione "MelodyScript: Executar Arquivo" no menu de contexto

Isso abrirá um terminal integrado no VSCode e executará o interpretador MelodyScript no arquivo atual.

## Personalização

### Temas

O destaque de sintaxe é compatível com todos os temas do VSCode, mas algumas cores podem variar dependendo do tema utilizado.

### Atalhos de Teclado

Você pode personalizar o atalho para o comando "MelodyScript: Executar Arquivo":
1. Vá para File > Preferences > Keyboard Shortcuts (ou Ctrl+K Ctrl+S)
2. Pesquise por "melodyscript.execute"
3. Clique no item e pressione a combinação de teclas desejada

## Solução de Problemas

### Scripts Auxiliares para Execução

A extensão VSCode para MelodyScript utiliza scripts auxiliares para garantir que o ambiente virtual seja corretamente ativado:

- `run_melodyscript.sh` (macOS/Linux)
- `run_melodyscript.bat` (Windows)

Se você tiver problemas com a execução:

1. **Verifique os scripts auxiliares**:
   - Certifique-se de que os scripts existem na raiz do projeto
   - Verifique se têm permissão de execução (no caso do .sh): `chmod +x run_melodyscript.sh`
   - Teste o script manualmente: `./run_melodyscript.sh executar examples/ola_mundo.mscr`

2. **Corrija o caminho do ambiente virtual se necessário**:
   Se a estrutura do seu projeto for diferente, edite os scripts para apontar para o caminho correto do ambiente virtual.

3. **Mensagens de diagnóstico**:
   Os scripts agora incluem mensagens de diagnóstico que mostram:
   - Qual Python está sendo usado
   - A versão do Python
   - Se o ambiente virtual foi ativado corretamente

### Problemas com o Ambiente Virtual Python

A extensão MelodyScript depende do ambiente virtual Python (`.venv`) para acessar as dependências necessárias (pygame, numpy, etc.). Se você encontrar erros como "No module named 'numpy'" ou similares:

1. **Verifique se o ambiente virtual está configurado corretamente**:
   ```bash
   # Ative o ambiente virtual manualmente
   source .venv/bin/activate  # No Linux/macOS
   .venv\Scripts\activate.bat  # No Windows
   
   # Verifique se as dependências estão instaladas
   pip list
   ```

2. **Reinstale as dependências no ambiente virtual, se necessário**:
   ```bash
   # Certifique-se de que o ambiente virtual está ativado
   pip install -r requirements.txt
   ```

3. **Execute manualmente para testar**:
   ```bash
   # Com o ambiente virtual ativado
   python -m src.melodyscript executar seu_arquivo.mscr
   ```

4. **Métodos alternativos se a extensão não conseguir acessar o ambiente virtual**:
   
   **Opção 1: Crie um alias no seu shell**
   
   No macOS/Linux (adicione ao seu `.bashrc` ou `.zshrc`):
   ```bash
   alias venv-python='/caminho/para/seu/projeto/.venv/bin/python'
   ```
   
   No Windows (crie um arquivo `.bat` e adicione ao PATH):
   ```batch
   @echo off
   C:\caminho\para\seu\projeto\.venv\Scripts\python.exe %*
   ```
   
   **Opção 2: Use o terminal integrado do VSCode**
   - Abra um terminal no VSCode
   - Ative manualmente o ambiente virtual
   - Execute os comandos MelodyScript nesse terminal

5. **Se tudo mais falhar, atualize a extensão**:
   - A extensão agora foi atualizada para ativar explicitamente o ambiente virtual
   - Execute o comando de recompilação: `./rebuild_extension.sh` ou `rebuild_extension.bat`
   - Reinicie o VSCode

### Problemas com a Compilação da Extensão

Se as alterações feitas na extensão não estiverem tendo efeito:

1. **Certifique-se de recompilar após cada alteração**:
   - Use o script `rebuild_extension.sh` (Linux/macOS) ou `rebuild_extension.bat` (Windows)
   - Ou compile manualmente: `cd linter && npm run compile`

2. **Reinicie a janela do VSCode** após a recompilação:
   - Comando na paleta: "Developer: Reload Window" (Ctrl+Shift+P)
   - Ou feche e reabra o VSCode

3. **Verifique se há erros de compilação**:
   - Olhe a saída do comando de compilação
   - Verifique o console de depuração (Ctrl+Shift+Y) para mensagens de erro

### Ciclo de Desenvolvimento Completo

Se você precisar modificar a extensão, siga este fluxo:

1. **Edite os arquivos** da extensão (principalmente `linter/src/extension.ts`)
2. **Recompile a extensão**:
   ```bash
   ./rebuild_extension.sh  # Linux/macOS
   rebuild_extension.bat   # Windows
   ```
3. **Recarregue o VSCode**:
   - Use o comando "Developer: Reload Window" na paleta (Ctrl+Shift+P)
4. **Teste suas alterações**:
   - Abra um arquivo `.mscr`
   - Use F5 ou o comando "MelodyScript: Executar Arquivo"
5. **Verifique a saída** no terminal para diagnóstico

### Erros na Execução de Arquivos

Se você encontrar problemas ao executar arquivos MelodyScript:
1. Certifique-se de que o Python 3.8+ está instalado e disponível no PATH
2. Verifique se o MelodyScript está instalado corretamente
3. Tente executar o arquivo manualmente no terminal:
   ```
   python -m src.melodyscript executar seu_arquivo.mscr
   ```

### Problemas com Destaque de Sintaxe

Se o destaque de sintaxe não estiver funcionando:
1. Certifique-se de que o arquivo tem a extensão `.mscr`
2. Verifique se a extensão está ativa (aparece na lista de extensões ativas)
3. Tente recarregar o VSCode (Ctrl+R ou Cmd+R no Mac)

## Atualizações e Feedback

Para atualizar a extensão, reconstrua o arquivo VSIX e reinstale-o seguindo as instruções de instalação.

Se encontrar bugs ou tiver sugestões, por favor reporte no repositório do projeto. 