#!/usr/bin/env python3
"""Builds the Nook marketing site in four languages from one source.

Run it from the repo root:

    python3 docs/build_site.py

It writes index.html (English) plus nl/, de/ and fr/ into docs/. The legal
pages (privacy.html, support.html, story.html) are hand-written and are NOT
touched: privacy.html in particular is baked into the shipped app and into App
Store Connect, so its URL can never move.

Why a generator rather than four hand-kept files: the moment a section is added
in one language and forgotten in another, the site starts lying about the
product in whichever language you speak. Here the structure comes from one
template and only the words differ.
"""

import pathlib
import html

OUT = pathlib.Path(__file__).parent

# Language order is the order of the switcher. English lives at the root
# because that is the URL already in circulation.
LANGS = ["en", "nl", "de", "fr"]
LANG_NAME = {"en": "EN", "nl": "NL", "de": "DE", "fr": "FR"}
APP_STORE_URL = "https://apps.apple.com/app/id0000000000"   # fill in once live

ARCH = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true">'
        '<path class="mark-arch" fill-rule="evenodd" d="M5.6 60 L5.6 30.4 '
        'A26.4 26.4 0 0 1 58.4 30.4 L58.4 60 L53.1 60 L53.1 30.5 '
        'A21.1 21.1 0 0 0 10.9 30.5 L10.9 60 Z"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Cpath fill-rule='evenodd' fill='%23C68A34' d='M5.6 60 L5.6 30.4 A26.4 26.4 0 0 1 "
           "58.4 30.4 L58.4 60 L53.1 60 L53.1 30.5 A21.1 21.1 0 0 0 10.9 30.5 L10.9 60 Z'/%3E%3C/svg%3E")

# Small inline icon set. Stroke-based so they inherit the accent colour.
ICONS = {
    "eyeoff": "M2 2l20 20M6.7 6.8A10.6 10.6 0 001 12s4 7 11 7a10.5 10.5 0 005.3-1.4M9.9 5.2A11.6 11.6 0 0112 5c7 0 11 7 11 7a20.7 20.7 0 01-3.2 4.2M9.9 9.9a3 3 0 004.2 4.2",
    "cover":  "M3 5.5h18v13H3zM6 9.5h9M6 13.5h6M17.5 14.5v3M16 17.5h3",
    "lock":   "M6 10V7.5a6 6 0 1112 0V10M4.5 10h15v10.5h-15z",
    "spark":  "M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z",
    "cloud":  "M2 2l20 20M7.5 18h9.8a4 4 0 00.9-7.9A6 6 0 007.3 8.2M6.6 10.1A4 4 0 007 18",
    "text":   "M5 6h14M5 12h9M5 18h11",
    "ipad":   "M5 2.5h14v19H5zM10.5 19h3",
    "coffee": "M4 8h13v5.5A5.5 5.5 0 0111.5 19h-2A5.5 5.5 0 014 13.5zM17 9.5h1.8a2.4 2.4 0 010 4.8H17M4.5 22h12",
}


def icon(name, size=20):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


# ---------------------------------------------------------------- content

C = {}

