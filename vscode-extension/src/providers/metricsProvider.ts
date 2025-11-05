/**
 * Metrics Tree View Provider
 */

import * as vscode from 'vscode';
import { CodeMetrics } from '../analyzer';

export class MetricsProvider implements vscode.TreeDataProvider<MetricItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<MetricItem | undefined | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    private metrics: CodeMetrics | null = null;

    constructor() {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    update(metrics: CodeMetrics): void {
        this.metrics = metrics;
        this.refresh();
    }

    clear(): void {
        this.metrics = null;
        this.refresh();
    }

    getTreeItem(element: MetricItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: MetricItem): Thenable<MetricItem[]> {
        if (!this.metrics) {
            return Promise.resolve([
                new MetricItem('No metrics available', '', 'info')
            ]);
        }

        if (element) {
            return Promise.resolve([]);
        }

        const items: MetricItem[] = [
            new MetricItem(
                'Total Lines',
                this.metrics.total_lines.toString(),
                'file'
            ),
            new MetricItem(
                'Code Lines',
                `${this.metrics.code_lines} (${this.percentage(this.metrics.code_lines, this.metrics.total_lines)}%)`,
                'code'
            ),
            new MetricItem(
                'Comment Lines',
                `${this.metrics.comment_lines} (${this.percentage(this.metrics.comment_lines, this.metrics.total_lines)}%)`,
                'comment'
            ),
            new MetricItem(
                'Docstring Lines',
                `${this.metrics.docstring_lines} (${this.percentage(this.metrics.docstring_lines, this.metrics.total_lines)}%)`,
                'book'
            ),
            new MetricItem(
                'Blank Lines',
                `${this.metrics.blank_lines} (${this.percentage(this.metrics.blank_lines, this.metrics.total_lines)}%)`,
                'whitespace'
            ),
            new MetricItem(
                'File Size',
                this.formatBytes(this.metrics.file_size),
                'database'
            )
        ];

        return Promise.resolve(items);
    }

    private percentage(value: number, total: number): string {
        if (total === 0) {
            return '0';
        }
        return ((value / total) * 100).toFixed(1);
    }

    private formatBytes(bytes: number): string {
        if (bytes < 1024) {
            return `${bytes} B`;
        }
        if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(2)} KB`;
        }
        return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
    }
}

class MetricItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly value: string,
        public readonly iconName: string
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);

        this.description = value;
        this.iconPath = new vscode.ThemeIcon(iconName);
        this.contextValue = 'metric';
    }
}
