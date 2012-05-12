; WARNING: This script has been created by py2exe. Changes to this script
; will be overwritten the next time py2exe is run!

[Languages]
Name: "de"; MessagesFile: "compiler:Languages\\German.isl"

[Setup]
AppName=TouchIT Log
AppVerName=TouchIT Log v1.0
DefaultDirName={pf}\Arcus EDS\TouchIT Log
DefaultGroupName=TouchIT Log
Compression=bzip

[Files]
Source: "build\*.*"; DestDir: "{app}\prog"; Flags: ignoreversion recursesubdirs
Source: "data\TestData\*.*"; DestDir: "{app}\TestData"; Flags: ignoreversion recursesubdirs


[Icons]
Name: "{group}\TouchIT Log"; Filename: "{app}\prog\main.exe"
Name: "{group}\Uninstall TouchIT Log"; Filename: "{uninstallexe}"
