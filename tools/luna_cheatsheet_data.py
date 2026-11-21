# Data for the luna-send cheatsheet guide (rendered by build-pages.py).
# Every command below was checked against the WEBOS-LUNA-SEND-ATLAS catalog
# (the service + method exist and the access level is real) and reworded /
# regrouped by task.  Tags: "" normal, "d" dangerous, "root" needs root,
# "sub" subscription (streams until Ctrl-C), "pub" uses luna-send-pub,
# "sh" a plain shell line (not luna-send).  Each (title, cmd, tag) is one entry;
# the command count is the number of luna-send / luna-send-pub lines.

# SEO
TITLE = "webOS luna-send command cheatsheet for LG TVs (hacking, debugging, development)"
DESC = ("A big webOS luna-send command cheatsheet for rooted LG TVs: power, apps, sound, settings, "
        "screenshots, IR and more, for hacking, debugging and development.")
KEYWORDS = ["webos command cheatsheet", "luna-send commands", "lg tv luna-send", "webos hacking commands",
            "webos debugging", "webos development commands", "luna service bus commands", "lg webos ssh commands",
            "rooted lg tv commands", "luna-send cheatsheet"]
CARD = ("luna-send command cheatsheet",
        "A big, grouped list of real luna-send commands for a rooted LG TV")
H1 = "webOS luna-send command cheatsheet"
LEAD = ("A grouped, copy-paste list of real <code>luna-send</code> commands for a rooted LG webOS TV: "
        "power, apps, sound, picture, notifications, inputs, channels, settings, network, Bluetooth, "
        "storage, screenshots, developer tools, IR and the service menu.  Every command is checked "
        "against the <a href=\"/luna-atlas/\">Luna Atlas</a> catalog.")

# [ (section_title, intro_html, [ (title, command, tag), ... ]) ]
SHEET = [
("Running commands", "<code>luna-send</code> is on every webOS TV; you reach it over SSH on a rooted set or in Developer Mode.  <code>-n 1</code> waits for one reply then exits, <code>-f</code> prints it formatted, and <code>-i</code> stays subscribed and streams updates until Ctrl-C.  A few calls are only on the <b>public</b> bus, where you use <code>luna-send-pub</code>.  Private methods need root; Developer Mode's shell is not root.", [
    ("Call shape", '''luna-send -n 1 -f luna://<service>/<method> '{"key":"value"}' ''', ""),
    ("Stay subscribed to updates", '''luna-send -i -f luna://<service>/<method> '{"subscribe":true}' ''', "sub"),
]),

("Power & screen", "Read or watch the power state, turn just the panel off while sound keeps playing, and reboot.", [
    ("Watch the power state live", '''luna-send -i -f luna://com.webos.service.tvpower/power/getPowerState '{"subscribe":true}' ''', "sub"),
    ("Turn the panel off (backlight only, audio keeps playing)", '''luna-send -n 1 -f luna://com.webos.service.tvpower/power/turnOffScreen '{}' ''', ""),
    ("Turn the panel back on", '''luna-send -n 1 -f luna://com.webos.service.tvpower/power/turnOnScreen '{}' ''', ""),
    ("Screen off that sticks like the remote's own option", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"picture","settings":{"energySaving":"screen_off"}}' ''', ""),
    ("Open the energy-saving / screensaver screen", '''luna-send-pub -n 1 -f luna://com.webos.service.applicationManager/launch '{"id":"com.webos.app.tvhotkey","params":{"activateType":"energy-saving-mode"}}' ''', "pub"),
    ("Reboot the TV", '''luna-send -n 1 -f luna://com.webos.service.tvpower/power/reboot '{"reason":"luna-send"}' ''', "d"),
    ("Power the TV off", '''luna-send -n 1 -f luna://com.webos.service.tvpower/power/powerOff '{"reason":"luna-send"}' ''', "d"),
    ("\"Stealth\" reboot (not logged the way a normal reboot is)", '''luna-send -a webosbrew -f -n 1 luna://com.webos.service.sleep/shutdown/machineReboot '{"reason":"remoteKey"}' ''', "d"),
]),

