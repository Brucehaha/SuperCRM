import os
import uuid

class ImageHandler(object):
    """ accept image upload from ajax for preview in web page """
    def __init__(self):
        self.paths = []
        self.request = None
        self.root = None
        self.folder = None
        self.media_root = None

    def register(self, request, root, media_root, folder):
        self.request = request
        self.root = root
        self.folder = folder
        self.id = uuid.uuid4()
        self.media_root = media_root
        if not hasattr(self, str(request.user)):
            setattr(self, str(request.user), [])

    def get_file(self):
        _, file = list(self.request.FILES.items())[0]
        return file

    def get_file_name(self):
        return self.get_file().name

    def get_file_size(self):
        return self.get_file().name

    def get_file_path(self):
        file_path = os.path.join(self.root, str(self.request.user), self.folder, str(self.id)+'-'+self.get_file_name())
        self.paths.append(file_path)
        return file_path

    def create_file(self):
        file_path = self.get_file_path()
        self.add_ospath_to_list(file_path)
        print(getattr(self, str(self.request.user)))
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                print('file is not found or not accessible')
        with open(file_path, 'wb') as f:
            for line in self.get_file().chunks():
                f.write(line)
        self.remove_last_pic()

    def get_media_url(self):
        file_url = os.path.join(self.media_root, str(self.request.user), self.folder, str(self.id)+'-'+self.get_file_name())
        print(file_url)
        return file_url

    def add_ospath_to_list(self, path):
        if hasattr(self, str(self.request.user)):
            getattr(self, str(self.request.user)).append(path)

    def remove_last_pic(self):
        if hasattr(self, str(self.request.user)):
            url_list = getattr(self, str(self.request.user))
            while len(url_list) > 1:
                file = url_list.pop(0)
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except OSError as exc:
                        print('file is not found or not accessible')

#Singleton
handelImage = ImageHandler()


