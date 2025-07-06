# Status do Projeto - MelodyScript

## Visão Geral
Este documento registra o status atual do desenvolvimento da MelodyScript, uma linguagem de programação musical que permite aos usuários criar e reproduzir melodias usando uma sintaxe simples e intuitiva.

## O que já foi feito
- [x] Definição inicial dos requisitos para a MelodyScript (`requisitos_linguagem_python.md`)
- [x] Estabelecimento da estrutura de gerenciamento do projeto
- [x] Definição das histórias de usuário
- [x] Planejamento das tarefas para implementação
- [x] Definição da linguagem: nome (MelodyScript) e extensão (`.mscr`)
- [x] Definição da sintaxe com chaves no estilo C/Java/Dart
- [x] Implementação do parser básico para a nova sintaxe
- [x] Implementação do interpretador para executar melodias
- [x] Implementação do motor de áudio com Pygame e NumPy
- [x] Implementação de modulação de envelope ADSR para melhorar a qualidade sonora
- [x] Suporte a diferentes formas de onda (senoidal, quadrada, triangular, dente de serra)
- [x] Implementação de estruturas de repetição (`repetir X vezes { ... }`)
- [x] Suporte a notas alteradas (sustenidos e bemóis)
- [x] Criação de exemplos demonstrando os recursos da linguagem:
  - [x] Exemplo "Olá Mundo" musical (`ola_mundo.mscr`)
  - [x] Exemplo de escala musical (`escala_maior.mscr`)
  - [x] Implementação da música "Frère Jacques" (`frere_jacques.mscr`)
  - [x] Exemplo com repetição (`repeticao.mscr`)
  - [x] Exemplo com notas alteradas (`notas_alteradas.mscr`)
  - [x] Exemplo demonstrando formas de onda e envelope ADSR (`formas_de_onda.mscr`)
  - [x] Exemplos para teste da extensão VSCode:
    - [x] Teste de ambiente virtual (`ambiente_virtual.mscr`)
    - [x] Teste de scripts auxiliares (`teste_script_auxiliar.mscr`) 
    - [x] Demonstração de diagnósticos (`diagnostico_vscode.mscr`)
    - [x] Demonstração de destaque de sintaxe e snippets (`demonstracao_extensao.mscr`)
  - [x] Documentação dos exemplos (`examples/README.md`)
- [x] Documentação da linguagem no README.md
- [x] Ferramentas de desenvolvimento:
  - [x] Linter para verificação de código MelodyScript
  - [x] Extensão VSCode com destaque de sintaxe, snippets e validação em tempo real
  - [x] Scripts auxiliares para execução e validação (`run_melodyscript.sh` e `run_melodyscript.bat`)
  - [x] Integração aprimorada com ambiente virtual Python para garantir acesso às dependências

## O que está sendo feito (Em andamento)
- [ ] Implementação de recursos avançados:
  - [ ] Polifonia (tocar múltiplas notas simultaneamente)
  - [ ] Suporte a outros instrumentos além de ondas sintéticas
  - [ ] Exportação para formatos de áudio (WAV, MP3)
- [ ] Interface gráfica para composição musical
- [ ] Exemplo conceitual de funcionalidades futuras (`recursos_futuros.mscr`)

## O que falta fazer (Priorizado)
### Prioridade Alta
1. **Polifonia e Harmonia:**
   - Implementação de acordes e múltiplas vozes
   - Recursos harmônicos (definição e progressão de acordes)
   - Comandos de expressão musical (dinâmica, articulação)

2. **Instrumentos e Síntese Sonora:**
   - Biblioteca de instrumentos baseados em samples
   - Efeitos de áudio (reverb, delay, filtros)
   - Síntese sonora avançada (FM, wavetable, granular)

3. **Estruturas Musicais e Composição:**
   - Estruturas de composição reutilizáveis
   - Recursos de teoria musical (escalas, modos, harmonização)
   - Ferramentas de composição assistida (acompanhamento, padrões rítmicos)

### Prioridade Média
1. **Exportação e Integração:**
   - Exportação para formatos de áudio (WAV, MP3, OGG)
   - Exportação para formatos de notação (MIDI, MusicXML)
   - Integração com outras ferramentas musicais

2. **Interface do Usuário:**
   - Editor gráfico para composição e edição
   - Visualização em tempo real de notas e partitura
   - Ferramentas avançadas de edição e controle

3. **Recursos Avançados de Linguagem:**
   - Funções, loops e condicionais
   - Sistema de módulos e bibliotecas
   - Programação orientada a eventos

### Prioridade Baixa
1. **Recursos de Performance:**
   - Ferramentas para performance ao vivo
   - Recursos de ensaio e prática
   - Funcionalidades colaborativas

2. **Educação e Acessibilidade:**
   - Recursos educacionais interativos
   - Melhorias de acessibilidade
   - Documentação avançada e tutoriais

3. **Inteligência Artificial e Composição Algorítmica:**
   - Assistência por IA para composição
   - Geradores algorítmicos de melodias e harmonias
   - Aprendizado baseado nas preferências do usuário

## Marcos do Projeto
1. **Marco 1: Sintaxe básica e execução de melodias (CONCLUÍDO)** - Implementação da sintaxe básica e capacidade de tocar notas simples
2. **Marco 2: Recursos avançados e qualidade sonora (CONCLUÍDO)** - Implementação de envelope ADSR, formas de onda e repetições
3. **Marco 3: Ferramentas de desenvolvimento (CONCLUÍDO)** - Implementação de linter e extensão VSCode
4. **Marco 4: Polifonia e instrumentos (ATUAL)** - Implementação de polifonia e suporte a diferentes instrumentos
5. **Marco 5: Exportação e interface gráfica** - Interface gráfica e exportação para formatos de áudio

## Estado atual dos componentes
- **Parser:** Implementado e funcional, com suporte a blocos com chaves, repetições e configurações de som
- **Interpretador:** Implementado e funcional, capaz de executar melodias com diferentes notas, durações e pausas
- **Motor de áudio:** Implementado com Pygame e NumPy, oferecendo boa qualidade sonora com envelope ADSR e múltiplas formas de onda
- **CLI:** Interface de linha de comando implementada com comandos para execução e validação de código
- **Linter:** Implementado com verificação de sintaxe, validação de notas e durações, e recomendações de boas práticas
- **Extensão VSCode:** Implementada com destaque de sintaxe, snippets, validação em tempo real e execução de código. Melhorada a integração com o ambiente virtual Python para garantir acesso a todas as dependências necessárias (numpy, pygame) em diferentes sistemas operacionais.
- **Documentação:** README.md com descrição da linguagem, sintaxe e exemplos de uso, e guia da extensão VSCode atualizado com informações sobre resolução de problemas com o ambiente virtual.

## Próximas Ações
1. Implementar suporte a polifonia (tocar múltiplas notas simultaneamente)
2. Adicionar suporte a outros instrumentos além de ondas sintéticas
3. Implementar exportação para formatos de áudio (WAV, MP3)
4. Desenvolver interface gráfica para composição musical 