("Apps & launcher", "See what's on screen, launch and close apps, and list what's installed.", [
    ("Show the foreground app, and each time it changes", '''luna-send -i -f luna://com.webos.applicationManager/getForegroundAppInfo '{"subscribe":true}' ''', "sub"),
    ("Launch an app by ID", '''luna-send -n 1 -f luna://com.webos.applicationManager/launch '{"id":"com.webos.app.browser"}' ''', "d"),
    ("Launch an app with parameters", '''luna-send -n 1 -f luna://com.webos.applicationManager/launch '{"id":"com.webos.app.livetv","params":{"channelId":"..."}}' ''', "d"),
    ("Jump to the Home launcher", '''luna-send -n 1 -f luna://com.webos.applicationManager/launch '{"id":"com.webos.app.home","params":{"activateType":"powerOn"}}' ''', "d"),
    ("Close an app by ID", '''luna-send -n 1 -f luna://com.webos.applicationManager/closeByAppId '{"id":"com.webos.app.hdmi3"}' ''', ""),
    ("List every installed app", '''luna-send -n 1 -f luna://com.webos.applicationManager/listApps '{}' ''', "root"),
    ("List the launcher tiles (launch points)", '''luna-send -n 1 -f luna://com.webos.applicationManager/listLaunchPoints '{}' ''', ""),
    ("Get one app's metadata", '''luna-send -n 1 -f luna://com.webos.applicationManager/getAppInfo '{"id":"com.webos.app.livetv"}' ''', ""),
    ("Check whether an app is running", '''luna-send -n 1 -f luna://com.webos.applicationManager/getAppStatus '{"appId":"com.webos.app.browser","appInfo":true}' ''', "root"),
]),

("Volume & sound", "Volume, mute and sound output.  Some read methods are on the public bus; the write methods under <code>com.webos.service.audio/master</code> are public too.", [
    ("Read the volume and mute state", '''luna-send -n 1 -f luna://com.webos.audio/getVolume '{}' ''', ""),
    ("Watch the volume live", '''luna-send -i -f luna://com.webos.service.audio/master/getVolume '{"subscribe":true}' ''', "sub"),
    ("Volume up one step", '''luna-send -n 1 -f luna://com.webos.audio/volumeUp '{}' ''', ""),
    ("Volume down one step", '''luna-send -n 1 -f luna://com.webos.audio/volumeDown '{}' ''', ""),
    ("Set an exact volume", '''luna-send -n 1 -f luna://com.webos.service.audio/master/setVolume '{"volume":15}' ''', ""),
    ("Mute / unmute", '''luna-send -n 1 -f luna://com.webos.audio/setMuted '{"muted":true}' ''', ""),
    ("Mute one output only", '''luna-send -n 1 -f luna://com.webos.service.audiooutput/audio/volume/muteSoundOut '{"mute":true,"soundOutput":"tv_external_speaker"}' ''', ""),
    ("Read the current sound output", '''luna-send -n 1 -f luna://com.webos.service.audio/getSoundOutput '{}' ''', ""),
    ("Change the sound output (e.g. to a soundbar)", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"sound","settings":{"soundOutput":"external_optical"}}' ''', ""),
]),

("Picture & display", "Read and change picture settings through the settings service.", [
    ("Read the picture mode", '''luna-send -n 1 -f luna://com.webos.settingsservice/getSystemSettings '{"category":"picture","keys":["pictureMode"]}' ''', ""),
    ("Set the picture mode", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"picture","settings":{"pictureMode":"expert1"}}' ''', ""),
    ("Set the OLED light / backlight level", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"picture","settings":{"backlight":"80"}}' ''', ""),
    ("Turn energy saving off (brightest picture)", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"picture","settings":{"energySaving":"off"}}' ''', ""),
    ("List the allowed values for a setting", '''luna-send -n 1 -f luna://com.webos.settingsservice/getSystemSettingValues '{"category":"picture","key":"pictureMode"}' ''', ""),
]),

