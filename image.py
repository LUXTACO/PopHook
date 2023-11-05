import logger as loglib
import crypto
import PIL.Image

class GatherData:
    def __init__(self, image_path, do_hash=False, hash_type="sha256", debug=False):
        self.image_path = image_path
        self.image_hash = None
        self.do_hash = do_hash
        self.hash_type = hash_type
        self.debug = debug
        
        if self.debug:
            self.logger = loglib
        else:
            class logger:
                def Log(typeL, execPart, message):
                    pass
            self.logger = logger
        
        try:
            self.image = PIL.Image.open(image_path)
            self.logger.Log(typeL="info", execPart="PopImage", message=f"Image opened successfully")
            self.image = self.image.convert("RGB")
            self.logger.Log("info", "PopImage", f"Image converted to RGB")
            self.image_first = self.image.crop((0, 0, 100, 100))
            self.image_last = self.image.crop((self.image.size[0] - 100, self.image.size[1] - 100, self.image.size[0], self.image.size[1]))
            self.logger.Log(typeL="info", execPart="PopImage", message=f"Gathered first and last 100 pixels of the image")
            
            if self.do_hash:
                self.image_data = self.image.tobytes()
                self.image_data = str(self.image_data)
                self.logger.Log(typeL="info", execPart="PopImage", message=f"Hashed first and last 100 pixels of the image")
                self.image_hash = crypto.Hash(self.hash_type, self.image_data.encode(), debug=self.debug).hash
                self.logger.Log(typeL="info", execPart="PopImage", message=f"Hashed image: {self.image_hash}")
        except Exception as e:
            self.logger.Log(typeL="error", execPart="PopImage", message=type(e).__name__ + " - " + str(e))