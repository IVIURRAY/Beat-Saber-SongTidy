from os import walk, rename, path
import json


BSABER_FILE_PATH = 'C:/YOUR/DIR/HERE'


def run():
    for (dirpath, dirnames, filenames) in walk(BSABER_FILE_PATH):
        if 'info.dat' in filenames:
            with open(dirpath + '/info.dat', 'r') as info_file:
                data = json.load(info_file)
                artist_name = data.get('_songAuthorName') or 'UnknownArtist'
                creator_name = data.get('_levelAuthorName') or 'UnknownCreator'
                song_name = data.get('_songName') or 'UnknownSongName'
                song_sub_name = data.get('_songSubName')
                song_name = song_name + (f' ({song_sub_name})' if song_sub_name else '')

                tidy = SongTidy(artist_name, song_name, creator_name)
                

            old_dir = path.normpath(dirpath).split('\\')[-1]
            new_dir = path.normpath(BSABER_FILE_PATH + '/' + tidy.dir_name())

            if old_dir != new_dir.split('\\')[-1]: # they're the same so don't touch
                try:
                    print('Renaming: ', dirpath, '\nNewDir: ', new_dir)
                    rename(dirpath, new_dir)
                except Exception as e:
                    print(f'Unable to change {new_dir}', e)


class SongTidy:

    def __init__(self, artist_name, song_name, creator_name):
        self.artist_name = self.sanatise(artist_name)
        self.song_name = self.sanatise(song_name)
        self.creator_name = self.sanatise(creator_name)

    def sanatise(self, t):
        return ''.join([char for char in t if char not in  ['/', '\\', ':', '?', '*', '"', '<', '>', '|']])

    def dir_name(self):
        return f'{self.artist_name} - {self.song_name} - {self.creator_name}'


if __name__ == '__main__':
    run()