("Notifications", "Put a message on the screen.  The friendliest place to start.", [
    ("Show a toast (small corner banner)", '''luna-send -n 1 -f luna://com.webos.notification/createToast '{"message":"Hello from luna-send"}' ''', ""),
    ("Toast with a tap action", '''luna-send -n 1 -f luna://com.webos.notification/createToast '{"message":"Open the browser","onclick":{"appId":"com.webos.app.browser"}}' ''', ""),
    ("Show an alert box with buttons", '''luna-send -n 1 -f luna://com.webos.notification/createAlert '{"message":"Pick one","buttons":[{"label":"OK","focus":true},{"label":"Cancel"}]}' ''', ""),
    ("Close a toast", '''luna-send -n 1 -f luna://com.webos.notification/closeToast '{"toastId":"..."}' ''', ""),
    ("Close an alert", '''luna-send -n 1 -f luna://com.webos.notification/closeAlert '{"alertId":"..."}' ''', ""),
]),

("Inputs & sources", "List HDMI and other inputs, and add an app so it shows up under \"All Inputs\".", [
    ("List the inputs and what's connected", '''luna-send -n 1 -f luna://com.webos.service.eim/getAllInputStatus '{}' ''', ""),
    ("Add an app as an input tile", '''luna-send-pub -n 1 luna://com.webos.service.eim/addDevice '{"appId":"com.example.app","pigImage":""}' ''', "pub"),
    ("Remove an app's input tile", '''luna-send-pub -n 1 luna://com.webos.service.eim/deleteDevice '{"appId":"com.example.app","pigImage":""}' ''', "pub"),
]),

("TV, channels & recording", "The tuner side: channel lists, channel info and starting a recording.", [
    ("List the channels", '''luna-send -n 1 -f luna://com.webos.service.iepg/getChannelList '{}' ''', "root"),
    ("Get info for one channel", '''luna-send -n 1 -f luna://com.webos.service.iepg/getChannelInfo '{"channelId":"...","type":2}' ''', "root"),
    ("Start a DVR recording to USB", '''luna-send -n 1 -f luna://com.webos.service.utp.dvr/record/startProgramRecord '{"channelId":"...","duration":2880,"quality":"record_quality_high","recordingMode":"recording_direct","storagePath":"/tmp/usb/sda/sda1"}' ''', "d"),
]),

("System info", "Model, firmware, build and device properties.", [
    ("Model, webOS version and build date", '''luna-send -n 1 -f luna://com.webos.service.systemservice/osInfo/query '{"parameters":["webos_manufacturing_version","webos_release","webos_build_datetime"]}' ''', ""),
    ("Model, firmware and SDK version", '''luna-send -n 1 -f luna://com.webos.service.tv.systemproperty/getSystemInfo '{"keys":["modelName","firmwareVersion","sdkVersion"]}' ''', ""),
    ("Device properties (serial, board, IDs)", '''luna-send -n 1 -f luna://com.webos.service.systemservice/deviceInfo/query '{"parameters":["device_name","board_type"]}' ''', ""),
    ("Read platform config values", '''luna-send -n 1 -f luna://com.webos.service.config/getConfigs '{"configNames":["tv.model.sysType"]}' ''', ""),
]),

("Settings: read & write", "The settings service reads and changes almost everything the on-screen menus do.  Categories include <code>picture</code>, <code>sound</code>, <code>option</code>, <code>time</code> and <code>network</code>.", [
    ("Read any setting", '''luna-send -n 1 -f luna://com.webos.settingsservice/getSystemSettings '{"category":"option","keys":["country"]}' ''', ""),
    ("Write a setting", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"option","settings":{"audioGuidance":"off"}}' ''', ""),
    ("Read a setting's description / allowed values", '''luna-send -n 1 -f luna://com.webos.settingsservice/getSystemSettingDesc '{"category":"picture","keys":["pictureMode"]}' ''', ""),
    ("Stop the 15-minute no-signal auto power-off", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"time","settings":{"autoOff15Min":"off"}}' ''', ""),
    ("Turn off mobile (SSAP) access after rooting", '''luna-send -n 1 -f luna://com.webos.settingsservice/setSystemSettings '{"category":"network","settings":{"allowMobileDeviceAccess":false}}' ''', ""),
]),

