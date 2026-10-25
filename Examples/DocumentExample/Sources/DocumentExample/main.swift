import Foundation
import SiriusDocsKit

@main
struct DocumentExample {
    static func main() async throws {
        guard CommandLine.arguments.count == 3 else {
            throw NSError(domain: "DocumentExample", code: 1,
                userInfo: [NSLocalizedDescriptionKey: "Usage: DocumentExample input-file new-output-directory"])
        }
        let client = try await DocumentClient.start()
        do {
            let result = try await client.extract(URL(fileURLWithPath: CommandLine.arguments[1]))
            try result.write(to: URL(fileURLWithPath: CommandLine.arguments[2]))
            await client.close()
        } catch {
            await client.close()
            throw error
        }
    }
}
