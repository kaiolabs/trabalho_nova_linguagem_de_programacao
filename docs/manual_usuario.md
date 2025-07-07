# Manual do Usuário MelodyScript

## Introdução

MelodyScript é uma linguagem de programação musical que permite criar melodias, ritmos e sequências musicais através de código. Inspirada na sintaxe de Python, a linguagem foi projetada para ser intuitiva e fácil de aprender.

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd melodyscript
```

2. Instale as dependências:
```bash
# No Windows
setup.bat

# No Linux/macOS
./setup.sh
```

Ou instale manualmente:
```bash
pip install -r requirements.txt
```

## Uso Básico

### Execução com Validação Rigorosa

Para executar um arquivo MelodyScript (com validação automática):

```bash
python -m src.melodyscript executar caminho/para/arquivo.mscr
```

Para validar a sintaxe de um arquivo MelodyScript sem executá-lo:

```bash
python -m src.melodyscript lint caminho/para/arquivo.mscr
```

### Sistema de Validação Robusto

O MelodyScript possui um **Analisador Sintático Robusto** que:
- ✅ **NUNCA executa código com erros de sintaxe**
- ✅ **Detecta comandos malformados** como `tocadasdasdasnima`
- ✅ **Fornece sugestões precisas** de correção
- ✅ **Para execução imediatamente** ao encontrar qualquer erro

#### Exemplo de Detecção de Erro:
```bash
python -m src.melodyscript lint examples/arquivo_com_erro.mscr

# Resultado:
❌ ERRO DE COMPILAÇÃO: Foram encontrados 1 erro(s) de sintaxe.
📋 Lista de erros encontrados:
  1. Linha 9: Comando malformado 'tocadasdasdasnima' - Use: 'tocar do seminima'

🛑 A execução foi interrompida. Corrija TODOS os erros antes de executar o arquivo.
```

## Sintaxe da Linguagem

### Estrutura Básica

Um arquivo MelodyScript típico contém:
1. Definições globais
2. Definições de acordes
3. Definições de melodias

Exemplo:

```
# Definições globais
tempo = 120  # BPM
instrumento piano
forma_onda sine

# Definição de acordes
acorde DoMaior = <do mi sol>

# Definição de melodia
melodia intro {
    tocar do minima
    tocar re minima
    tocar mi minima
    tocar DoMaior semibreve
}
```

### Definições Globais

- **Tempo**: Define o andamento em batidas por minuto (BPM)
  ```
  tempo = 120
  ```

- **Instrumento**: Define o instrumento a ser usado
  ```
  instrumento piano
  ```

- **Forma de Onda**: Define o tipo de onda para síntese de som
  ```
  forma_onda sine
  ```
  Valores possíveis: `sine`, `square`, `triangle`, `sawtooth`

- **Envelope ADSR**: Define os parâmetros de ataque, decaimento, sustentação e liberação
  ```
  envelope {
      attack = 0.02;   # Tempo de ataque em segundos
      decay = 0.05;    # Tempo de decaimento em segundos
      sustain = 0.7;   # Nível de sustentação (0.0 a 1.0)
      release = 0.05;  # Tempo de liberação em segundos
  }
  ```

### Definição de Acordes

Os acordes são definidos usando a sintaxe:

```
acorde NOME = <nota1 nota2 nota3 ...>
```

Exemplos:
```
acorde DoMaior = <do mi sol>
acorde ReMenor = <re fa la>
```

### Definição de Melodias

As melodias são definidas usando a sintaxe:

```
melodia NOME {
    # Comandos
}
```

### Comandos Musicais

- **Tocar nota**: Toca uma nota com duração específica
  ```
  tocar NOTA DURAÇÃO
  ```
  Exemplo: `tocar do minima`

- **Tocar nota com modificador**: Toca uma nota alterada com duração específica
  ```
  tocar NOTA# DURAÇÃO  # Sustenido
  tocar NOTAb DURAÇÃO  # Bemol
  ```
  Exemplo: `tocar fa# seminima`

- **Tocar acorde**: Toca um acorde definido anteriormente
  ```
  tocar NOME_ACORDE DURAÇÃO
  ```
  Exemplo: `tocar DoMaior minima`

- **Tocar acorde literal**: Toca um acorde definido na hora
  ```
  tocar <NOTA1 NOTA2 NOTA3 ...> DURAÇÃO
  ```
  Exemplo: `tocar <do mi sol> seminima`

