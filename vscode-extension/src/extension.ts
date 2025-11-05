/**
 * ENHANCER VS Code Extension
 *
 * Provides real-time AI-powered code analysis directly in VS Code.
 */

import * as vscode from 'vscode';
import { EnhancerAnalyzer } from './analyzer';
import { ResultsProvider } from './providers/resultsProvider';
import { ModelsProvider } from './providers/modelsProvider';
import { MetricsProvider } from './providers/metricsProvider';
import { DiagnosticsManager } from './diagnostics';
import { StatusBarManager } from './statusBar';

let analyzer: EnhancerAnalyzer;
let diagnosticsManager: DiagnosticsManager;
let statusBarManager: StatusBarManager;
let resultsProvider: ResultsProvider;
let modelsProvider: ModelsProvider;
let metricsProvider: MetricsProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('ENHANCER Code Intelligence is now active!');

    // Initialize core components
    analyzer = new EnhancerAnalyzer();
    diagnosticsManager = new DiagnosticsManager();
    statusBarManager = new StatusBarManager();

    // Initialize sidebar providers
    resultsProvider = new ResultsProvider();
    modelsProvider = new ModelsProvider();
    metricsProvider = new MetricsProvider();

    // Register tree views
    vscode.window.registerTreeDataProvider('enhancerResults', resultsProvider);
    vscode.window.registerTreeDataProvider('enhancerModels', modelsProvider);
    vscode.window.registerTreeDataProvider('enhancerMetrics', metricsProvider);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('enhancer.analyzeFile', analyzeCurrentFile),
        vscode.commands.registerCommand('enhancer.analyzeWorkspace', analyzeWorkspace),
        vscode.commands.registerCommand('enhancer.showSuggestions', showSuggestions),
        vscode.commands.registerCommand('enhancer.selectModel', selectModel),
        vscode.commands.registerCommand('enhancer.exportReport', exportReport),
        vscode.commands.registerCommand('enhancer.clearDiagnostics', clearDiagnostics)
    );

    // Register document change listeners for real-time analysis
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(onDocumentChange),
        vscode.workspace.onDidSaveTextDocument(onDocumentSave),
        vscode.window.onDidChangeActiveTextEditor(onEditorChange)
    );

    // Add status bar and diagnostics to subscriptions
    context.subscriptions.push(statusBarManager, diagnosticsManager);

    // Analyze current file on activation if it's Python
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.languageId === 'python') {
        analyzeCurrentFile();
    }

    vscode.window.showInformationMessage('ENHANCER Code Intelligence activated! 🚀');
}

export function deactivate() {
    console.log('ENHANCER Code Intelligence deactivated');
}

/**
 * Analyze the currently active file
 */
async function analyzeCurrentFile() {
    const editor = vscode.window.activeTextEditor;

    if (!editor) {
        vscode.window.showWarningMessage('No active editor found');
        return;
    }

    if (editor.document.languageId !== 'python') {
        vscode.window.showWarningMessage('ENHANCER only supports Python files');
        return;
    }

    const document = editor.document;
    const config = vscode.workspace.getConfiguration('enhancer');
    const maxFileSize = config.get<number>('maxFileSize', 10485760);

    // Check file size
    const text = document.getText();
    if (text.length > maxFileSize) {
        vscode.window.showWarningMessage(
            `File too large (${(text.length / 1024 / 1024).toFixed(2)} MB). ` +
            `Max size: ${(maxFileSize / 1024 / 1024).toFixed(2)} MB`
        );
        return;
    }

    statusBarManager.setStatus('analyzing', 'Analyzing...');

    try {
        // Run analysis
        const results = await analyzer.analyzeFile(document.uri.fsPath, text);

        // Update UI
        diagnosticsManager.updateDiagnostics(document.uri, results);
        resultsProvider.update(results);
        metricsProvider.update(results.metrics);
        statusBarManager.setStatus('success', `✓ ${results.issues.length} issues found`);

        // Show notification for critical issues
        const criticalIssues = results.issues.filter(i => i.severity === 'critical');
        if (criticalIssues.length > 0) {
            vscode.window.showWarningMessage(
                `⚠️ Found ${criticalIssues.length} critical issue(s)`,
                'View Details'
            ).then(selection => {
                if (selection === 'View Details') {
                    vscode.commands.executeCommand('workbench.view.extension.enhancer-sidebar');
                }
            });
        }

    } catch (error) {
        statusBarManager.setStatus('error', '✗ Analysis failed');
        vscode.window.showErrorMessage(`Analysis failed: ${error}`);
        console.error('Analysis error:', error);
    }
}

/**
 * Analyze entire workspace
 */
async function analyzeWorkspace() {
    const workspaceFolders = vscode.workspace.workspaceFolders;

    if (!workspaceFolders) {
        vscode.window.showWarningMessage('No workspace folder open');
        return;
    }

    const files = await vscode.workspace.findFiles('**/*.py', '**/node_modules/**');

    if (files.length === 0) {
        vscode.window.showInformationMessage('No Python files found in workspace');
        return;
    }

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "ENHANCER: Analyzing workspace",
        cancellable: true
    }, async (progress, token) => {
        let analyzed = 0;
        const total = files.length;

        for (const file of files) {
            if (token.isCancellationRequested) {
                break;
            }

            try {
                const document = await vscode.workspace.openTextDocument(file);
                const results = await analyzer.analyzeFile(file.fsPath, document.getText());
                diagnosticsManager.updateDiagnostics(file, results);

                analyzed++;
                progress.report({
                    increment: (100 / total),
                    message: `${analyzed}/${total} files`
                });
            } catch (error) {
                console.error(`Failed to analyze ${file.fsPath}:`, error);
            }
        }

        vscode.window.showInformationMessage(
            `✓ Analyzed ${analyzed} Python file(s)`
        );
    });
}

