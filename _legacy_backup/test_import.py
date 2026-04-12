try:
    from fer.fer import FER
    print("Imported from fer.fer")
except ImportError:
    print("Failed to import from fer.fer")

try:
    from fer import FER
    print("Imported from fer")
except ImportError:
    print("Failed to import from fer")