C["en"] = {
    "locale": "en", "dir": "ltr",
    "title": "Nook: the private journal that never leaves your phone",
    "desc": "A calm, private place for your notes. Privacy Typing blacks out every word as you write, and the whole list can be covered too. No cloud, no account, no tracking.",
    "nav": {"features": "Features", "privacy": "Privacy", "pricing": "Pricing", "support": "Support",
            "menu_note": "Every feature works offline, on your device.", "get": "Get Nook"},
    "mega": [
        ("eyeoff", "Privacy Typing", "Each word blacks out the moment you finish it."),
        ("cover", "Hide your notes", "Cover every title and preview in the list."),
        ("lock", "Face ID and folder locks", "Your face, your passcode, your rules."),
        ("spark", "Writing prompts", "Fifty one of them, written by hand."),
        ("text", "Rich text and colour", "Titles, lists, checkboxes, your own palette."),
        ("ipad", "iPad and widgets", "A two column desk, and quick capture."),
    ],
    "hero": {
        "eyebrow": "Private by design",
        "h1_a": "The journal you can write in", "h1_b": "with someone beside you",
        "lede": "Nook keeps your writing on your phone and out of sight. Every word blacks out as you type, and your whole list can be covered until Face ID says otherwise.",
        "cta_small": "Download on the", "cta_big": "App Store",
        "trust": ["No account", "No cloud", "No tracking", "Pay once"],
    },
    "rows": [
        {"eyebrow": "Privacy Typing", "h": "Nobody reads over your shoulder",
         "p": "Turn it on and each word blacks out the moment you finish it. The word under your cursor stays faintly visible, just for you, so you can still see what you are doing. Tap the eye and the page comes back.",
         "bul": ["The person beside you sees black bars", "You still see the word you are writing", "Remembered per note, never a global switch"],
         "img": "privacy-typing.jpg", "alt": "A note with every word blacked out except the one being typed."},
        {"eyebrow": "New in 1.1", "h": "Even the list gives nothing away",
         "p": "Protecting the page while you write it does little if your list still reads like a table of contents. Cover every title and preview behind glass, and bring them back with Face ID, all at once or one note at a time.",
         "bul": ["A covered note never renders its text at all", "Uncover a single note, leave the rest covered", "Everything covers itself again when you leave the app"],
         "img": "hidden.jpg", "alt": "The home screen with every note title and preview covered."},
        {"eyebrow": "Nothing to collect", "h": "There is no server to send it to",
         "p": "Nook has no networking code beyond the purchase. Not disabled, not opt in: absent. No account, no sync, no analytics, no crash reporting. The App Store privacy label reads Data Not Collected because there is genuinely nothing to collect.",
         "bul": ["Everything is stored on your device", "Encrypted backups only you can open", "Spotlight is off until you turn it on"],
         "img": "home-light.jpg", "alt": "The Nook home screen with folders and notes."},
    ],
    "grid_h": "Everything you would want from a notebook",
    "grid_p": "And nothing you would not.",
    "grid": [
        ("lock", "Face ID or a passcode", "Lock the app, and put a separate passcode on any folder."),
        ("text", "Write properly", "Titles, headings, bold, italic, lists, checkboxes and dividers."),
        ("spark", "Prompts for empty days", "Fifty one hand written prompts, grouped by what you might need."),
        ("ipad", "Made for iPad", "Folders down one side, your pages beside them."),
        ("cloud", "Works on a plane", "No connection needed, because there is nothing to connect to."),
        ("coffee", "One payment", "No subscription, no account, no upsell later."),
    ],
    "prompts_h": "For the days you do not know where to start",
    "prompts_p": "Fifty one prompts, written by hand and grouped by what you might need: today, how you are, the people in your head, looking back, looking ahead, the quiet ones, the unsaid ones. On devices with Apple Intelligence, Nook can also suggest a topic or reflect on an entry, using on device models that make no network call.",
    "ipad_h": "A whole desk on iPad",
    "ipad_p": "Folders down one side, your pages beside them, so a week of writing is visible at a glance. The same app, the same promise.",
    "price_h": "Buy us a coffee, once",
    "price_p": "Try everything free for seven days. If Nook earns a place on your phone, one payment keeps it there for life.",
    "price_amount": "$5.99", "price_once": "One time, not a subscription",
    "price_bul": ["Seven days free, everything unlocked", "No account and no email needed", "Your notes stay readable if you never buy"],
    "faq_h": "Questions people ask",
    "faq": [
        ("Where are my notes stored?", "On your device, and nowhere else. Nook has no server and no cloud storage. If you want a copy, you can export an encrypted backup and keep it wherever you like."),
        ("What happens after the seven days?", "Your notes stay readable and exportable. Creating and editing pause until the one time purchase, which never expires."),
        ("Can I move my notes to a new phone?", "Yes. Export an encrypted backup, choose a passphrase, and open it on the new device. Without the passphrase nobody can open that file, including us."),
        ("Does Privacy Typing hide my notes from VoiceOver?", "No, and that is deliberate. Privacy Typing is visual only, so the person who relies on VoiceOver, the owner of the notes, keeps full access."),
    ],
    "cta_h": "Somewhere to be honest",
    "cta_p": "Free for seven days. No account, nothing to sign up for.",
    "foot": {"product": "Product", "company": "Company", "legal": "Legal",
             "tagline": "A calm, private corner for your notes. They never leave your phone.",
             "story": "Our story", "privacy": "Privacy policy", "support": "Support",
             "features": "Features", "pricing": "Pricing",
             "made": "Made by AI Adviesbureau B.V. in the Netherlands"},
}

