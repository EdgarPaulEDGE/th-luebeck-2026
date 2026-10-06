// Gibt den Gesichtsrahmen eines Bildes aus: x y breite hoehe (Pixel, Ursprung oben links)
import Foundation
import Vision
import CoreImage

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let bild = CIImage(contentsOf: url, options: [.applyOrientationProperty: true]) else { exit(1) }
let anfrage = VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(ciImage: bild).perform([anfrage])
// Größtes Gesicht gewinnt, falls mehrere gefunden werden
guard let g = anfrage.results?.max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { print("kein"); exit(0) }
let w = bild.extent.width, h = bild.extent.height, b = g.boundingBox
print(Int(b.minX * w), Int((1 - b.maxY) * h), Int(b.width * w), Int(b.height * h))
