import base64
import os


class ImageExtractor(object):
    def __init__(self):
        self.input_path = 'Select Input Folder'
        self.output_path = os.path.expanduser('~')
        self.is_extracting = False
        self.working_file_number = 0
        self.total_file_number = 0
        self.cancel_extractor = False
        self._file_path = ''
        self._iteration_number = 0

    def write_image_from_label(self, label_path):
        self._iteration_number = 0
        label = open(label_path)
        label_filename = os.path.basename(label_path)
        for label_line in label:
            stripped_label_line = label_line.strip()
            if stripped_label_line.startswith('<Image>') and stripped_label_line.endswith('</Image>'):
                self._iteration_number += 1
                trimmed_line = stripped_label_line[len('<Image>'):-len('</Image>')]
                trimmed_line += '=' * (-len(trimmed_line) % 4)
                output_filename = os.path.join(self.output_path,
                                               label_filename.rstrip('.label') + ' image ' +
                                               str(self._iteration_number) + '.png')
                image = open(output_filename, 'wb')
                image.write(base64.b64decode(trimmed_line))
                image.close()
        label.close()

    def start_extracting(self):

        self.total_file_number = 0
        self.working_file_number = 0

        def do_loop():
            if not self.check_for_ready():
                return

            for root, dirs, files in os.walk(self.input_path):
                self.total_file_number = len(files)
                if self.cancel_extractor:
                    break
                for entry in files:
                    if self.cancel_extractor:
                        break
                    self._file_path = os.path.join(root, entry)
                    self.working_file_number += 1
                    if self._file_path.endswith('.label'):
                        self.write_image_from_label(self._file_path)
        self.is_extracting = True
        do_loop()
        self.working_file_number = 0
        self.is_extracting = False
        self.cancel_extractor = False

    def check_for_ready(self):
        if os.path.isdir(self.input_path) and os.path.isdir(self.output_path):
            return True
        else:
            return False

    def get_count_files_in_folder(self):
        files = next(os.walk(self.input_path))[2]  # dir is your directory path as string
        return len(files)
