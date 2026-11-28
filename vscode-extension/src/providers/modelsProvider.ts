/**
 * Models Tree View Provider
 */

import * as vscode from 'vscode';

export class ModelsProvider implements vscode.TreeDataProvider<ModelItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<ModelItem | undefined | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    constructor() {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: ModelItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: ModelItem): Promise<ModelItem[]> {
        if (element) {
            return [];
        }

        const config = vscode.workspace.getConfiguration('enhancer');
        const currentModel = config.get<string>('defaultModel', 'codestral:latest');

        // Get available models (would normally call analyzer.getAvailableModels())
        const models = [
            { name: 'enhancer-llama:latest', provider: 'ollama', recommended: ['code analysis'] },
            { name: 'codestral:latest', provider: 'ollama', recommended: ['quality', 'security'] },
            { name: 'qwen2.5-coder:latest', provider: 'ollama', recommended: ['code', 'performance'] },
            { name: 'deepseek-r1:latest', provider: 'ollama', recommended: ['reasoning'] },
            { name: 'phi4:latest', provider: 'ollama', recommended: ['speed'] },
            { name: 'command-r7b:latest', provider: 'ollama', recommended: ['quick analysis'] }
        ];

        return models.map(model => new ModelItem(
            model.name,
            model.provider,
            model.recommended,
            model.name === currentModel
        ));
    }
}

class ModelItem extends vscode.TreeItem {
    constructor(
        public readonly modelName: string,
        public readonly provider: string,
        public readonly recommended: string[],
        public readonly isActive: boolean
    ) {
        super(modelName, vscode.TreeItemCollapsibleState.None);

        this.description = provider;
        this.tooltip = `Provider: ${provider}\nRecommended for: ${recommended.join(', ')}`;
        this.iconPath = isActive
            ? new vscode.ThemeIcon('check', new vscode.ThemeColor('charts.green'))
            : new vscode.ThemeIcon('circle-outline');
        this.contextValue = 'model';

        // Make clickable to select model
        this.command = {
            command: 'enhancer.selectModel',
            title: 'Select Model'
        };
    }
}
