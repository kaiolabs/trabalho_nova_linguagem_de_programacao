import { spawn } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';

let diagnosticCollection: vscode.DiagnosticCollection;

// Lista de palavras-chave reservadas
const RESERVED_KEYWORDS = [
    'melodia', 'tocar', 'pausa', 'repetir', 'vezes', 'tempo', 'instrumento',
    'forma_onda', 'acorde', 'envelope', 'attack', 'decay', 'sustain', 'release',
    'funcao', 'retornar', 'escala', 'se', 'senao', 'configurar_envelope',
    'configurar_forma_onda', 'para_cada', 'em', 'reverso'
];

// Palavras-chave comumente escritas incorretamente
const COMMON_TYPOS: { [key: string]: string } = {
    'tocar_acode': 'tocar_acorde',
    'repitir': 'repetir',
    'veses': 'vezes',
    'ves': 'vezes',
    'tempu': 'tempo',
    'tempoo': 'tempo',
    'tiempo': 'tempo',
    'instrumentu': 'instrumento',
    'imstrumento': 'instrumento',
    'envelope_config': 'configurar_envelope',
    'senão': 'senao',
    'envleope': 'envelope',
    'atacar': 'attack',
    'sustain_level': 'sustain',
    'liberar': 'release',
    'decaimento': 'decay',
    'ataque': 'attack',
    'funçao': 'funcao',
    'funcion': 'funcao',
    'function': 'funcao',
};

// Mapeamento de notas válidas
const VALID_NOTES = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si', 'c', 'd', 'e', 'f', 'g', 'a', 'b'];

// Mapeamento de durações válidas
const VALID_DURATIONS = ['breve', 'semibreve', 'minima', 'seminima', 'colcheia', 'semicolcheia', 'fusa', 'semifusa'];

// Mapeamento de formas de onda válidas
const VALID_WAVEFORMS = ['sine', 'square', 'triangle', 'sawtooth'];

// Função para remover comentários do estilo \_ ... _/
function removeComments(text: string): string {
    return text.replace(/\\_.*?_\//g, '');
}

export function activate(context: vscode.ExtensionContext) {
    console.log('A extensão MelodyScript foi ativada!');

    // Criar coleção de diagnósticos
    diagnosticCollection = vscode.languages.createDiagnosticCollection('melodyscript');
    context.subscriptions.push(diagnosticCollection);

    // Registrar comando para executar arquivo MelodyScript
    const disposable = vscode.commands.registerCommand('melodyscript.execute', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('Nenhum editor ativo encontrado');
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'melodyscript') {
            vscode.window.showErrorMessage('O arquivo atual não é um arquivo MelodyScript');
            return;
        }

        // Salvar o arquivo antes de executar
        document.save().then(() => {
            const filePath = document.fileName;
            executeMelodyScript(filePath);
        });
    });

    context.subscriptions.push(disposable);

    // Registrar validador para alterações de texto (validação em tempo real)
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            if (event.document.languageId === 'melodyscript') {
                // Executar validação com debounce
                setTimeout(() => {
                    validateDocumentStatic(event.document);
                }, 500); // Aguardar 500ms para evitar validações excessivas
            }
        })
    );

    // Registrar validador de documentos ao salvar (validação com o backend Python)
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(document => {
            if (document.languageId === 'melodyscript') {
                // Primeiro validação estática
                validateDocumentStatic(document);
                // Depois validação completa com o backend Python
                validateMelodyScript(document);
            }
        })
    );

    // Validar documentos abertos inicialmente
    if (vscode.window.activeTextEditor && 
        vscode.window.activeTextEditor.document.languageId === 'melodyscript') {
        validateDocumentStatic(vscode.window.activeTextEditor.document);
    }
}

/**
 * Executa validação estática do documento sem chamar o backend Python
 */
