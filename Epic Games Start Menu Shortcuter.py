import os

outputPath = os.path.expandvars("%ProgramData%\Microsoft\Windows\Start Menu\Programs\Epic Games")

# check admin permissions
testFilePath = os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs\test")
try:
    urlFile = open(testFilePath, "w")
except PermissionError:
    print("PermissionError:\nTry to run the program as an administrator")
    while True:
        pass
else:
    urlFile.close()
    os.remove(testFilePath)

if (not os.path.exists(outputPath)):
    os.makedirs(outputPath)

print()
# remove old shortcuts
for f in os.listdir(outputPath):
    try:
        os.remove(f"{outputPath}\{f}")
    except Exception:
        print(f'file "{f}" cannot be deleted')

# all Epic manifest files
maniFiles = []

maniPath = os.path.expandvars('%ProgramData%\Epic\EpicGamesLauncher\Data\Manifests')
print(f'Reading Epic manifest files from "{maniPath}"...')
print()
for path in os.scandir(maniPath):
    if path.is_file():
        maniFiles.append(path.name)

print(
    f"Adding shortcuts to Start Menu from {len(maniFiles)} Epic manifest files...")
added = 0
for i in range(len(maniFiles)):
    with open(f"{maniPath}\{maniFiles[i]}", 'r') as file:
        fileLines = file.readlines()
        LaunchExecutable = DisplayName = InstallLocation = CatalogNamespace = CatalogItemId = AppName = ""

        for j in range(len(fileLines)):
            if (fileLines[j].find("LaunchExecutable") != -1):
                LaunchExecutable = fileLines[j].split('"')[3]

            elif (fileLines[j].find("DisplayName") != -1):
                DisplayName = fileLines[j].split('"')[3].translate(
                    {ord(i): None for i in '#%&}{<>*$?!:@+`|='})
                DisplayName = DisplayName.encode(
                    'ascii', errors='ignore').decode()

            elif (fileLines[j].find("InstallLocation") != -1):
                InstallLocation = fileLines[j].split('"')[3].replace(
                    r"\\", r'\\'[0]).replace("/", r"\\"[0])

        # for url
            elif (fileLines[j].find("CatalogNamespace") != -1):
                CatalogNamespace = fileLines[j].split('"')[3]

            elif (fileLines[j].find("CatalogItemId") != -1):
                CatalogItemId = fileLines[j].split('"')[3]

            elif (fileLines[j].find("AppName") != -1):
                AppName = fileLines[j].split('"')[3]

        print(f"{DisplayName} ← {maniFiles[i]}", end="")
        exePath = f"{InstallLocation}\{LaunchExecutable}"

        if (LaunchExecutable == "" or DisplayName == "" or InstallLocation == "" or CatalogNamespace == "" or CatalogItemId == "" or AppName == ""):
            skip = True
            print(" skipped")
        else:
            skip = False
            print()

    if (not skip):
        with open(f"{outputPath}\{DisplayName}.url", "w") as urlFile:
            urlFile.write('[{000214A0-0000-0000-C000-000000000046}]\n')
            urlFile.write('Prop3=19,0\n')
            urlFile.write('[InternetShortcut]\n')
            urlFile.write('IDList=\n')
            urlFile.write('IconIndex=0\n')
            urlFile.write(f'WorkingDirectory={InstallLocation}\n')
            urlFile.write(f'URL=com.epicgames.launcher://apps/{CatalogNamespace}%3A{CatalogItemId}%3A{AppName}?action=launch&silent=true\n')
            urlFile.write(f'IconFile={exePath}\n')
        added += 1

print()
print(f"{added} Shortcuts successfuly added")
print()
input("---PRESS ENTER TO EXIT---")
