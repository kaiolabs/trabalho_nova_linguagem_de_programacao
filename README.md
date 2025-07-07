# MelodyScript

MelodyScript é uma linguagem de programação musical projetada para facilitar a criação de melodias, progressões de acordes e composições musicais através de código.

## 🎯 **Sistema de Validação Robusto**

MelodyScript possui um **Analisador Sintático Robusto baseado em GLC** que garante:
- ✅ **NUNCA executa código com erros de sintaxe**
- ✅ **Detecção inteligente de comandos malformados** (ex: `tocadasdasdasnima` → `tocar do seminima`)
- ✅ **Sugestões precisas de correção**
- ✅ **Análise em múltiplas camadas** (léxica, sintática, semântica)
- ✅ **Sistema extensível automaticamente**

## Recursos

- Definição e execução de melodias com notas musicais
- Configurações de tempo (BPM) e instrumentos (piano, guitarra, violino, flauta, baixo e sintetizador)
- Suporte a notas com modificadores (# e b)
- Suporte a diferentes durações de notas (semibreve, mínima, semínima, etc.)
- Definição e uso de acordes
- Controle de envelope ADSR para modelar a forma do som
- Diferentes formas de onda (senoidal, quadrada, triangular, dente de serra)
- Estruturas de controle (repetições, condicionais)
- Funções definidas pelo usuário para reutilização de código
- Capacidade de iteração sobre coleções como acordes
- Suporte a pausas e silêncios
- Interface de linha de comando para execução fácil
- Integração com VSCode através de uma extensão
- **Reprodução Paralela**: capacidade de tocar múltiplos sons simultaneamente, criando harmonias complexas.

## Recursos da Linguagem

- **Notas Musicais**: suporte para notação musical em português (`do`, `re`, `mi`) e em inglês (`c`, `d`, `e`).
- **Acordes**: definição e reprodução de acordes com sintaxe simples.
- **Envelope ADSR**: controle detalhado da forma como os sons são executados.
- **Formas de Onda**: diferentes timbres utilizando formas de onda básicas (senoidal, quadrada, triangular, dente de serra).
- **Instrumentos**: vários instrumentos com perfis sonoros diferentes (piano, guitarra, violino, flauta, baixo e sintetizador).
- **Função Condicionais**: estruturas `se-senao` para controle de fluxo.
- **Loops de Repetição**: repetição de blocos musicais com número definido de vezes.
- **Para Cada (Iteração)**: iteração sobre notas de acordes.
- **Funções Definidas pelo Usuário**: criação de funções reutilizáveis.
- **Reprodução Paralela**: capacidade de tocar múltiplos sons simultaneamente
  - **Modo Global**: ative para toda a melodia com `modo_paralelo ativado;`
  - **Blocos Paralelos**: controle precisamente quais partes da melodia são tocadas em paralelo usando `inicio_paralelo { ... } fim_paralelo`

## Sintaxe Básica

### Configurações Globais

```
tempo = 120  # Define o tempo em BPM
instrumento piano  # Define o instrumento (piano, guitarra, violino, flauta, baixo ou sintetizador)
forma_onda sine  # Define a forma de onda (sine, square, triangle, sawtooth)

# Configuração de envelope ADSR
envelope {
  attack = 0.05;
  decay = 0.1;
  sustain = 0.7;
  release = 0.2;
}

# Ativar modo paralelo global
modo_paralelo ativado;

# Ou usar blocos paralelos específicos
inicio_paralelo {
  tocar do minima;
  tocar mi minima; 
  tocar_acorde DoM semibreve;  # Toca junto com as notas individuais
} fim_paralelo
```

### Definição de Acordes

```
acorde DoMaior = <do mi sol>
acorde FaMaior = <fa la do>
acorde SolMaior = <sol si re>
```

### Definição de Funções

```
funcao arpejo(acorde, duracao) {
  para cada nota em acorde {
    tocar nota duracao
  }
}

funcao progressao(acorde1, acorde2, duracao) {
  tocar acorde1 duracao
  tocar acorde2 duracao
}
```

### Definição de Melodias

```
melodia exemplo {
  tocar do minima
  tocar re seminima
  tocar mi seminima
  pausa seminima
  
  repetir 2 vezes {
    tocar do colcheia
    tocar mi colcheia
    tocar sol colcheia
  }
  
  se(variavel == "valor") {
    tocar la minima
  } senao {
    tocar si minima
  }
  
  # Chamada de função
  arpejo(DoMaior, colcheia)
  progressao(DoMaior, SolMaior, seminima)
  
  # Blocos de reprodução paralela (notas tocam simultaneamente)
  iniciar_paralelo {
    tocar do minima
    tocar mi minima
    tocar sol minima
  }
  
  # Ou usando comandos separados para maior controle
  iniciar_paralelo;
  tocar fa seminima;
  tocar la seminima;
  parar_paralelo;
}
```

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/melodyscript.git
```

2. Configure o ambiente:
```
cd melodyscript
./setup.sh  # ou setup.bat no Windows
```

3. Execute um exemplo:
```bash
# Validação rigorosa + execução
./run_melodyscript.sh executar examples/ola_mundo.mscr

# Apenas validação (sem execução)
./run_melodyscript.sh lint examples/ola_mundo.mscr
```

### Exemplo de Validação Rigorosa

```bash
# Sistema detecta erro automaticamente
python -m src.melodyscript lint examples/arquivo_com_erro.mscr

# Resultado:
❌ ERRO DE COMPILAÇÃO: Foram encontrados 1 erro(s) de sintaxe.
📋 Lista de erros encontrados:
  1. Linha 9: Comando malformado 'tocadasdasdasnima' - Use: 'tocar do seminima'

🛑 A execução foi interrompida. Corrija TODOS os erros antes de executar o arquivo.
```

## Extensão VSCode

A extensão para VSCode está disponível no diretório `linter/` e oferece:

- Destaque de sintaxe
- Validação em tempo real com feedback claro
- Snippets para comandos comuns

## Exemplos

Vários exemplos estão disponíveis no diretório `examples/`:

- `ola_mundo.mscr` - Exemplo básico "Olá Mundo"
- `escalas.mscr` - Demonstração de escalas musicais
- `progressao_acordes.mscr` - Demonstração de progressões de acordes
- `formas_onda.mscr` - Demonstração das diferentes formas de onda disponíveis
- `funcoes_usuario.mscr` - Demonstração de funções definidas pelo usuário
- `ola_mundo.mscr` - Exemplo básico tocando "Frère Jacques"
- `escala_cromatica.mscr` - Demonstração de uma escala cromática completa
- `envelopes.mscr` - Demonstração de diferentes configurações de envelope ADSR
- `formas_onda.mscr` - Demonstração das diferentes formas de onda disponíveis
- `novos_recursos.mscr` - Demonstração de funções e iteração sobre acordes
- `reprodução_paralela.mscr` - Exemplo de reprodução simultânea de múltiplos sons usando modo global
- `blocos_paralelos.mscr` - Exemplo de uso de blocos paralelos em partes específicas da melodia
- `demonstracao_instrumentos.mscr` - Demonstração dos diferentes instrumentos disponíveis na linguagem
- `instrumentos_simples.mscr` - Exemplo simplificado para ouvir claramente cada instrumento
- `transicao_instrumentos.mscr` - Exemplo que toca a mesma melodia com cada instrumento para comparação
- `mini_orquestra.mscr` - Exemplo musical completo usando vários instrumentos em uma peça

## Estrutura do Projeto

```
melodyscript/
  ├── src/                # Código-fonte principal
  │   ├── core/           # Componentes centrais
  │   ├── linguagem/      # Processamento da linguagem
  │   ├── audio/          # Síntese de áudio
  │   └── utils/          # Utilitários
  ├── examples/           # Exemplos de uso
  ├── docs/               # Documentação
  ├── tests/              # Testes unitários e de integração
  ├── linter/             # Extensão para VSCode
  └── memory/             # Arquivos de memória para desenvolvimento
```

## Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua funcionalidade (`git checkout -b minha-funcionalidade`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Envie para o branch (`git push origin minha-funcionalidade`)
5. Crie um novo Pull Request

## Licença

Este projeto está licenciado sob a licença MIT.

## Instrumentos Disponíveis

A linguagem MelodyScript oferece diferentes instrumentos com timbres característicos:

- **Piano**: Som clássico de piano com decay natural
- **Guitarra**: Timbre brilhante de guitarra elétrica
- **Violino**: Som suave e expressivo de violino
- **Flauta**: Som puro e delicado de flauta
- **Baixo**: Som profundo e ressoante de baixo
- **Sintetizador**: Som sintético quadrado com característica eletrônica

Para utilizar um instrumento específico, basta declarar:

```
instrumento piano;
```

Ou qualquer outro instrumento da lista acima. 