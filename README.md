# AIMAGoR
AIMAGoR - Artificial IMAges GeneratoR - for Linux only - NEXT GEN

![AIMAGoR-panel](https://raw.githubusercontent.com/vitforlinux-gimp/AIMAGoR/refs/heads/main/images/AIMAGoR-panel.jpg)

![AIMAGoR-suggest](https://raw.githubusercontent.com/vitforlinux-gimp/AIMAGoR/refs/heads/main/images/AIMAGoR-suggest.jpg)

![AIMAGoR-viewer](https://raw.githubusercontent.com/vitforlinux-gimp/AIMAGoR/refs/heads/main/images/AIMAGoR-viewer.jpg)

(ITALIAN)

Ho cominciato a sviluppare AIGoR per scherzo, per avere un giocattolo per creare immagini con Pollinations.Ai.

Poi la cosa mi ha preso la mano, ho anche fatto un corso di AI tentuto da [Giovanni Occhipinti di DigiFare.net](https://www.digifare.net/), che mi ha dato alcune idee su come semplificare la creazione di immagini con AI.

Poi ho pensato che il nome AIGoR è spiritoso, ma poco originale, allora ho pensato che cambiarlo per la nuova generazione era una buona idea.

Ora l'aggiunta di nuove funzioni sarà introdotta in AIMAGoR

Questo programma è stato scritto in Yad e Bash usa solo Wget per generare immagini attraverso [https://pollinations.ai](https://pollinations.ai/)

È possibile aprire con Gimp (se installato) le immagini, o salvarle in una cartella in formato .jpg

L'installer oltre a scaricare il programma e installarlo in /usr/local/bin installa anche un file .desktop in /usr/share/applications così da avere un pulsante in Menu > Grafica

La nuova funzione suggest prompt permette di avere suggerimenti direttamente dall'AI.

La funzione Style permette di scegliere alcuni stili predefiniti.

La funzione autosave permette di avere i file direttamante salvati nella cartella /home/nome_utente/AIGMAGoR

(ENGLISH)

I started developing Aigor as a joke, to have a toy to create images with Pollinations.ai.

Then the thing took my hand, I also made a course of the Ai tempted by [Giovanni Occhipinti to DigiFare.net](https://www.digifare.net/), which gave me some ideas on how to simplify the creation of images with AI.

Then I thought that the name Aigor is witty, but not very original, then I thought that changing it for the new generation was a good idea.

Now the addition of new functions will be introduced in AIMAGoR

This program was written in Yad, and Bash only uses Wget to generate images through [https://pollinations.ai](https://pollinations.ai/)

You can open images with Gimp (if installed), or save them to a folder in .jpg format

In addition to downloading the program and install it in/usr/local/bin, the Installer also install an .Desktop in/usr/share/applications file so as to have a button on the menu> graphics.

The new suggest prompt function allows you to have suggestions directly from the AI.

The Style function allows you to choose some predefined styles.

The Autosave function allows you to have direct files saved in the/home/user_name/AIMAGoR folder


(DEPENDENCIES - DIPENDENZE)

You need to install Yad and WGET

È necessario installare Yad e WGET


(INSTALL - INSTALLAZIONE)

Copy the code below in the Linux terminal and press the Enter button, the administration password will be requested.

Copia il codice qui sotto nel terminale di Linux e premi il tasto Invio, sarà chiesta la password di amministazione.

```
wget https://raw.githubusercontent.com/vitforlinux-gimp/aimagor/refs/heads/main/aimagor-installer.sh && chmod a+x ./aimagor-installer.sh && ./aimagor-installer.sh

```
