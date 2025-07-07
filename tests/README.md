# Exemplos da MelodyScript

Este diretório contém vários exemplos que demonstram os recursos e a sintaxe da linguagem MelodyScript.

## Execução dos Exemplos

Você pode executar qualquer um desses exemplos usando um dos seguintes métodos:

### Método 1: Usando os scripts auxiliares

#### Linux/macOS:
```bash
./run_melodyscript.sh executar examples/nome_do_arquivo.mscr
```

#### Windows:
```batch
run_melodyscript.bat executar examples/nome_do_arquivo.mscr
```

### Método 2: No VS Code

1. Abra o arquivo `.mscr` no VS Code
2. Pressione F5 ou use o comando "MelodyScript: Executar Arquivo" na paleta de comandos

## Exemplos Disponíveis

### Exemplos Básicos
- **ola_mundo.mscr**: Um simples "Olá Mundo" musical que toca uma sequência de notas.
- **escala_maior.mscr**: Demonstra a escala de Dó maior.

### Exemplos para Recursos Específicos
- **notas_alteradas.mscr**: Mostra o uso de notas alteradas (sustenidos e bemóis).
- **repeticao.mscr**: Demonstra o uso de estruturas de repetição.
- **formas_de_onda.mscr**: Mostra diferentes formas de onda e configurações de envelope ADSR.
- **frere_jacques.mscr**: Implementação da música "Frère Jacques" usando repetições.

### Exemplos para Teste de Extensão
- **ambiente_virtual.mscr**: Testa se o ambiente virtual Python está funcionando corretamente.
- **teste_script_auxiliar.mscr**: Testa a execução através dos scripts auxiliares em diferentes sistemas.
- **diagnostico_vscode.mscr**: Contém erros intencionais para demonstrar as mensagens de diagnóstico.
- **demonstracao_extensao.mscr**: Mostra diferentes elementos da sintaxe para testar o destaque de cores e snippets.

### Exemplos Conceituais
- **recursos_futuros.mscr**: Um exemplo conceitual que demonstra como poderiam ser implementadas funcionalidades futuras como polifonia, acordes, efeitos de áudio, e muito mais. (Este é apenas um exemplo ilustrativo e não vai funcionar na versão atual da MelodyScript).

### Exemplos com Erros
- **com_erros.mscr**: Exemplo que contém erros para demonstrar a validação do código.

## Solução de Problemas

Se você encontrar erros como "No module named 'numpy'" ao executar os exemplos, verifique:

1. Se o ambiente virtual Python está ativado corretamente
2. Se todas as dependências estão instaladas no ambiente virtual

```bash
# Ativar o ambiente virtual
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

# Instalar as dependências
pip install -r requirements.txt
```

Consulte o guia da extensão VSCode em `docs/vscode_extension_guide.md` para mais informações sobre a solução de problemas. 