- **Pausa**: Insere um silêncio
  ```
  pausa DURAÇÃO
  ```
  Exemplo: `pausa colcheia`

### Estruturas de Controle

- **Repetição**: Repete um bloco de comandos
  ```
  repetir N vezes {
      # Comandos a repetir
  }
  ```
  Exemplo:
  ```
  repetir 4 vezes {
      tocar do seminima
      tocar mi seminima
  }
  ```

- **Condicional**: Executa comandos condicionalmente
  ```
  se (CONDIÇÃO) {
      # Comandos se verdadeiro
  } senao {
      # Comandos se falso (opcional)
  }
  ```
  Exemplo:
  ```
  se (tempo > 100) {
      tocar do seminima
  } senao {
      tocar do minima
  }
  ```

## Notas Musicais

### Notas Básicas
- Notação em português: `do`, `re`, `mi`, `fa`, `sol`, `la`, `si`
- Notação internacional: `c`, `d`, `e`, `f`, `g`, `a`, `b`

### Modificadores
- `#`: Sustenido (aumenta meio tom)
- `b`: Bemol (diminui meio tom)

### Durações
- `breve`: 4 tempos
- `semibreve`: 2 tempos
- `minima`: 1 tempo
- `seminima`: 1/2 tempo
- `colcheia`: 1/4 de tempo
- `semicolcheia`: 1/8 de tempo

## Exemplos

### Exemplo Simples: Escala de Dó Maior

```
# Escala de Dó Maior
tempo = 120
instrumento piano

melodia escala_do {
    tocar do seminima
    tocar re seminima
    tocar mi seminima
    tocar fa seminima
    tocar sol seminima
    tocar la seminima
    tocar si seminima
    tocar do seminima
}
```

### Exemplo com Acordes e Repetição

```
# Progressão básica
tempo = 100
instrumento piano

acorde DoMaior = <do mi sol>
acorde SolMaior = <sol si re>
acorde LaMenor = <la do mi>
acorde FaMaior = <fa la do>

melodia progressao {
    repetir 2 vezes {
        tocar DoMaior minima
        tocar SolMaior minima
        tocar LaMenor minima
        tocar FaMaior minima
    }
    
    # Final
    tocar DoMaior semibreve
}
```

## Dicas e Boas Práticas

1. Organize seu código com comentários para facilitar a leitura.
2. Defina os acordes antes de usá-los nas melodias.
3. Utilize tempo adequado para o estilo de música (60-180 BPM).
4. Experimente diferentes formas de onda para obter diferentes timbres.
5. Ajuste o envelope ADSR para controlar a expressividade das notas.

## Solução de Problemas

### Erros Comuns e Sistema de Validação

#### Erros de Sintaxe Detectados Automaticamente

O **Analisador Sintático Robusto** detecta automaticamente:

1. **Comandos Malformados:**
   ```bash
   # Erro: tocadasdasdasnima
   ❌ Linha 9: Comando malformado 'tocadasdasdasnima' - Use: 'tocar do seminima'
   
   # Erro: reper 2 vzes  
   ❌ Linha 5: Comando malformado 'reper' - Use: 'repetir'
   ❌ Linha 5: Token desconhecido 'vzes' - Sugestão: 'vezes'
   ```

2. **Estruturas Incompletas:**
   ```bash
   # Erro: tocar do (sem duração)
   ❌ Linha 3: Comando 'tocar' incompleto - Esperado duração após nota
   ```

3. **Balanceamento de Símbolos:**
   ```bash
   # Erro: chaves não fechadas
   ❌ Linha 8: Bloco de repetição não fechado - Faltando '}'
   ```

#### Como Corrigir Erros

1. **Use o comando `lint` primeiro:**
   ```bash
   python -m src.melodyscript lint seu_arquivo.mscr
   ```

2. **Corrija TODOS os erros listados**

3. **Execute apenas após validação bem-sucedida:**
   ```bash
   ✅ Validação de sintaxe concluída com sucesso!
   ```

#### Erros Tradicionais

- **Arquivo não encontrado**: Verifique se o caminho do arquivo está correto.
- **Melodia não encontrada**: Verifique se a melodia está definida no arquivo.
- **Acorde não definido**: Verifique se o acorde foi definido antes de ser usado.
- **Dependências faltando**: Execute `pip install -r requirements.txt`

### Suporte

Para mais ajuda, consulte a documentação adicional na pasta `docs/` ou abra uma issue no repositório do projeto. 