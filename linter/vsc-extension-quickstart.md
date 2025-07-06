# Bem-vindo à Extensão MelodyScript para VSCode

## O que há na pasta

* `package.json` - Manifesto da extensão
* `tsconfig.json` - Configuração do TypeScript
* `src/extension.ts` - Código principal da extensão (ponto de entrada)
* `syntaxes/melodyscript.tmLanguage.json` - Definição de gramática para destaque de sintaxe
* `language-configuration.json` - Configurações da linguagem (indentação, comentários, etc.)
* `snippets/melodyscript.json` - Snippets de código

## Começando a Desenvolver

* Instale as dependências: `npm install`
* Pressione `F5` para abrir uma nova janela com a extensão carregada
* Abra um arquivo `.mscr` ou crie um novo arquivo com esta extensão
* Faça alterações na extensão e recarregue (`Ctrl+R` ou `Cmd+R` no Mac) para testá-las

## Modificando a Extensão

* Na pasta `syntaxes`, você pode modificar as regras de destaque de sintaxe
* Na pasta `snippets`, você pode adicionar ou modificar snippets de código
* Em `src/extension.ts`, você pode estender as funcionalidades de validação e execução

## Empacotando a Extensão

* Instale a CLI do VSCode: `npm install -g vsce`
* Empacote a extensão para distribuição: `vsce package`
* Isso criará um arquivo `.vsix` que pode ser instalado em qualquer instalação do VSCode

## Integrando com MelodyScript

* A extensão chama o linter e interpretador MelodyScript via linha de comando
* Certifique-se de que a instalação do Python e do MelodyScript estão corretas
* Os erros e avisos são coletados da saída do linter e exibidos no editor

## Recursos Adicionais

* [Documentação de Extensões do VSCode](https://code.visualstudio.com/api)
* [Gramáticas TextMate](https://macromates.com/manual/en/language_grammars)
* [Guia de Colorização de Sintaxe](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)
* [Guia de Snippets](https://code.visualstudio.com/api/language-extensions/snippet-guide) 