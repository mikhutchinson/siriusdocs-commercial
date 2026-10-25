// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "SiriusDocs",
    platforms: [.macOS(.v26)],
    products: [
        .library(name: "SiriusDocsKit", targets: ["SiriusDocsKit", "SiriusPDFKit", "SiriusPDFApple", "SiriusDoc", "SiriusDocsRuntimeLink"]),
        .library(name: "SiriusPDFKit", targets: ["SiriusPDFKit", "SiriusPDFApple", "SiriusDoc", "SiriusDocsRuntimeLink"]),
        .library(name: "SiriusPDFApple", targets: ["SiriusPDFApple"]),
        .library(name: "SiriusDoc", targets: ["SiriusDoc"])
    ],
    dependencies: [.package(url: "https://github.com/mikhutchinson/swiftpython-commercial", exact: "0.7.0-preview.1.7")],
    targets: [
        .binaryTarget(name: "SiriusDocsKit", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusDocsKit.xcframework.zip", checksum: "f4bb445b6b2db8239b18ff836812b4917658f34a1c3f6ae0cf293489554a73d7"),
        .binaryTarget(name: "SiriusPDFKit", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusPDFKit.xcframework.zip", checksum: "90eeecc59858b4cde0faff14f6a9964c820b256da2c1b7c1dfd2e26c78a69445"),
        .binaryTarget(name: "SiriusPDFApple", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusPDFApple.xcframework.zip", checksum: "da9f8941d11e1bd7a5e264d1f0311d5d0573fe81b6280e536ed8ac099d4da68e"),
        .binaryTarget(name: "SiriusDoc", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusDoc.xcframework.zip", checksum: "4e2502e39c4363b25e3612508477fcddecf1282fcfb37dd7b4ddb86aad3cce12"),
        .target(name: "SiriusDocsRuntimeLink", dependencies: [.product(name: "SwiftPythonRuntime", package: "swiftpython-commercial")], path: "Integration/RuntimeLink")
    ]
)
