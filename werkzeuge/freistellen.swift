// Stellt das Hauptmotiv eines Fotos frei und speichert ein transparentes PNG.
// Aufruf: freistellen <eingabe> <ausgabe.png>
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { print("Aufruf: freistellen <eingabe> <ausgabe.png>"); exit(2) }
let eingabe = URL(fileURLWithPath: args[1]), ausgabe = URL(fileURLWithPath: args[2])

// EXIF Drehung beachten, sonst liegt die Maske falsch
guard var bild = CIImage(contentsOf: eingabe, options: [.applyOrientationProperty: true]) else { print("Bild nicht lesbar"); exit(1) }
bild = bild.transformed(by: CGAffineTransform(translationX: -bild.extent.origin.x, y: -bild.extent.origin.y))

let anfrage = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: bild)
do {
    try handler.perform([anfrage])
    guard let ergebnis = anfrage.results?.first else { print("Kein Motiv gefunden"); exit(1) }
    let puffer = try ergebnis.generateMaskedImage(ofInstances: ergebnis.allInstances, from: handler, croppedToInstancesExtent: false)
    let frei = CIImage(cvPixelBuffer: puffer)
    let ctx = CIContext()
    guard let cg = ctx.createCGImage(frei, from: frei.extent),
          let ziel = CGImageDestinationCreateWithURL(ausgabe as CFURL, UTType.png.identifier as CFString, 1, nil) else { exit(1) }
    CGImageDestinationAddImage(ziel, cg, nil)
    CGImageDestinationFinalize(ziel)
    print("ok \(cg.width)x\(cg.height) -> \(ausgabe.path)")
} catch { print("Fehler: \(error)"); exit(1) }
