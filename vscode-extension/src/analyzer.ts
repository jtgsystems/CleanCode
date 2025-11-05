/**
 * Analyzer - Communicates with Python ENHANCER backend
 */

import { spawn } from 'child_process';
import * as vscode from 'vscode';
import * as path from 'path';

export interface AnalysisResult {
    file: string;
    issues: Issue[];
    metrics: CodeMetrics;
    security_warnings: SecurityWarning[];
    ai_analysis?: any;
}

export interface Issue {
    line: number;
    column: number;
    severity: 'critical' | 'high' | 'medium' | 'low';
    type: 'security' | 'performance' | 'quality' | 'style';
    message: string;
    code?: string;
}

export interface CodeMetrics {
    total_lines: number;
    code_lines: number;
    comment_lines: number;
    blank_lines: number;
    docstring_lines: number;
    file_size: number;
}

export interface SecurityWarning {
    type: string;
    severity: string;
    pattern: string;
    message: string;
}

export interface ModelInfo {
    name: string;
    provider: string;
    requires_api_key: boolean;
    recommended_for?: string[];
}

export class EnhancerAnalyzer {
    private pythonPath: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('enhancer');
        this.pythonPath = config.get<string>('pythonPath', 'python');
    }

    /**
     * Analyze a Python file
     */
    async analyzeFile(filePath: string, content: string): Promise<AnalysisResult> {
        return new Promise((resolve, reject) => {
            // Create temporary file with content
            const tempFile = path.join(require('os').tmpdir(), `enhancer_${Date.now()}.py`);
            require('fs').writeFileSync(tempFile, content);

            const config = vscode.workspace.getConfiguration('enhancer');
            const model = config.get<string>('defaultModel');
            const enableSecurity = config.get<boolean>('enableSecurityScanning', true);
            const enablePerformance = config.get<boolean>('enablePerformanceAnalysis', true);

            // Build analysis command
            const args = [
                '-m', 'ENHANCER.cli',
                'analyze',
                tempFile
            ];

            if (model) {
                args.push('--model', model);
            }

            // Execute Python ENHANCER CLI
            const process = spawn(this.pythonPath, args);

            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            process.on('close', (code) => {
                // Clean up temp file
                try {
                    require('fs').unlinkSync(tempFile);
                } catch (e) {
                    console.error('Failed to delete temp file:', e);
                }

                if (code !== 0) {
                    reject(new Error(stderr || 'Analysis failed'));
                    return;
                }

                try {
                    // Parse analysis output
                    const result = this.parseAnalysisOutput(stdout, filePath);
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
            });

            process.on('error', (error) => {
                reject(new Error(`Failed to start Python: ${error.message}`));
            });
        });
    }

    /**
     * Get improvement suggestions
     */
    async getSuggestions(filePath: string, content: string): Promise<any> {
        return new Promise((resolve, reject) => {
            const tempFile = path.join(require('os').tmpdir(), `enhancer_${Date.now()}.py`);
            require('fs').writeFileSync(tempFile, content);

            const config = vscode.workspace.getConfiguration('enhancer');
            const model = config.get<string>('defaultModel');

            const args = [
                '-m', 'ENHANCER.cli',
                'suggest',
                tempFile
            ];

            if (model) {
                args.push('--model', model);
            }

            const process = spawn(this.pythonPath, args);

            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            process.on('close', (code) => {
                try {
                    require('fs').unlinkSync(tempFile);
                } catch (e) {
                    console.error('Failed to delete temp file:', e);
                }

                if (code !== 0) {
                    reject(new Error(stderr || 'Failed to generate suggestions'));
                    return;
                }

                resolve({ analysis: stdout });
            });

            process.on('error', (error) => {
                reject(new Error(`Failed to start Python: ${error.message}`));
            });
        });
    }

    /**
     * Get available AI models
     */
    async getAvailableModels(): Promise<ModelInfo[]> {
        return new Promise((resolve, reject) => {
            const process = spawn(this.pythonPath, [
                '-m', 'ENHANCER.cli',
                'models'
            ]);

            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            process.on('close', (code) => {
                if (code !== 0) {
                    reject(new Error(stderr || 'Failed to get models'));
                    return;
                }

                try {
                    const models = this.parseModelsOutput(stdout);
                    resolve(models);
                } catch (error) {
                    reject(error);
                }
            });

            process.on('error', (error) => {
                reject(new Error(`Failed to start Python: ${error.message}`));
            });
        });
    }

    /**
     * Parse analysis output from ENHANCER CLI
     */
    private parseAnalysisOutput(output: string, filePath: string): AnalysisResult {
        // Extract metrics from output
        const metrics: CodeMetrics = {
            total_lines: this.extractNumber(output, /total_lines:\s*(\d+)/) || 0,
            code_lines: this.extractNumber(output, /code_lines:\s*(\d+)/) || 0,
            comment_lines: this.extractNumber(output, /comment_lines:\s*(\d+)/) || 0,
            blank_lines: this.extractNumber(output, /blank_lines:\s*(\d+)/) || 0,
            docstring_lines: this.extractNumber(output, /docstring_lines:\s*(\d+)/) || 0,
            file_size: this.extractNumber(output, /file_size:\s*(\d+)/) || 0
        };

        // Extract security warnings
        const security_warnings: SecurityWarning[] = [];
        const securityMatches = output.matchAll(/\[(\w+)\]\s*(.+)/g);
        for (const match of securityMatches) {
            security_warnings.push({
                type: 'security',
                severity: match[1].toLowerCase(),
                pattern: '',
                message: match[2]
            });
        }

        // Extract issues
        const issues: Issue[] = security_warnings.map((warning, index) => ({
            line: 1,  // Default to line 1, would need better parsing
            column: 0,
            severity: warning.severity as any,
            type: 'security',
            message: warning.message,
            code: `ENHANCER${index + 1}`
        }));

        return {
            file: filePath,
            issues,
            metrics,
            security_warnings
        };
    }

    /**
     * Parse models output
     */
    private parseModelsOutput(output: string): ModelInfo[] {
        const models: ModelInfo[] = [];
        const lines = output.split('\n');

        let currentProvider = '';
        for (const line of lines) {
            const trimmed = line.trim();

            // Check for provider header (e.g., "OLLAMA:")
            if (trimmed.endsWith(':') && trimmed.length < 20) {
                currentProvider = trimmed.slice(0, -1).toLowerCase();
                continue;
            }

            // Check for model entry (e.g., "- model-name:latest")
            if (trimmed.startsWith('-')) {
                const modelName = trimmed.substring(1).trim();
                models.push({
                    name: modelName,
                    provider: currentProvider,
                    requires_api_key: currentProvider !== 'ollama',
                    recommended_for: this.getRecommendations(modelName)
                });
            }
        }

        return models;
    }

    /**
     * Get recommendations for a model
     */
    private getRecommendations(modelName: string): string[] {
        if (modelName.includes('coder') || modelName.includes('code')) {
            return ['code analysis', 'quality', 'security'];
        }
        if (modelName.includes('deepseek-r1')) {
            return ['reasoning', 'complex analysis'];
        }
        if (modelName.includes('phi') || modelName.includes('command-r7b')) {
            return ['speed', 'quick analysis'];
        }
        return ['general'];
    }

    /**
     * Extract number from regex match
     */
    private extractNumber(text: string, regex: RegExp): number | null {
        const match = text.match(regex);
        return match ? parseInt(match[1], 10) : null;
    }
}
