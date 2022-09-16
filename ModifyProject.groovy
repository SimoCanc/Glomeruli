/*
Script per creare o modificare un progetto

- Posizionarsi sulla cartella di isatallazione di QuPath:
  Es: cd C:\Users\Simone\AppData\Local\QuPath-0.3.2"
- Dare il seguente comando da shell:
  "QuPath-0.3.2 (console).exe" script "C:\Users\Simone\Desktop\CreateProject.groovy" --args "C:\Users\Simone\Desktop\topolino"
Ricordarsi di mettere le virgolette "" dove necessario
*/

import groovy.io.FileType
import java.awt.image.BufferedImage
import qupath.lib.images.servers.ImageServerProvider
import qupath.lib.gui.commands.ProjectCommands

if (args.size() > 0)
    selectedDir = new File(args[0])
else
    selectedDir = Dialogs.promptForDirectory(null)

if (selectedDir == null)
    return
    
//Controllo se presente directory con un progetto QuPAth
projectName = "QuPathProject"
File directory = new File(selectedDir.toString() + File.separator + projectName)

if (!directory.exists())
{
    print("No project directory, creating one!")
    directory.mkdirs()
}

// Creazione progetto
def project = Projects.createProject(directory , BufferedImage.class)

// Creazione lista di files
def files = []
selectedDir.eachFileRecurse (FileType.FILES) { file ->
    if (file.getName().toLowerCase().endsWith(".ndpi"))
    {
        files << file
        print(file.getCanonicalPath())      
    }
}

// Aggiunta di un file al progetto
for (file in files) {
    def imagePath = file.getCanonicalPath()
    
    // Utilizzo serverBuilder
    def support = ImageServerProvider.getPreferredUriImageSupport(BufferedImage.class, imagePath, "")
    def builder = support.builders.get(0)

    // Controllo che non sia null 
    if (builder == null) {
       print "Image not supported: " + imagePath
       continue
    }
    
    // Aggiunta di un immagine al progetto
    print "Adding: " + imagePath
    entry = project.addImage(builder)
    
    // Impostazione del tipo di immagine
    def imageData = entry.readImageData()
    imageData.setImageType(ImageData.ImageType.BRIGHTFIELD_H_DAB)
    entry.saveImageData(imageData)
    
    // Creazione di un "thubnail", se possibile
    var img = ProjectCommands.getThumbnailRGB(imageData.getServer());
    entry.setThumbnail(img)
    
    // Aggiunta nome dell'imagine (il filename)
    entry.setImageName(file.getName())
}

// Propagazione delle modifiche alla directory del progetto
project.syncChanges()
