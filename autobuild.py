import os, subprocess, glob

def run_auto_build():
    print("🚀 Auto-Build Process Shuru Ho Raha Hai...")
    
    os.environ["CFLAGS"] = "-Wno-incompatible-pointer-types -Wno-discarded-qualifiers"
    os.environ["CXXFLAGS"] = "-Wno-incompatible-pointer-types -Wno-discarded-qualifiers"
    
    # 1ST ATTEMPT
    print("\n📦 Attempt 1: Building APK with Buildozer...")
    process = subprocess.run("yes | buildozer -s android debug", shell=True, capture_output=True, text=True)
    
    # ERROR AUTO-FIXER LOGIC
    if process.returncode != 0:
        print("\n❌ Attempt 1 Fail ho gaya. Error analyze kiya ja raha hai...")
        error_log = process.stdout + "\n" + process.stderr
        
        if "longintrepr.h" in error_log or "Python.h" in error_log:
            print("🔧 Issue Detected: CPython Header error (`longintrepr.h`).")
            print("🛠️ Auto-Fixing: `buildozer.spec` mein Python version lock kar rahe hain...")
            
            if os.path.exists("buildozer.spec"):
                with open("buildozer.spec", "r") as f:
                    content = f.read()
                if "python3==" not in content:
                    content = content.replace("requirements = python3,", "requirements = python3==3.11.5,hostpython3==3.11.5,")
                    with open("buildozer.spec", "w") as f:
                        f.write(content)
                    print("✅ `buildozer.spec` auto-update ho gayi.")

        elif "Cython" in error_log:
            print("🔧 Issue Detected: Cython version mismatch.")
            print("🛠️ Auto-Fixing: Compatible Cython install kar rahe hain...")
            subprocess.run(["pip", "install", "cython==0.29.36"])

        else:
            print("⚠️ Unknown log error. Last few lines of log:")
            print("\n".join(error_log.splitlines()[-15:]))
            
        # 2ND ATTEMPT
        print("\n🔄 Attempt 2: Auto-Rebuilding APK starting now...")
        process = subprocess.run("yes | buildozer -s android debug", shell=True, capture_output=True, text=True)

    # FINAL CHECK
    apk_files = glob.glob('bin/*.apk')
    if apk_files:
        print(f"\n🎉 SUCCESS! APK ready hai: {apk_files[0]}")
    else:
        print("\n❌ Build abhi bhi complete nahi hua. Detailed error log check karein.")

run_auto_build()
