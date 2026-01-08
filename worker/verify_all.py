import os
import ast
import sys

def check_syntax(directory):
    errors = []
    print(f"Checking directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                print(f"  Scanning: {path}")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    print(f"  ❌ Syntax Error in {path}")
                    errors.append(f"Syntax Error in {path}: {e}")
                except Exception as e:
                    print(f"  ❌ Error reading {path}")
                    errors.append(f"Error reading {path}: {e}")
    return errors

def check_imports():
    try:
        print("Checking imports...")
        # Add current directory to path so we can import 'worker.hydra_controller'
        sys.path.append(os.getcwd())
        
        print("1. Importing worker.hydra_controller...")
        # We use __import__ to avoid issues with static analysis
        # import worker.hydra_controller
        __import__('worker.hydra_controller')
        print("✅ HydraController imported successfully!")
        
        return []
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return [f"Import Error: {e}"]

if __name__ == "__main__":
    print("STARTING WORKER AUDIT")
    
    print("\n[PHASE 1] Syntax Check")
    syntax_errors = check_syntax('worker')
    
    print("\n[PHASE 2] Import Check")
    import_errors = check_imports()

    print("\n[SUMMARY]")
    if not syntax_errors and not import_errors:
        print("✅ ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print(f"❌ {len(syntax_errors)} Syntax Errors found")
        print(f"❌ {len(import_errors)} Import Errors found")
        sys.exit(1)
