# MelodyScript Language Extension

Esta é a extensão oficial para a linguagem MelodyScript no Visual Studio Code. A extensão fornece destaque de sintaxe, snippets e validação em tempo real para arquivos `.mscr`.

## Recursos

- **Destaque de Sintaxe**: Coloração apropriada para todos os elementos da linguagem MelodyScript
- **Snippets**: Modelos para criar rapidamente melodias, acordes, funções e outras estruturas
- **Validação em Tempo Real**: Feedback imediato sobre erros de sintaxe
- **Executar Arquivo**: Atalho F5 para executar o arquivo MelodyScript atual
- **Ícone Personalizado**: Ícone de nota musical para arquivos .mscr, tornando-os facilmente identificáveis no explorador de arquivos

## Instalação

### Instalação a partir do VSIX

1. Certifique-se de ter o Visual Studio Code instalado
2. Execute o script `rebuild_extension.sh` (Linux/Mac) ou `rebuild_extension.bat` (Windows) para gerar o arquivo VSIX:
   ```
   # Linux/Mac
   ./rebuild_extension.sh
   
   # Windows
   rebuild_extension.bat
   ```
3. Instale a extensão usando o comando:
   ```
   code --install-extension linter/melodyscript-language-0.1.0.vsix
   ```
   
Alternativamente, no VS Code:
1. Vá para a aba Extensões (Ctrl+Shift+X ou ⇧⌘X)
2. Clique nos três pontos (...) no topo da barra lateral
3. Selecione "Instalar a partir do VSIX..."
4. Navegue até o arquivo VSIX gerado e selecione-o

### Desenvolvimento da Extensão

Para contribuir com o desenvolvimento da extensão:

1. Clone o repositório
2. Navegue até a pasta `linter`
3. Instale as dependências:
   ```
   npm install
   ```
4. Abra a pasta no VS Code
5. Pressione F5 para iniciar uma nova janela do VS Code com a extensão carregada

## Uso da Extensão

### Snippets

Digite um dos prefixos abaixo e pressione Tab para inserir o snippet:

- `melodia`: Cria uma estrutura básica de melodia
- `acorde`: Cria a definição de um acorde
- `envelope`: Cria a configuração de envelope ADSR
- `repetir`: Cria um bloco de repetição
- `se`: Cria uma estrutura condicional
- `funcao`: Cria a definição de uma função
- `para-cada`: Cria um loop para iterar sobre elementos de um acorde

### Executar Arquivo

Com um arquivo MelodyScript aberto:

1. Pressione F5
2. O arquivo será executado usando o interpretador MelodyScript
3. A saída será exibida no terminal integrado

### Validação em Tempo Real

A extensão valida automaticamente o código MelodyScript enquanto você digita:

- Erros de sintaxe são sublinhados em vermelho
- Passe o mouse sobre o erro para ver uma descrição detalhada
- O diagnóstico também é exibido no painel "Problemas" (Ctrl+Shift+M ou ⇧⌘M)

## Configuração do Projeto

```
linter/
  ├── src/                # Código-fonte da extensão
  ├── syntaxes/           # Definições de gramática para destaque de sintaxe
  ├── snippets/           # Snippets para autocompleção
  ├── dist/               # Código compilado
  └── package.json        # Configurações e metadados da extensão
```

## Requisitos

- Visual Studio Code v1.60.0 ou superior
- Node.js e npm para desenvolvimento

## Resolução de Problemas

Se encontrar problemas ao usar a extensão:

1. Verifique se você está usando a versão mais recente do VS Code
2. Recompile a extensão usando `./rebuild_extension.sh` ou `rebuild_extension.bat`
3. Verifique o console de desenvolvimento do VS Code (Help > Toggle Developer Tools) para mensagens de erro

## Contribuições

Contribuições são bem-vindas! Por favor, envie um pull request ou abra uma issue no repositório.

## Licença

Esta extensão é distribuída sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

### Ícone Personalizado

A extensão inclui um ícone personalizado de nota musical para arquivos MelodyScript:

- Os arquivos .mscr são representados com um ícone de nota musical
- O ícone é visível no explorador de arquivos e nas abas de editores
- Este ícone torna arquivos MelodyScript facilmente distinguíveis de outros tipos de arquivos

Para garantir que os ícones apareçam corretamente:
1. Instale a extensão conforme as instruções acima
2. Reinicie o VS Code
3. Os arquivos .mscr agora devem mostrar o ícone de nota musical 