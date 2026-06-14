# modelscan PyTorch Bypass PoC

## Summary

Demonstrates that `modelscan` (<= 0.8.5) can be bypassed by malicious `.pt` (PyTorch) files because:
1. The .pt format is essentially a ZIP archive containing pickle data
2. When the pickle is built using the marshal+types+base64 chain, it evades modelscan's `unsafe_globals` blacklist
3. `torch.load()` triggers the pickle deserialization, executing the embedded payload

## Affected

- modelscan <= 0.8.5
- PyTorch >= 1.0
- torch.load() with default weights_only=False (the historical default)

## Reproduction

```bash
pip install modelscan torch

# Step 1: scan reports "No issues" (BYPASSED)
modelscan scan -p rce.pt

# Step 2: loading the file executes arbitrary code
python -c "import torch; torch.load('rce.pt')"
# Check: cat pwned_p4.txt  ->  PWNED_P4
```

## Attack Chain

1. Attacker creates a malicious `.pt` file (ZIP containing pickle)
2. The inner pickle uses `types.FunctionType(marshal.loads(base64.b64decode(\"...\")), {})()` as its `__reduce__` target
3. `types`, `marshal`, and `base64` are NOT in modelscan's blacklist
4. When `torch.load()` deserializes the file, the chain executes
5. Result: arbitrary code execution on the host

## Files

- `rce.pt` — Malicious PyTorch PoC file (raw pickle with .pt extension)
- `rce_pt.py` — Generator script
- `README.md` — This file

## Workaround (for users)

Until a fix is released, set `weights_only=True` when calling `torch.load()` (PyTorch 1.13+):

```python
import torch
torch.load('model.pt', weights_only=True)  # refuses arbitrary pickle
```

## Disclosure

- Discovered by: jasonmiao0511-hue
- Reported via: huntr.com Model Format Vulnerability Form
- Date: 2026-06-15
- Related: see also [modelscan-pickle-bypass-poc](https://github.com/jasonmiao0511-hue/modelscan-pickle-bypass-poc) for the same root cause in pure .pkl format
