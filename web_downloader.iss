[Setup]
AppName=YT Downloader
AppVersion=1.0.1
AppPublisher=Aditya Kumar
DefaultDirName={autopf}\YTDownloader
DefaultGroupName=YT Downloader
OutputDir=dist_installer
OutputBaseFilename=YTDownloaderInstaller
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\YTDownloader.exe


[Files]
Source: "YTDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YT Downloader"; Filename: "{app}\YTDownloader.exe"
Name: "{commondesktop}\YT Downloader"; Filename: "{app}\YTDownloader.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\YTDownloader.exe"; Description: "Launch YT Downloader"; Flags: nowait postinstall skipifsilent

[VersionInfo]
FileVersion=1.0.1
ProductVersion=1.0.1
FileDescription=YT Downloader App by Aditya
LegalCopyright=© 2025 Aditya Kumar