/**
 * Show improvement suggestions for current file
 */
async function showSuggestions() {
    const editor = vscode.window.activeTextEditor;

    if (!editor || editor.document.languageId !== 'python') {
        vscode.window.showWarningMessage('Open a Python file to see suggestions');
        return;
    }

    statusBarManager.setStatus('analyzing', 'Generating suggestions...');

    try {
        const suggestions = await analyzer.getSuggestions(
            editor.document.uri.fsPath,
            editor.document.getText()
        );

        // Create webview panel to show suggestions
        const panel = vscode.window.createWebviewPanel(
            'enhancerSuggestions',
            'ENHANCER: Code Suggestions',
            vscode.ViewColumn.Beside,
            { enableScripts: true }
        );

        panel.webview.html = getSuggestionsHtml(suggestions);
        statusBarManager.setStatus('success', '✓ Suggestions ready');

    } catch (error) {
        statusBarManager.setStatus('error', '✗ Failed to generate suggestions');
        vscode.window.showErrorMessage(`Failed to generate suggestions: ${error}`);
    }
}

/**
 * Select AI model for analysis
 */
async function selectModel() {
    const models = await analyzer.getAvailableModels();
    const config = vscode.workspace.getConfiguration('enhancer');
    const currentModel = config.get<string>('defaultModel');

    const quickPick = vscode.window.createQuickPick();
    quickPick.title = 'Select AI Model';
    quickPick.placeholder = 'Choose a model for code analysis';
    quickPick.items = models.map(model => ({
        label: model.name,
        description: model.provider,
        detail: model.recommended_for?.join(', '),
        picked: model.name === currentModel
    }));

    quickPick.onDidChangeSelection(async ([item]) => {
        if (item) {
            await config.update('defaultModel', item.label, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`✓ Model changed to: ${item.label}`);
            modelsProvider.refresh();
            quickPick.dispose();
        }
    });

    quickPick.show();
}

/**
 * Export analysis report
 */
async function exportReport() {
    const options: vscode.SaveDialogOptions = {
        filters: {
            'JSON': ['json'],
            'Text': ['txt'],
            'All Files': ['*']
        },
        defaultUri: vscode.Uri.file('enhancer-report.json')
    };

    const uri = await vscode.window.showSaveDialog(options);

    if (uri) {
        try {
            const results = resultsProvider.getResults();
            const content = JSON.stringify(results, null, 2);
            await vscode.workspace.fs.writeFile(uri, Buffer.from(content, 'utf8'));
            vscode.window.showInformationMessage(`✓ Report exported to ${uri.fsPath}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to export report: ${error}`);
        }
    }
}

/**
 * Clear all diagnostics
 */
function clearDiagnostics() {
    diagnosticsManager.clear();
    resultsProvider.clear();
    metricsProvider.clear();
    statusBarManager.setStatus('idle', 'ENHANCER');
    vscode.window.showInformationMessage('✓ Diagnostics cleared');
}

/**
 * Handle document changes (real-time analysis)
 */
let changeTimeout: NodeJS.Timeout | undefined;
function onDocumentChange(event: vscode.TextDocumentChangeEvent) {
    const config = vscode.workspace.getConfiguration('enhancer');
    const enabled = config.get<boolean>('enableRealTimeAnalysis', true);
    const delay = config.get<number>('analysisDelay', 1000);

    if (!enabled || event.document.languageId !== 'python') {
        return;
    }

    // Debounce: only analyze after user stops typing
    if (changeTimeout) {
        clearTimeout(changeTimeout);
    }

    changeTimeout = setTimeout(() => {
        analyzeCurrentFile();
    }, delay);
}

/**
 * Handle document save
 */
function onDocumentSave(document: vscode.TextDocument) {
    if (document.languageId === 'python') {
        analyzeCurrentFile();
    }
}

/**
 * Handle active editor change
 */
function onEditorChange(editor: vscode.TextEditor | undefined) {
    if (editor && editor.document.languageId === 'python') {
        analyzeCurrentFile();
    }
}

/**
 * Generate HTML for suggestions webview
 */
function getSuggestionsHtml(suggestions: any): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Suggestions</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            padding: 20px;
            color: var(--vscode-editor-foreground);
            background: var(--vscode-editor-background);
        }
        h1 { color: var(--vscode-textLink-foreground); }
        .suggestion {
            margin: 20px 0;
            padding: 15px;
            background: var(--vscode-editor-inactiveSelectionBackground);
            border-left: 3px solid var(--vscode-textLink-foreground);
            border-radius: 4px;
        }
        .suggestion h3 { margin-top: 0; }
        code {
            background: var(--vscode-textCodeBlock-background);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: var(--vscode-editor-font-family);
        }
        pre {
            background: var(--vscode-textCodeBlock-background);
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>💡 Code Improvement Suggestions</h1>
    <div class="suggestions-container">
        ${suggestions.analysis || 'No suggestions available.'}
    </div>
</body>
</html>`;
}
