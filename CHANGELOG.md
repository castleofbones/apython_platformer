# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Game Engine**: Basic `Game` class loop with `update`, `draw`, and `events` methods.
- **Player**: `Player` class with physics (gravity, acceleration, friction).
    - Horizontal movement with arrow keys.
    - Jumping mechanics.
- **World**: `Platform` class and basic platform collision detection.
- **Documentation**:
    - `README.md` with installation and control instructions.
    - `CHANGELOG.md` to track project history.
- **Setup**:
    - Project structure (venv, requirements.txt).
    - Git repository initialization.
    - GitHub Actions (planned/setup).
- **UI**: Added Start Screen and Game Over Screen with 2-second delay protection.
- **Assets**: Added game logo with fade-in animation.
- **Assets**: Updated font to 'Cascadia Code'.
- **Mechanics**: Added moving platforms with configurable speed boundaries.

### Changed
- **Controls**: Pressing 'Q' during gameplay triggers Game Over; pressing 'Q' on splash screens quits the application.
- **UI**: Game Over instructions now appear after the delay to prevent accidental restarts.
- **Refactor**: Moved game constants and configuration to `settings.py` (extracted `SCREEN_DELAY`).
- **Refactor**: Extracted `wait_for_duration` helper for consistent UI delays.
- **Dependencies**: Updated `pygame` to version 2.6.1 for Python 3.13 compatibility.
- **Docs**: Added docstrings and comments to `main.py` and `sprites.py`.
