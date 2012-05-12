#License: BSD 2-clause license


""" ga csv export
"""
__version__ = '1.0'
_debug = 0


import csv


def compleatExport(filepath, gaRepresenations, sep = ';', projectName = "Unknown", oneFile=False):
    if oneFile:
        __exportSingelFile(filepath,gaRepresenations,projectName,sep)
    else:
        __exportDifferentFiles(filepath,gaRepresenations, sep)


def __exportSingelFile(FilePath, gaRepresenations,projectName ,sep):
    f = open(filePath, 'wt')
    writer = csv.writer(f,delimiter = sep,lineterminator = '\n')
    try:
        writer.writerow( ('Timestamp', 'Data', 'Groupaddress', 'Groupaddres Name', 'Lenth [bit]', 'EIS') )
        for gaRep in gaRepresenations:
            for data in gaRep:
                    writer.writerow( (data[0].strftime("%d.%m.%Y %H:%M:%S.%f") , data[1], gaRep.gaStr , gaRep.mainMidGAName + '.' + gaRep.gaName , gaRep.length , gaRep.eis ) )
    finally:
        f.close()


def __exportDifferentFiles(filePath, gaRepresenations,sep):
    for gaRep in gaRepresenations:
        groupAddressExport(filePath, gaRep, sep= sep)

def groupAddressExport(filePath, gaRepresenation, sep= ';'):
    f = open(filePath, 'wt')
    try:
        writer = csv.writer(f,delimiter = sep, lineterminator = '\n')
        writer.writerow( ('Timestamp', 'Data') )
        for data in gaRepresenation:
            writer.writerow( (data[0].strftime("%d.%m.%Y %H:%M:%S.%f") , data[1] ) )
    finally:
        f.close()
