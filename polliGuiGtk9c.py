"""
crea un programma in python e pygtk per creare immagini tramite image.pollinations.ai/prompt il programma deve avere:  
- la possibilità di regolare la dimensione orizzontale e verticale separatamente anche oltre il limite di 1024x1024 pixel  
- il valore width deve essere collegato a '&width=' e il valore height essere collegato al valore '&height='  
- un campo seed con un numero intero generato a caso con vicino il pulsante reset che rinnoverà il numero se nella casella viane impostato il
 numero zero sarà generato un nuovo numero a caso ogni volta  
- l immagine viene ridimensionata automaticamente con python pil per avere i valori indicati mantenendo le proporzioni  
- il campo di inserimento del prompt deve essere alto tre righe e avere una barra di scorrimento  
- ci deve essere un menu a tendina con almeno 20 stili artistici di immagine, il primo sarà none che non inserirà nessuno stile, gli altri avr
anno nell url la parola style davanti  
- ci deve essere un menu a tendina con almeno 20 tipologie di immagine, il primo sarà none che non inserirà nessuna tipologia, gli altri avranno
 nell url la parola type davanti  
- ci deve essere un menu a tendina con almeno 20 tipologie di colori, il primo sarà none che non inserirà nessuna tipologia di colore, gli altri
 avranno nell url le parole color type davanti  
- ci deve essere un menu a tendina con almeno 20 tipologie di luce, il primo sarà none che non inserirà nessuna tipologia di luce, gli altri avr
anno nell url le parole light type davanti  
- ci deve essere un menu a tendina con almeno 20 tipi di ripresa, il primo sarà non ne non inserirà nessun tipo di ripresa, gli altri avranno
 nell url le parole shoot type davanti  
- ci deve essere un menu a tendina tipo di sfondo, il primo sarà none che non inserirà nessun tipo di sfondo, gli altri avranno nell url le
 parole background type davanti  
- ci deve essere un opzione no watermark configurata su true collegata alla coda dell url '&nologo=true'  
- ci deve essere un opzione enhance configurata su false collegata alla coda dell url '&enhance='  
- ci deve essere un opzione safe configurata su false collegata alla coda dell url '&safe='  
- ci deve essere un opzione no feed configurata su false collegata alla coda dell url '&nofeed='  
- ci deve essere un menu a tendina con la scelta tra i due modelli di generazione flux e turbo collegati al termine dell url a '&model='  
- ci deve essere un pulsante per la generazione dell immagine che deve segnalare la generazione in corso e tra parentesi il numero del tentativo
  
- ci deve essere un opzione preselezionata su true per salvare automaticamente l immagine nella cartella dell utente polliGuiGtk che se non es
iste verra creata  
- in caso di errore nella generazione il programma deve fare automaticamente tre tentativi per generarla a ogni tentativo aumenta il timeout di 
10 secondi, il primo 25 secondi, poi 50 e poi 75  
- ci deve essere un pulsante per aprire l'immagine in Gimp  
- ci deve essere un pulsante per salvare l immagine  
- ci deve essere un pulsante per chiudere il programma  
- ci deve essere un visualizzatore per l immagine generata con le barre di scorrimento  
- deve anche essere possibile copiare l immagine per incollarla in un programma, la copia deve essere possibile ugualemente se si usa windows
 linux o mac  
- l'url ottenuta deve anche essere stampata in un print per permettere il debug da terminale  
- questo prompt deve essere aggiunto al programma in un commento multilinea senza modifiche  
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import urllib.request
import urllib.parse
import io
import os
import platform
import subprocess
import random
import datetime
from PIL import Image

try:
    import win32clipboard
    import win32con
except ImportError:
    win32clipboard = None

# Define your options with at least 20 entries each (some example values)
OPTIONS_STYLE = [
    ("none", ""), 
    ("impressionist", "style impressionist"),
    ("cubist", "style cubist"),
    ("abstract", "style abstract"),
    ("surrealist", "style surrealist"),
    ("photorealistic", "style photorealistic"),
    ("pop art", "style pop art"),
    ("pixel art", "style pixel art"),
    ("watercolor", "style watercolor"),
    ("expressionism", "style expressionism"),
    ("minimalist", "style minimalist"),
    ("renaissance", "style renaissance"),
    ("baroque", "style baroque"),
    ("gothic", "style gothic"),
    ("realism", "style realism"),
    ("modern", "style modern"),
    ("digital art", "style digital art"),
    ("vaporwave", "style vaporwave"),
    ("anime", "style anime"),
    ("futuristic", "style futuristic"),
    ("comic", "style comic"),
    ("political satire cartoon", "style political satire cartoon"),
    ("Pablo Picasso", "style Pablo Picasso"),
    ("Maurice Utrillo", "style Maurice Utrillo"),
    ("Leonardo da Vinci drawing", "style Leonardo da Vinci drawing"),
    ("Leonardo da Vinci painting", "style Leonardo da Vinci painting"),
    ("Walt Disney", "style Walt Disney"),
    ("Tamara De Lempicka Art", "style Tamara De Lempicka Art"),
    ("Ai Weiwei", "style Ai Weiwei"),
    ("Antonio Ligabue", "style Antonio Ligabue"),
    ("Edgar Degas", "style Edgar Degas"),
    ("Edvard Munch", "style Edvard Munch"),
    ("Frida Kahlo", "style Frida Kahlo"),
    ("Gustav Klimt", "style Gustav Klimt"),
    ("Hueronymus Bosch", "style Hueronymus Bosch"),
    ("Joan Mirò", "style Joan Mirò"),
    ("Michelangelo Merisi Caravaggio", "style Michelangelo Merisi Caravaggio"),
    ("Vincent van Gogh", "style Vincent van Gogh"),
    ("William Turner", "style William Turner"),
    ("acrilyc paint", "style acrilyc paint"),
    ("Papier Machè", "style Papier Machè"),
    ("Cute Creature", "style Cute Creature"),
    ("Peter Max", "style Peter Max"),
    ("Andy Warhol", "style Andy Warhol"),
    ("Jean-Michel Basquiat", "style Jean-Michel Basquiat"),
    ("Keith Haring", "style Keith Haring"),
    ("Pop Art poster", "style Pop Art poster"),
    ("Norman Rockwell paintings", "style Norman Rockwell paintings"),
    ("decoupage", "style decoupage"),
    ("tropical paradise", "style tropical paradise"),
    ("1960 sci-fi magazine", "style 1960 sci-fi magazine"),
    ("1960 cartoon", "style 1960 cartoon"),
    ("post-impressionist painting", "style post-impressionist painting"),
    ("Colors like National Geographic", "style Colors like National Geographic"),
    ("Colors like HDR", "style Colors like HDR"),
    ("Color Splash", "style Color Splash"),
    ("3d Objects", "style 3d Objects"),
    ("Action Figure", "style Action Figure"),
    ("Caricatural Action Figure", "style Caricatural Action Figure"),
    ("clockwork toy", "style clockwork toy"),
    ("steampunk", "style steampunk"),
    ("cyberpunk", "style cyberpunk"),
    ("solarpunk", "style solarpunk"),
    ("psychedelic poster", "style psychedelic poster"),
    ("Psychedelic Crazy Trippy painting", "style Psychedelic Crazy Trippy painting"),
    ("atlantis world", "style atlantis world"),
    ("ice world", "style ice world"),
    ("Origami Paper Art", "style Origami Paper Art"),
    ("Old Masters Art", "style Old Masters Art"),
    ("Post-apocalyptic art", "style Post-apocalyptic art"),
    ("Ukiyo-e", "style Ukiyo-e"),
    ("ASCII art", "style ASCII art"),
    ("Surrealism", "style Surrealism"),
    ("Renaissance", "style Renaissance"),
    ("Impressionism", "style Impressionism"),
    ("Bauhaus", "style Bauhaus"),
    ("Baroque", "style Baroque"),
    ("Art Nouveau", "style Art Nouveau"),
    ("Art Deco", "style Art Deco"),
    ("Abstract Expressionism", "style Abstract Expressionism"),
    ("Vector art", "style Vector art"),
    ("Street art", "style Street art"),
]


OPTIONS_TYPE = [
    ("none", ""),
    ("portrait", "type portrait"),
    ("landscape", "type landscape"),
    ("macro", "type macro"),
    ("aerial", "type aerial"),
    ("night", "type night"),
    ("action", "type action"),
    ("fantasy", "type fantasy"),
    ("still life", "type still life"),
    ("street", "type street"),
    ("wildlife", "type wildlife"),
    ("abstract", "type abstract"),
    ("sports", "type sports"),
    ("fashion", "type fashion"),
    ("architecture", "type architecture"),
    ("concept art", "type concept art"),
    ("cartoon", "type cartoon"),
    ("comic", "type comic"),
    ("film", "type film"),
    ("product", "type product"),
    ("photorealistic", "type photorealistic"),
    ("photorealistic BW", "type photorealistic BW"),
    ("Aged Color photo", "type aged color photo"),
    ("Old BW Photo", "type old bw photo"),
    ("old pencil drawing", "type old pencil drawing"),
    ("old drawing black paper and white pencil", "type old drawing black paper and white pencil"),
    ("Watercolor", "type watercolor"),
    ("Psychedelic poster", "type psychedelic poster"),
    ("1960 cartoon", "type 1960 cartoon"),
    ("Seamless pattern", "type seamless pattern"),
    ("Pop Art poster", "type pop art poster"),
    ("Vintage travel poster", "type vintage travel poster"),
    ("decoupage", "type decoupage"),
    ("painting", "type painting"),
    ("tempera", "type tempera"),
    ("oil on canvas paint", "type oil on canvas paint"),
    ("acrilyc paint", "type acrilyc paint"),
    ("batik", "type batik"),
    ("3d Objects", "type 3d objects"),
    ("steampunk", "type steampunk"),
    ("cyberpunk", "type cyberpunk"),
    ("Urban Street Art", "type urban street art"),
    ("Graffiti Street Art", "type graffiti street art"),
    ("Street Art", "type street art"),
    ("Old Masters Art", "type old masters art"),
    ("Fairy Tale Art", "type fairy tale art"),
    ("Tattoo", "type tattoo"),
    ("preparatory drawing for tattoo", "type preparatory drawing for tattoo"),
]


OPTIONS_COLOR = [
    ("none", ""),
    ("monochrome", "color type monochrome"),
    ("vibrant", "color type vibrant"),
    ("pastel", "color type pastel"),
    ("sepia", "color type sepia"),
    ("neon", "color type neon"),
    ("warm", "color type warm"),
    ("cool", "color type cool"),
    ("dark", "color type dark"),
    ("bright", "color type bright"),
    ("earth tones", "color type earth tones"),
    ("muted", "color type muted"),
    ("primary", "color type primary"),
    ("secondary", "color type secondary"),
    ("soft", "color type soft"),
    ("high contrast", "color type high contrast"),
    ("low contrast", "color type low contrast"),
    ("grayscale", "color type grayscale"),
    ("infrared", "color type infrared"),
    ("duotone", "color type duotone"),
]

OPTIONS_LIGHT = [
    ("none", ""),
    ("natural", "light type natural"),
    ("studio", "light type studio"),
    ("dramatic", "light type dramatic"),
    ("soft", "light type soft"),
    ("harsh", "light type harsh"),
    ("backlit", "light type backlit"),
    ("spotlight", "light type spotlight"),
    ("cinematic", "light type cinematic"),
    ("golden hour", "light type golden hour"),
    ("neon", "light type neon"),
    ("ambient", "light type ambient"),
    ("low key", "light type low key"),
    ("high key", "light type high key"),
    ("colored", "light type colored"),
    ("flash", "light type flash"),
    ("hard", "light type hard"),
    ("softbox", "light type softbox"),
    ("ring light", "light type ring light"),
    ("moonlight", "light type moonlight"),
]

OPTIONS_SHOOT = [
    ("none", ""),
    ("close-up", "shoot type close-up"),
    ("wide-angle", "shoot type wide-angle"),
    ("macro", "shoot type macro"),
    ("birdseye", "shoot type bird's eye"),
    ("panorama", "shoot type panorama"),
    ("long exposure", "shoot type long exposure"),
    ("fisheye", "shoot type fisheye"),
    ("portrait", "shoot type portrait"),
    ("landscape", "shoot type landscape"),
    ("aerial", "shoot type aerial"),
    ("underwater", "shoot type underwater"),
    ("night", "shoot type night"),
    ("time-lapse", "shoot type time-lapse"),
    ("street", "shoot type street"),
    ("motion blur", "shoot type motion blur"),
    ("drone", "shoot type drone"),
    ("macro", "shoot type macro"),
    ("tilt-shift", "shoot type tilt-shift"),
    ("hidden camera", "shoot type hidden camera"),
]

OPTIONS_BG = [
    ("none", ""),
    ("plain", "background type plain"),
    ("complex", "background type complex"),
    ("blurred", "background type blurred"),
    ("gradient", "background type gradient"),
    ("urban", "background type urban"),
    ("nature", "background type nature"),
    ("studio", "background type studio"),
    ("abstract", "background type abstract"),
    ("solid", "background type solid"),
    ("textured", "background type textured"),
    ("patterned", "background type patterned"),
    ("bokeh", "background type bokeh"),
    ("sky", "background type sky"),
    ("water", "background type water"),
    ("wood", "background type wood"),
    ("metal", "background type metal"),
    ("space", "background type space"),
    ("fantasy", "background type fantasy"),
    ("vintage", "background type vintage"),
]

MODELS = ["flux", "turbo"]

class PolliGuiGtkApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Pollinations.ai Image Generator - Sky Foresko")
        self.set_default_size(980, 980)
        self.set_border_width(8)

        self.image_data = None
        self.pixbuf = None
        self.current_image_path = None

        self.autosave_folder = os.path.join(os.path.expanduser("~"), "polliGuiGtk")
        if not os.path.exists(self.autosave_folder):
            try:
                os.makedirs(self.autosave_folder, exist_ok=True)
            except Exception as e:
                print(f"DEBUG: Could not create autosave folder: {e}")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        # Prompt Entry with scroll
        lbl_prompt = Gtk.Label(label="Prompt:")
        lbl_prompt.set_halign(Gtk.Align.START)
        vbox.pack_start(lbl_prompt, False, False, 0)

        self.txt_prompt = Gtk.TextView()
        self.txt_prompt.set_wrap_mode(Gtk.WrapMode.WORD)
        self.txt_prompt.set_size_request(-1, 72)
        scroll_prompt = Gtk.ScrolledWindow()
        scroll_prompt.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_prompt.set_min_content_height(72)
        scroll_prompt.add(self.txt_prompt)
        vbox.pack_start(scroll_prompt, False, False, 0)

        # Grid for controls
        grid = Gtk.Grid(column_spacing=8, row_spacing=4)
        vbox.pack_start(grid, False, False, 0)

        # Width and Height spin buttons
        lbl_width = Gtk.Label(label="Width:")
        self.spin_width = Gtk.SpinButton.new_with_range(64, 8192, 1)  # allow big sizes
        self.spin_width.set_value(1024)
        lbl_height = Gtk.Label(label="Height:")
        self.spin_height = Gtk.SpinButton.new_with_range(64, 8192, 1)
        self.spin_height.set_value(768)

        grid.attach(lbl_width, 0, 0, 1, 1)
        grid.attach(self.spin_width, 1, 0, 1, 1)
        grid.attach(lbl_height, 2, 0, 1, 1)
        grid.attach(self.spin_height, 3, 0, 1, 1)

        # Combos for options with URL prefix logic
        self.combo_style, self.opt_style = self.create_combo_with_options("Artistic Style", OPTIONS_STYLE, grid, 0,1)
        self.combo_type, self.opt_type = self.create_combo_with_options("Image Type", OPTIONS_TYPE, grid, 1,1)
        self.combo_color, self.opt_color = self.create_combo_with_options("Color Type", OPTIONS_COLOR, grid, 0,2)
        self.combo_light, self.opt_light = self.create_combo_with_options("Light Type", OPTIONS_LIGHT, grid, 1,2)
        self.combo_shoot, self.opt_shoot = self.create_combo_with_options("Shoot Type", OPTIONS_SHOOT, grid, 0,3)
        self.combo_bg, self.opt_bg = self.create_combo_with_options("Background Type", OPTIONS_BG, grid, 1,3)

        # No watermark checkbox
        self.chk_nologo = Gtk.CheckButton(label="No Watermark (&nologo=true)")
        self.chk_nologo.set_active(True)
        grid.attach(self.chk_nologo, 2, 4, 2, 1)

        # Enhance checkbox
        self.chk_enhance = Gtk.CheckButton(label="Enhance (&enhance=)")
        self.chk_enhance.set_active(False)
        grid.attach(self.chk_enhance, 0, 5, 1, 1)

        # Safe checkbox
        self.chk_safe = Gtk.CheckButton(label="Safe (&safe=)")
        self.chk_safe.set_active(False)
        grid.attach(self.chk_safe, 1, 5, 1, 1)

        # No feed checkbox
        self.chk_nofeed = Gtk.CheckButton(label="No Feed (&nofeed=)")
        self.chk_nofeed.set_active(False)
        grid.attach(self.chk_nofeed, 2, 5, 2, 1)

        # Model combo
        lbl_model = Gtk.Label(label="Model:")
        self.combo_model = Gtk.ComboBoxText()
        for m in MODELS:
            self.combo_model.append_text(m)
        self.combo_model.set_active(0)
        grid.attach(lbl_model, 0, 4, 1, 1)
        grid.attach(self.combo_model, 1, 4, 1, 1)

        # Seed input and reset button
        lbl_seed = Gtk.Label(label="Seed:")
        self.seed_entry = Gtk.Entry()
        self.seed_entry.set_width_chars(12)
        self.seed_entry.set_text(str(random.randint(1, 999999999)))
        self.btn_reset_seed = Gtk.Button(label="Reset")
        self.btn_reset_seed.connect("clicked", self.on_reset_seed)
        grid.attach(lbl_seed, 0, 6, 1, 1)
        grid.attach(self.seed_entry, 1, 6, 1, 1)
        grid.attach(self.btn_reset_seed, 2, 6, 1, 1)

        # Autosave checkbox preselected true
        self.chk_autosave = Gtk.CheckButton(label="Auto save image in ~/polliGuiGtk")
        self.chk_autosave.set_active(True)
        grid.attach(self.chk_autosave, 0, 7, 4, 1)

        # Buttons area
        hbox_buttons = Gtk.Box(spacing=10)
        vbox.pack_start(hbox_buttons, False, False, 0)

        self.btn_generate = Gtk.Button(label="Generate Image")
        self.btn_generate.connect("clicked", self.on_generate_clicked)
        hbox_buttons.pack_start(self.btn_generate, False, False, 0)

        self.btn_open_gimp = Gtk.Button(label="Open in GIMP")
        self.btn_open_gimp.set_sensitive(False)
        self.btn_open_gimp.connect("clicked", self.on_open_gimp_clicked)
        hbox_buttons.pack_start(self.btn_open_gimp, False, False, 0)

        self.btn_save = Gtk.Button(label="Save Image")
        self.btn_save.set_sensitive(False)
        self.btn_save.connect("clicked", self.on_save_clicked)
        hbox_buttons.pack_start(self.btn_save, False, False, 0)

        self.btn_copy = Gtk.Button(label="Copy Image to Clipboard")
        self.btn_copy.set_sensitive(False)
        self.btn_copy.connect("clicked", self.on_copy_clicked)
        hbox_buttons.pack_start(self.btn_copy, False, False, 0)

        self.btn_quit = Gtk.Button(label="Quit")
        self.btn_quit.connect("clicked", lambda x: Gtk.main_quit())
        hbox_buttons.pack_end(self.btn_quit, False, False, 0)

        # Image view
        self.scr_image = Gtk.ScrolledWindow()
        self.scr_image.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scr_image, True, True, 0)
        self.img_widget = Gtk.Image()
        self.scr_image.add(self.img_widget)

        self.show_all()

    def create_combo_with_options(self, label_text, options_list, grid, col, row):
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        combo = Gtk.ComboBoxText()
        for text, _val in options_list:
            combo.append_text(text)
        combo.set_active(0)
        grid.attach(label, col*2, row, 1, 1)
        grid.attach(combo, col*2+1, row, 1, 1)
        return combo, options_list

    def on_reset_seed(self, button):
        new_seed = random.randint(1, 999999999)
        self.seed_entry.set_text(str(new_seed))

    def on_generate_clicked(self, button):
        prompt = self.get_prompt_text().strip()
        if not prompt:
            self.dialog_message("Please enter a prompt.")
            return

        width = self.spin_width.get_value_as_int()
        height = self.spin_height.get_value_as_int()

        def get_val(combo, opt_list):
            idx = combo.get_active()
            if idx < 0 or idx >= len(opt_list):
                return ""
            return opt_list[idx][1]

        parts = [prompt]
        for combo, opts in [(self.combo_style, self.opt_style),
                            (self.combo_type, self.opt_type),
                            (self.combo_color, self.opt_color),
                            (self.combo_light, self.opt_light),
                            (self.combo_shoot, self.opt_shoot),
                            (self.combo_bg, self.opt_bg)]:
            val = get_val(combo, opts)
            if val:
                parts.append(val)
        full_prompt = ", ".join(parts)

        no_logo = self.chk_nologo.get_active()
        enhance = self.chk_enhance.get_active()
        safe = self.chk_safe.get_active()
        nofeed = self.chk_nofeed.get_active()
        model = self.combo_model.get_active_text()
        autosave = self.chk_autosave.get_active()

        seed_text = self.seed_entry.get_text().strip()
        seed_val = None
        if seed_text.isdigit():
            s = int(seed_text)
            if s != 0:
                seed_val = s
        else:
            self.dialog_message("Seed must be 0 or a positive integer.")
            return

        base_url = "https://image.pollinations.ai/prompt/"
        url_encoded_prompt = urllib.parse.quote_plus(full_prompt)

        params = [
            f"width={width}",
            f"height={height}&quality=high",
            f"enhance={'true' if enhance else 'false'}",
            f"safe={'true' if safe else 'false'}",
            f"nofeed={'true' if nofeed else 'false'}",
        ]
        if no_logo:
            params.append("nologo=true")
        if seed_val is not None:
            params.append(f"seed={seed_val}")
        if model in MODELS:
            params.append(f"model={model}")

        url_params = "&".join(params)
        url = f"{base_url}{url_encoded_prompt}?{url_params}"

        print("DEBUG: Image URL:", url)

        self.btn_generate.set_sensitive(False)
        timeouts=[25,50,75]
        for attempt, timeout in enumerate(timeouts, start=1):
            self.btn_generate.set_label(f"Generating... (Attempt {attempt})")
            while Gtk.events_pending():
                Gtk.main_iteration()
            try:
                with urllib.request.urlopen(url, timeout=timeout) as resp:
                    image_bytes = resp.read()
                break
            except Exception as e:
                print(f"DEBUG: Attempt {attempt} failed with timeout={timeout}s: {e}")
                if attempt == len(timeouts):
                    self.dialog_message("Failed to generate image after 3 attempts.")
                    self.btn_generate.set_label("Generate Image")
                    self.btn_generate.set_sensitive(True)
                    return

        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        except Exception as e:
            self.dialog_message(f"Failed to open image: {e}")
            self.btn_generate.set_label("Generate Image")
            self.btn_generate.set_sensitive(True)
            return

        pil_img = self.resize_keep_aspect(pil_img, width, height)

        mem = io.BytesIO()
        pil_img.save(mem, format="PNG")
        mem.seek(0)
        img_data = mem.read()
        mem.close()

        try:
            loader = GdkPixbuf.PixbufLoader.new_with_type("png")
            loader.write(img_data)
            loader.close()
            self.pixbuf = loader.get_pixbuf()
        except Exception as e:
            self.dialog_message(f"Failed to load image for display: {e}")
            self.btn_generate.set_label("Generate Image")
            self.btn_generate.set_sensitive(True)
            return

        self.image_data = img_data

        if autosave and self.image_data:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pollinations_{timestamp}.png"
            path = os.path.join(self.autosave_folder, filename)
            try:
                with open(path, "wb") as f:
                    f.write(self.image_data)
                self.current_image_path = path
                print(f"DEBUG: Image auto-saved to {path}")
            except Exception as e:
                print(f"DEBUG: Auto-save failed: {e}")

        self.img_widget.set_from_pixbuf(self.pixbuf)
        self.btn_generate.set_label("Generate Image")
        self.btn_generate.set_sensitive(True)
        self.btn_open_gimp.set_sensitive(True)
        self.btn_save.set_sensitive(True)
        self.btn_copy.set_sensitive(True)

    def resize_keep_aspect(self, img: Image.Image, target_w, target_h):
        orig_w, orig_h = img.size
        scale_w = target_w / orig_w
        scale_h = target_h / orig_h
        scale = min(scale_w, scale_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))
        return img.resize((new_w, new_h), Image.LANCZOS)

    def get_prompt_text(self):
        buf = self.txt_prompt.get_buffer()
        start_iter = buf.get_start_iter()
        end_iter = buf.get_end_iter()
        return buf.get_text(start_iter, end_iter, True)

    def on_open_gimp_clicked(self, button):
        if not self.image_data:
            self.dialog_message("No image to open.")
            return
        import tempfile
        if not self.current_image_path or not os.path.isfile(self.current_image_path):
            fd, tmp_path = tempfile.mkstemp(prefix="pollinations_", suffix=".png")
            os.close(fd)
            try:
                with open(tmp_path, "wb") as f:
                    f.write(self.image_data)
                self.current_image_path = tmp_path
            except Exception as e:
                self.dialog_message(f"Failed to save temp file for GIMP: {e}")
                return
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["gimp.exe", self.current_image_path])
            else:
                subprocess.Popen(["gimp", self.current_image_path])
        except Exception as e:
            self.dialog_message(f"Failed to open GIMP: {e}")

    def on_save_clicked(self, button):
        if not self.image_data:
            self.dialog_message("No image to save.")
            return
        dialog = Gtk.FileChooserDialog(title="Save Image As", parent=self, 
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        dialog.set_current_name("generated_image.png")
        filter_png = Gtk.FileFilter()
        filter_png.set_name("PNG Image")
        filter_png.add_pattern("*.png")
        dialog.add_filter(filter_png)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if not filename.lower().endswith(".png"):
                filename += ".png"
            try:
                with open(filename, "wb") as f:
                    f.write(self.image_data)
                self.current_image_path = filename
            except Exception as e:
                self.dialog_message(f"Failed to save image: {e}")
        dialog.destroy()

    def on_copy_clicked(self, button):
        if not self.image_data:
            self.dialog_message("No image to copy.")
            return
        system = platform.system()
        if system == "Windows" and win32clipboard:
            try:
                self.copy_image_windows()
                self.dialog_message("Image copied to clipboard.")
            except Exception as e:
                self.dialog_message(f"Failed to copy image to clipboard on Windows: {e}")
        else:
            self.copy_image_gtk()
            self.dialog_message("Image copied to clipboard.")

    def copy_image_gtk(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_image(self.pixbuf)
        clipboard.store()

    def copy_image_windows(self):
        pil_img = Image.open(io.BytesIO(self.image_data)).convert("RGBA")
        bg = Image.new("RGB", pil_img.size, (255, 255, 255))
        bg.paste(pil_img, mask=pil_img.split()[3])
        from io import BytesIO
        output = BytesIO()
        bg.save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
        finally:
            win32clipboard.CloseClipboard()

    def dialog_message(self, msg):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK,
                                   text=msg)
        dialog.run()
        dialog.destroy()

def main():
    app = PolliGuiGtkApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__=="__main__":
    main()
