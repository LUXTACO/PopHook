import logger as loglib
import hashlib

class Hash:
    def __init__(self, hash_type, data, debug=False):
        self.hash_type = hash_type
        self.data = data
        self.debug = debug
        
        if self.debug:
            self.logger = loglib
        else:
            class logger:
                def Log(typeL, execPart, message):
                    pass
            self.logger = logger
        
        if self.hash_type == "sha256":
            self.hash = self.sha256(self.data)
        elif self.hash_type == "sha512":
            self.hash = self.sha512(self.data)
        elif self.hash_type == "sha1":
            self.hash = self.sha1(self.data)
        elif self.hash_type == "md5":
            self.hash = self.md5(self.data)
        elif self.hash_type == "sha224":
            self.hash = self.sha224(self.data)
        else:
            logger.Log("error", "PopCrypt", f"Hash type not supported")
    
    def sha256(self, data):
        self.logger.Log("info", "PopCrypt", f"Hashing data with SHA256")
        return hashlib.sha256(data).hexdigest()
    
    def sha512(self, data):
        self.logger.Log("info", "PopCrypt", f"Hashing data with SHA512")
        return hashlib.sha512(data).hexdigest()
    
    def sha1(self, data):
        self.logger.Log("info", "PopCrypt", f"Hashing data with SHA1")
        return hashlib.sha1(data).hexdigest()
    
    def md5(self, data):
        self.logger.Log("info", "PopCrypt", f"Hashing data with MD5")
        return hashlib.md5(data).hexdigest()
    
    def sha224(self, data):
        self.logger.Log("info", "PopCrypt", f"Hashing data with SHA224")
        return hashlib.sha224(data).hexdigest()
    