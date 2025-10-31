#!/usr/bin/env python3
"""
Validation script for Bhaskar Daily AI News setup
Checks configuration, dependencies, and API connectivity
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment variables...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ❌ GEMINI_API_KEY not set")
        print("     Run: export GEMINI_API_KEY='your-key-here'")
        return False
    elif api_key.startswith("AIza"):
        print(f"  ✅ GEMINI_API_KEY is set (length: {len(api_key)})")
        return True
    else:
        print("  ⚠️  GEMINI_API_KEY format looks incorrect (should start with 'AIza')")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print("\n🔍 Checking Python dependencies...")
    
    required = [
        ('requests', '2.32.3'),
        ('tenacity', '9.0.0'),
        ('jsonschema', '4.23.0'),
        ('PIL', '11.0.0'),
        ('dotenv', '1.0.1')
    ]
    
    all_ok = True
    for module_name, expected_version in required:
        try:
            if module_name == 'PIL':
                import PIL
                version = PIL.__version__
            elif module_name == 'dotenv':
                # python-dotenv doesn't expose __version__ reliably
                import dotenv
                try:
                    from importlib.metadata import version as get_version
                    version = get_version('python-dotenv')
                except:
                    version = 'installed'
            else:
                module = __import__(module_name)
                try:
                    version = module.__version__
                except AttributeError:
                    try:
                        from importlib.metadata import version as get_version
                        version = get_version(module_name)
                    except:
                        version = 'installed'
            
            print(f"  ✅ {module_name:12} {version}")
        except ImportError:
            print(f"  ❌ {module_name} not installed")
            all_ok = False
    
    return all_ok

def check_directory_structure():
    """Check required directories exist"""
    print("\n🔍 Checking directory structure...")
    
    repo = Path(__file__).resolve().parents[1]
    required_dirs = [
        repo / "_posts",
        repo / "assets" / "images",
        repo / "_layouts",
        repo / "_includes",
        repo / "pages"
    ]
    
    all_ok = True
    for directory in required_dirs:
        if directory.exists():
            print(f"  ✅ {directory.relative_to(repo)}")
        else:
            print(f"  ❌ {directory.relative_to(repo)} not found")
            all_ok = False
    
    return all_ok

def check_required_files():
    """Check required files exist"""
    print("\n🔍 Checking required files...")
    
    repo = Path(__file__).resolve().parents[1]
    required_files = [
        repo / "_config.yml",
        repo / "requirements.txt",
        repo / "_layouts" / "default.html",
        repo / "_layouts" / "post.html",
        repo / "_includes" / "seo.html",
        repo / "_includes" / "lang-toggle.html",
        repo / "_includes" / "adsense.html",
        repo / ".github" / "workflows" / "auto_post.yml"
    ]
    
    all_ok = True
    for filepath in required_files:
        if filepath.exists():
            size = filepath.stat().st_size
            rel_path = str(filepath.relative_to(repo))
            print(f"  ✅ {rel_path:45} ({size:,} bytes)")
        else:
            rel_path = str(filepath.relative_to(repo))
            print(f"  ❌ {rel_path} not found")
            all_ok = False
    
    return all_ok

def check_api_connectivity():
    """Test API connectivity (without making actual requests)"""
    print("\n🔍 Checking API endpoints...")
    
    try:
        import requests
        
        # Just check if endpoints are reachable (HEAD request)
        endpoints = [
            "https://generativelanguage.googleapis.com",
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.head(endpoint, timeout=5)
                print(f"  ✅ {endpoint} is reachable")
            except requests.RequestException as e:
                print(f"  ⚠️  {endpoint} - {str(e)[:50]}")
        
        return True
    except ImportError:
        print("  ❌ requests module not available")
        return False

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("  Bhaskar Daily AI News - Setup Validation")
    print("=" * 60)
    
    results = {
        "Environment": check_environment(),
        "Dependencies": check_dependencies(),
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "API Connectivity": check_api_connectivity()
    }
    
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check:20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("  🎉 All checks passed! Ready to generate posts.")
        print("  Run: python scripts/generate_post.py")
    else:
        print("  ⚠️  Some checks failed. Fix issues before proceeding.")
        print("  See errors above for details.")
    print("=" * 60 + "\n")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
