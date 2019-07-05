import os


class ImageHandler(object):

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
        self.media_root = media_root
        print(self.paths)

    def get_file(self):
        _, file = list(self.request.FILES.items())[0]
        return file

    def get_file_name(self):
        return self.get_file().name

    def get_file_size(self):
        return self.get_file().name

    def get_file_path(self):
        file_path = os.path.join(self.root, str(self.request.user), self.folder, self.get_file_name())
        self.paths.append(file_path)
        return file_path

    def create_file(self):
        file_path = self.get_file_path()
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                print('file is not found or not accessible')
        with open(file_path, 'wb') as f:
            for line in self.get_file().chunks():
                f.write(line)

    def get_media_url(self):
        file_url = os.path.join(self.media_root, str(self.request.user), self.folder, self.get_file_name())
        print(file_url)
        return file_url

    def remove_prepic(self):
            if len(self.paths) > 1:
                file = self.paths.pop(0)
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except OSError as exc:
                        print('file is not found or not accessible')


handelImage = ImageHandler()


