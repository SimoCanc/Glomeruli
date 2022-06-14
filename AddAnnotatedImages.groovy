/*
Script che aggiunge le immagini annotate presenti nella cartella 'path', all'attuale progetto aperto in QuPath
*/

def path = '\\path\\to\\folder\\with\\qpdata\\files'

def project = getProject()
def files = new File(path).listFiles().findAll {f -> f.isFile() && f.getName().endsWith('.qpdata')}
for (file in files) {
    def imageData = loadImageData(file.getAbsolutePath(), false)
    def server = imageData.getServer()
    def entry = project.addImage(server.getBuilder())
    entry.setImageName(server.getMetadata().getName())
    entry.setThumbnail(qupath.lib.gui.commands.ProjectCommands.getThumbnailRGB(server))
    entry.saveImageData(imageData)
}
project.syncChanges()
getQuPath().refreshProject()
