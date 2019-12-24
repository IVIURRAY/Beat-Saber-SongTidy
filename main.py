from os import walk, rename
import json


BSABER_FILE_PATH = '/Users/Haydn/Downloads/BeatSaberFiles'


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
                print(tidy.dir_name())

            old_dir = dirpath.split('/')[-1]
            new_dir = dirpath.replace(old_dir, tidy.dir_name())
            print('Renaming: ', dirpath, '\nNewDir: ', new_dir)
            rename(dirpath, new_dir)


class SongTidy:

    def __init__(self, artist_name, song_name, creator_name):
        self.artist_name = artist_name
        self.song_name = song_name
        self.creator_name = creator_name

    def dir_name(self):
        return f'{self.artist_name} - {self.song_name} - {self.creator_name}'


if __name__ == '__main__':
    run()
