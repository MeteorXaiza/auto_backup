# coding:utf-8


from my_functions_2 import *


class BackupResult():
    def __init__(self, strDirStructurePath, strFaultlListPath, message=True):
        self.strDirStructurePath = strDirStructurePath
        self.dicDirStructure = getDicJSON(strDirStructurePath, message=message)
        self.strFaultlListPath = strFaultlListPath
        self.lsStrFaultPath = []
        self.backupSize = 0
        self.message = message
        self.copySpeedStat = CopySpeedStat()
    def updateDirStructure(self, strFileAbsPath, mtime=None):
        if mtime is None:
            mtime = os.path.getmtime(strFileAbsPath)
        if mtime is False:
            self.appendFault(strFileAbsPath)
        strDirPath, strFileName = genLsStrDirPathAndFileName(strFileAbsPath)
        lsStrDirName = strDirPath[:-1].split('/')
        dicDeepDir = self.dicDirStructure
        for strDirName in lsStrDirName:
            if strDirName not in dicDeepDir.keys():
                dicDeepDir[strDirName] = {}
            dicDeepDir = dicDeepDir[strDirName]
        dicDeepDir[strFileName] = mtime
    def appendFault(self, strFileAbsPath):
        self.lsStrFaultPath.append(strFileAbsPath)
    def genNecessity(self, strFilePath, mtime):
        if mtime is None:
            return True
        strDirPath, strFileName = genLsStrDirPathAndFileName(strFilePath)
        lsStrDirName = strDirPath[:-1].split('/')
        dicDeepDir = self.dicDirStructure
        for strDirName in lsStrDirName:
            if strDirName in dicDeepDir.keys():
                dicDeepDir = dicDeepDir[strDirName]
                if type(dicDeepDir) != dict:
                    return True
            else:
                return True
        if strFileName in dicDeepDir:
            return dicDeepDir[strFileName] < mtime
        else:
            return True
    def autoSave(self, message=None, size=10**9):
        if self.backupSize > size:
            self.save(message=message)
            self.backupSize = 0
    def save(self, message=None):
        if message is None:
            message = self.message
        saveAsJSON(
            self.dicDirStructure, self.strDirStructurePath, message=message)
        saveAsTxt(
            self.lsStrFaultPath, self.strFaultlListPath, message=message)
        if message:
            print('')
    def increaseBackupSize(self, fileSize):
        if fileSize is not None:
            self.backupSize += fileSize


class CopySpeedStat():
    def __init__(self):
        self.cnt = 0
        self.sum = 0
        self.sumSq = 0
        self.mean = None
        self.std = None
        self.err = None
    def update(self, copySpeed):
        self.cnt += 1
        self.sum += copySpeed
        self.sumSq += copySpeed ** 2
        self.mean = self.sum / self.cnt
        if self.cnt > 1:
            self.std = sqrt(
                (self.sumSq/self.cnt - self.mean**2)
                * ((self.cnt - 1) / self.cnt))
            self.err = self.std / sqrt(self.cnt)
        else:
            self.std = np.nan
            self.err = np.nan
    def printPrediction(self, strFilePath, indent=2):
        fileSize = getFileSize(strFilePath)
        strIndent = ' ' * indent
        strStartTime = self.genStrLocalTime(round(time.time(), 1))
        print('prediction :')
        print(strIndent + 'target_file_path : ' + strFilePath)
        print(strIndent + 'start_time : ' + strStartTime)
        if fileSize is None:
            print(strIndent + 'filesize is unknown.')
        elif self.cnt <= 0:
            print('copy stats data is none.')
        else:
            requiredTime = fileSize / self.mean
            errRequiredTime = requiredTime * (self.std / self.mean)
            strEndTime = self.genStrLocalTime(round(time.time()+requiredTime, 1))
            print(strIndent + 'file_size : ' + str(fileSize) + ' byte')
            if self.cnt <= 1:
                print(
                    strIndent + 'copy_speed : ' + str(round(self.mean, 1))
                    + ' byte/sec')
                print(
                    strIndent + 'required_time : ' + str(round(requiredTime, 1))
                    + ' sec')
            else:
                print(
                    strIndent + 'copy_speed : '
                    + str(round(self.mean, 1)) + ' [+/- ' + str(round(self.std, 1))
                    + ' (1sigma)] byte/sec')
                print(
                    strIndent + 'required_time : ' + str(round(requiredTime, 1))
                    + ' [+/- ' + str(round(errRequiredTime, 1))
                    + ' (1sigma)] sec')
            print(
                strIndent + 'end_time : ' + strEndTime + ' [+/- '
                + str(round(errRequiredTime, 1)) + ' sec (1sigma)]')
    def genStrLocalTime(self, localTime):
        dicLocalTime = genDicLocalTime(localTime)
        tpStrTimeKey = ('year', 'month', 'day', 'hour', 'min', 'sec')
        tpZfillSize = (4, 2, 2, 2, 2, 2)
        tpStrJoin = ('/', '/', '-', ':', ':')
        strRet = ''
        for cnt in range(len(tpStrJoin)):
            strRet += (
                str(dicLocalTime[tpStrTimeKey[cnt]]).zfill(tpZfillSize[cnt])
                + tpStrJoin[cnt])
        strRet += str(dicLocalTime[tpStrTimeKey[-1]]).zfill(tpZfillSize[-1])
        return strRet