C["nl"] = {
    "locale": "nl", "dir": "ltr",
    "title": "Nook: het privédagboek dat je telefoon nooit verlaat",
    "desc": "Een rustige, private plek voor je notities. Privacy Typing lakt elk woord zwart terwijl je schrijft, en je hele lijst kun je ook afdekken. Geen cloud, geen account, geen tracking.",
    "nav": {"features": "Functies", "privacy": "Privacy", "pricing": "Prijs", "support": "Hulp",
            "menu_note": "Alles werkt offline, op je eigen toestel.", "get": "Nook halen"},
    "mega": [
        ("eyeoff", "Privacy Typing", "Elk woord wordt zwart zodra je het afmaakt."),
        ("cover", "Notities afschermen", "Dek elke titel en voorbeeldregel in de lijst af."),
        ("lock", "Face ID en mapsloten", "Jouw gezicht, jouw code, jouw regels."),
        ("spark", "Schrijfprompts", "Eenenvijftig stuks, met de hand geschreven."),
        ("text", "Opmaak en kleur", "Titels, lijsten, vinkjes, je eigen palet."),
        ("ipad", "iPad en widgets", "Een bureau met twee kolommen, en snel vastleggen."),
    ],
    "hero": {
        "eyebrow": "Privé van opzet",
        "h1_a": "Het dagboek waarin je durft te schrijven", "h1_b": "met iemand naast je",
        "lede": "Nook houdt je woorden op je telefoon en uit het zicht. Elk woord wordt zwart terwijl je typt, en je hele lijst blijft afgedekt tot Face ID anders beslist.",
        "cta_small": "Download in de", "cta_big": "App Store",
        "trust": ["Geen account", "Geen cloud", "Geen tracking", "Eenmalig betalen"],
    },
    "rows": [
        {"eyebrow": "Privacy Typing", "h": "Niemand leest over je schouder mee",
         "p": "Zet het aan en elk woord wordt zwart zodra je het afmaakt. Het woord onder je cursor blijft vaag zichtbaar, alleen voor jou, zodat je nog steeds ziet wat je doet. Tik op het oog en de pagina komt terug.",
         "bul": ["Degene naast je ziet zwarte balken", "Jij ziet nog wel het woord dat je schrijft", "Per notitie onthouden, geen globale schakelaar"],
         "img": "privacy-typing.jpg", "alt": "Een notitie waarin elk woord zwart is, behalve het woord dat wordt getypt."},
        {"eyebrow": "Nieuw in 1.1", "h": "Ook je lijst geeft niets prijs",
         "p": "De pagina beschermen tijdens het schrijven helpt weinig als je lijst nog leest als een inhoudsopgave. Dek elke titel en voorbeeldregel af achter glas, en haal ze terug met Face ID: allemaal tegelijk, of één notitie per keer.",
         "bul": ["Een afgedekte notitie bouwt haar tekst helemaal niet op", "Ontgrendel er één, de rest blijft afgedekt", "Alles dekt zichzelf weer af zodra je de app verlaat"],
         "img": "hidden.jpg", "alt": "Het beginscherm met alle titels en voorbeeldregels afgedekt."},
        {"eyebrow": "Niets te verzamelen", "h": "Er is geen server om het heen te sturen",
         "p": "Nook heeft geen netwerkcode buiten de aankoop om. Niet uitgezet, niet optioneel: afwezig. Geen account, geen synchronisatie, geen statistieken, geen crashrapporten. Het privacylabel in de App Store zegt Data Not Collected, omdat er werkelijk niets te verzamelen valt.",
         "bul": ["Alles staat op je eigen toestel", "Versleutelde back-ups die alleen jij kunt openen", "Spotlight staat uit tot jij hem aanzet"],
         "img": "home-light.jpg", "alt": "Het beginscherm van Nook met mappen en notities."},
    ],
    "grid_h": "Alles wat je van een notitieboek wilt",
    "grid_p": "En niets wat je er niet in wilt.",
    "grid": [
        ("lock", "Face ID of een toegangscode", "Zet het slot op de app, en een aparte code op elke map."),
        ("text", "Fatsoenlijk schrijven", "Titels, koppen, vet, cursief, lijsten, vinkjes en scheidingslijnen."),
        ("spark", "Prompts voor lege dagen", "Eenenvijftig met de hand geschreven prompts, gegroepeerd naar wat je nodig hebt."),
        ("ipad", "Gemaakt voor iPad", "Mappen aan de ene kant, je pagina's ernaast."),
        ("cloud", "Werkt in het vliegtuig", "Geen verbinding nodig, want er is niets om verbinding mee te maken."),
        ("coffee", "Eén betaling", "Geen abonnement, geen account, later geen bijverkoop."),
    ],
    "prompts_h": "Voor de dagen dat je niet weet waar te beginnen",
    "prompts_p": "Eenenvijftig prompts, met de hand geschreven en gegroepeerd naar wat je nodig kunt hebben: vandaag, hoe het met je gaat, de mensen in je hoofd, terugkijken, vooruitkijken, de stille, de onuitgesprokene. Op toestellen met Apple Intelligence kan Nook ook een onderwerp voorstellen of op een notitie reflecteren, met modellen op het toestel zelf die geen enkele netwerkoproep doen.",
    "ipad_h": "Een heel bureau op de iPad",
    "ipad_p": "Mappen aan de ene kant, je pagina's ernaast, zodat een week schrijven in één oogopslag zichtbaar is. Dezelfde app, dezelfde belofte.",
    "price_h": "Trakteer ons op een koffie, één keer",
    "price_p": "Probeer alles zeven dagen gratis. Verdient Nook een plek op je telefoon, dan houdt één betaling hem daar voorgoed.",
    "price_amount": "Eenmalig", "price_once": "Geen abonnement, de App Store toont je eigen prijs",
    "price_bul": ["Zeven dagen gratis, alles beschikbaar", "Geen account en geen e-mailadres nodig", "Je notities blijven leesbaar als je nooit koopt"],
    "faq_h": "Vragen die mensen stellen",
    "faq": [
        ("Waar staan mijn notities?", "Op je eigen toestel, en nergens anders. Nook heeft geen server en geen cloudopslag. Wil je een kopie, dan exporteer je een versleutelde back-up en bewaar je die waar je wilt."),
        ("Wat gebeurt er na die zeven dagen?", "Je notities blijven leesbaar en exporteerbaar. Nieuwe maken en bewerken pauzeert tot de eenmalige aankoop, die nooit verloopt."),
        ("Kan ik mijn notities naar een nieuwe telefoon halen?", "Ja. Exporteer een versleutelde back-up, kies een wachtwoordzin en open die op het nieuwe toestel. Zonder die zin kan niemand het bestand openen, wij ook niet."),
        ("Verbergt Privacy Typing mijn notities ook voor VoiceOver?", "Nee, en dat is bewust. Privacy Typing werkt alleen visueel, zodat wie op VoiceOver leunt, de eigenaar van de notities, volledige toegang houdt."),
    ],
    "cta_h": "Ergens waar je eerlijk kunt zijn",
    "cta_p": "Zeven dagen gratis. Geen account, niets om je voor aan te melden.",
    "foot": {"product": "Product", "company": "Bedrijf", "legal": "Juridisch",
             "tagline": "Een rustige, private hoek voor je notities. Ze verlaten je telefoon nooit.",
             "story": "Ons verhaal", "privacy": "Privacybeleid", "support": "Hulp",
             "features": "Functies", "pricing": "Prijs",
             "made": "Gemaakt door AI Adviesbureau B.V. in Nederland"},
}

