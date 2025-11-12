"""
Mobile Development Plugin - Android and iOS app creation
"""
from typing import Dict, Any, List, Optional
import subprocess
import os
from pathlib import Path
import json

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class MobileDevPlugin(JarvisPlugin):
    """
    Plugin for mobile app development (Android & iOS) with teaching support.
    Supports React Native, Flutter, and native development.
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
        self.frameworks = {
            "react-native": self._check_react_native,
            "flutter": self._check_flutter,
            "android": self._check_android_studio,
            "ios": self._check_xcode
        }
    
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="mobile_dev",
            version="1.0.0",
            description="Mobile app development for Android and iOS with teaching support",
            capabilities=[PluginCapability.CODE_GENERATION, PluginCapability.FILE_OPERATION],
            permissions=["code.generate", "file.write", "shell.execute"],
            author="Jarvis AI Team",
            dependencies=["react-native-cli", "flutter", "android-studio"]
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        
        # Check available frameworks
        self.available_frameworks = {}
        for framework, check_func in self.frameworks.items():
            self.available_frameworks[framework] = check_func()
        
        logger.info(f"Mobile dev plugin initialized. Available: {list(self.available_frameworks.keys())}")
        return True
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def enable_teaching_mode(self):
        """Enable teaching mode"""
        self.teaching_mode = True
    
    def disable_teaching_mode(self):
        """Disable teaching mode"""
        self.teaching_mode = False
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute mobile dev action"""
        actions = {
            "create_app": self._create_app,
            "create_react_native": self._create_react_native_app,
            "create_flutter": self._create_flutter_app,
            "create_android": self._create_android_app,
            "create_ios": self._create_ios_app,
            "build": self._build_app,
            "run": self._run_app,
            "explain": self._explain_mobile_dev,
            "check_setup": self._check_setup,
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys())
            }
    
    def _create_app(
        self,
        name: str,
        framework: str = "react-native",
        platforms: List[str] = None,
        template: str = "default",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create a new mobile app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        platforms = platforms or ["android", "ios"]
        
        # Route to appropriate framework
        if framework == "react-native":
            return self._create_react_native_app(name, template, teaching)
        elif framework == "flutter":
            return self._create_flutter_app(name, platforms, teaching)
        elif framework == "android":
            return self._create_android_app(name, teaching)
        elif framework == "ios":
            return self._create_ios_app(name, teaching)
        else:
            return {
                "success": False,
                "error": f"Unknown framework: {framework}",
                "available_frameworks": ["react-native", "flutter", "android", "ios"]
            }
    
    def _create_react_native_app(
        self,
        name: str,
        template: str = "default",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create React Native app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            logger.info(f"Creating React Native app: {name}")
            
            # Use npx to create React Native app
            cmd = ["npx", "react-native", "init", name]
            
            if template and template != "default":
                cmd.extend(["--template", template])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            response = {
                "success": result.returncode == 0,
                "app_name": name,
                "framework": "React Native",
                "platforms": ["Android", "iOS"],
                "directory": name,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if result.returncode == 0 and teaching:
                response["explanation"] = self._get_react_native_explanation(name)
                response["next_steps"] = [
                    f"cd {name}",
                    "npm install  # Install dependencies",
                    "npx react-native run-android  # Run on Android",
                    "npx react-native run-ios  # Run on iOS (Mac only)",
                    "npm start  # Start Metro bundler"
                ]
                response["learning_resources"] = {
                    "docs": "https://reactnative.dev/docs/getting-started",
                    "components": "https://reactnative.dev/docs/components-and-apis",
                    "tutorial": "https://reactnative.dev/docs/tutorial"
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "React Native CLI not found",
                "install_command": "npm install -g react-native-cli",
                "message": "Install React Native CLI first"
            }
        except Exception as e:
            logger.error(f"Error creating React Native app: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_flutter_app(
        self,
        name: str,
        platforms: List[str],
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Create Flutter app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            logger.info(f"Creating Flutter app: {name}")
            
            cmd = ["flutter", "create", name]
            
            # Add platform options
            if "android" not in platforms:
                cmd.extend(["--platforms", "ios"])
            elif "ios" not in platforms:
                cmd.extend(["--platforms", "android"])
            else:
                cmd.extend(["--platforms", "android,ios"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            response = {
                "success": result.returncode == 0,
                "app_name": name,
                "framework": "Flutter",
                "platforms": platforms,
                "directory": name,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if result.returncode == 0 and teaching:
                response["explanation"] = self._get_flutter_explanation(name)
                response["next_steps"] = [
                    f"cd {name}",
                    "flutter pub get  # Get dependencies",
                    "flutter run  # Run app",
                    "flutter build apk  # Build Android APK",
                    "flutter build ios  # Build iOS (Mac only)"
                ]
                response["learning_resources"] = {
                    "docs": "https://docs.flutter.dev/",
                    "widgets": "https://docs.flutter.dev/development/ui/widgets",
                    "cookbook": "https://docs.flutter.dev/cookbook"
                }
            
            return response
            
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Flutter not found",
                "install_command": "Install from https://flutter.dev/docs/get-started/install",
                "message": "Install Flutter SDK first"
            }
        except Exception as e:
            logger.error(f"Error creating Flutter app: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_android_app(self, name: str, teaching: bool = None) -> Dict[str, Any]:
        """Create native Android app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # For native Android, we'll provide instructions and a template
        response = {
            "success": True,
            "app_name": name,
            "framework": "Native Android (Kotlin/Java)",
            "platforms": ["Android"],
            "message": "Native Android app project structure provided"
        }
        
        if teaching:
            response["explanation"] = {
                "what_is_android": "Native Android development using Kotlin or Java",
                "requirements": [
                    "Android Studio IDE",
                    "Android SDK",
                    "Java JDK 11 or higher",
                    "Gradle build system"
                ],
                "project_structure": {
                    "app/": "Main application module",
                    "app/src/main/java/": "Kotlin/Java source code",
                    "app/src/main/res/": "Resources (layouts, drawables, etc.)",
                    "app/src/main/AndroidManifest.xml": "App configuration",
                    "build.gradle": "Build configuration"
                },
                "key_concepts": {
                    "Activity": "Single screen with user interface",
                    "Fragment": "Reusable portion of UI",
                    "Intent": "Message for component communication",
                    "ViewModel": "Manages UI data",
                    "RecyclerView": "Efficient list display"
                }
            }
            response["next_steps"] = [
                "Open Android Studio",
                "Select 'New Project'",
                "Choose 'Empty Activity' template",
                f"Name your project '{name}'",
                "Select Kotlin as language",
                "Choose minimum SDK (API 21+)",
                "Click 'Finish'"
            ]
            response["learning_resources"] = {
                "docs": "https://developer.android.com/docs",
                "codelabs": "https://developer.android.com/courses",
                "kotlin": "https://kotlinlang.org/docs/android-overview.html"
            }
        
        return response
    
    def _create_ios_app(self, name: str, teaching: bool = None) -> Dict[str, Any]:
        """Create native iOS app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        response = {
            "success": True,
            "app_name": name,
            "framework": "Native iOS (Swift/SwiftUI)",
            "platforms": ["iOS"],
            "message": "Native iOS app instructions provided"
        }
        
        if teaching:
            response["explanation"] = {
                "what_is_ios": "Native iOS development using Swift and SwiftUI",
                "requirements": [
                    "Mac computer with macOS",
                    "Xcode IDE",
                    "Apple Developer Account (for device testing)",
                    "iOS Simulator"
                ],
                "project_structure": {
                    "ContentView.swift": "Main UI view",
                    "AppName.swift": "App entry point",
                    "Assets.xcassets": "Images and colors",
                    "Info.plist": "App configuration",
                    "Storyboards": "UI layouts (UIKit)"
                },
                "key_concepts": {
                    "SwiftUI": "Declarative UI framework",
                    "UIKit": "Traditional UI framework",
                    "View": "Visual element on screen",
                    "ViewController": "Manages view hierarchy",
                    "Storyboard": "Visual UI designer",
                    "Swift": "Modern, safe programming language"
                }
            }
            response["next_steps"] = [
                "Open Xcode",
                "Select 'Create a new Xcode project'",
                "Choose 'App' template",
                f"Name your project '{name}'",
                "Select 'SwiftUI' for Interface",
                "Select 'Swift' for Language",
                "Choose your team (if you have developer account)",
                "Click 'Next' and choose location"
            ]
            response["learning_resources"] = {
                "docs": "https://developer.apple.com/documentation/",
                "swiftui": "https://developer.apple.com/tutorials/swiftui",
                "swift": "https://docs.swift.org/swift-book/"
            }
        
        return response
    
    def _build_app(
        self,
        framework: str,
        platform: str = "android",
        directory: str = ".",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Build mobile app"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            if framework == "react-native":
                if platform == "android":
                    cmd = ["npx", "react-native", "run-android"]
                else:
                    cmd = ["npx", "react-native", "run-ios"]
            elif framework == "flutter":
                if platform == "android":
                    cmd = ["flutter", "build", "apk"]
                else:
                    cmd = ["flutter", "build", "ios"]
            else:
                return {
                    "success": False,
                    "error": "Native builds require IDE (Android Studio or Xcode)"
                }
            
            result = subprocess.run(
                cmd,
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            response = {
                "success": result.returncode == 0,
                "framework": framework,
                "platform": platform,
                "output": result.stdout if result.returncode == 0 else result.stderr
            }
            
            if teaching:
                response["explanation"] = {
                    "what_happened": f"Built {platform} app using {framework}",
                    "build_output": f"Check the build output for APK/IPA location",
                    "troubleshooting": {
                        "android": "Ensure Android SDK is installed and ANDROID_HOME is set",
                        "ios": "Requires Mac with Xcode installed"
                    }
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_app(
        self,
        framework: str,
        platform: str = "android",
        directory: str = ".",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Run mobile app on emulator/simulator"""
        if teaching is None:
            teaching = self.teaching_mode
        
        try:
            if framework == "react-native":
                cmd = ["npx", "react-native", f"run-{platform}"]
            elif framework == "flutter":
                cmd = ["flutter", "run"]
            else:
                return {
                    "success": False,
                    "error": "Use Android Studio or Xcode to run native apps"
                }
            
            # Start in background
            process = subprocess.Popen(
                cmd,
                cwd=directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            response = {
                "success": True,
                "framework": framework,
                "platform": platform,
                "message": f"App starting on {platform}...",
                "pid": process.pid
            }
            
            if teaching:
                response["explanation"] = {
                    "what_happened": f"Launched app on {platform} emulator/simulator",
                    "requirements": {
                        "android": "Android emulator must be running",
                        "ios": "iOS simulator opens automatically (Mac only)"
                    },
                    "hot_reload": "Changes will auto-reload in development mode"
                }
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_setup(self, teaching: bool = None) -> Dict[str, Any]:
        """Check mobile development setup"""
        if teaching is None:
            teaching = self.teaching_mode
        
        status = {
            "react_native": self._check_react_native(),
            "flutter": self._check_flutter(),
            "android_sdk": self._check_android_studio(),
            "xcode": self._check_xcode()
        }
        
        response = {
            "success": True,
            "setup_status": status,
            "ready_frameworks": [k for k, v in status.items() if v]
        }
        
        if teaching:
            response["explanation"] = self._get_setup_explanation(status)
        
        return response
    
    def _check_react_native(self) -> bool:
        """Check if React Native is available"""
        try:
            result = subprocess.run(
                ["npx", "react-native", "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_flutter(self) -> bool:
        """Check if Flutter is available"""
        try:
            result = subprocess.run(
                ["flutter", "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_android_studio(self) -> bool:
        """Check if Android SDK is available"""
        android_home = os.getenv("ANDROID_HOME") or os.getenv("ANDROID_SDK_ROOT")
        return android_home is not None and Path(android_home).exists()
    
    def _check_xcode(self) -> bool:
        """Check if Xcode is available (Mac only)"""
        try:
            result = subprocess.run(
                ["xcodebuild", "-version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _explain_mobile_dev(self, topic: str = "basics") -> Dict[str, Any]:
        """Explain mobile development concepts"""
        explanations = {
            "basics": {
                "mobile_development": "Creating applications for mobile devices (phones, tablets)",
                "platforms": {
                    "Android": "Google's mobile OS, uses Java/Kotlin",
                    "iOS": "Apple's mobile OS, uses Swift/Objective-C"
                },
                "approaches": {
                    "Native": "Platform-specific code, best performance",
                    "Cross-platform": "One codebase for both platforms",
                    "Hybrid": "Web technologies wrapped in native container"
                }
            },
            "frameworks": {
                "React Native": {
                    "description": "JavaScript framework by Facebook",
                    "pros": ["JavaScript/React knowledge", "Hot reload", "Large community"],
                    "cons": ["Bridge overhead", "Some native code needed"]
                },
                "Flutter": {
                    "description": "Dart framework by Google",
                    "pros": ["Fast performance", "Beautiful UI", "Single codebase"],
                    "cons": ["Larger app size", "Dart language learning curve"]
                },
                "Native": {
                    "description": "Platform-specific development",
                    "pros": ["Best performance", "Full platform access", "Latest features"],
                    "cons": ["Separate codebases", "More resources needed"]
                }
            },
            "choosing": {
                "use_react_native": [
                    "You know JavaScript/React",
                    "Want to share code with web app",
                    "Need quick MVP",
                    "Have React developers"
                ],
                "use_flutter": [
                    "Want beautiful, custom UI",
                    "Need high performance",
                    "Like Dart language",
                    "Want true cross-platform"
                ],
                "use_native": [
                    "Need maximum performance",
                    "Require latest platform features",
                    "Building platform-specific app",
                    "Have platform expertise"
                ]
            }
        }
        
        return {
            "success": True,
            "topic": topic,
            "explanation": explanations.get(topic, explanations["basics"])
        }
    
    def _get_react_native_explanation(self, name: str) -> Dict[str, Any]:
        """Get React Native project explanation"""
        return {
            "framework": "React Native",
            "description": "Cross-platform mobile framework using React and JavaScript",
            "project_structure": {
                "index.js": "Entry point",
                "App.js": "Main app component",
                "android/": "Android-specific code",
                "ios/": "iOS-specific code",
                "package.json": "Dependencies"
            },
            "key_concepts": {
                "Components": "Reusable UI elements",
                "JSX": "JavaScript XML syntax",
                "Props": "Component parameters",
                "State": "Component data",
                "Navigation": "Screen transitions"
            },
            "advantages": [
                "Write once, run on both platforms",
                "Hot reloading for fast development",
                "Large ecosystem of packages",
                "JavaScript/React skills reusable"
            ]
        }
    
    def _get_flutter_explanation(self, name: str) -> Dict[str, Any]:
        """Get Flutter project explanation"""
        return {
            "framework": "Flutter",
            "description": "Google's UI toolkit for building natively compiled apps",
            "project_structure": {
                "lib/main.dart": "Entry point",
                "lib/": "Dart source code",
                "android/": "Android configuration",
                "ios/": "iOS configuration",
                "pubspec.yaml": "Dependencies and assets"
            },
            "key_concepts": {
                "Widgets": "Everything is a widget",
                "StatelessWidget": "Immutable widgets",
                "StatefulWidget": "Widgets with mutable state",
                "BuildContext": "Widget location in tree",
                "Hot reload": "Instant UI updates"
            },
            "advantages": [
                "Fast performance (compiled to native)",
                "Beautiful, customizable UI",
                "Single codebase for all platforms",
                "Rich widget library"
            ]
        }
    
    def _get_setup_explanation(self, status: Dict[str, bool]) -> Dict[str, Any]:
        """Get setup explanation based on current status"""
        missing = [k for k, v in status.items() if not v]
        
        install_instructions = {
            "react_native": {
                "steps": [
                    "Install Node.js from nodejs.org",
                    "Install React Native CLI: npm install -g react-native-cli",
                    "For Android: Install Android Studio",
                    "For iOS: Install Xcode (Mac only)"
                ],
                "docs": "https://reactnative.dev/docs/environment-setup"
            },
            "flutter": {
                "steps": [
                    "Download Flutter SDK from flutter.dev",
                    "Extract and add to PATH",
                    "Run: flutter doctor",
                    "Install missing dependencies it reports"
                ],
                "docs": "https://docs.flutter.dev/get-started/install"
            },
            "android_sdk": {
                "steps": [
                    "Download Android Studio",
                    "Install Android SDK",
                    "Set ANDROID_HOME environment variable",
                    "Add SDK tools to PATH"
                ],
                "docs": "https://developer.android.com/studio"
            },
            "xcode": {
                "steps": [
                    "Install Xcode from App Store (Mac only)",
                    "Install command line tools: xcode-select --install",
                    "Accept license: sudo xcodebuild -license"
                ],
                "docs": "https://developer.apple.com/xcode/"
            }
        }
        
        return {
            "ready": [k for k, v in status.items() if v],
            "missing": missing,
            "install_instructions": {k: install_instructions[k] for k in missing}
        }
