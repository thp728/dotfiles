# Portable Homebrew packages, applied on macOS and Linux by .chezmoiscripts/run_onchange_after_10-brew.sh.tmpl
# whenever this file changes. Work-only packages live in the work repo's Brewfile.work.
# Ghostty, Cursor, VS Code, Docker Desktop and T3 Code are installed from their own sites and
# update themselves, so they're left out here.

# Shell
brew "atuin"
brew "fzf"
brew "fzf-tab"
brew "starship"
brew "zoxide"
brew "zsh-autosuggestions"
brew "zsh-fast-syntax-highlighting"

# Command-line tools
brew "bat"
brew "btop"
brew "eza"
brew "fastfetch"
brew "fd"
brew "ripgrep"

# Development
brew "chezmoi"
brew "gh"
brew "git"
brew "gitleaks"
brew "mise"
brew "uv"
cask "codex" if OS.mac?
# Linux machines are personal ones.
cask "claude-code" if OS.linux?
brew "opencode" if OS.linux?

# Desktop, macOS only
if OS.mac?
  cask "alt-tab"
  cask "font-jetbrains-mono-nerd-font"
  cask "mac-mouse-fix"
  cask "rectangle"
end