C["de"] = {
    "locale": "de", "dir": "ltr",
    "title": "Nook: das private Tagebuch, das dein iPhone nie verlässt",
    "desc": "Ein ruhiger, privater Ort für deine Notizen. Privacy Typing schwärzt jedes Wort beim Schreiben, und die ganze Liste lässt sich ebenfalls abdecken. Keine Cloud, kein Konto, kein Tracking.",
    "nav": {"features": "Funktionen", "privacy": "Datenschutz", "pricing": "Preis", "support": "Hilfe",
            "menu_note": "Alles funktioniert offline, auf deinem Gerät.", "get": "Nook holen"},
    "mega": [
        ("eyeoff", "Privacy Typing", "Jedes Wort wird geschwärzt, sobald du es beendest."),
        ("cover", "Notizen abdecken", "Verdecke jeden Titel und jede Vorschau in der Liste."),
        ("lock", "Face ID und Ordnersperren", "Dein Gesicht, dein Code, deine Regeln."),
        ("spark", "Schreibimpulse", "Einundfünfzig Stück, von Hand geschrieben."),
        ("text", "Text und Farbe", "Titel, Listen, Häkchen, deine eigene Palette."),
        ("ipad", "iPad und Widgets", "Ein Schreibtisch mit zwei Spalten, und schnelles Notieren."),
    ],
    "hero": {
        "eyebrow": "Privat von Grund auf",
        "h1_a": "Das Tagebuch, in das du schreibst", "h1_b": "auch wenn jemand neben dir sitzt",
        "lede": "Nook behält deine Worte auf deinem iPhone und außer Sichtweite. Jedes Wort wird beim Tippen geschwärzt, und deine ganze Liste bleibt abgedeckt, bis Face ID etwas anderes sagt.",
        "cta_small": "Laden im", "cta_big": "App Store",
        "trust": ["Kein Konto", "Keine Cloud", "Kein Tracking", "Einmal zahlen"],
    },
    "rows": [
        {"eyebrow": "Privacy Typing", "h": "Niemand liest über deine Schulter",
         "p": "Schalte es ein und jedes Wort wird geschwärzt, sobald du es beendest. Das Wort unter deinem Cursor bleibt schwach sichtbar, nur für dich, damit du siehst, was du tust. Tippe auf das Auge und die Seite kommt zurück.",
         "bul": ["Wer neben dir sitzt, sieht schwarze Balken", "Du siehst weiterhin das Wort, das du schreibst", "Pro Notiz gemerkt, kein globaler Schalter"],
         "img": "privacy-typing.jpg", "alt": "Eine Notiz, in der jedes Wort geschwärzt ist, außer dem gerade getippten."},
        {"eyebrow": "Neu in 1.1", "h": "Auch die Liste verrät nichts",
         "p": "Die Seite beim Schreiben zu schützen bringt wenig, wenn die Liste weiter wie ein Inhaltsverzeichnis liest. Decke jeden Titel und jede Vorschau hinter Glas ab und hole sie mit Face ID zurück, alle auf einmal oder eine Notiz nach der anderen.",
         "bul": ["Eine abgedeckte Notiz baut ihren Text gar nicht erst auf", "Eine einzelne öffnen, der Rest bleibt abgedeckt", "Alles deckt sich wieder ab, sobald du die App verlässt"],
         "img": "hidden.jpg", "alt": "Der Startbildschirm mit abgedeckten Titeln und Vorschauen."},
        {"eyebrow": "Nichts zu sammeln", "h": "Es gibt keinen Server, an den etwas ginge",
         "p": "Nook hat außer dem Kauf keinen Netzwerkcode. Nicht deaktiviert, nicht optional: nicht vorhanden. Kein Konto, keine Synchronisierung, keine Analyse, keine Absturzberichte. Das Datenschutzlabel im App Store sagt Data Not Collected, weil es wirklich nichts zu sammeln gibt.",
         "bul": ["Alles liegt auf deinem Gerät", "Verschlüsselte Backups, die nur du öffnen kannst", "Spotlight bleibt aus, bis du es einschaltest"],
         "img": "home-light.jpg", "alt": "Der Startbildschirm von Nook mit Ordnern und Notizen."},
    ],
    "grid_h": "Alles, was du von einem Notizbuch willst",
    "grid_p": "Und nichts, was du nicht willst.",
    "grid": [
        ("lock", "Face ID oder ein Code", "Sperre die App, und lege auf jeden Ordner einen eigenen Code."),
        ("text", "Richtig schreiben", "Titel, Überschriften, fett, kursiv, Listen, Häkchen und Trennlinien."),
        ("spark", "Impulse für leere Tage", "Einundfünfzig von Hand geschriebene Impulse, nach Bedarf gruppiert."),
        ("ipad", "Für das iPad gemacht", "Ordner an der einen Seite, deine Seiten daneben."),
        ("cloud", "Funktioniert im Flugzeug", "Keine Verbindung nötig, weil es nichts zu verbinden gibt."),
        ("coffee", "Eine Zahlung", "Kein Abo, kein Konto, später kein Nachverkauf."),
    ],
    "prompts_h": "Für die Tage, an denen du nicht weißt, wo du anfangen sollst",
    "prompts_p": "Einundfünfzig Impulse, von Hand geschrieben und danach gruppiert, was du gerade brauchen könntest: heute, wie es dir geht, die Menschen in deinem Kopf, zurückblicken, vorausschauen, die leisen, die unausgesprochenen. Auf Geräten mit Apple Intelligence kann Nook auch ein Thema vorschlagen oder über einen Eintrag nachdenken, mit Modellen auf dem Gerät, die keinen einzigen Netzwerkaufruf machen.",
    "ipad_h": "Ein ganzer Schreibtisch auf dem iPad",
    "ipad_p": "Ordner an der einen Seite, deine Seiten daneben, sodass eine Woche Schreiben auf einen Blick sichtbar ist. Dieselbe App, dasselbe Versprechen.",
    "price_h": "Lade uns einmal auf einen Kaffee ein",
    "price_p": "Probiere sieben Tage lang alles aus. Verdient sich Nook einen Platz auf deinem iPhone, hält ihn eine Zahlung für immer.",
    "price_amount": "Einmalig", "price_once": "Kein Abo, den Preis zeigt dir der App Store",
    "price_bul": ["Sieben Tage frei, alles freigeschaltet", "Kein Konto und keine E-Mail nötig", "Deine Notizen bleiben lesbar, auch ohne Kauf"],
    "faq_h": "Häufige Fragen",
    "faq": [
        ("Wo liegen meine Notizen?", "Auf deinem Gerät, und sonst nirgends. Nook hat keinen Server und keinen Cloudspeicher. Willst du eine Kopie, exportierst du ein verschlüsseltes Backup und legst es ab, wo du magst."),
        ("Was passiert nach den sieben Tagen?", "Deine Notizen bleiben lesbar und exportierbar. Neu anlegen und bearbeiten pausiert bis zum einmaligen Kauf, der nie abläuft."),
        ("Kann ich meine Notizen auf ein neues iPhone holen?", "Ja. Exportiere ein verschlüsseltes Backup, wähle eine Passphrase und öffne es auf dem neuen Gerät. Ohne diese Passphrase kann niemand die Datei öffnen, wir auch nicht."),
        ("Versteckt Privacy Typing meine Notizen auch vor VoiceOver?", "Nein, und das ist Absicht. Privacy Typing wirkt nur visuell, damit wer auf VoiceOver angewiesen ist, die Eigentümerin der Notizen, vollen Zugang behält."),
    ],
    "cta_h": "Ein Ort, an dem du ehrlich sein kannst",
    "cta_p": "Sieben Tage frei. Kein Konto, nichts anzumelden.",
    "foot": {"product": "Produkt", "company": "Unternehmen", "legal": "Rechtliches",
             "tagline": "Eine ruhige, private Ecke für deine Notizen. Sie verlassen dein iPhone nie.",
             "story": "Unsere Geschichte", "privacy": "Datenschutz", "support": "Hilfe",
             "features": "Funktionen", "pricing": "Preis",
             "made": "Gemacht von AI Adviesbureau B.V. in den Niederlanden"},
}