("Network & Wi-Fi", "Connection state for wired and wireless.", [
    ("Overall connection status (wired + Wi-Fi)", '''luna-send -n 1 -f luna://com.webos.service.connectionmanager/getStatus '{}' ''', ""),
    ("Watch the connection status live", '''luna-send -i -f luna://com.webos.service.connectionmanager/getStatus '{"subscribe":true}' ''', "sub"),
    ("Wi-Fi status", '''luna-send -n 1 -f luna://com.webos.service.wifi/getstatus '{}' ''', ""),
]),

("Bluetooth", "Adapter and device status for the TV's Bluetooth stack.", [
    ("Bluetooth adapter status", '''luna-send -n 1 -f luna://com.webos.service.bluetooth2/adapter/getStatus '{}' ''', ""),
    ("Paired / connected device status", '''luna-send -n 1 -f luna://com.webos.service.bluetooth2/device/getStatus '{}' ''', ""),
]),

("Storage & USB", "List attached drives and browse their contents.", [
    ("List attached storage (USB, internal)", '''luna-send -n 1 -f luna://com.webos.service.attachedstoragemanager/listDevices '{}' ''', ""),
    ("List a folder on a device", '''luna-send -n 1 -f luna://com.webos.service.attachedstoragemanager/listFolderContents '{"deviceId":"...","path":"/","limit":100}' ''', "root"),
]),

("Screenshots", "Capture the current frame to a file.  The service was renamed from <code>com.webos.service.tv.capture</code> to <code>com.webos.service.capture</code> on newer sets; the call is the same.  Formats: BMP, JPG, PNG, RGB, RGBA, YUV422.  Methods: DISPLAY (the UI), SCREEN_WITH_SOURCE_VIDEO, VIDEO, GRAPHIC.  Defaults to 960x540.", [
    ("Capture to /tmp (default size)", '''luna-send -n 1 -f luna://com.webos.service.capture/executeOneShot '{"path":"/tmp/capture.png","method":"DISPLAY","format":"PNG"}' ''', ""),
    ("Capture at full 4K", '''luna-send -n 1 -f luna://com.webos.service.capture/executeOneShot '{"path":"/tmp/capture.png","method":"DISPLAY","format":"PNG","width":3840,"height":2160}' ''', ""),
    ("Capture with the date in the filename", '''luna-send -n 1 -f luna://com.webos.service.capture/executeOneShot "{\\"path\\":\\"/home/root/cap_$(date +%Y-%m-%d_%H-%M-%S).png\\",\\"method\\":\\"DISPLAY\\",\\"format\\":\\"PNG\\"}" ''', ""),
    ("Older sets (renamed service)", '''luna-send -n 1 -f luna://com.webos.service.tv.capture/executeOneShot '{"path":"/tmp/capture.png","method":"DISPLAY","format":"PNG"}' ''', "root"),
    ("Alternate compositor capture", '''luna-send -n 1 -f luna://com.webos.surfacemanager/captureCompositorOutput '{"output":"/tmp/screenshot.jpg","format":"JPG"}' ''', ""),
]),

("Developer & logging", "Install apps, turn on developer logs and read them.  The <code>PmLogCtl</code> and <code>tail</code> lines are plain shell, not luna-send.", [
    ("Install an IPK already on the TV", '''luna-send -i -f luna://com.webos.appInstallService/dev/install '{"id":"com.example.app","ipkUrl":"/media/internal/downloads/app.ipk","subscribe":true}' ''', "sub"),
    ("Turn on developer logging", '''luna-send -n 1 -f luna://com.webos.service.config/setConfigs '{"configs":{"system.collectDevLogs":true}}' ''', "d"),
    ("Set one component's log level", '''PmLogCtl set <context> debug''', "sh"),
    ("Follow the logs for an app", '''tail -F /var/log/messages | grep <app-or-context>''', "sh"),
    ("Turn Developer Mode on (reboots the TV)", '''luna-send -n 1 -f luna://com.palm.service.devmode/setDevMode '{"enabled":true}' ''', "d"),
    ("Read the Developer Mode passphrase", '''luna-send -n 1 -f luna://com.palm.service.devmode/getPassphrase '{}' ''', ""),
]),

