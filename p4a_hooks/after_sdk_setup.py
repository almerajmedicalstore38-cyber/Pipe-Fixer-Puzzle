# p4a_hooks/after_sdk_setup.py
import os

def after_sdk_setup(ctx):
    gradle_path = os.path.join(ctx.dist_dir, 'src', 'main', 'build.gradle')
    
    # Agar file mil jaye to usme AdMob add karo
    if os.path.exists(gradle_path):
        with open(gradle_path, 'r') as f:
            content = f.read()
        
        if 'play-services-ads' not in content:
            content = content.replace(
                'dependencies {',
                'dependencies {\n    implementation "com.google.android.gms:play-services-ads:22.5.0"\n'
            )
            with open(gradle_path, 'w') as f:
                f.write(content)
            print(">>> AdMob Dependency Added via Hook")
