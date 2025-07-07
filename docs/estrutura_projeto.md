# Estrutura do Projeto MelodyScript

Este documento descreve a estrutura do projeto MelodyScript e como os diferentes módulos se relacionam.

## Visão Geral

MelodyScript é organizado seguindo o princípio de responsabilidade única, dividindo o código em módulos específicos para cada aspecto do sistema.

### 🎯 **Sistema de Validação Robusto**

O projeto foi aprimorado com um **Analisador Sintático Robusto baseado em GLC** que implementa:
- **Análise Lexical Rigorosa:** Sistema de tipos de tokens com classificação precisa
- **Gramática Livre de Contexto Formal:** Regras de produção BNF implementadas
- **Análise Sintática Avançada:** Detecção de comandos malformados e estruturas incorretas
- **Validação Semântica:** Análise contextual e verificação de coerência
- **Sistema Extensível:** Adaptação automática a novos tokens e comandos

```
src/
├── __init__.py         # Inicialização do pacote
├── melodyscript.py     # Ponto de entrada principal
├── cli.py              # Interface de linha de comando
├── linter.py           # Validador de sintaxe e semântica
├── core/               # Componentes centrais do interpretador
├── linguagem/          # Componentes de processamento da linguagem
├── audio/              # Componentes de síntese de áudio
└── utils/              # Utilitários e funções auxiliares
```

## Módulos

### Core

Contém os componentes centrais do interpretador MelodyScript:

- `interpretador.py`: Coordena a execução de programas MelodyScript, interpreta e executa comandos musicais.

### Linguagem

Contém componentes relacionados à definição e processamento da linguagem:

- `parser.py`: Classe base do parser, responsável por analisar arquivos MelodyScript.
- `parser_definicoes.py`: Processamento de definições (globais, acordes, funções, melodias).
- `parser_comandos.py`: Processamento de comandos (tocar, pausa, repetições, condicionais).
- `funcoes_padrao.py`: Definição das funções predefinidas da linguagem.

### Audio

Componentes de síntese e processamento de áudio:

- `sintetizador.py`: Motor de áudio para reprodução de notas musicais.

### Utils

Funções e classes auxiliares usadas por outros módulos:

- `teoria_musical.py`: Constantes e funções relacionadas à teoria musical.

## Fluxo de Execução

1. O usuário executa `melodyscript.py` via linha de comando.
2. O script chama a função `main()` de `cli.py`.
3. A CLI processa os argumentos e cria uma instância de `MelodyScriptInterpretador`.
4. O interpretador usa o `MelodyScriptParser` para analisar o arquivo MelodyScript.
5. O parser extrai definições e comandos do código-fonte.
6. O interpretador executa os comandos usando o `AudioEngine` para gerar sons.

## Extensibilidade

A estrutura modular permite fácil extensão do sistema:

- Novos comandos podem ser adicionados no `parser_comandos.py`.
- Novas definições podem ser adicionadas no `parser_definicoes.py`.
- Novos efeitos de áudio podem ser implementados no `sintetizador.py`.
- Funções musicais adicionais podem ser incluídas no `teoria_musical.py`.

## Testes

Os testes do sistema estão organizados de forma similar aos módulos:

```
tests/
├── __init__.py
├── test_parser.py
├── test_interpretador.py
├── test_audio.py
└── test_teoria_musical.py
```

Cada módulo tem seus próprios testes unitários para garantir seu funcionamento correto. 