/**
 * Diagnostics Manager - Manages VS Code diagnostics for ENHANCER
 */

import * as vscode from 'vscode';
import { AnalysisResult, Issue } from './analyzer';

export class DiagnosticsManager {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('enhancer');
    }

    /**
     * Update diagnostics for a file
     */
    updateDiagnostics(uri: vscode.Uri, results: AnalysisResult): void {
        const diagnostics: vscode.Diagnostic[] = [];

        // Add issues as diagnostics
        for (const issue of results.issues) {
            const diagnostic = this.issueToDiagnostic(issue);
            diagnostics.push(diagnostic);
        }

        // Add security warnings
        for (const warning of results.security_warnings) {
            const diagnostic = new vscode.Diagnostic(
                new vscode.Range(0, 0, 0, 0),
                `[Security] ${warning.message}`,
                this.severityToVSCodeSeverity(warning.severity)
            );
            diagnostic.source = 'ENHANCER';
            diagnostic.code = 'SEC001';
            diagnostics.push(diagnostic);
        }

        this.diagnosticCollection.set(uri, diagnostics);
    }

    /**
     * Convert Issue to VS Code Diagnostic
     */
    private issueToDiagnostic(issue: Issue): vscode.Diagnostic {
        const line = Math.max(0, issue.line - 1);  // VS Code lines are 0-indexed
        const column = Math.max(0, issue.column);
        const range = new vscode.Range(line, column, line, column + 100);

        const diagnostic = new vscode.Diagnostic(
            range,
            issue.message,
            this.severityToVSCodeSeverity(issue.severity)
        );

        diagnostic.source = 'ENHANCER';
        diagnostic.code = issue.code || `${issue.type.toUpperCase()}001`;

        // Add tags
        if (issue.severity === 'critical' || issue.severity === 'high') {
            diagnostic.tags = [vscode.DiagnosticTag.Deprecated];
        }

        return diagnostic;
    }

    /**
     * Convert severity string to VS Code severity
     */
    private severityToVSCodeSeverity(severity: string): vscode.DiagnosticSeverity {
        switch (severity.toLowerCase()) {
            case 'critical':
            case 'high':
                return vscode.DiagnosticSeverity.Error;
            case 'medium':
                return vscode.DiagnosticSeverity.Warning;
            case 'low':
                return vscode.DiagnosticSeverity.Information;
            default:
                return vscode.DiagnosticSeverity.Hint;
        }
    }

    /**
     * Clear all diagnostics
     */
    clear(): void {
        this.diagnosticCollection.clear();
    }

    /**
     * Dispose diagnostics collection
     */
    dispose(): void {
        this.diagnosticCollection.dispose();
    }
}