C["fr"] = {
    "locale": "fr", "dir": "ltr",
    "title": "Nook : le journal privé qui ne quitte jamais votre iPhone",
    "desc": "Un endroit calme et privé pour vos notes. Privacy Typing masque chaque mot pendant que vous écrivez, et toute la liste peut être couverte. Pas de cloud, pas de compte, pas de suivi.",
    "nav": {"features": "Fonctions", "privacy": "Confidentialité", "pricing": "Prix", "support": "Aide",
            "menu_note": "Tout fonctionne hors ligne, sur votre appareil.", "get": "Obtenir Nook"},
    "mega": [
        ("eyeoff", "Privacy Typing", "Chaque mot se masque dès que vous le terminez."),
        ("cover", "Couvrir vos notes", "Masquez chaque titre et chaque aperçu de la liste."),
        ("lock", "Face ID et dossiers verrouillés", "Votre visage, votre code, vos règles."),
        ("spark", "Invites d'écriture", "Cinquante et une, écrites à la main."),
        ("text", "Mise en forme et couleur", "Titres, listes, cases à cocher, votre palette."),
        ("ipad", "iPad et widgets", "Un bureau à deux colonnes, et la saisie rapide."),
    ],
    "hero": {
        "eyebrow": "Privé par conception",
        "h1_a": "Le journal où vous osez écrire", "h1_b": "même avec quelqu'un à côté",
        "lede": "Nook garde vos mots sur votre iPhone et hors de vue. Chaque mot se masque pendant que vous tapez, et toute votre liste reste couverte jusqu'à ce que Face ID en décide autrement.",
        "cta_small": "Télécharger dans l'", "cta_big": "App Store",
        "trust": ["Pas de compte", "Pas de cloud", "Pas de suivi", "Un seul paiement"],
    },
    "rows": [
        {"eyebrow": "Privacy Typing", "h": "Personne ne lit par dessus votre épaule",
         "p": "Activez-le et chaque mot se masque dès que vous le terminez. Le mot sous votre curseur reste faiblement visible, rien que pour vous, afin que vous voyiez encore ce que vous faites. Touchez l'œil et la page revient.",
         "bul": ["La personne à côté de vous voit des barres noires", "Vous voyez encore le mot que vous écrivez", "Retenu note par note, jamais un réglage global"],
         "img": "privacy-typing.jpg", "alt": "Une note dont chaque mot est masqué, sauf celui en cours de saisie."},
        {"eyebrow": "Nouveau en 1.1", "h": "Même la liste ne révèle rien",
         "p": "Protéger la page pendant que vous écrivez sert peu si votre liste se lit encore comme une table des matières. Couvrez chaque titre et chaque aperçu derrière du verre, et ramenez-les avec Face ID, tous d'un coup ou une note à la fois.",
         "bul": ["Une note couverte ne construit jamais son texte", "Ouvrez-en une, les autres restent couvertes", "Tout se recouvre dès que vous quittez l'app"],
         "img": "hidden.jpg", "alt": "L'écran d'accueil avec tous les titres et aperçus couverts."},
        {"eyebrow": "Rien à collecter", "h": "Il n'y a aucun serveur où l'envoyer",
         "p": "Nook n'a aucun code réseau au delà de l'achat. Ni désactivé, ni optionnel : absent. Pas de compte, pas de synchronisation, pas de statistiques, pas de rapports de plantage. L'étiquette de confidentialité de l'App Store indique Data Not Collected, parce qu'il n'y a vraiment rien à collecter.",
         "bul": ["Tout est stocké sur votre appareil", "Des sauvegardes chiffrées que vous seul pouvez ouvrir", "Spotlight reste éteint jusqu'à ce que vous l'activiez"],
         "img": "home-light.jpg", "alt": "L'écran d'accueil de Nook avec ses dossiers et ses notes."},
    ],
    "grid_h": "Tout ce qu'on attend d'un carnet",
    "grid_p": "Et rien de ce qu'on n'attend pas.",
    "grid": [
        ("lock", "Face ID ou un code", "Verrouillez l'app, et mettez un code distinct sur chaque dossier."),
        ("text", "Écrire correctement", "Titres, intertitres, gras, italique, listes, cases et séparateurs."),
        ("spark", "Des invites pour les jours vides", "Cinquante et une invites écrites à la main, groupées par besoin."),
        ("ipad", "Pensé pour l'iPad", "Les dossiers d'un côté, vos pages à côté."),
        ("cloud", "Marche en avion", "Aucune connexion requise, puisqu'il n'y a rien à connecter."),
        ("coffee", "Un paiement", "Pas d'abonnement, pas de compte, aucune vente additionnelle ensuite."),
    ],
    "prompts_h": "Pour les jours où vous ne savez pas par où commencer",
    "prompts_p": "Cinquante et une invites, écrites à la main et groupées selon ce dont vous pourriez avoir besoin : aujourd'hui, comment vous allez, les gens dans votre tête, regarder en arrière, regarder devant, les silencieuses, les non dites. Sur les appareils compatibles Apple Intelligence, Nook peut aussi proposer un sujet ou réfléchir à une entrée, avec des modèles embarqués qui ne font aucun appel réseau.",
    "ipad_h": "Un bureau entier sur iPad",
    "ipad_p": "Les dossiers d'un côté, vos pages à côté, pour voir une semaine d'écriture d'un seul regard. La même app, la même promesse.",
    "price_h": "Offrez-nous un café, une fois",
    "price_p": "Essayez tout gratuitement pendant sept jours. Si Nook mérite une place sur votre iPhone, un paiement l'y garde à vie.",
    "price_amount": "Paiement unique", "price_once": "Pas d'abonnement, l'App Store affiche votre prix",
    "price_bul": ["Sept jours gratuits, tout est débloqué", "Ni compte ni adresse e-mail", "Vos notes restent lisibles même sans achat"],
    "faq_h": "Questions fréquentes",
    "faq": [
        ("Où sont stockées mes notes ?", "Sur votre appareil, et nulle part ailleurs. Nook n'a ni serveur ni stockage cloud. Pour en garder une copie, exportez une sauvegarde chiffrée et rangez-la où vous voulez."),
        ("Que se passe-t-il après les sept jours ?", "Vos notes restent lisibles et exportables. La création et la modification s'interrompent jusqu'à l'achat unique, qui n'expire jamais."),
        ("Puis-je transférer mes notes vers un nouvel iPhone ?", "Oui. Exportez une sauvegarde chiffrée, choisissez une phrase secrète et ouvrez-la sur le nouvel appareil. Sans cette phrase, personne ne peut ouvrir le fichier, nous non plus."),
        ("Privacy Typing masque-t-il aussi mes notes à VoiceOver ?", "Non, et c'est volontaire. Privacy Typing n'agit que visuellement, pour que la personne qui dépend de VoiceOver, la propriétaire des notes, garde un accès complet."),
    ],
    "cta_h": "Un endroit où être honnête",
    "cta_p": "Sept jours gratuits. Pas de compte, rien à créer.",
    "foot": {"product": "Produit", "company": "Entreprise", "legal": "Mentions légales",
             "tagline": "Un coin calme et privé pour vos notes. Elles ne quittent jamais votre iPhone.",
             "story": "Notre histoire", "privacy": "Confidentialité", "support": "Aide",
             "features": "Fonctions", "pricing": "Prix",
             "made": "Réalisé par AI Adviesbureau B.V. aux Pays-Bas"},
}


