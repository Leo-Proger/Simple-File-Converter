import csv
import json
import os
import chardet

from pydub import AudioSegment


class FileConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1].lower()

    def _detect_encoding(self):
        with open(self.file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    def _load_and_export(self, from_format, to_format):
        assert self.file_extension in ['.mp3', '.wav'], 'Unsupported file format!'
        segment = AudioSegment.from_file(self.file_path, format=from_format)
        base_name = os.path.basename(self.file_path).rsplit('.', 1)[0]
        output_path = os.path.join(os.path.dirname(self.file_path), f"{base_name}_converted.{to_format}")
        segment.export(output_path, format=to_format)

    def convert_audiofile(self, from_format, to_format):
        self._load_and_export(from_format, to_format)

    def convert_csv_to_json(self):
        json_array = []
        detected_encoding = self._detect_encoding()
        with open(self.file_path, encoding=detected_encoding) as csvf:
            csv_reader = csv.DictReader(csvf)
            json_array.extend(csv_reader)
        self._save_as_json(json_array)

    def _save_as_json(self, data):
        base_name = os.path.basename(self.file_path).rsplit('.', 1)[0]
        output_path = os.path.join(os.path.dirname(self.file_path), f"{base_name}_converted.json")
        with open(output_path, 'w', encoding='utf-8') as jsonf:
            json.dump(data, jsonf, ensure_ascii=False, indent=4)


def main():
    greeting = '''
    Welcome to the file converter.
    Choose the desired number:
    '''
    available_formats = '''
    1. From MP3 to WAV
    2. From WAV to MP3
    3. From CSV to JSON
    '''
    print(greeting)
    user_input_format = input(available_formats)
    user_input_file = input('Now enter the path to the file >>> ')

    converters = {
        '1': lambda: FileConverter(user_input_file).convert_audiofile('mp3', 'wav'),
        '2': lambda: FileConverter(user_input_file).convert_audiofile('wav', 'mp3'),
        '3': lambda: FileConverter(user_input_file).convert_csv_to_json(),
    }

    converter = converters.get(user_input_format)
    if converter:
        converter()
    else:
        print('Unknown conversion format.')
    print('Done!')


if __name__ == "__main__":
    main()
