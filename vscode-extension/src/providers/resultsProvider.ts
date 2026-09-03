/**
 * Results Tree View Provider
 */

import * as vscode from 'vscode';
import { AnalysisResult, Issue } from '../analyzer';

export class ResultsProvider implements vscode.TreeDataProvider<ResultItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<ResultItem | undefined | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    private results: AnalysisResult | null = null;

    constructor() {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    update(results: AnalysisResult): void {
        this.results = results;
        this.refresh();
    }

    clear(): void {
        this.results = null;
        this.refresh();
    }

    getResults(): AnalysisResult | null {
        return this.results;
    }

    getTreeItem(element: ResultItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: ResultItem): Thenable<ResultItem[]> {
        if (!this.results) {
            return Promise.resolve([]);
        }

        if (!element) {
            // Root level: show categories
            const items: ResultItem[] = [];

            // Critical issues
            const criticalIssues = this.results.issues.filter(i => i.severity === 'critical');
            if (criticalIssues.length > 0) {
                items.push(new ResultItem(
                    `Critical Issues (${criticalIssues.length})`,
                    vscode.TreeItemCollapsibleState.Expanded,
                    'critical',
                    criticalIssues
                ));
            }

            // High severity issues
            const highIssues = this.results.issues.filter(i => i.severity === 'high');
            if (highIssues.length > 0) {
                items.push(new ResultItem(
                    `High Severity (${highIssues.length})`,
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'high',
                    highIssues
                ));
            }

            // Medium severity issues
            const mediumIssues = this.results.issues.filter(i => i.severity === 'medium');
            if (mediumIssues.length > 0) {
                items.push(new ResultItem(
                    `Medium Severity (${mediumIssues.length})`,
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'medium',
                    mediumIssues
                ));
            }

            // Low severity issues
            const lowIssues = this.results.issues.filter(i => i.severity === 'low');
            if (lowIssues.length > 0) {
                items.push(new ResultItem(
                    `Low Severity (${lowIssues.length})`,
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'low',
                    lowIssues
                ));
            }

            // Security warnings
            if (this.results.security_warnings.length > 0) {
                items.push(new ResultItem(
                    `Security Warnings (${this.results.security_warnings.length})`,
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'security',
                    []
                ));
            }

            if (items.length === 0) {
                return Promise.resolve([
                    new ResultItem(
                        '✓ No issues found',
                        vscode.TreeItemCollapsibleState.None,
                        'none',
                        []
                    )
                ]);
            }

            return Promise.resolve(items);
        } else {
            // Show individual issues
            if (element.issues.length > 0) {
                return Promise.resolve(
                    element.issues.map(issue => new IssueItem(issue))
                );
            }
            return Promise.resolve([]);
        }
    }
}

class ResultItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly severity: string,
        public readonly issues: Issue[]
    ) {
        super(label, collapsibleState);

        this.iconPath = this.getIcon(severity);
        this.contextValue = 'resultCategory';
    }

    private getIcon(severity: string): vscode.ThemeIcon {
        switch (severity) {
            case 'critical':
                return new vscode.ThemeIcon('error', new vscode.ThemeColor('errorForeground'));
            case 'high':
                return new vscode.ThemeIcon('warning', new vscode.ThemeColor('editorWarning.foreground'));
            case 'medium':
                return new vscode.ThemeIcon('info', new vscode.ThemeColor('editorInfo.foreground'));
            case 'low':
                return new vscode.ThemeIcon('lightbulb');
            case 'security':
                return new vscode.ThemeIcon('shield');
            case 'none':
                return new vscode.ThemeIcon('pass');
            default:
                return new vscode.ThemeIcon('circle-outline');
        }
    }
}

class IssueItem extends vscode.TreeItem {
    constructor(public readonly issue: Issue) {
        super(issue.message, vscode.TreeItemCollapsibleState.None);

        this.description = `Line ${issue.line}`;
        this.tooltip = `${issue.type} - ${issue.message}\nLine: ${issue.line}, Column: ${issue.column}`;
        this.iconPath = new vscode.ThemeIcon('file');
        this.contextValue = 'issue';

        // Make it clickable to jump to the issue location
        this.command = {
            command: 'vscode.open',
            title: 'Go to Issue',
            arguments: [
                vscode.window.activeTextEditor?.document.uri,
                {
                    selection: new vscode.Range(
                        issue.line - 1,
                        issue.column,
                        issue.line - 1,
                        issue.column
                    )
                }
            ]
        };
    }
}
