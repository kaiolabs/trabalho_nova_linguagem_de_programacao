# Histórias de Usuário - MelodyScript

## Objetivo Geral
Desenvolver a MelodyScript, uma linguagem de programação musical que permite aos usuários escrever e executar composições musicais através de código com uma sintaxe simples e intuitiva.

## Histórias de Usuário Concluídas ✅

### História 1: Configuração do Ambiente de Desenvolvimento ✅
**Como** desenvolvedor da MelodyScript  
**Quero** configurar o ambiente de desenvolvimento básico  
**Para** iniciar a implementação da linguagem

**Critérios de Aceitação:**
- ✅ Ambiente Python configurado com todas as bibliotecas necessárias
- ✅ Estrutura de diretórios do projeto criada
- ✅ Repositório de código inicializado

### História 2: Implementação do "Olá Mundo" Musical ✅
**Como** usuário da MelodyScript  
**Quero** escrever e executar um programa "Olá Mundo" simples 
**Para** verificar o funcionamento básico da linguagem

**Critérios de Aceitação:**
- ✅ Criar um arquivo com a extensão `.mscr` para a MelodyScript
- ✅ Escrever um programa simples usando a sintaxe definida
- ✅ Executar o programa e ouvir a melodia

### História 3: Definição da Gramática Básica ✅
**Como** desenvolvedor da MelodyScript  
**Quero** definir a gramática formal básica da linguagem  
**Para** permitir a análise sintática do código

**Critérios de Aceitação:**
- ✅ Definir tokens da linguagem
- ✅ Estabelecer regras de sintaxe para notas, durações, instrumentos e tempo
- ✅ Implementar estruturas de controle como repetições
- ✅ Documentar a gramática

### História 4: Implementação do Parser ✅
**Como** desenvolvedor da MelodyScript  
**Quero** implementar o analisador sintático (parser)  
**Para** analisar corretamente o código-fonte

**Critérios de Aceitação:**
- ✅ Identificar corretamente todos os tokens definidos na gramática
- ✅ Processar blocos com chaves corretamente
- ✅ Gerar mensagens de erro claras para tokens inválidos
- ✅ Integrar o parser ao pipeline de processamento

### História 5: Implementação do Motor de Áudio ✅
**Como** desenvolvedor da MelodyScript  
**Quero** implementar um motor de áudio de qualidade  
**Para** reproduzir as notas musicais com fidelidade

**Critérios de Aceitação:**
- ✅ Sintetizar corretamente notas musicais usando NumPy
- ✅ Suportar diferentes formas de onda (senoidal, quadrada, triangular, dente de serra)
- ✅ Implementar envelope ADSR para melhorar a qualidade sonora
- ✅ Controlar adequadamente o tempo entre as notas

### História 6: Execução de Composições Musicais ✅
**Como** usuário da MelodyScript  
**Quero** executar minhas composições musicais com controle de tempo  
**Para** ouvi-las e verificar se estão corretas

**Critérios de Aceitação:**
- ✅ Executar programas MelodyScript através da linha de comando
- ✅ Reproduzir as notas com as durações corretas conforme o BPM definido
- ✅ Aplicar modificadores (sustenidos e bemóis) corretamente
- ✅ Fornecer feedback visual durante a execução

### História 7: Implementação de Estruturas de Repetição ✅
**Como** usuário da MelodyScript  
**Quero** usar estruturas de repetição nos meus programas  
**Para** escrever códigos mais concisos e expressivos

**Critérios de Aceitação:**
- ✅ Implementar sintaxe para repetições `repetir X vezes { ... }`
- ✅ Suportar repetições aninhadas
- ✅ Processar corretamente o conteúdo dentro dos blocos de repetição
- ✅ Demonstrar o funcionamento com um exemplo real (Frère Jacques)

### História 8: Documentação da Linguagem ✅
**Como** usuário da MelodyScript  
**Quero** ter acesso a uma documentação clara e completa  
**Para** aprender a usar a linguagem e seus recursos

**Critérios de Aceitação:**
- ✅ Documentar a sintaxe da linguagem
- ✅ Explicar os tipos de notas e durações disponíveis
- ✅ Descrever os comandos e estruturas suportados
- ✅ Fornecer exemplos de uso

### História 11: Implementação de Ferramentas de Desenvolvimento ✅
**Como** desenvolvedor de programas MelodyScript  
**Quero** ter ferramentas que me ajudem a detectar erros e melhorar o código  
**Para** criar programas mais robustos e eficientes

**Critérios de Aceitação:**
- ✅ Implementar um linter para verificação de código
- ✅ Detectar erros comuns de sintaxe e lógica musical
- ✅ Fornecer sugestões de melhoria
- ✅ Integrar com editor de código (VSCode)

### História 12: Melhoria da Integração do Ambiente de Desenvolvimento ✅
**Como** desenvolvedor de programas MelodyScript  
**Quero** ter uma integração perfeita entre o VSCode e o ambiente Python  
**Para** executar e validar meus programas sem problemas de dependências

**Critérios de Aceitação:**
- ✅ Criar scripts auxiliares para garantir a execução correta em diferentes sistemas
- ✅ Garantir que o ambiente virtual Python seja sempre usado corretamente
- ✅ Resolver automaticamente problemas comuns como "No module named 'numpy'"
- ✅ Implementar mensagens de diagnóstico claras para facilitar a resolução de problemas
- ✅ Atualizar a documentação com instruções detalhadas para resolver problemas comuns

## Histórias de Usuário Em Andamento ⏳

### História 9: Implementação de Polifonia ⏳
**Como** usuário da MelodyScript  
**Quero** executar múltiplas notas simultaneamente  
**Para** criar harmonias e acordes

**Critérios de Aceitação:**
- [ ] Definir sintaxe para execução de múltiplas notas
- [ ] Processar acordes corretamente
- [ ] Reproduzir várias linhas melódicas ao mesmo tempo
- [ ] Criar exemplos demonstrando o uso de polifonia

### História 10: Suporte a Diferentes Instrumentos ⏳
**Como** usuário da MelodyScript  
**Quero** utilizar diferentes timbres instrumentais  
**Para** enriquecer minhas composições

**Critérios de Aceitação:**
- [ ] Implementar sintaxe para seleção de instrumentos
- [ ] Suportar pelo menos 3 tipos diferentes de instrumentos
- [ ] Permitir a troca de instrumentos durante a execução
- [ ] Criar exemplos demonstrando o uso de diferentes instrumentos 