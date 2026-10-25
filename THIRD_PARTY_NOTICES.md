# Third-party notices

SiriusDocs 0.1.0 uses Commercial SDK License 1.0 for newly supplied rights.
Earlier MIT grants remain intact; see LICENSES/MIT-previous-grants.txt.
Third-party components retain their original licenses.

The compiled Python wheels depend on the following packages. The Swift offline
reader closure includes them and retains their wheel license/notice files.
Exact resolved versions and artifact hashes accompany that closure in
`dependencies.json`. No model weights are included.

| Component | Purpose | License |
| --- | --- | --- |
| pdfminer.six, charset-normalizer | Independent PDF text validation | MIT |
| cryptography | PDF cryptographic primitives | Apache-2.0 OR BSD-3-Clause; retained bundled notices |
| cffi, pycparser | Native dependency support | MIT-0; BSD-3-Clause |
| markdown-it-py, mdurl | Markdown text integrity | MIT |
| psutil | Owned worker resource monitoring | BSD-3-Clause |
| python-docx, openpyxl, python-pptx | Office source readers | MIT |
| lxml | XML parsing | BSD-3-Clause; retained libxml2/libxslt notices |
| Pillow | Local image assets | MIT-CMU; retained bundled library notices |
| XlsxWriter, et_xmlfile, typing_extensions | Office reader dependencies | BSD-2-Clause; MIT; PSF-2.0 |
| xlrd, olefile | Bounded legacy Office readers | BSD-3-Clause; BSD-2-Clause and permissive PIL notice |
| resvg-py | Bounded drawing previews | MIT; Rust dependency notices retained |

The resvg closure includes the complete hash-verified notice-file superset from
its published source Cargo lock. Registry crate licenses provide permissive
alternatives including MIT, Apache-2.0, BSD, Zlib, Unlicense, Unicode-3.0 and the
LLVM exception. Its inventory identifies the exact source archive checksums.
The complete superset is retained without claiming every crate is linked.

The Swift SDK uses published SwiftPython 0.7.0-preview.1.7 under its separately
supplied Commercial SDK License 1.0. CPython and its bundled library notices
remain in the supplied runtime. This license does not relicense those components.
The app integration helper retains the exact SwiftPython license and installed
reader notices. The platform provides Foundation, CoreGraphics, PDFKit, Vision,
FoundationModels, CryptoKit and AppKit; no Apple frameworks or weights are copied
into the Python wheel.

Optional Docling is not bundled. Its code, parser/OCR dependencies and locally
prepared models have their own terms. No Docling or Paddle model redistribution
is included in 0.1.0. The optional pypdf forms dependency uses BSD-3-Clause;
forms are outside the extraction support claims.

SiriusMarkdown is a separately licensed renderer and is not a runtime dependency
or a redistributed component of SiriusDocs.
