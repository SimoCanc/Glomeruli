/**
 * Script to export image tiles (can be customized in various ways).
 */
// Get the current image (supports 'Run for project')
def imageData = getCurrentImageData()

def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
%Change pathToFolder
def pathOutputGloBad = buildFilePath('pathToFolder', 'GloBad')
def pathOutputGloGood = buildFilePath('pathToFolder', 'GloGood')
mkdirs(pathOutputGloBad)
mkdirs(pathOutputGloGood)

// Define output resolution in calibrated units (e.g. µm if available)
//// Questo piu e' piccolo piu tiles mi fa, e quindi le dimensioni dei glomeruli aumentano. Percui
//questo mi serve per provare a confrontarlo con quei glomeruli su cui funziona l'altra rete.
double requestedPixelSize = 2.0

// Convert output resolution to a downsample factor
double pixelSize = imageData.getServer().getPixelCalibration().getAveragedPixelSize()
double downsample = requestedPixelSize / pixelSize




def labelServer = new LabeledImageServer.Builder(imageData)
    .backgroundLabel(255, ColorTools.BLACK) // Specify background label (usually 0 or 255)
    .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
    .addLabel('Glogood', 2)      // Choose output labels (the order matters!)
    .multichannelOutput(false)  // If true, each label is a different channel (required for multiclass probability)
    .build()


// Create an exporter that requests corresponding tiles from the original & labelled image servers
new TileExporter(imageData)
    .downsample(downsample)   // Define export resolution
    .imageExtension('.jpg')   // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
    .tileSize(512)            // Define size of each tile, in pixels
    .annotatedTilesOnly(true) // If true, only export tiles if there is a (classified) annotation present
    .overlap(64)              // Define overlap, in pixel units at the export resolution
    .labeledServer(labelServer)
    .writeTiles(pathOutputGloGood)
   // Write tiles to the specified directory



def labelServer1 = new LabeledImageServer.Builder(imageData)
    .backgroundLabel(255, ColorTools.BLACK) // Specify background label (usually 0 or 255)
    .downsample(downsample)    // Choose server resolution; this should match the resolution at which tiles are exported
    .addLabel('Globad', 2)      // Choose output labels (the order matters!)
    .multichannelOutput(false)  // If true, each label is a different channel (required for multiclass probability)
    .build()


// Create an exporter that requests corresponding tiles from the original & labelled image servers
new TileExporter(imageData)
    .downsample(downsample)   // Define export resolution
    .imageExtension('.jpg')   // Define file extension for original pixels (often .tif, .jpg, '.png' or '.ome.tif')
    .tileSize(512)            // Define size of each tile, in pixels
    .annotatedTilesOnly(true) // If true, only export tiles if there is a (classified) annotation present
    .overlap(64)              // Define overlap, in pixel units at the export resolution
    .labeledServer(labelServer1)
    .writeTiles(pathOutputGloBad)
   // Write tiles to the specified directory

print 'Done!'
