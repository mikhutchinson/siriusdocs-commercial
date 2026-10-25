# SiriusDocs

Local document ingestion for Swift and Python: structured content, Markdown,
portable assets, source identities, warnings and machine-readable provenance.
Extraction does not fetch documents, execute macros or download models.

SiriusDocs 0.1.0 uses [Commercial SDK License 1.0](LICENSE).
Community use is free below USD 100,000 in trailing twelve-month business revenue;
paid Indie and Business tiers cover larger businesses. [Licensing details](LICENSING.md).
Earlier MIT grants and third-party licenses remain intact.

## Document types

| Family | Extensions | Scope |
| --- | --- | --- |
| PDF | `.pdf` | Ordered physical pages, integrity checks, layout/OCR on supported Apple systems; explicit warnings/failures |
| Word | `.docx`, `.doc` | Source paragraphs, tables and supported formatting; legacy DOC uses the macOS reader |
| Spreadsheets | `.xlsx`, `.xls` | Sheets, cells, formula/cache evidence, merges and assets; formulas are not evaluated |
| Presentations | `.pptx`, `.ppt` | Slide order, text, notes and supported drawings/assets |
| OpenDocument | `.odt`, `.ods`, `.odp` | Text, sheets, slides, source lists/tables and supported embedded assets |
| EPUB | `.epub` | Spine/chapter order, links and local images |
| HTML | `.html`, `.htm`, `.xhtml` | Supported document structure and safe links; no scripts or remote fetches |
| Rich text | `.rtf` | Native macOS text and supported emphasis |
| Delimited text | `.csv` | Quoted UTF-8 cells |
| Markdown and text | `.md`, `.markdown`, `.txt` | Original Markdown or escaped literal UTF-8 text |
| Source markup | `.adoc`, `.tex` | Complete source in a code block with an explicit warning; semantic conversion is unavailable |

There are 18 format identifiers. AsciiDoc and LaTeX are source-preservation
routes. General layout fidelity, formula OCR, handwriting, arbitrary legacy
Office drawings, revisions and full Word semantics are not guaranteed. Results
surface unsupported content and retain source assets where the reader supports it.

## Python

Install the matching compiled wheel from the
[0.1.0 release](https://github.com/mikhutchinson/siriusdocs-commercial/releases/tag/0.1.0).
Use CPython 3.10–3.14; wheels are specific to the Python minor version. Install
`documents` to include the Office reader dependencies:

```sh
python -m pip install './sirius_docs-0.1.0-cp313-none-macosx_26_0_arm64.whl[documents]'
```

The macOS 26 Apple silicon wheel includes the native companion for PDF layout,
OCR, DOC and RTF. Core wheels keep non-Apple imports independent of Apple
frameworks. Native DOC/RTF require macOS; unavailable required profiles fail
explicitly. Optional Docling uses the `docling` extra and separately prepared
local models; those models are not included.

```python
from sirius_docs import DocumentExtractor

with DocumentExtractor() as client:
    result = client.extract("report.docx")
    result.write("new-output-directory")
```

For an explicit native PDF layout/OCR request on supported macOS:

```python
from sirius_docs import PDFExtractor

with PDFExtractor.apple() as pdf:
    result = pdf.extract("report.pdf", profile="layout")
```

The general Python document facade retains the conservative PDF default and
reports degraded native-text output visibly. A required layout/OCR profile
fails when its backend is unavailable.

## Swift

Select `SiriusDocsKit` from the binary Swift package at
`https://github.com/mikhutchinson/siriusdocs-commercial`, exact version `0.1.0`.
The initial binary Swift SDK targets macOS 26 on Apple silicon. iOS, simulator,
Intel Mac and App Store distribution are not qualified by this release.
The SDK uses pinned SwiftPython `0.7.0`, under its separately
supplied license, for shared routing and validation.

```swift
import SiriusDocsKit

let client = try await DocumentClient.start()
let result = try await client.extract(inputURL)
try result.write(to: newOutputDirectory)
await client.close()
```

Package the supplied reader resources and SwiftPython worker/frameworks into the
consumer app using the distribution's integration helper. The ordinary client
owns the pool and native callbacks; applications with an existing pool can use
`DocumentClient.connect(pool:)`. No extraction-time compilation or installation
occurs. See the public package's integration instructions.

## Results and compatibility

Results retain ordered source units, blocks, asset hashes, loss warnings, limits,
backend identity and timings. PDF units have physical page identities; Word and
HTML do not acquire invented pages. Export writes local assets and a JSON sidecar
to a new directory, preserving existing output.

Existing `sirius_pdf` imports and `SiriusPDFKit` APIs remain available.
SiriusMarkdown is a separate renderer and is not a runtime dependency.