function validateDocumentStatic(document: vscode.TextDocument) {
    const diagnostics: vscode.Diagnostic[] = [];
    const text = document.getText();
    const lines = text.split("\n");

    // Verificar balanceamento de chaves
    let openBraces = 0;
    let closeBraces = 0;
    let openParens = 0;
    let closeParens = 0;

    // Para os acordes, vamos usar expressões regulares para evitar contar operadores de comparação
    const openChordPattern = /<(?![=>])/g;
    const closeChordPattern = /(?<![<=>-])>/g;
    
    let openChords = (text.match(openChordPattern) || []).length;
    let closeChords = (text.match(closeChordPattern) || []).length;

    for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
        const line = lines[lineIndex];
        // Remover comentários usando a nova sintaxe
        const lineWithoutComments = removeComments(line).trim();
        
        if (lineWithoutComments === '') continue;

        // Contar chaves e parênteses
        for (const char of lineWithoutComments) {
            if (char === '{') openBraces++;
            else if (char === '}') closeBraces++;
            else if (char === '(') openParens++;
            else if (char === ')') closeParens++;
        }

        // Verificar erros de sintaxe comuns em cada linha
        checkForTypos(document, lineIndex, line, diagnostics);
        checkForMissingTerminators(document, lineIndex, line, diagnostics);
        checkForInvalidCommands(document, lineIndex, line, diagnostics);
    }

    // Verificar balanceamento de chaves
    if (openBraces > closeBraces) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Faltam ${openBraces - closeBraces} chaves de fechamento '}'`,
            vscode.DiagnosticSeverity.Error
        ));
    } else if (closeBraces > openBraces) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Há ${closeBraces - openBraces} chaves de fechamento '}' a mais`,
            vscode.DiagnosticSeverity.Error
        ));
    }

    // Verificar balanceamento de parênteses
    if (openParens > closeParens) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Faltam ${openParens - closeParens} parênteses de fechamento ')'`,
            vscode.DiagnosticSeverity.Error
        ));
    } else if (closeParens > openParens) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Há ${closeParens - openParens} parênteses de fechamento ')' a mais`,
            vscode.DiagnosticSeverity.Error
        ));
    }

    // Verificar balanceamento de definições de acordes
    if (openChords > closeChords) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Faltam ${openChords - closeChords} fechamentos de acordes '>'`,
            vscode.DiagnosticSeverity.Error
        ));
    } else if (closeChords > openChords) {
        diagnostics.push(createDiagnostic(
            document,
            0, 0, 0, 1,
            `Há ${closeChords - openChords} fechamentos de acordes '>' a mais`,
            vscode.DiagnosticSeverity.Error
        ));
    }

    // Atualizar diagnósticos
    diagnosticCollection.set(document.uri, diagnostics);
}

/**
 * Verifica se há erros de digitação comuns em palavras-chave
 */
function checkForTypos(document: vscode.TextDocument, lineIndex: number, line: string, diagnostics: vscode.Diagnostic[]) {
    // Remover comentários
    const lineWithoutComments = removeComments(line);
    if (lineWithoutComments.trim() === '') return;

    // Dividir a linha em palavras
    const words = lineWithoutComments.split(/\s+/);

    for (const word of words) {
        // Checar por erros de digitação em palavras-chave
        if (word in COMMON_TYPOS) {
            const startCharIndex = lineWithoutComments.indexOf(word);
            if (startCharIndex >= 0) {
                diagnostics.push(createDiagnostic(
                    document,
                    lineIndex, startCharIndex, lineIndex, startCharIndex + word.length,
                    `Palavra-chave incorreta: '${word}'. Use '${COMMON_TYPOS[word]}' em vez disso.`,
                    vscode.DiagnosticSeverity.Warning
                ));
            }
        }
    }
}

/**
 * Verifica se faltam terminadores (ponto e vírgula) em comandos que exigem
 */
function checkForMissingTerminators(document: vscode.TextDocument, lineIndex: number, line: string, diagnostics: vscode.Diagnostic[]) {
    // Remover comentários
    const lineWithoutComments = removeComments(line).trim();
    if (lineWithoutComments === '') return;

    // Lista de comandos que devem terminar com ponto e vírgula
    const requiresSemicolon = [
        'tocar', 'pausa', 'tempo', 'instrumento', 'forma_onda',
        'configurar_envelope', 'configurar_forma_onda'
    ];

    // Verificar se algum desses comandos está presente e não termina com ponto e vírgula
    for (const command of requiresSemicolon) {
        if (lineWithoutComments.startsWith(command) && !lineWithoutComments.endsWith(';')) {
            // Verificar exceções:
            // 1. Definições de acordes contendo '<'
            if (command === 'tocar' && (lineWithoutComments.includes('<') || lineWithoutComments.includes('>'))) {
                // Verificar se a definição de acorde está completa
                const match = /tocar\s+<([^>]+)>\s+\w+/.exec(lineWithoutComments);
                if (match && !lineWithoutComments.endsWith(';')) {
                    diagnostics.push(createDiagnostic(
                        document,
                        lineIndex, 0, lineIndex, lineWithoutComments.length,
                        `Falta ponto e vírgula no final do comando '${command}'.`,
                        vscode.DiagnosticSeverity.Warning
                    ));
                }
            } 
            // 2. Exceções para comandos que podem aparecer em outros contextos
            else if (!lineWithoutComments.includes('{') && !lineWithoutComments.endsWith('}')) {
                diagnostics.push(createDiagnostic(
                    document,
                    lineIndex, 0, lineIndex, lineWithoutComments.length,
                    `Falta ponto e vírgula no final do comando '${command}'.`,
                    vscode.DiagnosticSeverity.Warning
                ));
            }
        }
    }

    // Verificar definições de acordes especificamente
    if (lineWithoutComments.startsWith('acorde') && 
        lineWithoutComments.includes('=') && 
        lineWithoutComments.includes('>') && 
        !lineWithoutComments.endsWith(';')) {
        diagnostics.push(createDiagnostic(
            document,
            lineIndex, 0, lineIndex, lineWithoutComments.length,
            `Falta ponto e vírgula no final da definição de acorde.`,
            vscode.DiagnosticSeverity.Warning
        ));
    }
}

/**
 * Verifica comandos inválidos ou com parâmetros incorretos
 */
function checkForInvalidCommands(document: vscode.TextDocument, lineIndex: number, line: string, diagnostics: vscode.Diagnostic[]) {
    // Remover comentários
    const lineWithoutComments = removeComments(line).trim();
    if (lineWithoutComments === '') return;

    // Verificar comando 'tocar' com parâmetros inválidos
    if (lineWithoutComments.startsWith('tocar ')) {
        const parts = lineWithoutComments.replace(/;$/, '').split(/\s+/);
        
        // Verificar se o comando tem pelo menos 3 partes: 'tocar', nota e duração
        if (parts.length >= 3) {
            // Verificar se a nota é válida (considerando notas com modificadores como do# ou reb)
            let noteValid = false;
            let durationValid = false;
            
            // Tratar caso especial de acorde literal: tocar <do mi sol> minima
            if (parts[1].startsWith('<') && parts.some(p => p.endsWith('>'))) {
                noteValid = true;
                // Verificar a duração, que deve ser o elemento após o fechamento do acorde
                const durationIndex = parts.findIndex(p => p.endsWith('>')) + 1;
                if (durationIndex < parts.length) {
                    durationValid = VALID_DURATIONS.includes(parts[durationIndex]) || isProbablyFunctionParameter(parts[durationIndex]);
                    if (!durationValid) {
                        diagnostics.push(createDiagnostic(
                            document,
                            lineIndex, line.indexOf(parts[durationIndex]), lineIndex, line.indexOf(parts[durationIndex]) + parts[durationIndex].length,
                            `Duração inválida: '${parts[durationIndex]}'. Valores válidos: ${VALID_DURATIONS.join(', ')}`,
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                }
            } else {
                // Caso padrão: verificar se a nota é válida
                // Verificar se é uma nota com modificador (do#, reb)
                const notePattern = /^([a-zA-Z]+)([#b])?$/;
                const noteMatch = notePattern.exec(parts[1]);
                
                if (noteMatch) {
                    noteValid = VALID_NOTES.includes(noteMatch[1]);
                } else {
                    // Pode ser um nome de variável ou acorde, não validamos aqui
                    noteValid = true;
                }
                
                // Verificar se a duração é válida ou se parece um parâmetro de função
                durationValid = VALID_DURATIONS.includes(parts[2]) || isProbablyFunctionParameter(parts[2]);
                
                if (!durationValid) {
                    diagnostics.push(createDiagnostic(
                        document,
                        lineIndex, line.indexOf(parts[2]), lineIndex, line.indexOf(parts[2]) + parts[2].length,
                        `Duração inválida: '${parts[2]}'. Valores válidos: ${VALID_DURATIONS.join(', ')}`,
                        vscode.DiagnosticSeverity.Error
                    ));
                }
            }
        } else {
            diagnostics.push(createDiagnostic(
                document,
                lineIndex, 0, lineIndex, lineWithoutComments.length,
                `Comando 'tocar' incompleto. Uso: 'tocar nota duração;' ou 'tocar acorde duração;'`,
                vscode.DiagnosticSeverity.Error
            ));
        }
    }
    
    // Verificar comando 'pausa' com parâmetros inválidos
    else if (lineWithoutComments.startsWith('pausa ')) {
        const parts = lineWithoutComments.replace(/;$/, '').split(/\s+/);
        
        // Verificar se o comando tem pelo menos 2 partes: 'pausa' e duração
        if (parts.length >= 2) {
            const durationValid = VALID_DURATIONS.includes(parts[1]) || isProbablyFunctionParameter(parts[1]);
            if (!durationValid) {
                diagnostics.push(createDiagnostic(
                    document,
                    lineIndex, line.indexOf(parts[1]), lineIndex, line.indexOf(parts[1]) + parts[1].length,
                    `Duração inválida: '${parts[1]}'. Valores válidos: ${VALID_DURATIONS.join(', ')}`,
                    vscode.DiagnosticSeverity.Error
                ));
            }
        } else {
            diagnostics.push(createDiagnostic(
                document,
                lineIndex, 0, lineIndex, lineWithoutComments.length,
                `Comando 'pausa' incompleto. Uso: 'pausa duração;'`,
                vscode.DiagnosticSeverity.Error
            ));
        }
    }
    
    // Verificar comando 'forma_onda' com valores inválidos
    else if (lineWithoutComments.startsWith('forma_onda ')) {
        const parts = lineWithoutComments.replace(/;$/, '').split(/\s+/);
        
        // Verificar se o comando tem pelo menos 2 partes e o valor é válido
        if (parts.length >= 2 && !VALID_WAVEFORMS.includes(parts[1])) {
            diagnostics.push(createDiagnostic(
                document,
                lineIndex, line.indexOf(parts[1]), lineIndex, line.indexOf(parts[1]) + parts[1].length,
                `Forma de onda inválida: '${parts[1]}'. Valores válidos: ${VALID_WAVEFORMS.join(', ')}`,
                vscode.DiagnosticSeverity.Error
            ));
        }
    }
}

/**
 * Cria um objeto de diagnóstico para o VS Code
 */
function createDiagnostic(
    document: vscode.TextDocument,
    startLine: number, 
    startChar: number, 
    endLine: number, 
    endChar: number, 
    message: string, 
    severity: vscode.DiagnosticSeverity
): vscode.Diagnostic {
    const range = new vscode.Range(
        new vscode.Position(startLine, startChar),
        new vscode.Position(endLine, endChar)
    );
    
    const diagnostic = new vscode.Diagnostic(range, message, severity);
    diagnostic.source = 'MelodyScript';
    return diagnostic;
}

/**
 * Obtém o caminho para o script Python principal
 */
function getScriptPath(workspacePath: string): string {
    // Caminhos possíveis
    const possiblePaths = [
        path.join(workspacePath, 'src', 'melodyscript.py'),
        path.join(workspacePath, 'src', 'linter', 'cli.py')
    ];
    
    for (const scriptPath of possiblePaths) {
        if (fs.existsSync(scriptPath)) {
            return scriptPath;
        }
    }
    
    return '';
}

/**
 * Executa o interpretador MelodyScript para o arquivo
 */
function executeMelodyScript(filePath: string) {
    // Obter o diretório do workspace
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(vscode.Uri.file(filePath));
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Não foi possível determinar o diretório do workspace.');
        return;
    }

    // Criar terminal para execução
    const terminal = vscode.window.createTerminal('MelodyScript');
    terminal.show();

    // Usar o script run_melodyscript.sh/bat em vez de chamar Python diretamente
    // Determinar o sistema operacional para escolher o script correto
    const isWindows = os.platform() === 'win32';
    const scriptName = isWindows ? 'run_melodyscript.bat' : './run_melodyscript.sh';
    
    // Caminho para o arquivo
    const relativeFilePath = path.relative(workspaceFolder.uri.fsPath, filePath);
    
    // Executar o script com o comando "executar"
    // Usar sintaxe adequada para cada shell
    if (isWindows) {
        // Para Windows, usar ponto e vírgula em vez de && para compatibilidade com PowerShell
        terminal.sendText(`cd "${workspaceFolder.uri.fsPath}"; ${scriptName} executar "${relativeFilePath}"`);
    } else {
        // Para Linux/Mac, usar && como antes
    terminal.sendText(`cd "${workspaceFolder.uri.fsPath}" && ${scriptName} executar "${relativeFilePath}"`);
    }
}

/**
 * Valida o arquivo MelodyScript usando o backend Python
 */
function validateMelodyScript(document: vscode.TextDocument) {
    const filePath = document.fileName;
    
    // Obter o diretório do workspace
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(vscode.Uri.file(filePath));
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Não foi possível determinar o diretório do workspace.');
        return;
    }

    // Usar o novo linter modular
    const linterModulePath = path.join(workspaceFolder.uri.fsPath, 'src', 'linter');
    if (!fs.existsSync(linterModulePath)) {
        // Não exibir erro, já que isso pode ser apenas uma ativação inicial
        console.log('Módulo do linter não encontrado:', linterModulePath);
        return;
    }

    // Determinar o comando Python a ser usado
    const pythonCommand = os.platform() === 'win32' ? 'python' : 'python3';
    
    // Executar o linter modular como processo filho
    const linter = spawn(pythonCommand, ['-m', 'src.linter.cli', filePath], {
        cwd: workspaceFolder.uri.fsPath
    });
    
    let stdout = '';
    let stderr = '';
    
    linter.stdout.on('data', (data) => {
        stdout += data.toString();
    });
    
    linter.stderr.on('data', (data) => {
        stderr += data.toString();
    });
    
    linter.on('close', (code) => {
        const diagnostics: vscode.Diagnostic[] = [];
        
        if (code !== 0 || stderr) {
            // Processar erros/avisos retornados pelo linter
            const lines = stdout.split('\n');
            for (const line of lines) {
                // Formato esperado: "Linha X: Mensagem de erro"
                const match = /Linha\s+(\d+):\s+(.+)/.exec(line);
                if (match) {
                    const lineNumber = parseInt(match[1]) - 1;
                    const message = match[2];
                    
                    // Determinar severidade baseada na mensagem
                    const severity = line.includes('Erro') ? vscode.DiagnosticSeverity.Error : vscode.DiagnosticSeverity.Warning;
                    
                    // Criar diagnóstico para a linha inteira
                    const lineRange = new vscode.Range(
                        new vscode.Position(lineNumber, 0),
                        new vscode.Position(lineNumber, 1000) // Um valor grande para cobrir toda a linha
                    );
                    
                    const diagnostic = new vscode.Diagnostic(lineRange, message, severity);
                    diagnostic.source = 'MelodyScript';
                    diagnostics.push(diagnostic);
                }
                // Formato para erros globais: "Erro: Mensagem"
                else if (line.startsWith('Erro:')) {
                    const message = line.substring(5).trim();
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(0, 0, 0, 1),
                        message,
                        vscode.DiagnosticSeverity.Error
                    );
                    diagnostic.source = 'MelodyScript';
                    diagnostics.push(diagnostic);
                }
            }
            
            // Se houve erro no stderr, adicionar como diagnóstico global
            if (stderr) {
                const diagnostic = new vscode.Diagnostic(
                    new vscode.Range(0, 0, 0, 1),
                    `Erro do linter: ${stderr}`,
                    vscode.DiagnosticSeverity.Error
                );
                diagnostic.source = 'MelodyScript';
                diagnostics.push(diagnostic);
            }
        }
        
        // Atualizar diagnósticos no VS Code
        diagnosticCollection.set(document.uri, diagnostics);
    });
}

/**
 * Verifica se um nome é provavelmente um parâmetro de função
 */
function isProbablyFunctionParameter(param: string): boolean {
    // Palavras comuns usadas como parâmetros de função
    const commonParams = [
        'duracao', 'acorde', 'nota', 'tom', 'tempo', 'velocidade', 
        'parametro', 'valor', 'freq', 'frequencia', 'oitava',
        'tonalidade', 'volume', 'intensidade'
    ];
    
    // Se o nome está na lista, é provavelmente um parâmetro
    if (commonParams.includes(param)) {
        return true;
    }
    
    // Se o nome não é uma duração válida e não contém números,
    // provavelmente é um parâmetro passado
    if (!VALID_DURATIONS.includes(param) && !/\d/.test(param)) {
        return true;
    }
    
    return false;
}

export function deactivate() {
    // Limpar recursos ao desativar a extensão
    if (diagnosticCollection) {
        diagnosticCollection.clear();
        diagnosticCollection.dispose();
    }
} 