("IR & the Magic Remote", "Blast IR at other gear through the TV or Magic Remote.", [
    ("Send an IR command (e.g. power a soundbar)", '''luna-send -n 1 -f luna://com.webos.service.irdbmanager/sendIrCommand '{"buttonState":"single","deviceType":"audio","keyCode":"IR_KEY_POWER"}' ''', "root"),
    ("Magic Remote IR-blaster status", '''luna-send -n 1 -f luna://com.webos.service.mrcu/getStatus '{}' ''', ""),
    ("Push raw IR codes through the Magic Remote", '''luna-send -n 1 -f luna://com.webos.service.mrcu/ir/pushIrCodes '{"codes":[]}' ''', "root"),
]),

("Service menu & factory tools", "The factory / service menu (ezAdjust, inStart, inStop).  These change deep, undocumented settings and one of them is a factory reset, so treat the whole section as dangerous and know how to undo what you change.", [
    ("Open a service-menu screen", '''luna-send -n 1 -f luna://com.webos.service.applicationManager/launch '{"id":"com.webos.app.factorywin","params":{"id":"executeFactory","irKey":"inStart"}}' ''', "d"),
]),
]

# Extra notes rendered after the service-menu section (not counted as commands)
SERVICE_MENU_NOTE = ("<b>irKey values:</b> <code>ezAdjust</code> (service menu 1), <code>inStart</code> "
    "(service menu 2), <code>inStop</code> (factory reset), <code>pCheck</code> (picture test), "
    "<code>sCheck</code> (audio test), <code>tilt</code> (white screen, locks the remote until a reboot), "
    "<code>powerOnly</code>.  Service menus ask for a code; the common LG one is widely published as "
    "<code>0413</code>.  Wrong values here can leave the TV mis-calibrated or wipe it, so write down "
    "every value before you change it.")

FAQ = [
    ("What is luna-send?",
     "The command-line client every LG webOS TV ships to talk to the Luna Service Bus, the internal message bus that power, apps, picture, sound, Wi-Fi, notifications and hundreds of other services listen on.  A call is a URI (<code>luna://service/method</code>) plus a JSON payload."),
    ("Do I need a rooted TV to run these?",
     "To run them, yes: a rooted TV with SSH from the Homebrew Channel, or LG's Developer Mode.  Browsing the <a href=\"/luna-atlas/\">catalog</a> needs nothing.  Private methods need root; Developer Mode's shell is not root."),
    ("What's the difference between luna-send and luna-send-pub?",
     "<code>luna-send</code> uses the private bus, <code>luna-send-pub</code> the public one.  A few methods are only registered on the public bus, so they need <code>luna-send-pub</code>.  When a call says permission denied on one, try the other."),
    ("Are these safe to run?",
     "Most just read or nudge the TV.  The ones marked dangerous change power, launch or reset state, and the service-menu and factory calls can mis-calibrate or wipe the set.  Running one is exactly as safe as typing the same <code>luna-send</code> yourself: read what it does first."),
    ("Where can I find every command, not just these?",
     "In the <a href=\"/luna-atlas/\">Luna Atlas</a> catalog: thousands of methods across hundreds of services, each with its parameters, access level and a command to run.  This cheatsheet is the handful people reach for most."),
    ("How were these verified?",
     "Every command here was checked against the Luna Atlas catalog so the service and method exist and the access level is right, then grouped by task and reworded.  Parameter shapes come from the catalog, community cheatsheets and real bus traffic."),
]
