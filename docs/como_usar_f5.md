# Como Usar F5 para Executar MelodyScript no VSCode

## 🎹 Execução Rápida com F5

A extensão MelodyScript para VSCode está configurada para permitir execução rápida de arquivos `.mscr` usando a tecla **F5**.

## 📋 Como Usar

### 1. Abrir Arquivo MelodyScript
- Abra qualquer arquivo com extensão `.mscr` no VSCode
- Certifique-se de que o arquivo está salvo (Ctrl+S)

### 2. Executar com F5
- Com o arquivo `.mscr` ativo no editor
- Pressione **F5**
- A extensão automaticamente:
  - Salva o arquivo
  - Ativa o ambiente virtual Python
  - Executa o arquivo usando `python -m src.melodyscript executar`
  - Mostra a saída no terminal integrado do VSCode

## 🎵 Exemplo de Teste

Use o arquivo `teste_f5.mscr` na raiz do projeto:

```melodyscript
// Arquivo de teste para demonstrar F5
tempo = 120;
instrumento piano;
forma_onda sine;

acorde DoMaior = <do mi sol>;

melodia teste_f5 {
    tocar do seminima;
    tocar mi seminima;
    tocar sol seminima;
    pausa seminima;
    tocar DoMaior minima;
    tocar do minima;
}

executar teste_f5;
```

## ⚙️ Configuração Técnica

### Keybinding
- **Tecla**: F5
- **Condição**: `editorLangId == melodyscript`
- **Comando**: `melodyscript.execute`

### Script de Execução
- **Windows**: `run_melodyscript.bat executar arquivo.mscr`
- **Linux/Mac**: `./run_melodyscript.sh executar arquivo.mscr`

## 🔧 Solução de Problemas

### Erro de Ambiente Virtual
Se aparecer erro sobre ambiente virtual:
```bash
python -m venv .venv --clear
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Extensão Não Reconhece F5
1. Verifique se a extensão MelodyScript está instalada e ativada
2. Confirme que o arquivo tem extensão `.mscr`
3. Recarregue o VSCode (Ctrl+Shift+P → "Developer: Reload Window")

## 🎼 Exemplos para Testar

- `examples/ola_mundo.mscr` - Exemplo básico com acordes
- `examples/escalas.mscr` - Escalas musicais
- `examples/frere_jacques.mscr` - Música completa
- `examples/instrumentos_simples.mscr` - Múltiplos instrumentos

## 🚀 Dicas de Produtividade

1. **Edição Rápida**: Use F5 para testar modificações instantaneamente
2. **Debug Musical**: Adicione pausas para ouvir seções específicas
3. **Iteração Rápida**: Modifique tempo, instrumentos ou notas e teste imediatamente
4. **Validação**: Use Ctrl+S para ativar o linter antes de F5

Aproveite a programação musical com MelodyScript! 🎵 