def copyFile(strSourceFilePath, strTargetFilePath, message=True):
    try:
        cp(strSourceFilePath, strTargetFilePath, cp2=True, message=message)
        return True
    except:
        print('ERROR')
        return False


def backupDir(
        backupResult, strSourceDirAbsPath, strTargetDirAbsPath, message=True):
    try:
        lsStrSourceFileName = sorted(getLsStrFileName(strSourceDirAbsPath))
        lsStrSourceBranchDirName = sorted(getLsStrDirName(strSourceDirAbsPath))
        for strSourceFileName in lsStrSourceFileName:
            startTime = time.time()
            strSourceFileAbsPath = strSourceDirAbsPath + strSourceFileName
            mtime = getMtime(strSourceFileAbsPath)
            necessity = backupResult.genNecessity(strSourceFileAbsPath, mtime)
            if necessity:
                fileSize = getFileSize(strSourceFileAbsPath)
                backupResult.copySpeedStat.printPrediction(strSourceFileAbsPath)
                startTime = time.time()
                res = copyFile(
                    strSourceFileAbsPath,
                    strTargetDirAbsPath+strSourceFileName, message=message)
                finishTime = time.time()
                if message:
                    print('')
                backupResult.increaseBackupSize(fileSize)
            if necessity:
                if res and mtime is not None:
                    backupResult.updateDirStructure(
                        strSourceFileAbsPath, mtime=mtime)
                    backupResult.autoSave()
                elif not(res):
                    backupResult.appendFault(strSourceFileAbsPath)
            if necessity and res:
                if fileSize is not None:
                    backupResult.copySpeedStat.update(
                        fileSize / (finishTime-startTime))
        for strSourceBranchDirName in lsStrSourceBranchDirName:
            backupResult = backupDir(
                backupResult,
                strSourceDirAbsPath+strSourceBranchDirName+'/',
                strTargetDirAbsPath+strSourceBranchDirName+'/')
        return backupResult
    except:
        if message:
            prints((
                'can\'t copy ' + strSourceDirAbsPath
                + ' to ' + strTargetDirAbsPath), '')
        backupResult.appendFault(strSourceDirAbsPath)
        return backupResult

def getMtime(strFilePath):
    try:
        ret = os.path.getmtime(strFilePath)
        return ret
    except:
        return None


def getFileSize(strFilePath):
    try:
        ret = os.path.getsize(strFilePath)
        return ret
    except:
        return None


def checkBackupConfigFile(strFilePath):
    if os.path.isfile(strFilePath):
        print(strFilePath + ' has already existed.')
        strInput = input('backup this file? [y/n] : ')
        if strInput == 'y':
            strDirPath, strFileName = genLsStrDirPathAndFileName(strFilePath)
            strFileHead, strFileExtend = re.match(
                '(.*)(\..+)', strFileName).groups()
            lsStrTxtLine = getLsStrTxtLine(strFilePath, message=True)
            saveAsTxt(
                lsStrTxtLine,
                strDirPath+strFileHead+'_'+str(int(time.time()))+strFileExtend,
                message=True)


message = True
dicBackupConfig = getDicIni(sys.argv[1], message=message)
strSourceDirPath = getStrAbsPath(
    dicBackupConfig['input']['directory_path']) + '/'
strDirStructurePath = dicBackupConfig['input']['directory_structure_path']
checkBackupConfigFile(strDirStructurePath)
strFaultlListPath = dicBackupConfig['input']['fault_list_path']
checkBackupConfigFile(strFaultlListPath)
lowLimitValidCopySpeedFileSize = int(dicBackupConfig['input'][''])
strTargetDirPath = getStrAbsPath(
    dicBackupConfig['output']['directory_path']) + '/'

backupResult = BackupResult(
    strDirStructurePath, strFaultlListPath, message=message)
backupResult = backupDir(
    backupResult, strSourceDirPath, strTargetDirPath, message=message)
backupResult.save(message=message)
