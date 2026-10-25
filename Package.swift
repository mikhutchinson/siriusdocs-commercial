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
    dependencies: [.package(url: "https://github.com/mikhutchinson/swiftpython-commercial", exact: "0.7.0")],
    targets: [
        .binaryTarget(name: "SiriusDocsKit", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusDocsKit.xcframework.zip", checksum: "a5ac7560adcbae47a245c94c7a5fdff8cf137b65696d02c47ae277b12cc7d7fc"),
        .binaryTarget(name: "SiriusPDFKit", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusPDFKit.xcframework.zip", checksum: "bd8469513f0cfa4d1230bae60968165ab5ec185f630b060cf03adcf8bcac9082"),
        .binaryTarget(name: "SiriusPDFApple", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusPDFApple.xcframework.zip", checksum: "6a74d086ad9194f8e6079e002e403dc8a1125f65b2e4cef0e136ed982be29a04"),
        .binaryTarget(name: "SiriusDoc", url: "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusDoc.xcframework.zip", checksum: "13cd25c43714733f9ee6630d78f2d772eed1d6ce5b2140323ad37671d5e2d579"),
        .target(name: "SiriusDocsRuntimeLink", dependencies: [.product(name: "SwiftPythonRuntime", package: "swiftpython-commercial")], path: "Integration/RuntimeLink")
    ]
)