# --------------------------------------------------------------- template

def rel(lang, path=""):
    """Link from a page in `lang` back to a root-level file."""
    return ("../" if lang != "en" else "") + path


def page(lang):
    c = C[lang]
    e = html.escape
    up = rel(lang)
    home = up if lang == "en" else up

    def lang_href(l):
        if lang == "en":
            return "" if l == "en" else l + "/"
        return "../" if l == "en" else "../" + l + "/"

    CURRENT = ' aria-current="true"'
    langbar = "".join(
        '<a href="%s" hreflang="%s"%s>%s</a>'
        % (lang_href(l), l, CURRENT if l == lang else "", LANG_NAME[l])
        for l in LANGS)

    mega = "".join(
        f'<a class="mega-item" href="#features"><span class="ico">{icon(i)}</span>'
        f'<span><b>{e(t)}</b><span>{e(d)}</span></span></a>'
        for i, t, d in c["mega"])

    rows = ""
    for n, r in enumerate(c["rows"]):
        flip = " flip" if n % 2 else ""
        bul = "".join(f"<li>{e(b)}</li>" for b in r["bul"])
        rows += f'''
    <section class="section{' alt' if n % 2 else ''}" {'id="privacy"' if n == 2 else ''}>
      <div class="wrap">
        <div class="row{flip}">
          <div>
            <span class="eyebrow">{e(r["eyebrow"])}</span>
            <h2>{e(r["h"])}</h2>
            <p class="lede">{e(r["p"])}</p>
            <ul class="clean">{bul}</ul>
          </div>
          <div class="row-art hero-art">
            <img class="device" src="{up}img/{r["img"]}" alt="{e(r["alt"])}" loading="lazy" width="540" height="1174">
          </div>
        </div>
      </div>
    </section>'''

    tiles = "".join(
        f'<div class="tile"><div class="ico">{icon(i)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, t, d in c["grid"])

    faq = "".join(
        f"<details{' open' if k == 0 else ''}><summary>{e(q)}</summary><p>{e(a)}</p></details>"
        for k, (q, a) in enumerate(c["faq"]))

    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="https://ai-adviesbureau.github.io/Nook-Private-Notes/'
        f'{"" if l == "en" else l + "/"}">' for l in LANGS)

    store = (f'<a class="appstore" href="{APP_STORE_URL}">'
             f'<span class="glyph" aria-hidden="true">&#63743;</span>'
             f'<span><small>{e(c["hero"]["cta_small"])}</small><b>{e(c["hero"]["cta_big"])}</b></span></a>')

    return f'''<!DOCTYPE html>
<html lang="{c["locale"]}" dir="{c["dir"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c["title"])}</title>
<meta name="description" content="{e(c["desc"])}">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["desc"])}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://ai-adviesbureau.github.io/Nook-Private-Notes/img/hidden.jpg">
<meta name="twitter:card" content="summary_large_image">
{alts}<link rel="alternate" hreflang="x-default" href="https://ai-adviesbureau.github.io/Nook-Private-Notes/">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{up}style.css">
<link rel="stylesheet" href="{up}site.css">
</head>
<body class="site">

<nav class="nav">
  <div class="nav-inner">
    <a class="logo" href="{home}">{ARCH}<span>Nook</span></a>
    <div class="nav-spacer"></div>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" data-menu><span></span></button>
    <ul class="nav-links" data-links>
      <li>
        <button class="nav-link" aria-expanded="false" data-mega>{e(c["nav"]["features"])}<i class="chev"></i></button>
        <div class="mega">
          <div class="mega-grid">{mega}</div>
          <div class="mega-foot"><span>{e(c["nav"]["menu_note"])}</span><span class="lang">{langbar}</span></div>
        </div>
      </li>
      <li><a class="nav-link" href="#privacy">{e(c["nav"]["privacy"])}</a></li>
      <li><a class="nav-link" href="#pricing">{e(c["nav"]["pricing"])}</a></li>
      <li><a class="nav-link" href="{up}support.html">{e(c["nav"]["support"])}</a></li>
      <li><a class="btn primary" href="{APP_STORE_URL}">{e(c["nav"]["get"])}</a></li>
    </ul>
  </div>
</nav>

<header class="hero-wrap">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">{e(c["hero"]["eyebrow"])}</span>
        <h1>{e(c["hero"]["h1_a"])} <span class="accent">{e(c["hero"]["h1_b"])}</span>.</h1>
        <p class="lede">{e(c["hero"]["lede"])}</p>
        <div class="badges">{store}</div>
        <div class="trust">{"".join(f"<span>{e(t)}</span>" for t in c["hero"]["trust"])}</div>
      </div>
      <div class="hero-art">
        <div class="device-pair">
          <img class="device device-tilt" src="{up}img/home-light.jpg" alt="{e(c["rows"][2]["alt"])}" width="540" height="1174">
          <img class="device device-tilt-r" src="{up}img/privacy-typing.jpg" alt="{e(c["rows"][0]["alt"])}" width="540" height="1174">
        </div>
      </div>
    </div>
  </div>
</header>

<main id="features">
{rows}

  <section class="section">
    <div class="wrap center">
      <h2>{e(c["grid_h"])}</h2>
      <p class="lede">{e(c["grid_p"])}</p>
      <div class="grid">{tiles}</div>
    </div>
  </section>

  <section class="section alt">
    <div class="wrap">
      <div class="row flip">
        <div>
          <h2>{e(c["prompts_h"])}</h2>
          <p class="lede">{e(c["prompts_p"])}</p>
        </div>
        <div class="row-art hero-art">
          <img class="device" src="{up}img/prompts.jpg" alt="{e(c["mega"][3][1])}" loading="lazy" width="540" height="1174">
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap center">
      <h2>{e(c["ipad_h"])}</h2>
      <p class="lede">{e(c["ipad_p"])}</p>
      <div style="margin-top:34px">
        <img class="device" src="{up}img/ipad.jpg" alt="{e(c["ipad_h"])}" loading="lazy" width="900" height="1200" style="max-width:820px;margin-inline:auto;border-radius:26px">
      </div>
    </div>
  </section>

  <section class="section alt" id="pricing">
    <div class="wrap center">
      <h2>{e(c["price_h"])}</h2>
      <p class="lede">{e(c["price_p"])}</p>
      <div class="price-card">
        <div class="amount">{e(c["price_amount"])}</div>
        <div class="once">{e(c["price_once"])}</div>
        <ul class="clean">{"".join(f"<li>{e(b)}</li>" for b in c["price_bul"])}</ul>
        {store}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="center"><h2>{e(c["faq_h"])}</h2></div>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <section class="section tight">
    <div class="wrap">
      <div class="cta">
        <h2>{e(c["cta_h"])}</h2>
        <p class="lede center" style="margin-inline:auto">{e(c["cta_p"])}</p>
        <div class="badges" style="justify-content:center">{store}</div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="{home}">{ARCH}<span>Nook</span></a>
        <p style="color:var(--muted);font-size:14.5px;max-width:30ch;margin-top:12px">{e(c["foot"]["tagline"])}</p>
      </div>
      <div>
        <h4>{e(c["foot"]["product"])}</h4>
        <ul>
          <li><a href="#features">{e(c["foot"]["features"])}</a></li>
          <li><a href="#pricing">{e(c["foot"]["pricing"])}</a></li>
          <li><a href="{APP_STORE_URL}">{e(c["nav"]["get"])}</a></li>
        </ul>
      </div>
      <div>
        <h4>{e(c["foot"]["company"])}</h4>
        <ul>
          <li><a href="{up}story.html">{e(c["foot"]["story"])}</a></li>
          <li><a href="{up}support.html">{e(c["foot"]["support"])}</a></li>
        </ul>
      </div>
      <div>
        <h4>{e(c["foot"]["legal"])}</h4>
        <ul>
          <li><a href="{up}privacy.html">{e(c["foot"]["privacy"])}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>{e(c["foot"]["made"])} &middot; &copy; 2026</span>
      <span class="lang">{langbar}</span>
    </div>
  </div>
</footer>

<script>
// Progressive enhancement only: the menu already opens on hover and on
// keyboard focus through CSS. This adds tap support and Escape.
document.querySelectorAll('[data-mega]').forEach(function (b) {{
  b.addEventListener('click', function (e) {{
    e.preventDefault();
    var m = b.nextElementSibling, open = m.dataset.open === 'true';
    m.dataset.open = String(!open);
    b.setAttribute('aria-expanded', String(!open));
  }});
}});
document.addEventListener('keydown', function (e) {{
  if (e.key !== 'Escape') return;
  document.querySelectorAll('.mega[data-open="true"]').forEach(function (m) {{
    m.dataset.open = 'false';
    m.previousElementSibling.setAttribute('aria-expanded', 'false');
  }});
}});
var t = document.querySelector('[data-menu]'), l = document.querySelector('[data-links]');
if (t) t.addEventListener('click', function () {{
  var open = l.dataset.open === 'true';
  l.dataset.open = String(!open);
  t.setAttribute('aria-expanded', String(!open));
}});
</script>
</body>
</html>
'''


def main():
    for lang in LANGS:
        target = OUT / "index.html" if lang == "en" else OUT / lang / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(lang), encoding="utf-8")
        print(f"  {target.relative_to(OUT)}  {len(target.read_text(encoding='utf-8'))//1024} kB")
    print(f"\n{len(LANGS)} talen gebouwd. Vergeet APP_STORE_URL niet zodra de app live is.")


if __name__ == "__main__":
    main()
