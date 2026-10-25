# macOS app integration

The binary Swift package supplies the SDK libraries. Applications also bundle
the offline reader closure and SwiftPython worker/frameworks. The helper below
downloads only the pinned installation artifacts, verifies SHA-256, then creates
a new local app bundle. Extraction itself never downloads or compiles anything.

```sh
swift build --package-path Examples/DocumentExample -c release
python3 Integration/package_app.py \
  --binary Examples/DocumentExample/.build/release/DocumentExample \
  --cache /path/to/new-install-cache \
  --output /path/to/DocumentExample.app
/path/to/DocumentExample.app/Contents/MacOS/DocumentExample input.docx new-output
```

Use CPython 3.10 or later to run the integration helper. The packaged application
uses the supplied CPython 3.13 runtime independently of the installation host.
The helper uses a local ad-hoc signature. Sign and qualify your finished
application with your own identity and deployment requirements. Its app-specific
entitlements and distribution are not supplied by the SDK.

Existing applications can use the same layout: `Contents/Resources/PythonPackages`,
`Contents/MacOS/SwiftPythonWorker`, and the supplied Python/SwiftPythonEngine
frameworks under `Contents/Frameworks`. Retain package/runtime license files.
The default `DocumentClient.start()` discovers this layout. A host-owned pool can
instead connect through the public API after installing the same module root.

Initial Swift binary target: macOS 26, Apple silicon. The SDK does not qualify
an app for iOS, the App Store, sandboxing or arbitrary worker entitlements.
