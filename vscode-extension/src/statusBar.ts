/**
 * Status Bar Manager - Manages VS Code status bar for ENHANCER
 */

import * as vscode from 'vscode';

export type StatusType = 'idle' | 'analyzing' | 'success' | 'error';

export class StatusBarManager {
    private statusBarItem: vscode.StatusBarItem;

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Left,
            100
        );
        this.statusBarItem.command = 'enhancer.analyzeFile';
        this.statusBarItem.tooltip = 'Click to analyze current file';
        this.statusBarItem.show();
        this.setStatus('idle', 'ENHANCER');
    }

    /**
     * Set status bar status
     */
    setStatus(type: StatusType, text: string): void {
        switch (type) {
            case 'idle':
                this.statusBarItem.text = `$(code) ${text}`;
                this.statusBarItem.backgroundColor = undefined;
                break;

            case 'analyzing':
                this.statusBarItem.text = `$(sync~spin) ${text}`;
                this.statusBarItem.backgroundColor = undefined;
                break;

            case 'success':
                this.statusBarItem.text = `$(check) ${text}`;
                this.statusBarItem.backgroundColor = undefined;
                break;

            case 'error':
                this.statusBarItem.text = `$(error) ${text}`;
                this.statusBarItem.backgroundColor = new vscode.ThemeColor(
                    'statusBarItem.errorBackground'
                );
                break;
        }
    }

    /**
     * Dispose status bar item
     */
    dispose(): void {
        this.statusBarItem.dispose();
    }
}
