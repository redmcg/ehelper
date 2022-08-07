def print_defaults(): 
    print("Default for Is is 1e-12A (a silicon diode)")
    print("Default for nVt is 26mV (approx 27°C with n = 1)")

def get_Is(argv, idx):
    if len(argv) > idx:
      Is = argv[idx]
    else:
      Is = "1e-12"
    return Is

def get_nVt(argv, idx):
    if len(argv) > idx: 
      nVt = argv[idx]
    else:
      nVt = .026
    return nVt

