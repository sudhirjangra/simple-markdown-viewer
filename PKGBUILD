# Maintainer: Sudhir Jangra <sudhirjangra@example.com>
pkgname=markdown-viewer
pkgver=1.0.1
pkgrel=1
pkgdesc="Professional Markdown Reader with Live Preview"
arch=('any')
url="https://github.com/sudhirjangra/markdown-viewer"
license=('MIT')
depends=('python' 'python-pyqt6' 'python-pyqt6-webengine' 'python-markdown')
makedepends=()
source=()
sha256sums=()

package() {
    cd "$startdir"

    # Install Python script
    install -Dm755 app.py "$pkgdir/usr/bin/markdown-viewer"

    # Install icon
    install -Dm644 icon.png "$pkgdir/usr/share/pixmaps/markdown-viewer.png"

    # Install desktop file
    install -Dm644 markdown-viewer.desktop "$pkgdir/usr/share/applications/markdown-viewer.desktop"

    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
