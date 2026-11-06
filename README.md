# Subtitle Sync Studio

Shift SRT subtitle timing with a live text preview and explicit export.

[![Build and verify](https://github.com/netcodermike/subtitle-sync-studio/actions/workflows/verify.yml/badge.svg)](https://github.com/netcodermike/subtitle-sync-studio/actions/workflows/verify.yml)

**Language:** Python · **Platform:** Windows, macOS, Linux desktop · **App type:** Desktop subtitle timing adjustment editor

First-release learning implementation, with explicit scope below. This is one independently runnable app, not a placeholder in a combined repository.

## Features

- UTF-8 SRT import
- Positive/negative millisecond offsets
- Zero-clamped timestamps
- Preserved multiline cue text

## Requirements

Python 3.11+ with Tkinter; no pip packages.

## Quick start

```sh
git clone https://github.com/netcodermike/subtitle-sync-studio.git
cd subtitle-sync-studio
python app.py
```

Commands run from the repository root. Lines marked for a particular operating system apply only there. Language tools are prerequisites, not installed by the app. Close desktop windows normally; terminal/server apps stop with Ctrl+C unless their usage notes say otherwise.

## Example workflow

Open a small SRT, enter 500 to delay all cues, then -2000 to move them earlier. Export to a fresh file and compare cue text.

## Architecture, configuration, and data

app.py parses numbered SRT blocks into millisecond tuples. A Tkinter form previews a global offset and exports renumbered UTF-8 cues. Self-tests cover round trips, crossing zero, timestamp formatting, and invalid input. No persistent preferences or network calls.

## Verification

Build with the quick-start command where needed, then run:

```sh
python app.py --self-test
```

Manual acceptance: Open a small SRT, enter 500 to delay all cues, then -2000 to move them earlier. Export to a fresh file and compare cue text. Also test malformed inputs and an unwritable output destination.

See [validation record](docs/VALIDATION.md) for observed checks and their limits. CI results verify only what the workflow runs; they do not establish native GUI correctness or production readiness.

## Limitations and next steps

SRT subset only: no timing settings, video playback, frame-based offsets, individual cue edits, encoding detection, or automatic sync. Earlier-than-zero start/end times clamp independently, so durations near zero can shrink. Preview is display-only; export derives from parsed originals. Files are read in memory. Export can replace a chosen file.

## Troubleshooting

Use the exact platform/toolchain above. Preserve originals and use synthetic fixtures first. Errors are displayed in the UI or stderr. A headless machine can run the model tests but cannot verify native GUI/audio behavior. Output paths are chosen explicitly; keep backups of important data.

## Source map

- `app.py`

## Development and license

Read [contributing](CONTRIBUTING.md) before changing the app, and [security/privacy](SECURITY.md) before supplying private data. Use synthetic fixtures for tests. No telemetry, paid API key, or account is required by the app itself. Dependencies, when present, are stated in Requirements.

[MIT license](LICENSE), copyright 2026 netcodermike.
