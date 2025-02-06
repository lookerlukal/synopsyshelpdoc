// 在Cursor中按 Ctrl+Shift+P 执行以下命令
await vscode.commands.executeCommand('workbench.action.openSettingsJson');
// 在settings.json中添加：
{
    "cursor.doc.extraDocs" [
        {
            "name": "光学手册",
            "root": "/path/to/your/index.html",
            "patterns": ["**/*.html"]
        }
    ]
} 