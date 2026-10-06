// Fotografiert eine Seite mit WebKit (Safaris Engine). Aufruf: webkitshot <url> <ausgabe.png> [wartezeit]
import Cocoa
import WebKit

class Lader: NSObject, WKNavigationDelegate {
    let ziel: String; let warte: Double
    init(ziel: String, warte: Double) { self.ziel = ziel; self.warte = warte }
    func webView(_ w: WKWebView, didFinish n: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + warte) {
            let k = WKSnapshotConfiguration(); k.rect = CGRect(x: 0, y: 0, width: 1920, height: 1080); k.snapshotWidth = 1920
            w.takeSnapshot(with: k) { bild, _ in
                if let b = bild, let t = b.tiffRepresentation, let r = NSBitmapImageRep(data: t), let p = r.representation(using: .png, properties: [:]) {
                    try? p.write(to: URL(fileURLWithPath: self.ziel)); print("ok")
                } else { print("fehler") }
                exit(0)
            }
        }
    }
}
let a = CommandLine.arguments
let app = NSApplication.shared; app.setActivationPolicy(.prohibited)
let fenster = NSWindow(contentRect: NSRect(x: -4000, y: -4000, width: 1920, height: 1080), styleMask: [.borderless], backing: .buffered, defer: false)
let web = WKWebView(frame: NSRect(x: 0, y: 0, width: 1920, height: 1080))
let lader = Lader(ziel: a[2], warte: a.count > 3 ? Double(a[3])! : 3)
web.navigationDelegate = lader; fenster.contentView = web; fenster.orderBack(nil)
web.load(URLRequest(url: URL(string: a[1])!))
DispatchQueue.main.asyncAfter(deadline: .now() + 40) { print("timeout"); exit(1) }
app.run()
