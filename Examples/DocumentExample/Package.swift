// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "DocumentExample",
    platforms: [.macOS(.v26)],
    dependencies: [.package(url: "https://github.com/mikhutchinson/siriusdocs-commercial", exact: "0.1.0")],
    targets: [.executableTarget(name: "DocumentExample", dependencies: [
        .product(name: "SiriusDocsKit", package: "siriusdocs-commercial")
    ])]
)
