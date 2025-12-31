import torch

if torch.backends.mps.is_available():
    print("✅ MPS is available! Your M2 GPU is ready for AI.")
else:
    print("❌ MPS not available. We may need to update your torch version.")

if torch.backends.mps.is_built():
    print("✅ PyTorch was built with MPS support.")