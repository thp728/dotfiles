# Markdown reading width

A VS Code extension that centers the built-in Markdown preview at 860 px. It isn't published, so
build it and install the package by hand:

```sh
cd ~/repos/dotfiles/themes/markdown-reading-width
npx @vscode/vsce package --allow-missing-repository --skip-license -o /tmp/markdown-reading-width.vsix
code --install-extension /tmp/markdown-reading-width.vsix
```

Rebuild after changing `preview.css` or `package.json`, and bump `version` so VS Code takes the new
package.
